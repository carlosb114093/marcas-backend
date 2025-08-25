import boto3
import uuid

# Cliente DynamoDB (ajusta la región y credenciales si no usas dotenv)
dynamodb = boto3.resource(
    'dynamodb',
    region_name='us-east-2'  # cámbiala por tu región
)
table = dynamodb.Table('Marcas')

# Crear un registro de prueba
brand_id = str(uuid.uuid4())
new_brand = {
    "id": brand_id,
    "brand_name": "Tienda Sigma",    
    "brand_owner": "Carlos López",
    "date": "2025-08-24",
    "brand status": "En trámite"    
}

table.put_item(Item=new_brand)

print("✅ Registro insertado en DynamoDB:", new_brand)