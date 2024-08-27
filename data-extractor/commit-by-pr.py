import requests
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['tcc-data-analysis']
collection = db['commits_prs']

# Configurações do GitHub
repo_owner = 'facebook'
repo_name = 'react'
headers = {'Authorization': 'token'}

# Datas de início e fim
start_date = '2022-12-31T00:00:00Z'
end_date = '2023-12-31T23:59:59Z'

def get_pull_requests(page=1):
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/pulls'
    params = {
        'state': 'all',
        'per_page': 100,
        'page': page,
        'sort': 'created',
        'direction': 'asc'
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Erro ao obter PRs: {e}')
        sleep(5)  # Espera antes de tentar novamente
        return get_pull_requests(page)

def get_commits_for_pr(pull_number, page=1):
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pull_number}/commits'
    params = {
        'per_page': 100,
        'page': page
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Erro ao obter commits para PR {pull_number}: {e}')
        sleep(5)  # Espera antes de tentar novamente
        return get_commits_for_pr(pull_number, page)

def main():
    page = 1
    while True:
        pulls = get_pull_requests(page=page)
        if not pulls:
            break
        
        for pr in pulls:
            created_at = pr['created_at']
            if created_at >= start_date and created_at <= end_date:
                pull_number = pr['number']
                commit_page = 1
                
                while True:
                    commits = get_commits_for_pr(pull_number, page=commit_page)
                    if not commits:
                        break
                    
                    for commit in commits:
                        commit_date = commit['commit']['committer']['date']
                        if commit_date >= start_date and commit_date <= end_date:
                            commit_hash = commit['sha']
                            # Armazena o commit e o número do PR no MongoDB
                            collection.insert_one({'commit_hash': commit_hash, 'pull_number': pull_number})
                    
                    commit_page += 1
        
        page += 1

if __name__ == '__main__':
    main()