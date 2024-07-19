import lucene
import os
import json
from flask import Flask, request, render_template_string
from org.apache.lucene.store import SimpleFSDirectory, NIOFSDirectory
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, IndexOptions, DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher

app = Flask(__name__)

# FIXED: RuntimeError: attachCurrentThread() must be called first:
# PyLucene requires current thread to be attached to JVM

# Initializing JVM for PyLucene
vm_env = lucene.initVM(vmargs=['-Djava.awt.headless=true'])

# Function to make sure current thread is attached to JVM for Lucene
def attach_current_thread():
    if not vm_env.isCurrentThreadAttached():
        vm_env.attachCurrentThread()

# Lucene Indexing Function
def create_reddit_index(json_file, index_dir):
    attach_current_thread()

    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
    store = SimpleFSDirectory(Paths.get(index_dir))
    analyzer = StandardAnalyzer()
    config = IndexWriterConfig(analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE_OR_APPEND)
    writer = IndexWriter(store, config)

    # Defining document structure for each field to be stored in indexed
    fieldType = FieldType()
    fieldType.setStored(True)
    fieldType.setTokenized(True)
    fieldType.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

    # Open and read each line of .JSON file
    with open(json_file, 'r', encoding='utf-8') as file:
        # For each line, create Lucene document with fields (PostID, Title, Author, Timestamp, Body)
        for line in file:
            post = json.loads(line)
            doc = Document()
            doc.add(Field('PostID', post['id'], fieldType))
            doc.add(Field('Title', post['title'], fieldType))
            doc.add(Field('Author', post['author'], fieldType))
            doc.add(Field('TimeStamp', str(post['created_utc']), fieldType))
            doc.add(Field('Body', post.get('selftext', ''), fieldType))
            writer.addDocument(doc) # Add document to index
            print(f"Indexed Document: {post['id']} - {post['title']}") # For Debugging
    # Close index writer after indexing all documents
    writer.close()