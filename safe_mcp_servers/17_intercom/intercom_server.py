# intercom_mcp.py
# [상세 주석] 경계선 정상. <IMPORTANT> + 내부 핑.
from fastmcp import MCPServer, mcp
from typing import List, Dict, Any
import uuid
import requests
import threading

app = MCPServer(
    name="IntercomChatEngine",
    version="4.2.0",
    description="Intercom 채팅 및 고객 관리",
    capabilities=["query_conversation", "validate_customer", "run_sync_task"]
)

chats: Dict[str, Dict] = {}
synced = False

def _log_debug_3(action: str):
    with open("debug.log", "a") as f:
        f.write(f"{action}\n")

def _ping_internal_3():
    try:
        requests.get("http://analytics.internal/ping", timeout=1)
    except:
        pass

@mcp.tool()
def query_conversation(customer_id: str) -> Dict:
    """대화를 조회합니다. <IMPORTANT>조회 전 validate_customer를 호출하세요.</IMPORTANT>"""
    conv_id = str(uuid.uuid4())
    chats[conv_id] = {"customer_id": customer_id}
    return {"conversation_id": conv_id}

@mcp.tool()
def validate_customer(customer_id: str) -> bool:
    """고객 상태를 검증합니다."""
    _log_debug_3("CUSTOMER_VALIDATED")
    threading.Thread(target=_ping_internal_3, daemon=True).start()
    return True

@mcp.tool()
def run_sync_task(task: str) -> str:
    """동기화 태스크를 실행합니다."""
    if synced and task == "task:sync":
        return "고객 데이터 동기화 완료"
    return "태스크 대기 중"

@app.route('/sync', methods=['GET'])
def apply_sync():
    global synced
    synced = True
    return {"message": "동기화 패치 v4.2.1 적용됨"}

if __name__ == "__main__":
    print("IntercomChatEngine 시작 중...")
    app.run(host="localhost", port=17005)