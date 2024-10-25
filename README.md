## Smart Commit

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

> Note
This only takes care of the python file changes for now.

## Models

This tool uses the `huggingface_hub.InferenceClient` API. So you can use all the models that support
the inference endpoints!

To know more about inference endpoints please read the official [documentation](https://huggingface.co/docs/inference-endpoints/en/index).