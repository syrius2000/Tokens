# -*- coding: utf-8 -*-
import os
import click
from typing import List, Set
from .counter import TokenCounter

# デフォルトの除外ディレクトリ
DEFAULT_EXCLUDES = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
    ".mypy_cache",
    ".pytest_cache",
    ".idea",
    ".vscode",
    "docs/Artifacts",  # このプロジェクトのドキュメントも除外
}

# テキストファイルとみなす拡張子（必要に応じて追加）
TEXT_EXTENSIONS = {
    ".py",
    ".r",
    ".sql",
    ".cpp",
    ".h",
    ".hpp",
    ".txt",
    ".md",
    ".yml",
    ".yaml",
    ".json",
    ".js",
    ".ts",
    ".html",
    ".css",
    ".ino",
    ".c",
    ".qmd",
    ".rmd",
    ".tex",
    ".rnw",
    ".Rnw",
}


def is_text_file(filename: str) -> bool:
    """拡張子からテキストファイルかどうかを判定する。"""
    _, ext = os.path.splitext(filename)
    return ext.lower() in TEXT_EXTENSIONS


@click.command()
@click.argument(
    "directory", type=click.Path(exists=True, file_okay=False, dir_okay=True)
)
@click.option("--model", default="gpt-4o", help="OpenAI model for tiktoken calculation")
@click.option(
    "--google-model",
    default="gemini-2.0-flash",
    help="Google model for Gemini calculation",
)
def main(directory: str, model: str, google_model: str):
    """
    DIRECTORY内の全テキストファイルのトークン数を計算し、集計結果を表示します。
    """
    counter = TokenCounter(openai_model=model, google_model=google_model)
    total_anthropic = 0
    total_openai = 0
    total_google = 0
    file_count = 0

    click.echo(
        f"Scanning directory: {directory} (OpenAI: {model}, Google: {google_model})"
    )
    click.echo("-" * 60)

    for root, dirs, files in os.walk(directory):
        # 除外ディレクトリの処理
        dirs[:] = [d for d in dirs if d not in DEFAULT_EXCLUDES]

        for file in files:
            if not is_text_file(file):
                continue

            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                counts = counter.get_all_counts(content)
                total_anthropic += counts["anthropic"]
                total_openai += counts["openai"]
                total_google += counts["google"]
                file_count += 1

                rel_path = os.path.relpath(file_path, directory)
                click.echo(
                    f"{rel_path}: Anthropic={counts['anthropic']}, OpenAI={counts['openai']}, Google={counts['google']}"
                )
            except Exception as e:
                click.echo(f"Error reading {file_path}: {e}", err=True)

    click.echo("-" * 60)
    click.echo(f"Processed {file_count} files.")
    click.echo(f"Total Anthropic Tokens: {total_anthropic}")
    click.echo(f"Total OpenAI Tokens:    {total_openai}")
    click.echo(f"Total Google Tokens:    {total_google}")


if __name__ == "__main__":
    main()
