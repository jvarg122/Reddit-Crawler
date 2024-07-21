# Reddit-Crawler

## Overview
This project is a Reddit post crawler and search engine. It consists of several components that work together to collect, index, and search Reddit posts. The system extracts relevant fields (e.g., username, timestamp, body) from Reddit and HTML data. It allows users to search for posts via a web interface, providing a user-friendly way to retrieve relevant information from the indexed data.

## System Architecture
The architecture of the system comprises four main components:

<img src="https://i.imgur.com/fL6uKDb.png" alt="Flowchart" style="width: 50%;">

1. **Data Collection:** The Reddit crawler compiles Reddit posts into JSON files.
2. **Data Indexing:** The JSON files are processed and indexed using PyLucene.
3. **Search Engine:** A search engine retrieves search results from the Lucene index.
4. **Web Application:** A Flask web application allows users to enter search queries and view relevant results.

## Tools & Technologies

**Backend**
- **Python:** The primary programming language used for data collection, indexing, search engine logic, and web application backend.
- **[Flask](https://flask.palletsprojects.com/en/3.0.x/):** A lightweight web framework used to create the web application and handle HTTP requests.
- **[PyLucene](https://lucene.apache.org/pylucene/):** A Python extension for accessing Java Lucene, used for indexing and searching Reddit posts.
- **[Requests](https://pypi.org/project/requests/):** A simple HTTP library for Python, used for making HTTPS requests to fetch data.
  
**Frontend**
- **HTML:** Used to structure the content and layout of web pages.
- **CSS:** Used to style the web pages and improve the user interface.
- **JavaScript:** Used to enhance user interaction and dynamic content rendering on the web pages.

**Data Formats**
- **JSON:** Used to store and parse Reddit post data collected by the crawler.

## Usage

**Installation**

1. Clone this repo:
```
git clone https://github.com/jvarg122/Reddit-Crawler.git
```

2. Dependencies

Install the following required python packages:
```
pip install flask
pip install pylucene
pip install requests
```
To start the Flask web application, run the script:
```
python3 index_reddit.py
```
To view an example of the app in action, refer to the snapshots below:

<p align="center">
<img src= "https://i.imgur.com/HsBN8mg.png">
</p>

The user submits a search query through the app's interface

<p align="center">
<img src= "https://i.imgur.com/CPWMjz9.png">
</p>

The app processes the query and retrieves relevant search results based on the user's input. The relevant search results are displayed.
