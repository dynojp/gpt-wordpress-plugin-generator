"""Generate a WordPress plugin with OpenAI ChatGPT."""

import os
import sys
from pathlib import Path

import click
from openai import OpenAI
from pydantic import BaseModel

MODEL_DEFAULT = "gpt-4o-2024-08-06"

SYSTEM_PROMPT = """
You are an experienced WordPress developer tasked with creating a new plugin. Please provide all files for a WordPress plugin based on the following specifications:

Your response should include:

1. A brief description of the plugin.
2. The main PHP file including.
   - Plugin header comment block with metadata
   - Security measures (e.g., preventing direct access)
   - Main plugin class structure
3. Key functions the plugin should include, such as:
   - Activation and deactivation hooks
   - Admin menu and settings page (if applicable)
   - Any custom post types or taxonomies (if applicable)
   - Enqueuing necessary scripts and styles
4. Action and filter hooks the plugin should use or create.
5. Any database interactions or custom tables required (provide table structure if needed).
6. Considerations for internationalization and localization.
7. Basic security measures and data sanitization methods.
8. Ideas for potential future enhancements or premium features.

Please make files using appropriate WordPress coding standards and best practices. Include comments in the code snippets to explain key parts of the functionality.

Assuming the current directory is the plugin directory `wp-content/plugins`, please specify the paths of each file using relative paths.
""".strip()

DIR_PARENT = Path(__file__).parent
DIR_OUT = DIR_PARENT / "out"


class File(BaseModel):
    path: str
    content: str


class PluginResponse(BaseModel):
    name: str
    description: str
    files: list[File]


@click.command()
@click.option("--name", required=True)
@click.option("--prompt", required=True)
@click.option("--model", default=MODEL_DEFAULT)
def main(name: str, prompt: str, model: str):
    if (api_key := os.environ.get("OPENAI_API_KEY")) is None:
        sys.exit("Environment variable `OPENAI_API_KEY` is required.")

    print(f"Asking {model}...")
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Create a plugin named {name}"},
        {"role": "user", "content": prompt},
    ]
    client = OpenAI(api_key=api_key)
    completion = client.beta.chat.completions.parse(
        model=model,
        messages=messages,
        response_format=PluginResponse,
    )

    message = completion.choices[0].message
    if message.refusal:
        sys.exit(str(completion))

    plugin = message.parsed
    pprint_plugin(plugin)

    parent = DIR_OUT
    if not parent.is_dir():
        parent.mkdir(parents=True)
    make_plugin_files(parent, plugin)

    print("Plugin generated.")


def pprint_plugin(plugin: PluginResponse):
    print(plugin.name)
    print(plugin.description)
    print("\n".join(x.path for x in plugin.files))


def make_plugin_files(parent: Path, plugin: PluginResponse):
    assert parent.is_dir(), f"Parent is not a dir: {parent}"

    for file in plugin.files:
        path = parent / file.path
        if not path.parent.is_dir():
            path.parent.mkdir(parents=True)
        path.write_text(file.content)


if __name__ == "__main__":
    main()
