created: 2026-03-23 18:00 (JST)
author: AI Agent (Gemini 2.0 Pro)

# Walkthrough: Poetryからuvへの移行完了

## 概要
トークン数計算ツール `tokencalc` において、パッケージ管理・環境構築ツールを **Poetry** から高速な **uv** へ全面的に移行する作業が完了しました。

## 実装内容の詳細

1. **`pyproject.toml` のモダナイズ**
   古い `[tool.poetry]` セクションを破棄し、PEP 621に準拠した標準の `[project]` メタデータへ移行しました。
   また、開発環境向けのパッケージ要件を `[dependency-groups]` 定義へ移行し、ビルドバックエンドを `poetry-core` から `hatchling` に変更しました。

2. **Poetry関連ファイルの完全削除**
   `poetry.lock` および既存の環境ディレクトリ `.venv/` を削除し、リポジトリをクリーンな状態に保ちました。

3. **ドキュメントの更新**
   `README.md` 内でユーザー向けに案内しているコマンド群（`poetry install` や `poetry run ...`）をすべて最新の `uv sync` および `uv run ...` 表記に書き換えました。

4. **NAS環境特有の権限問題（os error 1）への対応**
   作業ディレクトリがNAS（SMB/CIFS）上に存在するため、`uv sync` が依存キャッシュやvenv内のフラグ（`CACHEDIR.TAG` 等）を作成しようとした際に、パーミッションエラー（`Operation not permitted`）が発生することが判明しました。
   これを透過的に解決するため、以下のようなディレクトリを指定する `.env` ファイルを生成しました。
   ```env
   UV_PROJECT_ENVIRONMENT=/tmp/tokens_venv
   UV_CACHE_DIR=/tmp/tokens_uv_cache
   ```
   これにより、仮想環境の実体やキャッシュはマシン・ローカル（`/tmp`）に作られるため、ユーザーはディレクトリ制約を気にすることなく `uv run TokenCalc .` や `uv sync` を通常通り使用可能となります。

## 検証結果 (Verification)

移行後、再構築された仮想環境上で一連の検証を行いました。
- **CLIの動作確認**: `uv run TokenCalc .` が正常にディレクトリを走査し、トークン数を出力できることを確認しました。
- **ユニットテスト (*pytest*)**: 計4つのテストケースがすべて正常にパスしました。

> [!TIP]
> 今後は `poetry` に代わり、高速な `uv` を介して即座にツールを実行することができます。
