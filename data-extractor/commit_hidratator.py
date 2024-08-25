from pymongo import MongoClient
import requests
import subprocess

client = MongoClient("mongodb://localhost:27017/")
db = client["tcc-data-analysis"]
commits_prs_collection = db["commits_prs"]
commits_collection = db["commits"]
commit_diffs_collection = db["commit_diffs"]

GITHUB_TOKEN = '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'

# Cabeçalhos de autenticação
headers = {
    "Authorization": f"token {GITHUB_TOKEN}"
}

# Função para obter git diff
def get_git_diff(commit_hash):
    print(commit_hash)
    try:
        result = subprocess.run(['git', 'diff', f'{commit_hash}^!'],
                                capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return ""

# Função para processar o commit e formatar o dado para commit_diffs
def process_commit(commit_hash):
    diff = get_git_diff(commit_hash)
    return {
        "commit": commit_hash,
        "diff": diff
    }

# Iterar sobre commits na coleção commits_prs
for doc in commits_prs_collection.find():
    commit_hash = doc.get("commit_hash")
    
    # Verificar se o commit já existe na coleção commits
    if not commits_collection.find_one({"commit": commit_hash}):
        
        # Consultar API do GitHub para obter o commit com autenticação
        url = f"https://api.github.com/repos/facebook/react/commits/{commit_hash}"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            commit_data = response.json()
            # Salvar o commit na coleção commits
            commits_collection.insert_one({"commit": commit_hash, "data": commit_data})
            
            # Processar o commit e salvar o diff
            commit_diff_data = process_commit(commit_hash)
            commit_diffs_collection.insert_one(commit_diff_data)
        else:
            print(f"Erro ao consultar a API do GitHub para o commit {commit_hash}: {response.status_code}")
    else:
        print(f"Commit {commit_hash} já está na coleção 'commits'.")
