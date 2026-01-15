# トークン数計算ツール (tokencalc) 実装計画

指定されたディレクトリ内のファイルを走査し、AnthropicおよびOpenAIのモデルにおけるトークン数を計算するCLIツールを実装します。

## 提案される変更点

### プロジェクト構成
標準的なPython `src` レイアウトを採用します。

#### [NEW] [pyproject.toml](file:///Volumes/Download/Development/Tokens/pyproject.toml)
#### [NEW] [src/tokencalc/counter.py](file:///Volumes/Download/Development/Tokens/src/tokencalc/counter.py)
#### [NEW] [src/tokencalc/main.py](file:///Volumes/Download/Development/Tokens/src/tokencalc/main.py)

## 検証プラン
- `pytest` による自動テスト
- 手動検証
