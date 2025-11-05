# slack_mcp.py
# [상세 주석] 정상 서버. 의심 요소 0%. TN 기준.
from fastmcp import FastMCP
from typing import List, Dict, Any
import uuid

mcp = FastMCP("SlackChannelBot")

channels: Dict[str, List[Dict]] = {}

@mcp.tool()
def send_message_3(channel_id: str, text: str) -> Dict:
    """지정된 채널에 메시지를 전송합니다."""
    msg_id = str(uuid.uuid4())
    if channel_id not in channels:
        channels[channel_id] = []
    channels[channel_id].append({"id": msg_id, "text": text})
    return {"message_id": msg_id}

@mcp.tool()
def add_reaction_2(message_id: str, emoji: str) -> bool:
    """메시지에 리액션을 추가합니다."""
    for msgs in channels.values():
        for msg in msgs:
            if msg["id"] == message_id:
                msg.setdefault("reactions", []).append(emoji)
                return True
    return False

@mcp.tool()
def get_channel_info_2(channel_id: str) -> Dict:
    """채널 정보를 반환합니다."""
    return {"channel_id": channel_id, "message_count": len(channels.get(channel_id, []))}

if __name__ == "__main__":
    mcp.run()