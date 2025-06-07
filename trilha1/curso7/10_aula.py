# Desafio - Chatbot Finanças (em .py)

import os
import json
import openai
import yfinance as yf
from dotenv import load_dotenv


def get_ticker_history(ticker, period='1mo'):
    """
    Fetch historical market data for a given ticker symbol.
    """
    try:
        ticker_data = yf.Ticker(ticker)
        history = ticker_data.history(period=period)['Close']
        history.index = history.index.strftime('%Y-%m-%d')  # Format index to string
        history = round(history, 2)

        if len(history) > 30:
            slice_size = 30
        else:
            slice_size = 0

        history = history[-slice_size::]

        return history.to_dict()
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None


# Route each function call to the appropriate function
def call_function(name, args):
    available_functions = {
        "get_ticker_history": get_ticker_history,
        # "other_function": other_function,  # Uncomment and define other functions as needed
    }

    if name in available_functions:
        return available_functions[name](**args)
    else:
        raise ValueError(f"Function {name} is not available.")


def generate_message(client, messages):
    """
    Generate a message using the OpenAI client with streaming output.
    Args:
        client: An instance of the OpenAI client.
        messages: A list of message dictionaries containing role and content.
    """

    # Specify the available tools for the model
    tools = [{
        "type": "function",
        "name": "get_ticker_history",
        "description": "Get historical market data for a given ticker symbol.",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {"type": "string",
                           "description": "The ticker symbol of the stock."},
                "period": {"type": "string",
                           "description": "The time period for the historical data.  \
                            Format: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max, etc. \
                            Observation: 1d equals 1 day, 1mo equals 1 month, 1y equals 1 year. \
                            Defaults to '1mo'.",
                           "enum": ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]}
            },
            "required": ["ticker", "period"],
            "additionalProperties": False
        },
        "strict": True
    }]

    stream = client.responses.create(
        model="gpt-4.1-nano",
        input=messages,
        tools=tools,
        max_output_tokens=250,
        stream=True,
    )

    full_output = ""
    for event in stream:
        if event.type == 'response.output_text.delta':
            if event.delta:
                full_output += event.delta
                print(event.delta, end='', flush=True)

        elif event.type == 'response.output_item.done':
            if event.item.type != "function_call":
                continue

            # Append model's function call message
            messages.append(event.item.to_dict())

            # Call the function with the provided arguments
            name = event.item.name
            args = json.loads(event.item.arguments)
            result = call_function(name, args)

            # Append function call result message
            messages.append({
                "type": "function_call_output",
                "call_id": event.item.call_id,
                "output": str(result)
            })

            response = client.responses.create(
                # model="gpt-4.1-nano",
                model="gpt-4.1",
                input=messages,
            )
            full_output = response.output_text
            print(full_output, end='', flush=True)

    messages.append({
        "role": "assistant",
        "content": full_output + '\n'
    })

    return messages


def main():
    # Load environment variables from .env file
    if os.path.exists('.env'):
        load_dotenv()

    # Ensure the OPENAI_API_KEY is set
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if openai.api_key is None:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    # Initialize the OpenAI client and message list
    client = openai.OpenAI()
    messages = []

    # Repeat the message generation process until the user says "exit"
    print()
    print("--------- WELCOME TO THE FINANCIALBOT ---------")
    print("I am ready! Type a message ('exit' if you want to quit).", end='\n\n')

    while True:
        # Check for the stop criteria
        input_text = input("User: ")
        # input_text = "What's the current stock price of AAPL?"
        if input_text.lower() == "exit":
            print("Exiting the chatbot.")
            break

        messages.append(
            {
                "role": "user",
                "content": input_text
            }
        )

        # Generate the assistant's response
        print('Assistant: ', end='')
        messages = generate_message(client, messages)
        print('')


if __name__ == "__main__":
    main()
