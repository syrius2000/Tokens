created: 2026-03-23 17:45 (JST)
author: AI Agent (Gemini 2.0 Pro)

# Poetryからuvへの移行計画

現在のプロジェクト（トークン数計算ツール `tokencalc`）のパッケージ管理と環境構築を、Poetryから高速なPythonパッケージマネージャーである `uv` へ全面的に移行します。

## 目的
- 仮想環境の構築および依存関係の解決・インストールを高速化する
- PEP 621 (`[project]` セクション) 標準に準拠した `pyproject.toml` へのモダナイズ

## 実装内容（提案事項）

### 1. `pyproject.toml`の書き換え
Poetry固有の設定（`[tool.poetry]`）から、標準の`[project]`設定に移行します。
- `[tool.poetry]` を `[project]` に変換し、`name`, `version`, `description`, `authors`, `readme`, `requires-python` などを設定。
- `[tool.poetry.dependencies]` を `dependencies` リストに変換。
  - 開発用依存関係（`pytest`, `pytest-asyncio`）は `[dependency-groups]` に分離（今回は `uv` 標準の `[dependency-groups].dev` に設定します）。
- `[tool.poetry.scripts]` を `[project.scripts]` に変換。
- ビルドシステムを `poetry-core` から標準バックエンド（例: `hatchling`）へと変更し、`[build-system]`を再定義します。

#### [MODIFY] pyproject.toml
内容の全面的な書き換えを実施。

### 2. 環境のクリーンアップと再構築
不要になるPoetry関連ファイルを削除し、uvで環境を再構築します。
- **削除対象**: `poetry.lock`、既存の `.venv/`
- **構築手順**: 
  - `uv sync` を実行し、環境の作成と依存関係のインストールを実行。
  - これにより新しく `uv.lock` が生成されます。

#### [DELETE] poetry.lock
Poetryのロックファイルは不要となるため削除します。

### 3. ドキュメントの更新
Poetryコマンドで記載されているドキュメントを、uvコマンドを使用する形にアップデートします。
#### [MODIFY] README.md
セットアップおよび使用方法のセクションを、`poetry run` から `uv run` 等へ修正します。

## User Review Required
> [!IMPORTANT]
> 移行にあたり、`pyproject.toml`のフォーマットが大きく変更されます。
> 現在のPoetryからuvへの移行計画について、上記の内容で進めてもよろしいでしょうか。
> ご確認と「承認 (Approval)」をお願いいたします。承認を頂いてから、実際の変更作業（実行フェーズ）へ移行します。
