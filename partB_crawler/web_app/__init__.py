from flask import Flask, request, render_template
from searchEngine import retrieve, attach_current_thread

def create_app():
    app = Flask(__name__, template_folder='../templates')
    # app.config['SECRET_KEY'] = 'project172'

    @app.route('/', methods=['GET', 'POST'])
    def home():
        if request.method == 'POST':
            query = request.form['query']
            attach_current_thread()
            results = retrieve('reddit_index', query)
            return render_template('results.html', query=query, results=results)
        return render_template('index.html')

    return app
