from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

# Load the CSV files
rules_path = 'rules.csv'
frequent_itemset_path = 'frequent_itemsets.csv'

rules = pd.read_csv(rules_path)
frequent_itemsets = pd.read_csv(frequent_itemset_path)

# Convert antecedents and consequents from string to sets for easy search
rules['antecedents'] = rules['antecedents'].apply(lambda x: set(eval(x)) if isinstance(x, str) else set())
rules['consequents'] = rules['consequents'].apply(lambda x: set(eval(x)) if isinstance(x, str) else set())
frequent_itemsets['itemsets'] = frequent_itemsets['itemsets'].apply(lambda x: set(eval(x)) if isinstance(x, str) else set())

# Function to extract title and author
def extract_title_and_author(book_info):
    if '/' in book_info:
        split_info = book_info.rsplit('/', 1)
        title = split_info[0].strip()
        author = split_info[1].strip()
        return {"judul_buku": title, "pengarang": author}
    else:
        return {"judul_buku": book_info, "pengarang": "Tidak diketahui"}

# Function to perform the search
def search_books(search_term):
    search_term = search_term.lower()
    matching_books = set()
    for _, row in frequent_itemsets.iterrows():
        for book in row['itemsets']:
            if search_term in book.lower():
                matching_books.add(book)
    
    results = []
    for book in matching_books:
        results.append(extract_title_and_author(book))
    
    recommendations = rules[rules['antecedents'].apply(lambda x: any(book in x for book in matching_books))]
    recommendations = recommendations[recommendations['support'] > 0]
    recommendations = recommendations.sort_values(by=['support', 'confidence'], ascending=[False, False])
    
    recommended_books = []
    recommended_books_set = set(matching_books)
    
    for _, row in recommendations.iterrows():
        for book in row['consequents']:
            if book not in recommended_books_set:
                recommended_books.append({
                    **extract_title_and_author(book),
                    "support": row['support'],
                    "confidence": row['confidence'],
                    "lift": row['lift']
                })
                recommended_books_set.add(book)
    
    return results, recommended_books

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')  # Create a simple form in 'templates/index.html'

@app.route('/search', methods=['POST'])
def search():
    search_term = request.form.get('search_term', '')
    results, recommendations = search_books(search_term)
    return render_template('results.html', search_term=search_term, results=results, recommendations=recommendations)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
