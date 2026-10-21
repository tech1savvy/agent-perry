import argparse
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

from call_function import available_functions, call_function
from prompts import system_prompt


def main() -> None:
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_promt", type=str, help="User Promt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key is None:
        raise RuntimeError(
            "Env: api_key not found. Please add api_key var to .env file"
        )

    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_promt},
    ]

    if args.verbose:
        print("User prompt:", args.user_promt)

    for _ in range(20):
        message = generate_content(client, messages, args.verbose)
        # Check if final message
        if message.tool_calls is None:
            print("Final response:")
            print(message.content)
            return

    print("Error: agent hit maximum iteration limit")
    sys.exit(1)


def generate_content(client: OpenAI, messages: list, verbose: bool):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        temperature=0,
        tools=available_functions,
    )
    if response.usage is None:
        raise RuntimeError("Failed to send API request")

    if verbose:
        print("Prompt tokens:", response.usage.prompt_tokens)
        print("Response tokens:", response.usage.completion_tokens)
    message = response.choices[0].message

    # Append Feedback
    if message:
        messages.append(message)

    if message.tool_calls:
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, verbose)
            print(f"- Calling function: {tool_call.function.name}")

            if result_message["content"] is None:
                raise Exception("Function call failed")

            if verbose:
                print(f"-> {result_message['content']}")

            # Append Feedback
            messages.append(result_message)

    return message


if __name__ == "__main__":
    main()
