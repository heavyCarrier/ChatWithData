import os
import logging
from openai import AzureOpenAI

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up Azure OpenAI Service credentials
endpoint = "https://genai-openai-techtinkerers.openai.azure.com/"  # Replace with your Azure endpoint
key = "9905318139b445acb23c596d5f7d7251"  # Replace with your API key
model_name = "gpt-35-turbo"  # Replace with your Azure-deployed model name

# Initialize AzureOpenAI client
client = AzureOpenAI(azure_endpoint=endpoint, api_version="2024-02-01", api_key=key)

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
