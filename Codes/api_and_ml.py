from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import mysql.connector
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import pandas as pd

app = Flask(__name__)

# Replace these values with your actual MySQL connection details
mysql_host = 'your_mysql_host'
mysql_user = 'your_mysql_user'
mysql_password = 'your_mysql_password'
mysql_database = 'my_text_database'

@app.route('/extract_and_cluster', methods=['GET'])
def extract_and_cluster():
    # Step 1: Connect to MySQL database
    conn = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_database
    )
    cursor = conn.cursor()

    # Step 2: Web Scraping
    url = 'https://www.varzesh3.com/'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract text data from the website (customize based on the structure of the website)
        headlines = [headline.text.strip() for headline in soup.find_all('h3', class_='headline')]

    else:
        print(f"Error fetching data from the website. Status code: {response.status_code}")
        headlines = []

    # Step 3: Insert data into the MySQL database
    for headline in headlines:
        cursor.execute('''
            INSERT INTO text_data (content) VALUES (%s)
        ''', (headline,))

    conn.commit()

    # Step 4: Fetch data from the database
    cursor.execute('SELECT content FROM text_data')
    data_from_db = [row[0] for row in cursor.fetchall()]

    # Step 5: Text Preprocessing
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(data_from_db)

    # Step 6: Apply Clustering (KMeans)
    kmeans = KMeans(n_clusters=5)
    kmeans.fit(X)

    # Step 7: Dimensionality Reduction (PCA)
    pca = PCA(n_components=2)
    reduced_features = pca.fit_transform(X.toarray())
    reduced_cluster_centers = pca.transform(kmeans.cluster_centers_)

    # Step 8: Prepare and return results
    results = {'data': [], 'clusters': []}

    for i, text in enumerate(data_from_db):
        cluster_label = kmeans.labels_[i]
        results['data'].append({'text': text, 'cluster': cluster_label})

    for i, center in enumerate(reduced_cluster_centers):
        results['clusters'].append({'cluster': i, 'center': center.tolist()})

    # Step 9: Close the connection
    conn.close()

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
