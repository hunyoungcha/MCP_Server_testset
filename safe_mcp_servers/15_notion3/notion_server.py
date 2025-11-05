# notion_mcp.py
# [상세 주석] 정상 서버. 페이지 생성 및 블록 추가.
from fastmcp import FastMCP
from typing import List, Dict, Any
import uuid

mcp = FastMCP("NotionWorkspace")

pages: Dict[str, Dict] = {}

@mcp.tool()
def create_page2(title: str) -> Dict:
    """새로운 페이지를 생성합니다."""
    page_id = str(uuid.uuid4())
    pages[page_id] = {"title": title, "blocks": []}
    return {"page_id": page_id}

@mcp.tool()
def append_block_2(page_id: str, block_type: str, content: str) -> bool:
    """페이지에 블록을 추가합니다."""
    if page_id in pages:
        pages[page_id]["blocks"].append({"type": block_type, "content": content})
        return True
    return False

@mcp.tool()
def get_page(page_id: str) -> Dict:
    """페이지 내용을 반환합니다."""
    return pages.get(page_id, {"error": "없음"})

if __name__ == "__main__":
    mcp.run()