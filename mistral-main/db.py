import csv
import time
import mysql.connector
 
# Establish connection to Azure MySQL
connection = mysql.connector.connect(
    host="testneel.mysql.database.azure.com",
    user="admin_",
    password="NeelGaji@77",
    database="chatwsql"
)
cursor = connection.cursor()
 
# Function to insert data from a CSV file
def insert_data_from_csv():
    csv_file = r"C:\Users\YGoel\Desktop\ChatWithData\DataInput\queries.csv"  # Replace with the path to your CSV file
   
    try:
        with open(csv_file, mode='r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header row, if any
           
            # Convert rows to match table schema: cast id and account_number to integers
            data_to_insert = [
                (int(row[0]), row[1], row[2], row[3], row[4], row[5]) for row in csv_reader
            ]
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return
   
    # Insert data from CSV file into the table
    insert_query = """
    INSERT INTO table1 (id, name, account_number, account_type, country, occupation)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    try:
        cursor.executemany(insert_query, data_to_insert)
        connection.commit()
        print(f"{cursor.rowcount} rows inserted from CSV!")
    except mysql.connector.Error as e:
        print(f"Error inserting data into MySQL table: {e}")
        connection.rollback()  # Rollback in case of error
    finally:
        cursor.close()
        connection.close()
 
# Run the insert function
insert_data_from_csv()
print("COMPLETED SCRIPT")
 
# Optional delay
time.sleep(2)
 
has context menu