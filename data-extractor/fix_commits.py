from pymongo import MongoClient

# Conexão com o MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["tcc-data-analysis"]
commits_collection = db["commits"]

# Encontrar todos os documentos com a estrutura incorreta
for doc in commits_collection.find({"data": {"$exists": True}}):
    _id = doc["_id"]
    data = doc["data"]

    # Criar a nova estrutura do documento
    new_doc = {"_id": _id, **data}

    # Atualizar o documento no MongoDB
    commits_collection.replace_one({"_id": _id}, new_doc)

print("Documentos atualizados com sucesso.")
