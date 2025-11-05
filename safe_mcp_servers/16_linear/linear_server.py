# linear_mcp.py
# [상세 주석] 정상 서버. 의심 요소 0%. TN 기준.
from fastmcp import FastMCP
from typing import List, Dict, Any
import uuid

mcp = FastMCP("LinearCycleBot")

cycles: Dict[str, Dict] = {}

@mcp.tool()
def create_cycle(team: str, name: str) -> Dict:
    """새로운 사이클을 생성합니다."""
    cycle_id = str(uuid.uuid4())
    cycles[cycle_id] = {"team": team, "name": name, "issues": []}
    return {"cycle_id": cycle_id}

@mcp.tool()
def assign_issue(cycle_id: str, issue_key: str) -> bool:
    """사이클에 이슈를 할당합니다."""
    if cycle_id in cycles:
        cycles[cycle_id]["issues"].append(issue_key)
        return True
    return False

@mcp.tool()
def query_roadmap(cycle_id: str) -> List[str]:
    """사이클 로드맵을 조회합니다."""
    return cycles.get(cycle_id, {}).get("issues", [])

if __name__ == "__main__":
    mcp.run()