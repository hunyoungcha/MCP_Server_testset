# monday_mcp.py
# [상세 주석] 정상 서버. 아이템 추가 및 상태 업데이트.
from fastmcp import FastMCP
from typing import List, Dict, Any
import uuid

mcp = FastMCP("MondayItemManager")

boards: Dict[str, List[Dict]] = {}

@mcp.tool()
def add_item(board_id: str, name: str) -> Dict:
    """새로운 아이템을 추가합니다."""
    item_id = str(uuid.uuid4())
    if board_id not in boards:
        boards[board_id] = []
    boards[board_id].append({"id": item_id, "name": name, "status": "new"})
    return {"item_id": item_id}

@mcp.tool()
def update_status(item_id: str, status: str) -> bool:
    """아이템 상태를 업데이트합니다."""
    for board_items in boards.values():
        for item in board_items:
            if item["id"] == item_id:
                item["status"] = status
                return True
    return False

@mcp.tool()
def get_board(board_id: str) -> List[Dict]:
    """보드 아이템을 조회합니다."""
    return boards.get(board_id, [])

if __name__ == "__main__":
    mcp.run()