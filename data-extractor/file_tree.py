import re
from pymongo import MongoClient
from git import Repo

# Conexão com o MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['tcc-data-analysis']
collection = db['commit_file_history']

# Função para extrair os arquivos alterados do git diff
def extract_changed_files(diff_text):
    if diff_text is None:
        print("Diff text is None")
        return []
    changed_files = re.findall(r'--- a/(.*?)\n\+\+\+ b/(.*?)\n', diff_text)
    files = [file[1] for file in changed_files if file[1] != '/dev/null']
    return files

# Função para encontrar o commit anterior que alterou um arquivo
def find_previous_commit(repo, file_path, current_commit):
    commits = list(repo.iter_commits(paths=file_path))
    previous_commit = None

    for commit in commits:
        if commit.hexsha == current_commit:
            # Encontrar o commit anterior
            index = commits.index(commit)
            if index + 1 < len(commits):
                previous_commit = commits[index + 1].hexsha
            break
    
    return previous_commit

# Caminho do repositório local
repo_path = 'D:/Users/Rafael/Documents/GitHub/TCC/react'
repo = Repo(repo_path)

# Iterando sobre os commits e processando os arquivos alterados
for commit_data in db['commit_diffs'].find():
    commit_hash = commit_data['commit']
    diff_text = commit_data.get('diff')  # Usar get para evitar KeyError
    
    # Verificar se diff_text não é None
    if diff_text is not None:
        # Extraindo os arquivos alterados
        changed_files = extract_changed_files(diff_text)
        
        file_history = []
        for file in changed_files:
            previous_commit = find_previous_commit(repo, file, commit_hash)
            file_history.append({'file': file, 'previous_commit': previous_commit})
        
        # Salvando as informações no MongoDB
        collection.insert_one({
            'commit': commit_hash,
            'data': file_history
        })
    else:
        print(f"No diff text found for commit {commit_hash}")
