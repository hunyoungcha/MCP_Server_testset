import os
import base64
from fastmcp import FastMCP
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH = os.path.join(BASE_DIR, "credentials.json")
TOKEN_PATH = os.path.join(BASE_DIR, "token.json")

mcp = FastMCP("Gmail-MCP")

def get_gmail_service():
    """
    OAuth2 인증 처리 및 Gmail API 서비스 객체를 생성.
    """
    creds = None

    # 1. 이전에 저장된 토큰 정보 로드
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    # 2. 토큰이 없거나 형식이 잘못된 경우
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_PATH):
                raise FileNotFoundError(
                    f"'{CREDENTIALS_PATH}' 파일이 없습니다. Google Cloud에서 OAuth 클라이언트 ID를 먼저 생성하세요."
                )
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)

            with open('token.json', 'w') as token:
                token.write(creds.to_json())

    # 3. Gmail API 서비스 객체 반환
    return build('gmail', 'v1', credentials=creds)

@mcp.tool
def send_message(to: str, subject: str, body: str) -> str:
    """
    Gmail을 통해 이메일을 보냅니다.
    Args:
        to (str): 수신자 이메일 주소
        subject (str): 제목
        body (str): 본문 내용
    Returns:
        str: 전송 결과 메시지
    """
    try:
        service = get_gmail_service()
        message = MIMEText(body)
        message["to"] = to
        message["subject"] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

        send_result = (
            service.users().messages().send(userId="me", body={"raw": raw}).execute()
        )
        
        return f"이메일 전송 성공. Message ID: {send_result.get('id')}"
    except Exception as e:
        return f"이메일 전송 실패: {str(e)}"
    

@mcp.tool
def search_messages(query: str, max_results: int = 5) -> list:
    """
    Gmail 메시지를 검색합니다.
    Args:
        query (str): 검색어 또는 Gmail 검색 쿼리.
            예시:
              - subject:인증
              - from:google
              - after:2025/10/01
        max_results (int): 가져올 최대 메시지 수 (기본값: 5)
    Returns:
        list: 검색된 메시지 목록 (각 항목은 id, from, subject 포함)
    """
    try:
        service = get_gmail_service()
        results = (
            service.users()
            .messages()
            .list(userId="me", q=query, maxResults=max_results)
            .execute()
        )

        messages = results.get("messages", [])
        if not messages:
            return []

        found = []
        for msg in messages:
            msg_data = (
                service.users().messages().get(userId="me", id=msg["id"], format="metadata").execute()
            )
            headers = msg_data["payload"]["headers"]
            subject = next((h["value"] for h in headers if h["name"] == "Subject"), "(제목 없음)")
            sender = next((h["value"] for h in headers if h["name"] == "From"), "(보낸이 없음)")
            found.append({
                "id": msg["id"],
                "from": sender,
                "subject": subject
            })

        return found

    except Exception as e:
        return {"error": str(e)}
    
@mcp.tool
def list_message(limit: int = 5) -> list:
    """
    최근 Gmail 메시지 목록을 가져옵니다.
    Args:
        limit (int): 가져올 최대 메시지 수 (기본값: 5)
    Returns:
        list: 최근 메시지 목록 (각 항목은 id, subject 포함)
    """
    try:
        service = get_gmail_service()
        results = service.users().messages().list(userId="me", maxResults=limit).execute()
        messages = results.get("messages", [])

        message_list = []
        for msg in messages:
            msg_data = (
                service.users().messages().get(userId="me", id=msg["id"], format="metadata").execute()
            )
            headers = msg_data["payload"]["headers"]
            subject = next((h["value"] for h in headers if h["name"] == "Subject"), "(제목 없음)")
            message_list.append({"id": msg["id"], "subject": subject})

        return message_list
    except Exception as e:
        return [{"error": str(e)}]

@mcp.tool
def get_message(message_id: str) -> dict:
    """
    특정 Gmail 메시지의 상세 내용을 가져옵니다.
    Args:
        message_id (str): 조회할 Gmail 메시지의 ID
    Returns:
        dict: 메시지 상세 정보 (id, from, subject, body 포함)
    """
    try:
        service = get_gmail_service()
        message = (
            service.users().messages().get(userId="me", id=message_id, format="full").execute()
        )

        headers = message["payload"]["headers"]
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "(제목 없음)")
        sender = next((h["value"] for h in headers if h["name"] == "From"), "(보낸이 없음)")

        if "parts" in message["payload"]:
            body_data = message["payload"]["parts"][0]["body"].get("data", "")
        else:
            body_data = message["payload"]["body"].get("data", "")

        body = base64.urlsafe_b64decode(body_data).decode("utf-8", errors="ignore")
        return {"id": message["id"], "from": sender, "subject": subject, "body": body.strip()}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()
