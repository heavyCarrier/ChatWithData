import mysql.connector
from urllib.parse import urlparse, unquote

# MySQL connection string
connection_string = "mysql://admin_:NeelGaji@77@testneel.mysql.database.azure.com:3306/chatwsql"

# Parse the connection string
parsed_url = urlparse(connection_string)

# Extract the components
host = parsed_url.hostname
user = parsed_url.username
password = unquote(parsed_url.password)  # Decode the password
database = parsed_url.path.lstrip('/')

# Create the connection request format
connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database


)

print(host, user, password, database)

print("Connection established successfully")