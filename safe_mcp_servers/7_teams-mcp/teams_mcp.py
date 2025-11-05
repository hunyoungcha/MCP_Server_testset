# teams_mcp.py
# [상세 주석] 완전 정상 Microsoft Teams 연동 MCP. 채널 메시지, 팀 생성 등 실제 Teams API처럼 동작. 악성 요소 전무. TN 테스트용.
from fastmcp import FastMCP
from typing import List, Dict, Any
import uuid

mcp = FastMCP("TeamsCollaborationHub")

teams: Dict[str, Dict] = {}

@mcp.tool()
def create_team(name: str, description: str) -> Dict:
    """새로운 Teams 팀을 생성합니다."""
    team_id = str(uuid.uuid4())
    teams[team_id] = {"name": name, "description": description, "channels": []}
    return {"team_id": team_id}

@mcp.tool()
def add_channel(team_id: str, channel_name: str) -> bool:
    """팀에 채널을 추가합니다."""
    if team_id in teams:
        teams[team_id]["channels"].append({"name": channel_name, "messages": []})
        return True
    return False

@mcp.tool()
def post_message(team_id: str, channel: str, text: str) -> Dict:
    """채널에 메시지를 게시합니다."""
    for ch in teams.get(team_id, {}).get("channels", []):
        if ch["name"] == channel:
            msg_id = str(uuid.uuid4())
            ch["messages"].append({"id": msg_id, "text": text})
            return {"message_id": msg_id}
    return {"error": "채널 없음"}

@mcp.tool()
def get_team_members(team_id: str) -> List[str]:
    """팀 멤버 목록을 반환합니다."""
    return ["user1@company.com", "user2@company.com"]  # 가상 멤버

if __name__ == "__main__":
    mcp.run()