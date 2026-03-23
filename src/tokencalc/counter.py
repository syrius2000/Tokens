# -*- coding: utf-8 -*-
import sys
import asyncio
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
        # Anthropicクライアント（同期・非同期）
        self.anthropic_client = anthropic.Anthropic()
        self.async_anthropic_client = anthropic.AsyncAnthropic()
        self.anthropic_model = anthropic_model

        # OpenAIのトークン数計算にはtiktokenを使用（tiktokenはローカル計算のため同期的）
        try:
            self.openai_encoding = tiktoken.encoding_for_model(openai_model)
        except KeyError:
            self.openai_encoding = tiktoken.get_encoding("cl100k_base")

        # Googleクライアント（GenAI SDKは非同期をサポート）
        self.google_client = genai.Client()
        self.google_model_name = google_model

    def count_anthropic_tokens(self, text: str) -> int:
        """Anthropicのモデルにおけるトークン数を計算する（同期）。"""
        try:
            response = self.anthropic_client.beta.messages.count_tokens(
                model=self.anthropic_model,
                messages=[{"role": "user", "content": text}],
            )
            return response.input_tokens
        except Exception as e:
            print(
                f"Warning: Anthropic API unavailable ({e}), using tiktoken approximation",
                file=sys.stderr,
            )
            return len(self.openai_encoding.encode(text))

    async def async_count_anthropic_tokens(self, text: str) -> int:
        """Anthropicのモデルにおけるトークン数を計算する（非同期）。"""
        try:
            response = await self.async_anthropic_client.beta.messages.count_tokens(
                model=self.anthropic_model,
                messages=[{"role": "user", "content": text}],
            )
            return response.input_tokens
        except Exception as e:
            print(
                f"Warning: Anthropic async API unavailable ({e}), using tiktoken approximation",
                file=sys.stderr,
            )
            return len(self.openai_encoding.encode(text))

    def count_openai_tokens(self, text: str) -> int:
        """OpenAIのモデルにおけるトークン数を計算する（ tiktoken はローカルのため常に同期相当）。"""
        return len(self.openai_encoding.encode(text))

    def count_google_tokens(self, text: str) -> int:
        """Google (Gemini) のモデルにおけるトークン数を計算する（同期）。"""
        try:
            response = self.google_client.models.count_tokens(
                model=self.google_model_name,
                contents=text,
            )
            return response.total_tokens
        except Exception as e:
            print(
                f"Warning: Google API unavailable ({e}), using tiktoken approximation",
                file=sys.stderr,
            )
            return int(len(self.openai_encoding.encode(text)) * 1.1)

    async def async_count_google_tokens(self, text: str) -> int:
        """Google (Gemini) のモデルにおけるトークン数を計算する（非同期）。"""
        try:
            # genai SDK の非同期呼び出し (対応しているか要確認だが、通常SDKは aiohttp等を利用)
            # 現状のSDKドキュメントに基づき、models.count_tokens を async 実行可能と仮定
            # (もし非同期版が別にある場合は修正が必要)
            response = await self.google_client.aio.models.count_tokens(
                model=self.google_model_name,
                contents=text,
            )
            return response.total_tokens
        except Exception as e:
            print(
                f"Warning: Google async API unavailable ({e}), using tiktoken approximation",
                file=sys.stderr,
            )
            return int(len(self.openai_encoding.encode(text)) * 1.1)

    def get_all_counts(self, text: str) -> Dict[str, int]:
        """全モデルのトークン数を取得する（同期）。"""
        return {
            "anthropic": self.count_anthropic_tokens(text),
            "openai": self.count_openai_tokens(text),
            "google": self.count_google_tokens(text),
        }

    async def async_get_all_counts(self, text: str) -> Dict[str, int]:
        """全モデルのトークン数を取得する（非同期）。"""

        # OpenAI (tiktoken) は非同期版がないため、同期的だがオーバヘッドは極小
        # 他の2つを並行実行
        anthropic_task = asyncio.create_task(self.async_count_anthropic_tokens(text))
        google_task = asyncio.create_task(self.async_count_google_tokens(text))

        openai_count = self.count_openai_tokens(text)
        anthropic_count, google_count = await asyncio.gather(
            anthropic_task, google_task
        )

        return {
            "anthropic": anthropic_count,
            "openai": openai_count,
            "google": google_count,
        }
