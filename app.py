import uuid
import json
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

USE_DYNAMODB = False
dynamodb = None
table = None

try:
    dynamodb = boto3.resource(
        'dynamodb',
        region_name=os.getenv("AWS_DEFAULT_REGION"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    table = dynamodb.Table('Brands')

    table.load()
    print("Succesful connection")
except Exception as e:
    print(f"⚠️ it can't be posible connect to DynamoDB: {e}")
    USE_DYNAMODB = False

DATA_FILE = "data.json"

def read_local_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def write_local_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route('/api/brands', methods=['GET'])
def get_brands():
    try:
        if USE_DYNAMODB:
            response = table.scan()
            return jsonify(response.get('Items', []))
        else:
            return jsonify(read_local_data())
    except ClientError as e:
        return jsonify({"error": e.response['Error']['Message']}), 500


@app.route('/api/brands/<string:brand_id>', methods=['GET'])
def get_brand(brand_id):
    try:
        if USE_DYNAMODB:
            response = table.get_item(Key={'id': brand_id})
            item = response.get('Item')
            if item:
                return jsonify(item)
        else:
            data = read_local_data()
            for item in data:
                if item['id'] == brand_id:
                    return jsonify(item)
        return jsonify({"error": "Registro no encontrado"}), 404
    except ClientError as e:
        return jsonify({"error": e.response['Error']['Message']}), 500

@app.route('/api/brands', methods=['POST'])
def create_brand():
    data = request.get_json()
    brand_id = str(uuid.uuid4())

    new_brand = {
        "id": brand_id,
        "brand_name": data.get('brand_name'),
        "brand_owner": data.get('brand_owner'),
        "date": data.get('date'),
        "brand_status": data.get('brand_status', 'En trámite')        
    }

    try:
        if USE_DYNAMODB:
            table.put_item(Item=new_brand)
        else:
            brands = read_local_data()
            brands.append(new_brand)
            write_local_data(brands)
        return jsonify(new_brand), 201
    except ClientError as e:
        return jsonify({"error": e.response['Error']['Message']}), 500


@app.route('/api/brands/<string:brand_id>', methods=['PUT'])
def update_brand(brand_id):
    data = request.get_json()
    try:
        if USE_DYNAMODB:
            update_expression = (
                "SET brand_name = :bm, brand_owner = :bo, "
                "date = :d, brand_status = :bs"
            )
            expression_attribute_values = {
                ':bm': data.get('brand_name'),
                ':bo': data.get('brand_owner'),
                ':d': data.get('date'),
                ':bs': data.get('brand_status')
            }

            response = table.update_item(
                Key={'id': brand_id},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ReturnValues="ALL_NEW"
            )
            return jsonify(response.get('Attributes'))
        else:
            brands = read_local_data()
            for item in brands:
                if item['id'] == brand_id:
                    item.update(data)
                    write_local_data(brands)
                    return jsonify(item)
            return jsonify({"error": "Registro no encontrado"}), 404
    except ClientError as e:
        return jsonify({"error": e.response['Error']['Message']}), 500

    data = request.get_json()
    try:
        if USE_DYNAMODB:
            update_expression = (
                "SET brand_name = :bm, brand_owner = :bo, "
                "date = :d, brand_status = :bs"
            )
            expression_attribute_values = {
                ':bm': data.get('brand_name'),                
                ':bo': data.get('brand_owner'),
                ':d': data.get('date'),
                ':bs': data.get('brand_status')                
            }

            response = table.update_item(
                Key={'id': brand_id},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ReturnValues="ALL_NEW"
            )
            return jsonify(response.get('Attributes'))
        else:
            brands = read_local_data()
            for item in brands:
                if item['id'] == brand_id:
                    item.update(data)
                    write_local_data(brands)
                    return jsonify(item)
            return jsonify({"error": "Registro no encontrado"}), 404
    except ClientError as e:
        return jsonify({"error": e.response['Error']['Message']}), 500


@app.route('/api/brands/<string:brand_id>', methods=['DELETE'])
def delete_brand(brand_id):
    try:
        if USE_DYNAMODB:
            table.delete_item(Key={'id': brand_id})
        else:
            brands = read_local_data()
            brands = [item for item in brands if item['id'] != brand_id]
            write_local_data(brands)
        return jsonify({"success": True, "message": "Registro eliminado"})
    except ClientError as e:
        return jsonify({"error": e.response['Error']['Message']}), 500


@app.route('/')
def home():
    return jsonify({
        "message": "This is Brands' API",
        "mode": "DynamoDB" if USE_DYNAMODB else "JSON local",
        "endpoints": {
            "GET ALL": "/api/brands",
            "GET by ID": "/api/brands/<id>",
            "new POST": "/api/brands",
            "PUT update": "/api/brands/<id>",
            "DELETE erase": "/api/brands/<id>"
        }
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)
