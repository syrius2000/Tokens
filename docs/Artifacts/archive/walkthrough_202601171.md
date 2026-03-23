# TokenCalc 実施事項記録 (2026-01-17)

## 概要

本日は `TokenCalc` の最新モデル対応、ユーザビリティ向上、および Google SDK の最新化を実施しました。

## 実施事項

### 1. 最新モデル対応とパラメータ化
- **Anthropic**: ハードコードされていたモデルを `claude-sonnet-4-20250514` に更新し、内部でパラメータ化しました。
- **Google**: デフォルトモデルを `gemini-2.0-flash` に更新しました。

### 2. CLI機能の拡張
- **--google-model オプション**: Google (Gemini) のモデルをコマンドラインから柔軟に指定できるようになりました。
- **ヘッダー表示の改善**: スキャン開始時に OpenAI モデルと Google モデルの両方を表示するようにしました。

### 3. エラーハンドリングとユーザビリティの向上
- **警告メッセージの出力**: APIキーが設定されていない場合や API 呼び出しに失敗した場合、単に近似値を返すだけでなく `stderr` に警告メッセージを出力するようにし、ユーザーが状況を把握できるようにしました。

### 4. Google GenAI SDK (v1) への移行
- 非推奨となった `google-generativeai` パッケージを削除し、最新の `google-genai` パッケージへ移行しました。
- これにより、起動時に表示されていた `FutureWarning` が解消されました。

## 変更ファイル

- `src/tokencalc/counter.py`: ロジックの刷新と SDK 移行
- `src/tokencalc/main.py`: CLI オプション追加と出力改善
- `pyproject.toml`: 依存関係の更新 (`google-genai` へのスイッチ)
- `README.md`: ドキュメントを最新の実装と整合

## 検証結果

- `poetry run TokenCalc --help` にて新オプションが表示されることを確認。
- 依存関係の競合や、起動時の警告が発生しないことを確認。

---
**完了日**: 2026-01-17
**エンジニア**: Antigravity
