import requests
from bs4 import BeautifulSoup
import os
import json

def get_title_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title_tag = soup.title
        if title_tag:
            title = title_tag.string.strip()
            return title
        else:
            return "No Title Found"
    except Exception as e:
        print("Error:", e)
        return None


def extract_post_info(post):
    post_dict = {}
    post_dict['id'] = post.id
    post_dict['title'] = post.title
    post_dict['author'] = post.author.name if post.author else "Unknown"
    post_dict['score'] = post.score
    post_dict['url'] = post.url
    post_dict['created_utc'] = post.created_utc
    if 'http' in post.selftext:
        post_dict['selftext'] = post.selftext
    if 'http' in post.url:
        post_dict['title_from_url'] = get_title_from_url(post.url)

    #comments
    post_dict['comments'] = []
    post.comments.replace_more(limit=None)
    for comment in post.comments.list():
        post_dict['comments'].append({
            'id': comment.id,
            'author': comment.author.name if comment.author else "Unknown",
            'body': comment.body,
            'score': comment.score,
            'created_utc': comment.created_utc
        })

    return post_dict

def save_posts_to_file(post, filename):
    if not os.path.exists('data'):
        os.makedirs('data')
    filepath = os.path.join('data', filename)

    file_size_limit = 10 * 1024 * 1024  # 10 MB limit
    file_size = os.path.getsize(filepath) if os.path.exists(filepath) else 0

    post_info = extract_post_info(post)
    post_size = len(json.dumps(post_info))

    with open(filepath, 'a', encoding='utf-8') as file:
        if file_size + post_size > file_size_limit:
            file.close()
            current_file_number = len([f for f in os.listdir('data') if f.startswith(filename.split('.')[0])]) + 1
            filepath = os.path.join('data', f"{filename.split('.')[0]}{current_file_number}.json")
            file = open(filepath, 'a', encoding='utf-8')
            file_size = 0

        file.write(json.dumps(post_info) + '\n')
        file_size += post_size
                                                     