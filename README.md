
API REST para la gestión de marcas.  
Este proyecto está preparado para trabajar con la base de datos AWS DynamoDB, y también ofrece un modo local con json.data para facilitar pruebas sin necesidad de credenciales de AWS.


Requisitos previos

- Python 3.9+  
- pip  

 Clona este repositorio:
   
   git clone https://github.com/tu-repo/brands-api.git
   
Crea y activa un entorno virtual:      

python -m venv venv
source venv/bin/activate   #  en Linux / Mac
venv\Scripts\activate      # en Windows

Instala dependencias:
pip install -r requirements.txt
 
Crea un archivo .env con tus credenciales de AWS:(Opcional) 
AWS_ACCESS_KEY_ID=tu_access_key
AWS_SECRET_ACCESS_KEY=tu_secret_key
AWS_DEFAULT_REGION=us-east-1

endpoints	

DELETE 	"/api/brands/<id>"
GET ALL	"/api/brands"
GET  ID	"/api/brands/<id>"
PUT 	"/api/brands/<id>"
new POST	"/api/brands"

