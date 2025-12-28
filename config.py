import streamlit as st
import os

# -----------------------------------------------------------
# [핵심 수정] API 키 가져오기 (Render 오류 해결)
# -----------------------------------------------------------
def get_api_key():
    # 1순위: Render 환경 변수 확인 (가장 먼저 체크!)
    # Render 설정에서 넣은 GOOGLE_API_KEY가 여기서 잡힙니다.
    env_key = os.getenv("GOOGLE_API_KEY")
    if env_key:
        return env_key

    # 2순위: Streamlit Secrets 확인 (로컬 개발용)
    # 파일이 없어도 오류가 나지 않도록 try-except로 감싸줍니다.
    try:
        if "GOOGLE_API_KEY" in st.secrets:
            return st.secrets["GOOGLE_API_KEY"]
    except Exception:
        pass # 파일이 없으면 그냥 넘어감

    # 3순위: 아무것도 없으면 빈 값
    return ""

# 위 함수를 실행해서 키를 저장합니다.
GOOGLE_API_KEY = get_api_key()

# -----------------------------------------------------------
# 기타 설정들
# -----------------------------------------------------------
MAIN_CONTACT_NAME = "배종완 사장님"
MAIN_CONTACT_PHONE = "010-5089-1615" 

# 엑셀 파일 경로
EXCEL_FILE_PATH = "pm_data.xlsx"

# 로고 파일 경로
LOGO_FILE_PATH = "home_logo.png"

# 추천인 ID 리스트 (기존 데이터 유지)
FAMILY_IDS = [
    {"role": "아내", "name": "전은영", "id": "8486455"},
    {"role": "어머니", "name": "김월선", "id": "10057772"},
    {"role": "누나", "name": "배정하", "id": "21287855"},
    {"role": "친구", "name": "이송호", "id": "20207931"},
    {"role": "친구", "name": "김영애(호기웅)", "id": "20405088"}
]
