from process_text import vertical_search_engine, construct_index
from flask import Flask, render_template, request
import pandas as pd
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def search_engine():
    if request.method == 'POST':
        query = request.form['query']
        scraped_db = pd.read_csv('publications.csv').rename(columns={'Unnamed: 0':'SN'}).reset_index(drop=True)
        processed_db = scraped_db.copy()
        xtest = scraped_db.copy()
        indexed = construct_index(processed_db,
                     index = {})
        result = vertical_search_engine(df = xtest, query=query, index=indexed)
        print(type(result))
        return render_template('index.html', query=query, result=result)
    return render_template('index.html', query="", result="")

if __name__ == '__main__':
    app.run(debug = True)