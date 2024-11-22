from flask import Blueprint, render_template, jsonify, request
from app.utils.data_filter import search_books, most_borrowedBooks

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/api/data')
def api_data():
    most_borrowed_books = most_borrowedBooks(10)
    return jsonify({
        'status': 200,
        'message': "Berhasil mengambil data", 
        'data': most_borrowed_books
    })

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