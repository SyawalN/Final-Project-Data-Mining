from app.utils.data_extract import extract_title_and_author, frequent_itemsets, association_rules

# Function to filter data based on search input
def search_books(search_term: str):
    search_term = search_term.lower()

    # Finding matching books
    # create a set for matching books
    matching_books = set()
    # iterate every row in frequent_itemsets
    for _, row in frequent_itemsets.iterrows():
        # check each book in itemsets column of each row
        for book in row['itemsets']:
            if search_term in extract_title_and_author(book.lower())['judul_buku']:
                matching_books.add(book)

    results = []
    for book in matching_books:
        results.append(extract_title_and_author(book))
    
    # filters data from matching_books that appears in antecedants part of the rule
    recommendations = association_rules[association_rules['antecedents'].apply(
        lambda x: any(book in x for book in matching_books))]
    # filters data in recommendations that has supports greater than zero
    recommendations = recommendations[recommendations['support'] > 0]
    # sorts data in recommendtaions by support and confidence
    recommendations = recommendations.sort_values(by=['support', 'confidence'], ascending=[False, False])

    # print(recommendations)
    # Generating recommended books list
    # create a list for recommended books
    recommended_books = []
    recommended_books_set = set(matching_books)
    # iterate every row in recommendations
    for _, row in recommendations.iterrows():
        # iterate every book in consequents column of each row
        for book in row['consequents']:
            if book not in matching_books:
                recommended_books.append({
                    **extract_title_and_author(book),
                    "support": row['support'],
                    "confidence": row["confidence"],
                    "lift": row['lift']
                })
                recommended_books_set.add(book)

    return results, recommended_books

def most_borrowedBooks(count):
    most_borrowed_df = frequent_itemsets[frequent_itemsets['support'] > 0].sort_values(by=['support'], ascending=[False])
    most_borrowed_df = most_borrowed_df.head(10)
    most_borrowed_books = []
    for _, row in most_borrowed_df.iterrows():
        for book in row['itemsets']:
            most_borrowed_books.append({
                **extract_title_and_author(book),
                "support": row['support']
            })
    print(type(most_borrowed_books))

    return most_borrowed_books