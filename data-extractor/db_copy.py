from pymongo import MongoClient

# Conectar ao MongoDB local
local_client = MongoClient("mongodb+srv://rafaelsqf22:BzBidqMNpQq94@app-estetica-cluster.6vsjca1.mongodb.net/") #mongodb+srv://rafaelsqf22:BzBidqMNpQq94@app-estetica-cluster.6vsjca1.mongodb.net/
local_db = local_client["tcc-data-analysis"]

# Conectar ao MongoDB Atlas
atlas_client = MongoClient("mongodb://localhost:27017/") #mongodb://localhost:27017/
atlas_db = atlas_client["tcc-data-analysis"]

# Função para copiar coleções
def copy_collection(local_db, atlas_db, collection_name):
    collection_local = local_db[collection_name]
    collection_atlas = atlas_db[collection_name]
    
    # Verificar se há documentos na coleção local
    document_count = collection_local.count_documents({})
    
    if document_count > 0:
        # Copiar todos os documentos da coleção local para o Atlas
        documents = collection_local.find()
        for doc in documents:
            collection_atlas.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)
        print(f"Cópia da coleção '{collection_name}' concluída com sucesso.")
    else:
        print(f"A coleção '{collection_name}' está vazia, nenhuma ação realizada.")

# Listar todas as coleções no banco de dados local
collections = local_db.list_collection_names()

# Copiar cada coleção para o Atlas
for collection_name in collections:
    copy_collection(local_db, atlas_db, collection_name)

print("Todas as coleções foram copiadas com sucesso.")
