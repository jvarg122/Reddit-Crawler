import lucene
import os
from org.apache.lucene.store import SimpleFSDirectory
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.search import IndexSearcher

# FIXED: RuntimeError: attachCurrentThread() must be called first:
# PyLucene requires current thread to be attached to JVM

# Function to make sure current thread attached to JVM
def attach_current_thread():
    vm_env = lucene.getVMEnv()
    if vm_env is not None:
        vm_env.attachCurrentThread()

# Initializing JVM for PyLucene
if not lucene.getVMEnv():
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])

def retrieve(index_dir, query):
    attach_current_thread()

    print("Opening index directory: ", index_dir) # For Debugging
    store = SimpleFSDirectory(Paths.get(index_dir))
    reader = DirectoryReader.open(store)
    searcher = IndexSearcher(reader)

    print("Parsing Query: ", query) # For Debugging
    parser = QueryParser('Body', StandardAnalyzer())
    parsed_query = parser.parse(query)
    print("Parsed Query: ", parsed_query) # For Debugging

    topDocs = searcher.search(parsed_query, 10).scoreDocs # Max Results = 10
    results = []
    duplicate_docs = set() # Create set to handle duplicate document IDs

    print(f"Number of Document Hits: {len(topDocs)}") # For Debugging
    for hit in topDocs:
        doc = searcher.doc(hit.doc)
        doc_id = doc.get('PostID')
        if doc_id in duplicate_docs:
            continue
        duplicate_docs.add(doc_id)

        title = doc.get('Title') if doc.get('Title') else 'No Title'
        body = doc.get('Body') if doc.get('Body') else 'No Body'
        result = {
            'Title': title,
            'Body': body,
            'Score': hit.score
        }
        results.append(result)
        print(f"Retrieved Document: {result['Title']} with score {result['Score']}")

    return results