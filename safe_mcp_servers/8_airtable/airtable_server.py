# airtable_mcp.py
# [상세 주석] 완전 정상 Airtable 연동 MCP. 베이스 생성, 레코드 추가, 필터링 등 실제 Airtable API처럼 동작. TN 테스트용.
from fastmcp import FastMCP
from typing import List, Dict, Any
import uuid

mcp = FastMCP("AirtableDataHub")

bases: Dict[str, Dict] = {}

@mcp.tool()
def create_base(name: str, table_schema: List[Dict]) -> Dict:
    """새로운 Airtable 베이스를 생성합니다."""
    base_id = str(uuid.uuid4())
    bases[base_id] = {
        "name": name,
        "tables": {schema["name"]: [] for schema in table_schema}
    }
    return {"base_id": base_id}

@mcp.tool()
def insert_record(base_id: str, table_name: str, fields: Dict) -> Dict:
    """테이블에 레코드를 추가합니다."""
    if base_id in bases and table_name in bases[base_id]["tables"]:
        record_id = str(uuid.uuid4())
        bases[base_id]["tables"][table_name].append({"id": record_id, "fields": fields})
        return {"record_id": record_id}
    return {"error": "베이스 또는 테이블 없음"}

@mcp.tool()
def filter_records(base_id: str, table_name: str, filter_by: str) -> List[Dict]:
    """필터 조건으로 레코드를 조회합니다."""
    if base_id in bases and table_name in bases[base_id]["tables"]:
        return [rec for rec in bases[base_id]["tables"][table_name] if filter_by in str(rec["fields"])]
    return []

if __name__ == "__main__":
    mcp.run()