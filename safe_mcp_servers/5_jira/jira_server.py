# jira_mcp.py
# [상세 주석] 완전 정상 Jira 연동 MCP. 이슈 생성, 상태 변경, 코멘트 등 실제 Jira처럼 동작. 악성 요소 전무. TN 테스트용.
from fastmcp import MCPServer, mcp
from typing import List, Dict, Any
import uuid

app = MCPServer(
    name="JiraIssueTracker",
    version="8.1.0",
    description="Jira 이슈 관리 및 워크플로 자동화",
    capabilities=["issue_creation", "status_transition", "comment_add"]
)

issues: Dict[str, Dict] = {}

@mcp.tool()
def create_issue(project: str, summary: str, issue_type: str = "Task") -> Dict:
    """새로운 Jira 이슈를 생성합니다."""
    issue_id = f"{project}-{len(issues)+1}"
    issues[issue_id] = {
        "summary": summary,
        "type": issue_type,
        "status": "To Do",
        "comments": []
    }
    return {"issue_id": issue_id, "status": "생성됨"}

@mcp.tool()
def transition_issue(issue_id: str, to_status: str) -> bool:
    """이슈 상태를 변경합니다."""
    if issue_id in issues and to_status in ["To Do", "In Progress", "Done"]:
        issues[issue_id]["status"] = to_status
        return True
    return False

@mcp.tool()
def add_comment(issue_id: str, comment: str) -> int:
    """이슈에 코멘트를 추가합니다."""
    if issue_id in issues:
        issues[issue_id]["comments"].append({"text": comment})
    return len(issues[issue_id]["comments"])

@mcp.tool()
def get_issue_details(issue_id: str) -> Dict:
    """이슈 상세 정보를 반환합니다."""
    return issues.get(issue_id, {"error": "이슈 없음"})

if __name__ == "__main__":
    print("JiraIssueTracker 시작 중...")
    app.run(host="localhost", port=9001)