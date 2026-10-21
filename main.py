import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
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

    generate_content(client, messages, args.verbose)


def generate_content(client: OpenAI, messages: list, verbose: bool) -> None:
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        temperature=0,
    )
    if response.usage is None:
        raise RuntimeError("Failed to send API request")

    if verbose:
        print("Prompt tokens:", response.usage.prompt_tokens)
        print("Response tokens:", response.usage.completion_tokens)
    print("Response: ")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
