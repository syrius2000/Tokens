# -*- coding: utf-8 -*-
import sys
import re

# 最新の価格表 (1M tokens あたりの USD 価格)
# 2026-01-16 時点 (最新調査結果)
# type: 'anthropic', 'openai', または 'google' (TokenCalcの出力に対応)
PRICES = {
    "gemini-3-pro": {"input": 2.00, "output": 12.00, "type": "google"},
    "gemini-3-flash": {"input": 0.50, "output": 3.00, "type": "google"},
    "claude-4.5-sonnet": {"input": 3.00, "output": 15.00, "type": "anthropic"},
    "gpt-4.5": {"input": 75.00, "output": 150.00, "type": "openai"},
    "composer-1": {"input": 60.00, "output": 120.00, "type": "openai"},
}


def parse_tokencalc_output(output):
    """TokenCalc の標準出力をパースして合計値を抽出する"""
    anthropic_total = 0
    openai_total = 0
    google_total = 0

    anthropic_match = re.search(r"Total Anthropic Tokens:\s+(\d+)", output)
    openai_match = re.search(r"Total OpenAI Tokens:\s+(\d+)", output)
    google_match = re.search(r"Total Google Tokens:\s+(\d+)", output)

    if anthropic_match:
        anthropic_total = int(anthropic_match.group(1))
    if openai_match:
        openai_total = int(openai_match.group(1))
    if google_match:
        google_total = int(google_match.group(1))

    return anthropic_total, openai_total, google_total


def calculate_cost(anthropic_tokens, openai_tokens, google_tokens):
    """各モデルの参考コストを算出する"""
    results = []

    mapping = {
        "anthropic": anthropic_tokens,
        "openai": openai_tokens,
        "google": google_tokens,
    }

    for model, data in PRICES.items():
        tokens = mapping.get(data["type"], 0)
        cost = (tokens / 1_000_000) * data["input"]
        results.append({"model": model, "cost_usd": cost})

    return results


if __name__ == "__main__":
    input_text = sys.stdin.read()
    ant_t, oai_t, goo_t = parse_tokencalc_output(input_text)

    if ant_t == 0 and oai_t == 0 and goo_t == 0:
        print("Error: Could not find token totals in input.")
        sys.exit(1)

    costs = calculate_cost(ant_t, oai_t, goo_t)

    print("\n--- AI Cost Estimation Report (Jan 2026 Prices) ---")
    print(f"Total Anthropic Tokens: {ant_t:,}")
    print(f"Total OpenAI Tokens:    {oai_t:,}")
    print(f"Total Google Tokens:    {goo_t:,}")
    print("-" * 45)
    print(f"{'Model':<20} | {'Estimated Cost (USD)':<20}")
    print("-" * 45)
    for res in costs:
        print(f"{res['model']:<20} | ${res['cost_usd']:.4f}")
    print("-" * 45)
    print("Note: Estimates are for input tokens only. Actual costs may vary.")
