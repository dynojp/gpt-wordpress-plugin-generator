# WordPress plugin generator with OpenAI ChatGPT

A script to generate WordPress plugins using the OpenAI ChatGPT API.

## Prerequisites

- Python `>=3.12.0`
- Poetry `>=1.8.3`
- OpenAI API key

## Usage

Get OpenAI API key and set it to an environment variable `OPENAI_API_KEY`.

```bash
export OPENAI_API_KEY=...
```

Install dependencies.

```bash
poetry install
```

If you prefer not to use Poetry, install `click` and `openai` with `pip` directly in a venv.

```bash
pip install 'click~=8.1' 'openai~=1.40'
```

Once dependencies are installed, run the script.

```bash
poetry run python main.py
```

## Samples

```bash
por python main.py \
  --name='disable-search' \
  --prompt='Make a plugin to disable the WordPress core search function.'
```
