import requests
import requests
import json
import os
from tqdm import tqdm
from time import sleep
import argparse

PER_PAGE = 100
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

headers = {
    'Authorization': 'Bearer ' + GITHUB_TOKEN,
    'Accept': 'application/vnd.github.v3+json'
}

# Creating directory to store comment JSON files
os.makedirs('comments', exist_ok=True)


def get_comments_for_pr(user: str, repo: str, pr_number: int) -> list[dict]:
    comments_url = f'https://api.github.com/repos/{user}/{repo}/pulls/{pr_number}/comments'
    response = requests.get(comments_url, headers=headers)

    if response.status_code == 200:
        comments = json.loads(response.text)
    else:
        raise Exception
        comments = []

    return comments


def get_prs(user: str, repo: str):
    page = 1
    while True:
        pr_url = f'https://api.github.com/repos/{user}/{repo}/pulls?state=all&per_page={PER_PAGE}&page={page}'
        response = requests.get(pr_url, headers=headers)

        if response.status_code == 200:
            prs = json.loads(response.text)
            if not prs:
                break

            for pr in tqdm(prs, desc="Processing PRs"):
                pr_number = pr['number']
                print('-' * 50)
                print(f'PR #{pr_number}')

                file_path = f'comments/comments_{pr_number}.json'
                # Check if comments file for the PR already exists
                if os.path.exists(file_path):
                    continue
                comments = get_comments_for_pr(user, repo, pr_number)
                file_name = f'comments/comments_{pr_number}.json'
                print(f'Writing comments to file: {file_name}')
                with open(file_name, 'w') as f:
                    json.dump(comments, f)
                print('-' * 50)

            page += 1
        else:
            raise Exception('Error occurred while fetching PRs.')


def handle_rate_limit():
    for _ in tqdm(range(60), desc="Sleeping"):
        sleep(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="GitHub username")
    parser.add_argument("repo", help="GitHub repository name")
    args = parser.parse_args()

    while True:
        try:
            get_prs(args.username, args.repo)
            break
        except Exception as e:
            print(f"Error: {str(e)}")
            handle_rate_limit()

