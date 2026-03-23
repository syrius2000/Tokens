# コアコード最新モデル対応 実装計画

`TokenCalc` を最新のAIモデル市場（2026年）に適合させ、コスト計算スキルと完全に整合させます。

## 各ファイルへの変更点

### [Component] src/tokencalc/

#### [MODIFY] [counter.py](file:///Volumes/Download/Development/Tokens/src/tokencalc/counter.py)
- `google-generativeai` SDKのインポートと初期化。
- `count_google_tokens` メソッドの追加。
- Claude 4.5 や GPT-4.5 を意識したデフォルト設定の更新。

#### [MODIFY] [main.py](file:///Volumes/Download/Development/Tokens/src/tokencalc/main.py)
- Google (Gemini) トークンの集計ロジックを追加。
- 最終出力に `Total Google Tokens` を追加し、`cost_calc.py` がこれをパースできるようにする。
- デフォルトモデルを `gpt-4.5` や `gemini-3-pro` などの最新世代に合わせて調整。

#### [MODIFY] [__init__.py](file:///Volumes/Download/Development/Tokens/src/tokencalc/__init__.py)
- バージョンを `0.2.0` にバンプ。

### [Component] プロジェクト設定

#### [MODIFY] [pyproject.toml](file:///Volumes/Download/Development/Tokens/pyproject.toml)
- `google-generativeai` を依存関係に追加。

## 検証プラン
1. `poetry install` で新しい依存関係を導入。
2. `TokenCalc` を実行し、Anthropic, OpenAI, Google の3カテゴリの結果が表示されることを確認。
3. `cost_calc.py` にパイプで渡し、Gemini等のコストが正しく計算されることを確認。
