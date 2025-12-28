# config.py
import streamlit as st
import os

# -----------------------------------------------------------
# [보안 수정] API 키를 코드에 직접 적지 않고, Secrets에서 가져옵니다.
# -----------------------------------------------------------

# 1. Streamlit Cloud(웹)에서 실행 중일 때 Secrets에서 가져옴
if "GOOGLE_API_KEY" in st.secrets:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
else:
    # 2. 내 컴퓨터(로컬)에서 실행 중일 때 (환경변수 또는 빈 값)
    # 깃허브에 올릴 때는 절대 여기에 실제 키를 적지 마세요!
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# -----------------------------------------------------------
# 기타 설정들
# -----------------------------------------------------------
MAIN_CONTACT_NAME = "배종완 사장님"
MAIN_CONTACT_PHONE = "010-5089-1615"  # 필요시 수정하세요

# 엑셀 파일 경로
EXCEL_FILE_PATH = "pm_data.xlsx"

# 로고 파일 경로
LOGO_FILE_PATH = "home_logo.png"

# 추천인 ID 리스트 (가족 계정 등)
FAMILY_IDS = [
    {"role": "아내", "name": "전은영", "id": "8486455"},
    {"role": "어머니", "name": "김월선", "id": "10057772"},
    {"role": "누나", "name": "배정하", "id": "21287855"},
    {"role": "친구", "name": "이송호", "id": "20207931"},
    {"role": "친구", "name": "김영애(호기웅)", "id": "20405088"}
]


