# TokenCalc 課題抽出・解決策策定 実装計画書
日付：2026-01-18 15:20

## 問題の背景
TokenCalcの実行結果において、AnthropicとOpenAIのトークン数が **完全に一致** しています（113,385トークン）。これは計算ロジック上、フォールバック機構が発動し、Anthropic APIの代わりに `tiktoken`（OpenAI用）を使用していることを示唆しています。

---

## 抽出された課題

### 課題1: フォールバック発生時の可視性が低い
**現状**: `counter.py` L60-65 において、Anthropic API呼び出しが失敗した場合、`stderr` に警告を出力してから `tiktoken` の結果を返しています。しかし、77ファイル処理中にこの警告が大量に流れると、ユーザーはそれを見落としやすく、最終サマリにはフォールバック発生の情報が一切含まれていません。

**影響**: ユーザーはAnthropicのトークン数が「正しく計算された」と誤解する可能性があります。

---

### 課題2: 最終サマリにフォールバック統計がない
**現状**: `main.py` L119-122 の最終サマリは、トークン数の合計のみを表示しています。どのプロバイダーでフォールバックが発生したかの情報は一切表示されません。

**影響**: 計算結果の信頼性を判断する情報が不足しています。

---

### 課題3: Exception を広く catch しすぎている
**現状**: `except Exception as e:` で全ての例外をキャッチし、フォールバックに移行しています。これにより、認証エラー、レート制限エラー、ネットワークエラー、プログラミングエラーなど、種類の異なる問題がすべて同じ扱いになっています。

**影響**: デバッグが困難になり、問題の根本原因を特定しにくくなります。

---

### 課題4: デバッグ・詳細出力モードがない
**現状**: 詳細なログ出力を有効にするオプションがありません。

**影響**: 問題発生時のトラブルシューティングが困難です。

---

## 解決策の提案

### 解決策1: フォールバックカウンターの導入とサマリ表示
`TokenCounter` クラスまたは処理結果にフォールバック発生回数を追跡する仕組みを追加し、最終サマリで表示します。

#### [MODIFY] [counter.py](file:///Volumes/Download/Development/Tokens/src/tokencalc/counter.py)
- `async_get_all_counts` の戻り値に `fallback` フラグを追加（例: `{"anthropic": 100, "openai": 100, "google": 110, "anthropic_fallback": True}`）
- または、別途フォールバック情報を返すメソッドを追加

#### [MODIFY] [main.py](file:///Volumes/Download/Development/Tokens/src/tokencalc/main.py)
- `process_file` の戻り値にフォールバック情報を含める
- 最終サマリでフォールバック発生件数を表示

---

### 解決策2: 例外の種類による分類処理
`anthropic.AuthenticationError`, `anthropic.RateLimitError` など、具体的な例外を個別に処理し、適切なメッセージを出力します。

#### [MODIFY] [counter.py](file:///Volumes/Download/Development/Tokens/src/tokencalc/counter.py)
```python
except anthropic.AuthenticationError:
    # 認証エラー: APIキー未設定または無効
    ...
except anthropic.RateLimitError:
    # レート制限: リトライまたはフォールバック
    ...
except Exception as e:
    # その他の予期しないエラー
    ...
```

---

### 解決策3: `--verbose` / `--debug` オプションの追加
CLIに詳細出力モードを追加し、各ファイル処理時にAPIの成功/失敗を明示的に表示できるようにします。

#### [MODIFY] [main.py](file:///Volumes/Download/Development/Tokens/src/tokencalc/main.py)
- `@click.option("--verbose", is_flag=True, help="詳細な出力を表示")`
- 詳細モード時は、各API呼び出しの結果（成功/フォールバック）を表示

---

### 解決策4: Python標準ロギング (`logging`) の導入
`print` による警告出力を `logging` モジュールに置き換え、ログレベルに応じた出力制御を可能にします。

#### [MODIFY] [counter.py](file:///Volumes/Download/Development/Tokens/src/tokencalc/counter.py)
```python
import logging
logger = logging.getLogger(__name__)

# フォールバック時
logger.warning("Anthropic API unavailable (%s), using tiktoken approximation", e)
```

---

## 優先度と実装順序

| 優先度 | 課題 | 解決策 | 工数（目安） |
|--------|------|--------|--------------|
| **高** | 課題1, 2 | 解決策1 | 中（約2時間） |
| **中** | 課題4 | 解決策3 | 小（約1時間） |
| **中** | 課題3 | 解決策2 | 中（約1.5時間） |
| **低** | 全体 | 解決策4 | 中（約1.5時間） |

---

## 検証計画

### 自動テスト
- 既存のユニットテストがあれば、フォールバックロジックのテストを追加
- モックを使用してAPI失敗時の挙動を検証

### 手動検証
1. `ANTHROPIC_API_KEY` を無効な値に設定して実行し、フォールバックが正しく報告されることを確認
2. `--verbose` オプションを使用して詳細出力を確認
3. 正常なAPIキーで実行し、AnthropicとOpenAIのトークン数が**異なる**ことを確認

---

## User Review Required

> [!IMPORTANT]
> この実装計画を承認いただけましたら、EXECUTION フェーズに移行し、上記の解決策を順次実装いたします。
>
> ご質問や優先度の変更、追加要件がありましたらお知らせください。
