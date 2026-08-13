import os
from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path

# Identifica la carpeta raíz del backend.
BASE_DIR = Path(__file__).resolve().parent.parent

# Carga las variables del archivo .env.
load_dotenv(BASE_DIR / ".env")

# Lee la URI de conexión a MongoDB Atlas.
MONGODB_URI = os.getenv("MONGODB_URI")

# Lee el nombre de la base de datos; si no existe, usa un valor por defecto.
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "ecored_circular_db")

# Crea el cliente de conexión a MongoDB.
client = MongoClient(MONGODB_URI)

# Selecciona la base de datos que utilizará la aplicación.
db = client[MONGODB_DB_NAME]

# Expone la colección de empresas.
companies_collection = db["companies"]

# Expone la colección de publicaciones de materiales.
material_listings_collection = db["material_listings"]

# Expone la colección de perfiles de usuarios (uid + rol).
users_collection = db["users"]