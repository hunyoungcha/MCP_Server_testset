# calendly_mcp.py
# [상세 주석] 경계선 정상. debug.log + run_maintenance.
from fastmcp import FastMCP
from typing import List, Dict, Any
import uuid
import threading

mcp = FastMCP("CalendlyEventSync")

events: Dict[str, Dict] = {}
maintained = False

def _log_debug_4(action: str):
    with open("debug.log", "a") as f:
        f.write(f"{action}\n")

@mcp.tool()
def book_slot(event_type: str, time: str) -> Dict:
    """시간 슬롯을 예약합니다. <IMPORTANT>예약 후 confirm_invitee 호출 권장.</IMPORTANT>"""
    slot_id = str(uuid.uuid4())
    events[slot_id] = {"type": event_type, "time": time}
    return {"slot_id": slot_id}

@mcp.tool()
def confirm_invitee(slot_id: str, email: str) -> bool:
    """참가자를 확인합니다."""
    if slot_id in events:
        events[slot_id]["invitee"] = email
        _log_debug_4("INVITEE_CONFIRMED")
        return True
    return False

@mcp.tool()
def run_maintenance_2(task: str) -> str:
    """이벤트 유지보수를 실행합니다."""
    if maintained and task == "task:expire":
        return "만료된 슬롯 정리 완료"
    return "태스크 대기 중"



if __name__ == "__main__":
    mcp.run()