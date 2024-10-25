import subprocess
from fire import Fire
from huggingface_hub import InferenceClient, login


def get_git_diff():
    # Get the diff of staged Python files
    result = subprocess.run(
        ['git', 'diff', '--cached', '--', '*.py'],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print("Error getting git diff")
        return ''
    diff_output = result.stdout.strip()
    if not diff_output:
        print("No staged Python files detected.")
        return ''

    return diff_output


def generate_commit_message(diff_text, model_name, max_tokens=100):
    client = InferenceClient()

    # Construct the prompt with clearer instructions
    messages = [
        {
            "role": "system",
            "content": (
                "You are an AI assistant that writes concise and descriptive git commit messages based on code changes."
                "Given the following git diff, generate a clear and concise commit message that accurately describes the changes."
            )
        },
        {
            "role": "user",
            "content": f"Git diff:\n{diff_text}"
        },
    ]

    chat_completion = client.chat.completions.create(
        model=model_name,
        messages=messages,
        max_tokens=max_tokens,
    )
    return chat_completion.choices[0].message.content.strip()


def app(model="meta-llama/Llama-3.2-1B-Instruct", max_tokens=100):
    # login to hf
    login()

    diff_text = get_git_diff()
    if not diff_text:
        return

    # Optionally limit the diff size to avoid exceeding model input limits
    max_diff_length = 2048  # Adjust as needed based on model's context window
    if len(diff_text) > max_diff_length:
        print("Diff is too large; truncating to fit the model's input limits.")
        diff_text = diff_text[:max_diff_length]

    commit_message = generate_commit_message(
        diff_text, model_name=model, max_tokens=max_tokens
    )
    print("\nSuggested Commit Message:\n")
    print(commit_message)


def main():
    Fire(app)


if __name__ == "__main__":
    main()
