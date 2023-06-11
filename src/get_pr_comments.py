import requests
import json
import os
from tqdm import tqdm
import argparse
from src import util

PER_PAGE = 100
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
COMMENTS_DIR = 'src/data/comments'

headers = {
    'Authorization': 'Bearer ' + GITHUB_TOKEN,
    'Accept': 'application/vnd.github.v3+json'
}

# Creating directory to store comment JSON files
os.makedirs(COMMENTS_DIR, exist_ok=True)

def get_comments_for_pr(user: str, repo: str, pr_number: int) -> list[dict]:
    comments_url = util.get_pr_comments_url(user, repo, pr_number)
    response = requests.get(comments_url, headers=headers)

    if response.status_code != 200:
        raise util.build_response_exception(
            response, f'Error occurred while fetching comments for PR #{pr_number}\n'
        )
    return json.loads(response.text)


def get_prs(user: str, repo: str):
    page = 1
    while True:
        pr_url = util.get_pr_url(user, repo, page)
        response = requests.get(pr_url, headers=headers)

        if response.status_code == 200:
            prs = json.loads(response.text)
            if not prs:
                break

            for pr in tqdm(prs, desc="Processing PRs"):
                pr_number = pr['number']
                print('-' * 50)
                print(f'PR #{pr_number}')

                file_path = f'{COMMENTS_DIR}/comments_{pr_number}.json'
                # Check if comments file for the PR already exists
                if os.path.exists(file_path):
                    continue
                comments = get_comments_for_pr(user, repo, pr_number)
                file_name = f'{COMMENTS_DIR}/comments_{pr_number}.json'
                print(f'Writing comments to file: {file_name}')
                with open(file_name, 'w') as f:
                    json.dump(comments, f)
                print('-' * 50)

            page += 1
        else:
            raise util.build_response_exception(
                response, f'Error occurred while fetching PRs\n'
            )



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
            util.handle_rate_limit()

