from flask import Blueprint, render_template, jsonify, request
from app.utils.data_filter import search_books

bp = Blueprint('main', __name__)

@bp.route('/')
def index() -> str:
    return render_template('index.html')

@bp.route('/search', methods=['POST'])
def search():
    search_input = request.form['search_term']
    results, recommended_books = search_books(search_input)

    # Return data as JSON
    return jsonify({
        'results': results,
        'recommended_books': recommended_books
    })

@bp.route('/results')
def results():
    return "Hello: ", request.args.get('search')