import os
from pylucene_sample import create_reddit_index

# Access JSON files in data/ and store Lucene index in reddit_index/
def index_json_files(data_dir='data', index_dir='reddit_index'):
    # Check if reddit_index exists yet, if not then make it
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)

    # Identify all files in data/ that end with '.json' for indexing
    json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]

    # Checking condition for empty data/ meaning nothing to index
    if not json_files:
        print ("No JSON files are found in the data folder.")
        return -1

    # Loop thorugh each .json file and construct path for indexing
    for json_file in json_files:
        json_file_path = os.path.join(data_dir, json_file)
        print(f"Indexing {json_file_path}")
        # Call create_reddit_index with the .json path and index to reddit_index/
        create_reddit_index(json_file_path, index_dir)

if __name__ == '__main__':
    index_json_files()