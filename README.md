# MySQLtextAPI
A step-by-step roadmap to create a real database for text data extracted from an API using Python and MySQL

 ## **Step 1: Install Required Packages**
 
Ensure you have the necessary packages installed:
```python
pip install mysql-connector-python requests
```

```python
CREATE DATABASE IF NOT EXISTS my_text_database;
USE my_text_database;

CREATE TABLE IF NOT EXISTS text_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
## **Step 2: Set Up a MySQL Database**

Create a MySQL database and table for storing text data.
```python
import mysql.connector
import requests

# Replace these values with your MySQL connection details
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

# Step 2: Fetch data from the API
api_url = 'https://api.example.com/textdata'
response = requests.get(api_url)

if response.status_code == 200:
    data_from_api = response.json()  # Assuming the API returns JSON
else:
    print(f"Error fetching data from API. Status code: {response.status_code}")
    data_from_api = []

# Step 3: Insert data into the MySQL database
for item in data_from_api:
    cursor.execute('''
        INSERT INTO text_data (content) VALUES (%s)
    ''', (item['text'],))

conn.commit()

# Step 4: Close the connection
conn.close()
```
# **Step 3: Write a Python Script**
Create a Python script to fetch data from the API and store it in the MySQL database.

```python
python your_script_name.py
```

