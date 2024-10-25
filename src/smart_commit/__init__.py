import subprocess
from fire import Fire
from huggingface_hub import InferenceClient


def get_git_diff():
    result = subprocess.run(['git', 'diff', '--cached', '--', '*.py'], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error getting git diff")
        return ''
    if not result.stdout.strip():
        print("No staged Python files detected.")
        return ''
    return result.stdout

def generate_commit_message(diff_text, model_name, max_tokens=50):
    client = InferenceClient()

    chat_completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a helpful programming assistant with no verbosity."},
            {"role": "user", "content": f"Summarize and output the following git diff into a concise git commit message:\n\n{diff_text}\n\nCommit message:"},
        ],
        max_tokens=max_tokens,
    )
    return chat_completion.choices[0].message.content


def app(model="meta-llama/Llama-3.2-1B-Instruct", max_tokens=50):
    diff_text = get_git_diff()
    if not diff_text.strip():
        print("No staged changes detected.")
        return

    commit_message = generate_commit_message(
        diff_text, model_name=model, max_tokens=max_tokens
    )
    print(commit_message)


def main():
    Fire(app)
