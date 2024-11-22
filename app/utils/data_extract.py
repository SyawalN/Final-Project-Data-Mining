import pandas as pd
import os

# Get the data filepath
association_rules_path = os.path.join(os.getcwd(), 'app/data/association_rules.csv')
frequent_itemsets_path = os.path.join(os.getcwd(), 'app/data/frequent_itemsets.csv')

# Function to check if filepath exists
def check_filepath(filepaths):
    for idx, filepath in enumerate(filepaths):
        if (os.path.exists(filepath) == False):
            print(f'Invalid data or filepath not found:\n   {filepath}\n')
            exit()

# Check association_rules and frequent_itemsets filepath
check_filepath([association_rules_path, frequent_itemsets_path])

# Load CSV files from filepath
association_rules = pd.read_csv(association_rules_path)
frequent_itemsets = pd.read_csv(frequent_itemsets_path)

# Convert antecedents and consequents column data from string to sets
association_rules['antecedents'] = association_rules['antecedents'].apply(
    lambda x: set(eval(x)) if isinstance(x, str) else set())
association_rules['consequents'] = association_rules['consequents'].apply(
    lambda x: set(eval(x)) if isinstance(x, str) else set())
frequent_itemsets['itemsets'] = frequent_itemsets['itemsets'].apply(
    lambda x: set(eval(x)) if isinstance(x, str) else set())

# Function to extract title and author
def extract_title_and_author(book_info):
    if '/' in book_info:
        split_info = book_info.rsplit('/', 1)
        title      = split_info[0].strip()
        author     = split_info[1].strip()
        return {
            "judul_buku": title,
            "pengarang": author
        }
    else:
        return {
            "judul_buku": book_info,
            "pengarang": "Tidak diketahui"
        }