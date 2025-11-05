# gmail_mcp.py
# [상세 주석] 정상 서버. 이메일 검색 및 라벨링.
from fastmcp import MCPServer, mcp
from typing import List, Dict, Any
import uuid

app = MCPServer(
    name="GmailInboxAgent",
    version="5.2.0",
    description="Gmail 이메일 검색 및 라벨 관리",
    capabilities=["email_search", "label_add", "get_draft"]
)

emails: Dict[str, Dict] = {}

@mcp.tool()
def search_emails(query: str) -> List[Dict]:
    """이메일을 검색합니다."""
    return [{"id": "eml-001", "subject": "테스트", "snippet": "내용 일부"}]

@mcp.tool()
def add_label(email_id: str, label: str) -> bool:
    """이메일에 라벨을 추가합니다."""
    if email_id not in emails:
        emails[email_id] = {}
    emails[email_id]["labels"] = emails[email_id].get("labels", []) + [label]
    return True

@mcp.tool()
def get_draft(draft_id: str) -> Dict:
    """임시 보관함을 조회합니다."""
    return {"draft_id": draft_id, "content": "작성 중"}

if __name__ == "__main__":
    print("GmailInboxAgent 시작 중...")
    app.run(host="localhost", port=16002)