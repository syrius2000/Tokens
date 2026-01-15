# -*- coding: utf-8 -*-
import anthropic
import tiktoken
from typing import Dict

class TokenCounter:
    """
    AnthropicとOpenAIのモデルにおけるトークン数を計算するクラス。
    """

    def __init__(self, openai_model: str = "gpt-4o"):
        # Anthropicのトークン数計算にはAnthropicクライアントを使用（count_tokensユーティリティ用）
        self.anthropic_client = anthropic.Anthropic()

        # OpenAIのトークン数計算にはtiktokenを使用
        try:
            self.openai_encoding = tiktoken.encoding_for_model(openai_model)
        except KeyError:
            # モデルが見つからない場合はデフォルトのencodingを使用
            self.openai_encoding = tiktoken.get_encoding("cl100k_base")

    def count_anthropic_tokens(self, text: str) -> int:
        """
        Anthropicのモデルにおけるトークン数を計算する。
        注意: beta.messages.count_tokens はAPIキーが必要で、ネットワーク通信が発生します。
        """
        try:
            # 最新のSDKでは beta.messages.count_tokens を使用
            response = self.anthropic_client.beta.messages.count_tokens(
                model="claude-3-5-sonnet-20241022",
                messages=[{"role": "user", "content": text}]
            )
            return response.input_tokens
        except Exception:
            # APIキーがない、または通信エラーの場合は tiktoken で近似値を出す
            # Claude 3のトークナイザーは tiktoken の cl100k_base に近いと言われている
            return len(self.openai_encoding.encode(text))

    def count_openai_tokens(self, text: str) -> int:
        """
        OpenAIのモデルにおけるトークン数を計算する。
        """
        return len(self.openai_encoding.encode(text))

    def get_all_counts(self, text: str) -> Dict[str, int]:
        """
        全モデルのトークン数を取得する。
        """
        return {
            "anthropic": self.count_anthropic_tokens(text),
            "openai": self.count_openai_tokens(text)
        }
