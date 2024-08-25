import json
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['tcc-data-analysis']

bugs_collection = db['react_bugs']
prs_collection = db['react_prs']

with open('react_bugs.json', 'r', encoding='utf-8') as f:
    bugs_data = json.load(f)

with open('react_PRs.json', 'r', encoding='utf-8') as f:
    prs_data = json.load(f)

bugs_collection.insert_many(bugs_data)
prs_collection.insert_many(prs_data)

print(f"Inseridos {len(bugs_data)} bugs na coleção 'react_bugs'.")
print(f"Inseridos {len(prs_data)} PRs na coleção 'react_prs'.")
