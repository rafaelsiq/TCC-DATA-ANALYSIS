import requests
import json
from datetime import datetime

repo_owner = "facebook"
repo_name = "react"
start_date = "2022-12-31"
end_date = "2023-12-31"
token = "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"

url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues"

params = {
    "state": "all",
    "since": start_date,
    "per_page": 100
}

headers = {
    "Authorization": f"token {token}"
}

def issue_within_date_range(issue, start_date, end_date):
    created_at = datetime.strptime(issue["created_at"], "%Y-%m-%dT%H:%M:%SZ")
    return start_date <= created_at <= end_date

issues = []
while True:
    response = requests.get(url, headers=headers, params=params)
    print(response)
    response.raise_for_status()
    data = response.json()
    
    filtered_issues = [
        issue for issue in data if issue_within_date_range(issue, datetime.fromisoformat(start_date), datetime.fromisoformat(end_date))
    ]
    issues.extend(filtered_issues)

    if "next" in response.links:
        url = response.links["next"]["url"]
    else:
        break

with open("react_bugs.json", "w", encoding="utf-8") as f:
    json.dump(issues, f, ensure_ascii=False, indent=4)

print(f"{len(issues)} bugs exportados para 'react_bugs.json'.")
