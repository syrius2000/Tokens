# 最適化のケーススタディ: 冗長なコメントの削除

このリポジトリ自体の `main.py` を例に、最適化の効果をシミュレーションします。

## ケース1: ドキュメントコメントを最小化
Pythonの docstring は大規模なコードベースでは多くのトークンを消費します。

### 最適化前 (元のコード)
```python
def is_text_file(filename: str) -> bool:
    """
    拡張子からテキストファイルかどうかを判定する。
    この関数は TokenCalc の主要なフィルタリングロジックを担当し、
    指定された TEXT_EXTENSIONS リストに該当するかをチェックします。
    """
    _, ext = os.path.splitext(filename)
    return ext.lower() in TEXT_EXTENSIONS
```
**トークン数 (約): 85**

### 最適化後 (AIプロンプト用)
```python
def is_text_file(filename: str) -> bool:
    # 拡張子判定
    _, ext = os.path.splitext(filename)
    return ext.lower() in TEXT_EXTENSIONS
```
**トークン数 (約): 35 (-60% 削減)**

## 考察
AIエージェントにコードを渡す際、内部動作を熟知しているタスクであれば、 docstring を一時的に stripping するツールを Skill に含めることで、入力コストを大幅に削減できます。
