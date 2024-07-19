import lucene
from searchEngine import retrieve, attach_current_thread

# This file was made to test the retrieve() function in searchEngine
if not lucene.getVMEnv():
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])

def test_retrieve():
    attach_current_thread()

    index_dir = 'reddit_index'
    query = 'NBA'
    results = retrieve(index_dir, query)

    print(f"Search results for query '{query}': ")
    for result in results:
        print(f"Title: {result['Title']}")
        print(f"Body: {result['Body']}")
        print(f"Score: {result['Score']}")
        print('---')

if __name__ == "__main__":
    test_retrieve()