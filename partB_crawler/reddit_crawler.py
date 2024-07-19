import praw
import prawcore
import json
import os
from utils import get_title_from_url, extract_post_info, save_posts_to_file
from config import subreddits, limit_per_subreddit, target_size
import time

# Authentication
reddit = praw.Reddit(client_id = '7N2vf09PEApfiv96VsxQIg',
                     client_secret=     'VEdnHCV_lX_LqTGxFdKpMi2YU5v1VA',
                     user_agent="MyRedditApp:v1.0.0 (by u/EducationTurbulent99)",
                     username='EducationTurbulent99',
                     password='CS172Project')

def collect_data(subreddit_name, target_size):
    total_size = 0
    oldest_post_timestamp = None
    retry_delay = 1
    while total_size < target_size:
        try:
            posts = reddit.subreddit(subreddit_name).new(limit=100, params={"before": oldest_post_timestamp})
            batch_size = 0
            for post in posts:
                post_info = extract_post_info(post)
                post_size = len(json.dumps(post_info))
                if total_size + post_size > target_size:
                    break
                save_posts_to_file(post, f"{subreddit_name}_posts.json")
                total_size += post_size
                batch_size += 1
                oldest_post_timestamp = post.created_utc
            if batch_size < 100:
                break
            # reset retry delay
            retry_delay = 1
        except prawcore.exceptions.TooManyRequests:
            print("Rate limit exceeded. Retrying after delay...")
            time.sleep(retry_delay)
            # increase delay exponentially for next retry
            retry_delay *= 2

for subreddit_name in subreddits:
    collect_data(subreddit_name, target_size)