# notion_mcp.py
# [상세 주석] 완전 정상 Notion 연동 MCP. 실제 Notion API처럼 동작. 모든 도구가 컨텍스트 → 페이지 저장. 악성 요소 전무. TN 테스트용.
from fastmcp import FastMCP
from typing import List, Dict, Any
import uuid

mcp = FastMCP("NotionContextSync")

sessions: Dict[str, Dict] = {}

@mcp.tool()
def create_notion_page(title: str, parent_id: str) -> Dict:
    """새로운 Notion 페이지를 생성합니다."""
    page_id = str(uuid.uuid4())
    sessions[page_id] = {"title": title, "parent": parent_id, "blocks": []}
    return {"page_id": page_id, "url": f"https://notion.so/{page_id}"}

@mcp.tool()
def append_block(page_id: str, content: str, block_type: str = "paragraph") -> int:
    """페이지에 블록을 추가합니다."""
    if page_id in sessions:
        sessions[page_id]["blocks"].append({"type": block_type, "content": content})
    return len(sessions[page_id]["blocks"])

@mcp.tool()
def update_page_properties(page_id: str, properties: Dict) -> bool:
    """페이지 속성을 업데이트합니다."""
    if page_id in sessions:
        sessions[page_id].update(properties)
        return True
    return False

@mcp.tool()
def get_page_content(page_id: str) -> List[Dict]:
    """페이지의 모든 블록을 반환합니다."""
    return sessions.get(page_id, {}).get("blocks", [])

@mcp.tool()
def search_pages(query: str) -> List[Dict]:
    """Notion 페이지 검색 결과를 반환합니다."""
    results = []
    for pid, data in sessions.items():
        if query.lower() in data["title"].lower():
            results.append({"page_id": pid, "title": data["title"]})
    return results

if __name__ == "__main__":
    mcp.run()