import pandas as pd

# Load the rules.csv and frequent_itemset.csv files
rules_path = 'rules.csv'
frequent_itemset_path = 'frequent_itemsets.csv'

rules = pd.read_csv(rules_path)
frequent_itemsets = pd.read_csv(frequent_itemset_path)

# Convert antecedents and consequents from string to sets for easy search
rules['antecedents'] = rules['antecedents'].apply(lambda x: set(eval(x)) if isinstance(x, str) else set())
rules['consequents'] = rules['consequents'].apply(lambda x: set(eval(x)) if isinstance(x, str) else set())

# Section 1: Load the frequent itemsets data and filter by search term
frequent_itemsets['itemsets'] = frequent_itemsets['itemsets'].apply(lambda x: set(eval(x)) if isinstance(x, str) else set())

# Define the search engine function
def search_book_partial(search_term):
    search_term = search_term.lower()
    print(f"Search results for: {search_term}")

    # Section 1: Result Section - Show books matching the search term from frequent_itemsets.csv
    matching_books = set()
    for _, row in frequent_itemsets.iterrows():
        for book in row['itemsets']:
            if search_term in book.lower():
                matching_books.add(book)
    
    if matching_books:
        print("\nSection 1: Matching Books Found")
        print(f"Books matching '{search_term}': {', '.join(matching_books)}")
    else:
        print(f"No books matching '{search_term}' were found.")
    
    # Section 2: Recommendations Section - Find books frequently borrowed with the matching books (from rules.csv)
    recommendations = rules[rules['antecedents'].apply(lambda x: any(book in x for book in matching_books))]
    
    # Filter and sort recommendations by support > 0 and sort by support (desc) and confidence (desc)
    recommendations = recommendations[recommendations['support'] > 0]
    recommendations = recommendations.sort_values(by=['support', 'confidence'], ascending=[False, False])
    
    # Set to keep track of recommended books (to avoid duplicates)
    recommended_books_set = set(matching_books)  # Start with the matching books
    
    if not recommendations.empty:
        print("\nSection 2: Recommended Books Frequently Borrowed Together")
        for _, row in recommendations.iterrows():
            recommended_books = row['consequents']
            
            # Exclude books already shown in Section 1 (matching books)
            filtered_books = recommended_books - recommended_books_set
            
            if filtered_books:
                print(f"Recommended books: {', '.join(filtered_books)} (Support: {row['support']:.2f}, Confidence: {row['confidence']:.2f}, Lift: {row['lift']:.2f})")
                # Add the recommended books to the set to avoid showing them again
                recommended_books_set.update(filtered_books)
            else:
                # Skip this row if no new recommendations
                continue
    else:
        print("\nNo recommendations found for the matching books.")

# Example usage of the search function
search_book_partial("bank soal kimia")
