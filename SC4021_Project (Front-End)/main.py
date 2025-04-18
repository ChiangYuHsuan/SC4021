from flask import Flask, render_template, request
import sqlite3
import requests
import time
from datetime import datetime
import re

app = Flask(__name__)

# Sample 2D array (you can replace it with dynamic data fetching)
data = []
SOLR_URL = 'http://localhost:8983/solr/reddit/select'

def clean_query(query):
    if query is None:
        return
    return re.sub(r'[^\w\s]', '', query)

# Query Logic, Display All Based On Comment_Author
def query(search_term=None, start_date=None, end_date=None):
    clean_search_term = clean_query(search_term)
    print(clean_search_term)
    # Default Parameters
    params = {
        'q': f'{clean_search_term}' if clean_search_term else "*:*", #Term to search
        'q.op' : "AND",
        'sort' : "comment_score desc",
        'fl': 'comment_score, comment_date, comment_content, sentiment_score',  # Fields to return
        'df': 'comment_content', # Field to search from
        'wt': 'json',  # Specify format of response (JSON)
        'rows': 10000000,  # Limit to 1000 results, adjust as needed 
        'defType': 'edismax',
    }


    # Apply date filter
    if start_date and end_date:
        params['fq'] = f'comment_date:[{start_date}T00:00:00Z TO {end_date}T23:59:59Z]'
    elif start_date:
        params['fq'] = f'comment_date:[{start_date}T00:00:00Z TO *]'
    elif end_date:
        params['fq'] = f'comment_date:[* TO {end_date}T23:59:59Z]'

    try:
        start_time = time.time()

        response = requests.get(SOLR_URL, params=params)
        response.raise_for_status()
        # print(response.json())

        end_time = time.time()
        elapsed_time_ms = (end_time - start_time) * 1000
        elapsed_time_ms = round(elapsed_time_ms, 2)

        num_found = response.json()['response']['numFound']

        # Check for number of results received, if 0 then provide suggestions
        if response.json()['response']['numFound']==0:
            collations = response.json()['spellcheck']['collations']
            spellcheck_suggestions = []
            spellcheck_suggestions.append(['Word Suggestion', 'Number of results'])
            for i in range(1, len(collations), 2):
                suggestion = collations[i]
                collation_query = suggestion['collationQuery']
                hits = suggestion['hits']
                spellcheck_suggestions.append([collation_query, hits])

            return spellcheck_suggestions, elapsed_time_ms, num_found

        # Extract out information required and return information to display
        data = response.json()['response']['docs']
        processed_data = []
        processed_data.append(['comment_score', 'comment_date', 'comment_content', 'Net Sentiment'])
        for entry in data:
            processed_entry = []
            for field in ['comment_score', 'comment_date', 'comment_content', 'sentiment_score']:
                if field == 'comment_date':
                    date_str = entry.get(field, [None])[0]
                    if date_str:
                        date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
                        processed_entry.append(date_obj.strftime('%Y-%m-%d'))
                    else:
                        processed_entry.append(None)
                elif field == 'sentiment_score':
                    sentiment_score = entry.get(field, [None])[0]
                    if sentiment_score is not None:
                        if sentiment_score > 0:
                            processed_entry.append('Positive')
                        elif sentiment_score < 0:
                            processed_entry.append('Negative')
                        else:
                            processed_entry.append('Neutral')
                    else:
                        processed_entry.append(None)
                else:
                    processed_entry.append(entry.get(field, [None])[0])
            processed_data.append(processed_entry)

        # print(processed_data)
        return processed_data, elapsed_time_ms, num_found

    except requests.exceptions.RequestException as e:
        print(f"Error querying Solr: {e}")
        return []

@app.route('/', methods=['GET', 'POST'])
def index():
    search_term = None
    start_date = None
    end_date = None
    selected_query = 'Query 1'  # Default query
    sentiment_categories = []

    if request.method == 'POST':
        search_term = request.form.get('search', '')
        start_date = request.form.get('start_date', None)
        end_date = request.form.get('end_date', None)
    
    filtered_data, elapsed_time_ms, num_found = query(search_term, start_date, end_date)
    return render_template('display.html', data=filtered_data, elapsed_time=elapsed_time_ms, num_found=num_found)

if __name__ == '__main__':
    app.run(debug=True)