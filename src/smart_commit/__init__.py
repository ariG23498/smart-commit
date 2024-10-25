import os
import subprocess
from fire import Fire
from huggingface_hub import InferenceClient

def get_git_diff():
    """
    Retrieves the git diff of staged changes.
    """
    result = subprocess.run(
        ['git', 'diff', '--cached'],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print("Error getting git diff")
        return ''
    diff_output = result.stdout.strip()
    if not diff_output:
        print("No staged changes detected.")
        return ''
    return diff_output

def generate_commit_message(diff_text, model_name, max_tokens=100, token=None):
    """
    Generates a commit message using the language model based on the git diff.
    """
    # Use the provided token, or read from environment, or default to None
    token = token or os.getenv("HF_TOKEN")
    client = InferenceClient(token=token)

    # Construct the prompt similar to Andrej's script
    prompt = (
        "Below is a diff of all staged changes, coming from the command:\n\n"
        "```\n"
        "git diff --cached\n"
        "```\n\n"
        "Please generate a concise, one-line commit message for these changes."
        "Only output the one-line message with nothing else."
    )

    # Include the diff in the user's message
    messages = [
        {"role": "user", "content": f"{prompt}\n\n{diff_text}"}
    ]

    # Call the language model to generate the commit message
    chat_completion = client.chat.completions.create(
        model=model_name,
        messages=messages,
        max_tokens=max_tokens,
        temperature=0.5,
    )

    # Return the generated commit message
    return chat_completion.choices[0].message.content.strip()

def read_input(prompt):
    """
    Reads user input in a way that is compatible with both Python 2 and 3.
    """
    try:
        # For Python 3
        return input(prompt)
    except NameError:
        # For Python 2
        return raw_input(prompt)

def app(model="meta-llama/Llama-3.2-3B-Instruct", max_tokens=100, token=None):
    """
    Main function that orchestrates the commit message generation and user interaction.
    """
    diff_text = get_git_diff()
    if not diff_text:
        return

    # Optionally limit the diff size to avoid exceeding model input limits
    max_diff_length = 2048  # Adjust as needed based on model's context window
    if len(diff_text) > max_diff_length:
        print("Diff is too large; truncating to fit the model's input limits.")
        diff_text = diff_text[:max_diff_length]

    print("Generating AI-powered commit message...")
    commit_message = generate_commit_message(diff_text, model_name=model, max_tokens=max_tokens, token=token)

    while True:
        print("\nProposed Commit Message:\n")
        print(commit_message)

        # Prompt the user for action
        choice = read_input("\nDo you want to (a)ccept, (e)dit, (r)egenerate, or (c)ancel? ").strip().lower()

        if choice == 'a':
            # User accepts the commit message
            if subprocess.call(['git', 'commit', '-m', commit_message]) == 0:
                print("Changes committed successfully!")
                return
            else:
                print("Commit failed. Please check your changes and try again.")
                return
        elif choice == 'e':
            # User wants to edit the commit message
            commit_message = read_input("Enter your commit message: ").strip()
            if commit_message:
                if subprocess.call(['git', 'commit', '-m', commit_message]) == 0:
                    print("Changes committed successfully with your message!")
                    return
                else:
                    print("Commit failed. Please check your message and try again.")
                    return
            else:
                print("Commit message cannot be empty.")
        elif choice == 'r':
            # User wants to regenerate the commit message
            print("Regenerating commit message...")
            commit_message = generate_commit_message(diff_text, model_name=model, max_tokens=max_tokens, token=token)
        elif choice == 'c':
            # User cancels the operation
            print("Commit cancelled.")
            return
        else:
            print("Invalid choice. Please try again.")

def main():
    Fire(app)

if __name__ == "__main__":
    main()
