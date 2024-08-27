from pymongo import MongoClient
import subprocess

# Conectando ao MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['tcc-data-analysis']
collection = db['commit_file_history']


def get_previous_commit(file_path, commit_atual):
    try:
        # Obtenha o histórico de commits para o arquivo
        log_command = ['git', 'log', '--follow', '--format=%H', '--', file_path]
        result = subprocess.run(log_command, capture_output=True, text=True, check=True)
        
        # Obtenha a lista de commits
        commits = result.stdout.splitlines()
        
        # Encontre o commit anterior ao commit atual
        if commit_atual in commits:
            index = commits.index(commit_atual)
            if index + 1 < len(commits):
                previous_commit = commits[index + 1]
                return previous_commit

        return None
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar git log: {e}")
        return None
    

for document in collection.find():
    commit_atual = document['commit']
    data = document['data']

    for file_info in data:
        file_path = file_info['file']
        previous_commit = get_previous_commit(file_path, commit_atual)
        
        if previous_commit:
            file_info['previous_commit'] = previous_commit

    # Atualizando o documento no MongoDB
    collection.update_one({'_id': document['_id']}, {'$set': {'data': data}})

print("Processamento concluído.")
