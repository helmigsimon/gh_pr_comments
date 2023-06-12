import os
import pandas as pd
import json
import pydantic
from src import paths 

def main():
    pr_numbers = get_all_pr_numbers()
    print('Loading all comments...')
    comments = [comment for pr_number in pr_numbers for comment in get_comments_for_pr(pr_number)]
    df = pd.DataFrame([comment.dict() for comment in comments])
    print(f'Saving comments dataframe to {paths.COMMENTS_CSV}')
    df.to_csv(paths.COMMENTS_CSV, index=False)

def load_json(json_file: str):
    """Load json file"""
    with open(json_file) as f:
        return json.load(f)

class Comment(pydantic.BaseModel):
    """Comment model"""
    id: int
    url: str
    commit_id: str
    body: str
    path: str
    created_at: str
    updated_at: str
    user: str
    pull_request_url: str
    pull_request_number: int

    @classmethod
    def build(cls, source: dict):
        try:
            return cls(
                id=source['id'],
                commit_id=source['commit_id'],
                url=source['url'],
                body=source['body'],
                path=source['path'],
                created_at=source['created_at'],
                updated_at=source['updated_at'],
                user=source['user']['login'],
                pull_request_url=source['pull_request_url'],
                pull_request_number=source['pull_request_url'].split('/')[-1]
            )
        except Exception as e:
            print(f'Error: {e}')
            print(f'Source: {source}')
            raise e


def get_all_comment_paths() -> list[str]:
    """Get all comment paths"""
    return [str(path) for path in paths.COMMENTS.glob('comments_*.json')]

def comment_path_to_pr_number(comment_path: str) -> int:
    """Convert comment path to pr number"""
    return int(comment_path.split('/')[-1].split('_')[-1].split('.')[0])

def get_all_pr_numbers() -> list[int]:
    """Get all pr numbers"""
    return sorted([comment_path_to_pr_number(path) for path in get_all_comment_paths()])

def get_comments_for_pr(pr_number: int) -> list[Comment]: 
    """Get comments for a given PR"""
    return convert_comment_json_to_model(paths.COMMENTS / f'comments_{pr_number}.json')

def convert_comment_json_to_model(json_file: str) -> list[Comment]:
    """Convert json file to dict"""
    raw_comments = load_json(json_file)
    return [Comment.build(comment) for comment in raw_comments]

if __name__ == '__main__':
    main()
