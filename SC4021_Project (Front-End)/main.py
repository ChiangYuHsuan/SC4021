from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Sample 2D array (you can replace it with dynamic data fetching)
data = []

# Query_1 Logic, Display All Based On Comment_Author
def query_1(search_term=None):

    conn = sqlite3.connect('reddit_data.db')
    cursor = conn.cursor()
    
    query = "SELECT * FROM reddit_data WHERE comment_author IS NOT NULL  AND TRIM(comment_author) != '' AND comment_author = ?;"

    cursor.execute(query, (search_term,))

    data = cursor.fetchall()

    print(data)

    conn.close()

    return data

def query_2(search_term=None):
    # Query 2 logic (example: sort by age)

    return data

def query_3(search_term=None):
    # Query 3 logic (example: filter by country)
    if search_term:
        return [row for row in data if search_term.lower() in row[2].lower()]
    return data

def query_4(search_term=None):
    # Query 4 logic (example: dummy query)
    return data

def query_5(search_term=None):
    # Query 5 logic (example: another dummy query)
    return data

# Map of queries to function
queries = {
    'Query 1': query_1,
    'Query 2': query_2,
    'Query 3': query_3,
    'Query 4': query_4,
    'Query 5': query_5
}

@app.route('/', methods=['GET', 'POST'])
def index():
    search_term = None
    selected_query = 'Query 1'  # Default query

    if request.method == 'POST':
        search_term = request.form.get('search', '')
        selected_query = request.form.get('query', 'Query 1')
    
    # Call the corresponding function based on the selected query
    query_function = queries.get(selected_query, query_1)  # Default to query_1
    filtered_data = query_function(search_term)

    return render_template('display.html', data=filtered_data)

if __name__ == '__main__':
    app.run(debug=True)
