from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['tcc-data-analysis']

commits_collection = db['commits']
commit_file_history_collection = db['commit_file_history']

for commit in commits_collection.find():
    commit_sha = commit['sha']
    blame_count = 0

    for commit_file in commit_file_history_collection.find():
        for file_data in commit_file['data']:
            if file_data['previous_commit'] == commit_sha:
                blame_count += 1

    commits_collection.update_one(
        {'sha': commit_sha},
        {'$set': {'bug_count': blame_count}}
    )

print("Propriedade 'blame' atualizada para todos os commits.")