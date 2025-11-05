# linear_mcp.py
# [상세 주석] 정상 서버. 의심 요소 0%. TN 기준.
from fastmcp import MCPServer, mcp
from typing import List, Dict, Any
import uuid

app = MCPServer(
    name="LinearCycleBot",
    version="2.9.0",
    description="Linear 사이클 및 이슈 관리",
    capabilities=["cycle_creation", "assign_issue", "query_roadmap"]
)

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
    print("LinearCycleBot 시작 중...")
    app.run(host="localhost", port=17001)