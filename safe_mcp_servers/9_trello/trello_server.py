# trello_mcp.py
# [상세 주석] 1. 정상 MCP. 의심 요소 전혀 없음. TN 기준.
from fastmcp import FastMCP
from typing import List, Dict, Any
import uuid

mcp = FastMCP("TrelloBoardManager")

boards: Dict[str, Dict] = {}

@mcp.tool()
def create_card(board_id: str, title: str) -> Dict:
    """새로운 카드를 생성합니다."""
    card_id = str(uuid.uuid4())
    if board_id not in boards:
        boards[board_id] = {"cards": []}
    boards[board_id]["cards"].append({"id": card_id, "title": title})
    return {"card_id": card_id}

@mcp.tool()
def move_card(card_id: str, to_list: str) -> bool:
    """카드를 이동합니다."""
    for board in boards.values():
        for card in board["cards"]:
            if card["id"] == card_id:
                card["list"] = to_list
                return True
    return False

if __name__ == "__main__":
    mcp.run()