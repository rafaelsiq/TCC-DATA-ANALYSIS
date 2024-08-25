import requests
from datetime import datetime
from pymongo import MongoClient

# Configurações iniciais
GITHUB_API_URL = "https://api.github.com"
REPO_OWNER = "facebook"
REPO_NAME = "react"
BRANCH_NAME = "main"
SINCE_DATE = "2022-12-31T00:00:00Z"
UNTIL_DATE = "2023-12-31T23:59:59Z"
PER_PAGE = 100

# Configuração do MongoDB
MONGO_URI = "mongodb://localhost:27017/"  
DB_NAME = "tcc-data-analysis"
COLLECTION_NAME = "commits"

# Conexão com o MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Função para buscar commits
def get_commits(owner, repo, branch, since, until):
    commits = []
    page = 1
    while True:
        url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/commits"
        params = {
            "sha": branch,
            "since": since,
            "until": until,
            "per_page": PER_PAGE,
            "page": page
        }
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            raise Exception(f"Error fetching commits: {response.status_code} - {response.text}")

        data = response.json()

        if not data:
            break

        commits.extend(data)
        page += 1

    return commits

# Função para salvar os commits no MongoDB
def save_commits_to_mongo(commits):
    if commits:
        result = collection.insert_many(commits)
        print(f"Total de {len(result.inserted_ids)} commits inseridos na coleção '{COLLECTION_NAME}'")
    else:
        print("Nenhum commit para salvar.")

# Executando o script
if __name__ == "__main__":
    commits = get_commits(REPO_OWNER, REPO_NAME, BRANCH_NAME, SINCE_DATE, UNTIL_DATE)
    print(f"Total de commits encontrados: {len(commits)}")
    save_commits_to_mongo(commits)
