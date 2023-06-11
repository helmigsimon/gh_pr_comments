import requests
import json
import os
from tqdm import tqdm
from time import sleep
import argparse
import enum


class PRState(enum.Enum):
    OPEN = 'open'
    CLOSED = 'closed'
    ALL = 'all'


def get_pr_comments_url(user: str, repo: str, pr_number: int) -> str:
    return f'https://api.github.com/repos/{user}/{repo}/pulls/{pr_number}/comments'

def build_response_exception(response: requests.Response, message: str) -> Exception:
    return Exception(
        f'{message}\n'
        f'Status code: {response.status_code}\n'
        f'Response: {response.text}'
    )


def get_pr_url(user: str, repo: str, page: int, state: PRState = PRState.ALL) -> str:
    return f'https://api.github.com/repos/{user}/{repo}/pulls?state={state.value}&per_page={PER_PAGE}&page={page}'

        

def handle_rate_limit():
    for _ in tqdm(range(60), desc="Sleeping"):
        sleep(1)

