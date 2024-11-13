import mysql.connector
from openai import AzureOpenAI
from urllib.parse import urlparse, unquote

# Set up Azure OpenAI Service credentials
endpoint = "https://genai-openai-techtinkerers.openai.azure.com/"  # Replace with your Azure endpoint
key = "9905318139b445acb23c596d5f7d7251"  # Replace with your API key
model_name = "gpt-35-turbo"  # Replace with your Azure-deployed model name

# Initialize AzureOpenAI client
client = AzureOpenAI(azure_endpoint=endpoint, api_version="2024-02-01", api_key=key)


def fetch_table_schema(connection, table_name):
     # Parse the connection string
    parsed_url = urlparse(connection)

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

def generate_sql(schema, user_input,table_name):
    # Prepare the prompt for SQL generation, including schema for context
    dialect = "MySQL"
    top_k = 5
    table_info = schema
    input = user_input
    prompt = f"""You are a {dialect} expert. Given an input question, create a syntactically correct {dialect} query to run.
            Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the TOP clause as per {dialect}. You can order the results to return the most informative data in the database.
            Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in angular brackets (<>) to denote them as delimited identifiers.
            Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
            Pay attention to use date('now') function to get the current date, if the question involves "today".

            if table name is given in {user_input} then use that otherwise use {table_name} to create query.
            Even if multiple table names are given use them accordingly.
 
            Only use the following table_schema:
            {table_info}
 
            Write an initial draft of the query. Then double check the {dialect} query for common mistakes, including:
            - Using NOT IN with NULL values
            - Using UNION when UNION ALL should have been used
            - Using BETWEEN for exclusive ranges
            - Data type mismatch in predicates
            - Properly quoting identifiers
            - Using the correct number of arguments for functions
            - Casting to the correct data type
            - Using the proper columns for joins
           
            Question: {input}
           
            Use ALWAYS format:
 
            Final answer: <<FINAL_ANSWER_QUERY>>
            """

    
    messages = [
        {"role": "user", "content":prompt}]
    
    
    # Generate text using the Azure OpenAI Service
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=messages
        )
        generated_text = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating SQL: {e}")
        raise
    
    return generated_text

def user_request_handle(connection_string, user_input, table_name):
    # Generate the corresponding SQL code
    try:
       
        schema_output = fetch_table_schema(connection_string, table_name)
        sql_code = generate_sql(schema_output, user_input,table_name)
        # Print the generated SQL
        print("\nGenerated SQL Code:\n", sql_code)
        return {"is_successfull":True, "query":sql_code}    
    except Exception as e:
        print(f"Error in main: {e}")
        return {"is_successfull":False, "erro":e}


def main():
    print("SQL Query Generator using Azure OpenAI Service\n")
    
    # Take user input
    user_input = input("Enter your query description: ")
    table_name = "table1"
    # Fetch schema from MySQL table
    schema_string = fetch_table_schema(connection, table_name)
    
    
    # Generate the corresponding SQL code
    try:
        sql_code = generate_sql(schema_string, user_input,table_name)
        # Print the generated SQL
        print("\nGenerated SQL Code:\n", sql_code)
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    main()



