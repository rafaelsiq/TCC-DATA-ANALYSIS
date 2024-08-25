import subprocess
from pymongo import MongoClient

def get_git_diff(commit_hash):
    print(commit_hash)
    try:
        result = subprocess.run(['git', 'diff', f'{commit_hash}^!'],
                                capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return ""

def process_commit(commit_hash):
    diff = get_git_diff(commit_hash)
    return {
        "commit": commit_hash,
        "diff": diff
    }
client = MongoClient('mongodb://localhost:27017/')
db = client['tcc-data-analysis'] 

additional_data_collection = db['commit_diffs']
commit_hashes = db['commits'].find({}, {'sha': 1, '_id': 0})
commits = [process_commit(commit['sha']) for commit in commit_hashes]
additional_data_collection.insert_many(commits)

print(f'Inserido {len(commits)} commits na coleção de dados adicionais.')