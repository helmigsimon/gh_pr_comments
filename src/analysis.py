import pandas as pd
import matplotlib.pyplot as plt
from src import paths


def import_data():
    """Import data from csv file and return a pandas DataFrame."""
    try:
        return pd.read_csv(paths.COMMENTS_CSV)
    except FileNotFoundError as e:
        print(f'Error: {e}\n')
        print('Please run `python parse_json.py` to generate the csv file.\n')
        raise e

def get_comment_counts_per_user(df: pd.DataFrame) -> pd.DataFrame:
    """Get comment counts per user"""
    return df['user'].value_counts()

def get_comment_percentages_per_user(df: pd.DataFrame) -> pd.DataFrame:
    """Get comment percentages per user"""
    return df['user'].value_counts(normalize=True)

def get_comments_per_user_per_day(df: pd.DataFrame) -> pd.DataFrame:
    """Get comments per user per day"""
    return df.groupby(['user', 'created_at']).size()

def get_average_word_count_per_comment_per_user(df: pd.DataFrame) -> pd.DataFrame:
    """Get average word count per comment per user"""
    return df.groupby('user')['body'].apply(lambda x: x.str.split().str.len().mean()).sort_values(ascending=False)

def get_average_comments_per_pull_request_per_user(df: pd.DataFrame) -> pd.DataFrame:
    """Get average comments per pull request per user"""
    return df.groupby(['user', 'pull_request_number']).size().groupby('user').mean().sort_values(ascending=False)

def plot_comment_count_per_day_by_user(df: pd.DataFrame):
    """Plot comment count per day by user"""
    grouped = df.groupby(['user', 'created_at']).size().reset_index(name='counts')
    for user in grouped['user'].unique():
        user_data = grouped[grouped['user'] == user]
        plt.plot(user_data['created_at'], user_data['counts'], label=user)

    plt.xlabel('Date')
    plt.ylabel('Number of comments')
    plt.title('Number of comments per day per user')
    plt.legend()
    plt.show()

def get_top_commenting_users(df: pd.DataFrame) -> list[str]:
    """Get top commenting users"""
    comment_counts = get_comment_percentages_per_user_(df)

    

if __name__ == '__main__':
    df = import_data()
    print(get_comment_counts_per_user(df))
    print(get_comment_percentages_per_user(df))
    print(get_comments_per_user_per_day(df))
    print(get_average_word_count_per_comment_per_user(df))
    print(get_average_comments_per_pull_request_per_user(df))


