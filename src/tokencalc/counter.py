# -*- coding: utf-8 -*-
import sys
import anthropic
import tiktoken
from google import genai
from typing import Dict


class TokenCounter:
    """
    Anthropic, OpenAI, および Google (Gemini) のモデルにおけるトークン数を計算するクラス。
    """

    def __init__(
        self,
        openai_model: str = "gpt-4o",
        google_model: str = "gemini-2.0-flash",
        anthropic_model: str = "claude-sonnet-4-20250514",
    ):
        # Anthropicのトークン数計算にはAnthropicクライアントを使用
        self.anthropic_client = anthropic.Anthropic()
        self.anthropic_model = anthropic_model

        # OpenAIのトークン数計算にはtiktokenを使用
        try:
            self.openai_encoding = tiktoken.encoding_for_model(openai_model)
        except KeyError:
            self.openai_encoding = tiktoken.get_encoding("cl100k_base")

        # Googleのトークン数計算にはGenAI Clientを使用
        self.google_client = genai.Client()
        self.google_model_name = google_model

    def count_anthropic_tokens(self, text: str) -> int:
        """Anthropicのモデルにおけるトークン数を計算する。"""
        try:
            # 最新SDK機能でトークン数を計算
            response = self.anthropic_client.beta.messages.count_tokens(
                model=self.anthropic_model,
                messages=[{"role": "user", "content": text}],
            )
            return response.input_tokens
        except Exception as e:
            # 近似値として tiktoken を使用（警告メッセージを出力）
            print(
                f"Warning: Anthropic API unavailable ({e}), using tiktoken approximation",
                file=sys.stderr,
            )
            return len(self.openai_encoding.encode(text))

    def count_openai_tokens(self, text: str) -> int:
        """OpenAIのモデルにおけるトークン数を計算する。"""
        return len(self.openai_encoding.encode(text))

    def count_google_tokens(self, text: str) -> int:
        """Google (Gemini) のモデルにおけるトークン数を計算する。"""
        try:
            # count_tokens は Client を通じて実行
            response = self.google_client.models.count_tokens(
                model=self.google_model_name,
                contents=text,
            )
            return response.total_tokens
        except Exception as e:
            # 近似値 (Geminiは tiktoken とは異なるが、現状はフォールバックとして使用)
            print(
                f"Warning: Google API unavailable ({e}), using tiktoken approximation",
                file=sys.stderr,
            )
            return int(len(self.openai_encoding.encode(text)) * 1.1)

    def get_all_counts(self, text: str) -> Dict[str, int]:
        """全モデルのトークン数を取得する。"""
        return {
            "anthropic": self.count_anthropic_tokens(text),
            "openai": self.count_openai_tokens(text),
            "google": self.count_google_tokens(text),
        }
