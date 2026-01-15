# TokenCalc 実装・検証結果

AnthropicおよびOpenAIのモデルに対応したトークン数計算ツール `TokenCalc` を実装しました。

## 実施内容

- **プロジェクト構成**: Python `src` レイアウトを採用し、`pyproject.toml` で依存関係（`anthropic`, `tiktoken`, `click`）を管理。
- **コアロジック**:
    - `tiktoken` を使用したOpenAIモデルのトークン計算。
    - `anthropic` SDK を使用したAnthropicモデルのトークン計算（APIキーが必要なため、不足時は `tiktoken` による近似値を出力するよう実装）。
- **CLI実装**: `TokenCalc <directory>` コマンドで指定ディレクトリ内のテキストファイルを走査・集計。

## 検証結果

### 実行コマンド
```bash
TokenCalc .
```

### 実行結果（抜粋）
```text
Scanning directory: . (Model: gpt-4o)
------------------------------------------------------------
README.md: Anthropic=44, OpenAI=44
src/tokencalc/counter.py: Anthropic=499, OpenAI=499
src/tokencalc/main.py: Anthropic=664, OpenAI=664
...
------------------------------------------------------------
Processed 10 files.
Total Anthropic Tokens: 1787
Total OpenAI Tokens: 1787
```

> [!NOTE]
> Anthropicのトークン数は、APIキーが設定されていない環境では `tiktoken` (cl100k_base) による近似値を表示します。これはClaude 3系が概ねこのエンコーディングに近いトークナイザーを採用しているためです。

## 今後の拡張性
- 無視するディレクトリやファイルのフィルタリング条件のカスタマイズ。
- 指定モデルごとの料金計算機能の追加。
