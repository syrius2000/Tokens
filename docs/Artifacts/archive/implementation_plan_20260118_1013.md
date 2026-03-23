# 2026-01-18 01:13:52

# プロジェクト改善計画 (テスト導入・非同期化・設定外部化)

## 概要
プロジェクト分析レポートに基づき、コードの品質向上、パフォーマンス改善、および柔軟性の向上を目的とした以下の変更を提案します。

1. **テスト環境の整備**: `pytest` を導入し、コアロジックの信頼性を確保します。
2. **非同期処理の導入**: 大量ファイル処理時の待機時間を削減するため、`asyncio` を用いた並行処理を実装します。
3. **設定の外部化**: 除外ディレクトリや拡張子を外部ファイルから設定可能にします。

## ユーザーレビューが必要な項目
> [!IMPORTANT]
> - `main.py` の構成が大幅に変わります（同期から非同期へ）。
> - Google GenAI SDK の非同期クライアントを使用するため、APIキーが正しく設定されていない場合の挙動が現状より厳密になる可能性があります。

## 変更内容

### 開発基盤
#### [MODIFY] [pyproject.toml](file:///Volumes/Download/Development/Tokens/pyproject.toml)
- `pytest`, `pytest-asyncio` を開発用依存関係（`group.dev`）に追加します。

### トークン計算ロジック
#### [MODIFY] [counter.py](file:///Volumes/Download/Development/Tokens/src/tokencalc/counter.py)
- `TokenCounter` クラスに非同期メソッド `async_count_anthropic_tokens`, `async_count_google_tokens`, `async_get_all_counts` を追加します。
- `anthropic.AsyncAnthropic` クライアントを導入します。

### CLIエントリーポイント
#### [MODIFY] [main.py](file:///Volumes/Download/Development/Tokens/src/tokencalc/main.py)
- `click` コマンドを `asyncio.run` でラップし、非同期実行に対応させます。
- `asyncio.gather` を使用して、複数ファイルのトークン計算を並行して行います（セマフォで同時実行数を制御）。
- 指定された場合は設定ファイルから無視リスト等を読み込むようにします。

### テスト
#### [NEW] [test_counter.py](file:///Volumes/Download/Development/Tokens/tests/test_counter.py)
- `TokenCounter` の各メソッドに対するユニットテスト。
- モックを使用したAPI連携部分のテスト。

## 検証計画

### 自動テスト
- `pytest` を実行し、全てのテストがパスすることを確認します。
```bash
poetry run pytest
```

### 手動検証
- サンプルプロジェクトのディレクトリ（TokenCalc自身など）をスキャンし、結果が正しく表示されること。
- 非同期化前後の速度を比較（体感レベルでの確認）。
- 存在しないディレクトリを指定した際のエラーハンドリングの確認。
