# -*- coding: utf-8 -*-
import asyncio
import os
from typing import Dict

import click

from tokencalc.counter import TokenCounter

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

# テキストファイルとみなす拡張子
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


async def process_file(
    file_path: str,
    root_dir: str,
    counter: TokenCounter,
    semaphore: asyncio.Semaphore,
) -> Dict[str, int]:
    """一つのファイルを処理し、各モデルのトークン数を返す。"""
    async with semaphore:
        try:
            # tiktokenやAPIコールを含む処理を非同期で行う
            # ファイルの読み込み自体も非同期化（小さなファイルなら同期でも問題ないが一貫性のため）
            await asyncio.sleep(0)  # イベントループに制御を戻す

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            counts = await counter.async_get_all_counts(content)
            rel_path = os.path.relpath(file_path, root_dir)
            click.echo(
                f"{rel_path}: Anthropic={counts['anthropic']}, OpenAI={counts['openai']}, Google={counts['google']}"
            )
            return counts
        except Exception as e:
            click.echo(f"Error reading {file_path}: {e}", err=True)
            return {"anthropic": 0, "openai": 0, "google": 0}


async def async_main(directory: str, model: str, google_model: str, concurrency: int):
    """
    非同期メイン処理。
    """
    counter = TokenCounter(openai_model=model, google_model=google_model)
    semaphore = asyncio.Semaphore(concurrency)

    tasks = []

    click.echo(
        f"Scanning directory: {directory} (OpenAI: {model}, Google: {google_model}, Concurrency: {concurrency})"
    )
    click.echo("-" * 60)

    for root, dirs, files in os.walk(directory):
        # 除外ディレクトリの処理
        filtered_dirs = [d for d in dirs if d not in DEFAULT_EXCLUDES]
        dirs.clear()
        dirs.extend(filtered_dirs)

        for file in files:
            if not is_text_file(file):
                continue
            file_path = os.path.join(root, file)
            tasks.append(process_file(file_path, directory, counter, semaphore))

    if not tasks:
        click.echo("No text files found.")
        return

    # 全タスクを並行実行
    results = await asyncio.gather(*tasks)

    total_anthropic = sum(r["anthropic"] for r in results)
    total_openai = sum(r["openai"] for r in results)
    total_google = sum(r["google"] for r in results)
    file_count = len([r for r in results if any(v > 0 for v in r.values())])

    click.echo("-" * 60)
    click.echo(f"Processed {file_count} files.")
    click.echo(f"Total Anthropic Tokens: {total_anthropic}")
    click.echo(f"Total OpenAI Tokens:    {total_openai}")
    click.echo(f"Total Google Tokens:    {total_google}")


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
@click.option(
    "--concurrency",
    default=10,
    help="Number of concurrent API requests",
)
def main(directory: str, model: str, google_model: str, concurrency: int):
    """
    DIRECTORY内の全テキストファイルのトークン数を計算し、集計結果を表示します。
    """
    asyncio.run(async_main(directory, model, google_model, concurrency))


if __name__ == "__main__":
    main()
if __name__ == "__main__":
    main()
