import os
import dotenv
import openai


def generate_message(client, messages):
    """
    Generate a message using the OpenAI client with streaming output.
    Args:
        client: An instance of the OpenAI client.
        messages: A list of message dictionaries containing role and content.
    """

    stream = client.responses.create(
        model="gpt-4.1-nano",
        input=messages,
        max_output_tokens=250,
        stream=True,
    )

    full_output = ""
    for event in stream:
        if event.type == 'response.output_text.delta':
            if event.delta:
                full_output += event.delta
                print(event.delta, end='', flush=True)

    messages.append({
        "role": "assistant",
        "content": full_output + '\n'
    })

    return messages


def main():
    # Load environment variables from .env file
    if os.path.exists('.env'):
        dotenv.load_dotenv()

    # Ensure the OPENAI_API_KEY is set
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if openai.api_key is None:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    # Initialize the OpenAI client and message list
    client = openai.OpenAI()
    messages = []

    # Repeat the message generation process until the user says "exit"
    print()
    print("--------- WELCOME TO THE THIAGOBOT ---------")
    print("I am ready! Type a message ('exit' if you want to quit).", end='\n\n')
    while True:
        # Check for the stop criteria
        input_text = input("User: ")
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
