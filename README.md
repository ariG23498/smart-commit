## Smart Commit

<img src="./assets/git-diff.jpeg" height=200 width=300></img>

A tool that creates smart commit messages using the `git diff`.

## Usage

Install the CLI

```sh
$ pip install git+https://github.com/ariG23498/smart-commit
```

Go to a git repository

```sh
$ git add .
$ smart-commit
```

Smart commit gives you a commit message based on the staged changes.

## Tool Help

```sh
NAME
    smart-commit - Main function that orchestrates the commit message generation and user interaction.

SYNOPSIS
    smart-commit <flags>

DESCRIPTION
    Main function that orchestrates the commit message generation and user interaction.

FLAGS
    --model=MODEL
        Default: 'meta-llama/Llama...
    --max_tokens=MAX_TOKENS
        Default: 100
```


## Models

This tool uses the `huggingface_hub.InferenceClient` API. So you can use all the models that support
the inference endpoints!

To know more about inference endpoints please read the official [documentation](https://huggingface.co/docs/inference-endpoints/en/index).

## References

* [Andrej Karpathy's Tweet](https://x.com/karpathy/status/1827810695658029262)
* [Andrej Karpathy's Gist](https://gist.github.com/karpathy/1dd0294ef9567971c1e4348a90d69285)