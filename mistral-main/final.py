import mysql.connector
from openai import AzureOpenAI


# Set up Azure OpenAI Service credentials
endpoint = "https://genai-openai-techtinkerers.openai.azure.com/"  # Replace with your Azure endpoint
key = "9905318139b445acb23c596d5f7d7251"  # Replace with your API key
model_name = "gpt-35-turbo"  # Replace with your Azure-deployed model name

# Initialize AzureOpenAI client
client = AzureOpenAI(azure_endpoint=endpoint, api_version="2024-02-01", api_key=key)

# Establish connection to Azure MySQL
connection = mysql.connector.connect(
    host="testneel.mysql.database.azure.com",
    user="admin_",
    password="NeelGaji@77",
    database="chatwsql"
)

table_name = "table1"

def fetch_table_schema(connection, table_name):
    schema_query = f"DESCRIBE {table_name};"
    schema_string = ""

    try:
        cursor = connection.cursor()
        cursor.execute(schema_query)
        schema_data = cursor.fetchall()
        
        # Format schema details into a readable string
        schema_string = "\n".join(
            f"Column: {row[0]}, Type: {row[1]}, Null: {row[2]}, Key: {row[3]}, Default: {row[4]}, Extra: {row[5]}"
            for row in schema_data
        )
    except mysql.connector.Error as e:
        print(f"Error fetching schema from MySQL table: {e}")
        connection.rollback()
    finally:
        cursor.close()

    return schema_string

def generate_sql(user_input):
    # Prepare the prompt for SQL generation
    messages = [
        {"role": "user", "content": f"Convert the following natural language request into an SQL query: {user_input}"}
    ]
    
    # Generate text using the Azure OpenAI Service
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=messages
        )
        generated_text = response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error generating text: {e}")
        raise
    
    return generated_text

def main():
    print("SQL Query Generator using Azure OpenAI Service\n")
    
    # Take user input
    user_input = input("Enter your query description: ")
    
    # Generate the corresponding SQL code
    try:
        sql_code = generate_sql(user_input)
        # Print the generated SQL
        print("\nGenerated SQL Code:\n", sql_code)
    except Exception as e:
        logger.error(f"Error in main: {e}")

if __name__ == "__main__":
    main()

# Fetch schema and pass it to another function
schema_string = fetch_table_schema(connection, table_name)
print("Table Schema:\n", schema_string)

# Close the connection
connection.close()
