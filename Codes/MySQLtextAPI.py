import requests
from bs4 import BeautifulSoup
import mysql.connector

# Replace these values with your actual MySQL connection details
mysql_host = 'your_mysql_host'
mysql_user = 'your_mysql_user'
mysql_password = 'your_mysql_password'
mysql_database = 'my_text_database'

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

# Step 4: Close the connection
conn.close()
