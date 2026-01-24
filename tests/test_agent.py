"""エージェント単体テスト"""
import asyncio
import sys
from pathlib import Path

# agent.pyをインポートできるようにパスを追加
sys.path.insert(0, str(Path(__file__).parent.parent / "amplify" / "agent" / "runtime"))

from agent import agent, extract_markdown

async def test_chat():
    print("=== チャットテスト ===")
    prompt = "AWSの概要を3枚のスライドで説明して"

    print(f"プロンプト: {prompt}\n")
    print("レスポンス:")

    full_response = ""
    stream = agent.stream_async(prompt)

    async for event in stream:
        if "data" in event:
            chunk = event["data"]
            full_response += chunk
            print(chunk, end="", flush=True)

    print("\n\n=== マークダウン抽出 ===")
    markdown = extract_markdown(full_response)
    if markdown:
        print("成功！マークダウンを抽出しました:")
        print(markdown[:500] + "..." if len(markdown) > 500 else markdown)
    else:
        print("マークダウンが見つかりませんでした")

if __name__ == "__main__":
    asyncio.run(test_chat())
