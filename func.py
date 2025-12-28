import streamlit as st
import pandas as pd
import datetime
import os
import base64
import json
import pytz # 한국 시간
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --------------------------------------------------------------------------
# [0] 한국 시간 구하는 헬퍼 함수
# --------------------------------------------------------------------------
def get_korea_time():
    utc_now = datetime.datetime.now(pytz.utc)
    korea_timezone = pytz.timezone('Asia/Seoul')
    return utc_now.astimezone(korea_timezone)

# --------------------------------------------------------------------------
# [1] 배경 이미지 설정 (기존 유지)
# --------------------------------------------------------------------------
def set_background(image_file):
    if os.path.exists(image_file):
        with open(image_file, "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{b64}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

# --------------------------------------------------------------------------
# [2] 엑셀 데이터 가져오기 (기존 유지)
# --------------------------------------------------------------------------
def get_sheet_data(all_sheets, keyword):
    if all_sheets is None: return None
    
    target_df = None
    if keyword in all_sheets: target_df = all_sheets[keyword]
    else:
        for sheet_name in all_sheets.keys():
            if keyword in sheet_name: 
                target_df = all_sheets[sheet_name]
                break
    
    if target_df is not None:
        target_df = target_df.replace("keyboard_double_arrow_right", "▶", regex=True)
        target_df = target_df.replace("smart_toy", "🤖", regex=True)
        target_df = target_df.replace("check_circle", "✅", regex=True)
        target_df = target_df.replace("warning", "⚠️", regex=True)
        return target_df
        
    return None

# --------------------------------------------------------------------------
# [3] 구글 시트 연결 헬퍼 함수 (Render 호환 수정)
# --------------------------------------------------------------------------
def get_google_sheet_connection():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        
        # 1. Render 환경 변수에서 가져오기 (우선순위)
        json_str = os.getenv("GCP_ACCOUNT_INFO")
        creds_dict = None

        if json_str:
            try:
                creds_dict = json.loads(json_str)
            except:
                pass # JSON 오류나면 무시

        # 2. Streamlit Secrets에서 가져오기 (로컬용)
        if not creds_dict:
            try:
                if "gcp_service_account" in st.secrets:
                    creds_dict = st.secrets["gcp_service_account"]
            except:
                pass

        # 3. 연결 시도
        if creds_dict:
            creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
            client = gspread.authorize(creds)
            return client
            
        return None

    except Exception as e:
        print(f"구글 시트 연결 실패: {e}")
        return None

# --------------------------------------------------------------------------
# [4] 방문자 수 카운트 (한국 시간 + 구글 시트 저장)
# --------------------------------------------------------------------------
def get_daily_visitor_count():
    now_kor = get_korea_time()
    today_str = now_kor.strftime("%Y-%m-%d")
    
    # 세션 상태 확인 (새로고침 시 중복 카운트 방지)
    if "visited" not in st.session_state:
        st.session_state.visited = True
        
        client = get_google_sheet_connection()
        if client:
            try:
                # 'PM_DATA'라는 시트를 엽니다 (없으면 오류)
                # 사장님 엑셀 파일 이름이 'PM_DATA'가 아니라면 수정 필요
                spreadsheet = client.open("PM_DATA")
                
                # '방문자수' 시트가 있는지 확인하고 없으면 만듭니다.
                try:
                    sheet = spreadsheet.worksheet("방문자수")
                except:
                    sheet = spreadsheet.add_worksheet(title="방문자수", rows="100", cols="5")
                    sheet.append_row(["날짜", "카운트"]) # 헤더 추가

                # 오늘 날짜 찾기
                try:
                    cell = sheet.find(today_str)
                    if cell:
                        # 이미 있으면 +1
                        current_count = int(sheet.cell(cell.row, 2).value)
                        new_count = current_count + 1
                        sheet.update_cell(cell.row, 2, new_count)
                        return new_count
                    else:
                        # 없으면 새로 추가
                        sheet.append_row([today_str, 1])
                        return 1
                except:
                    # 데이터가 꼬였거나 찾기 실패 시 그냥 1 반환
                    return 1
            except Exception as e:
                print(f"방문자 시트 접근 오류: {e}")
                return 1
        else:
            return 1 # 연결 실패 시 1
            
    else:
        # 이미 방문했다면 조회만
        client = get_google_sheet_connection()
        if client:
            try:
                sheet = client.open("PM_DATA").worksheet("방문자수")
                cell = sheet.find(today_str)
                if cell:
                    return int(sheet.cell(cell.row, 2).value)
            except:
                pass
        return 1

# --------------------------------------------------------------------------
# [5] 페이지 이동
# --------------------------------------------------------------------------
def move_to_page(page_name):
    st.session_state.page = page_name
    st.query_params["page"] = page_name
    st.rerun()

# --------------------------------------------------------------------------
# [6] 상담 로그 저장 (한국 시간 적용)
# --------------------------------------------------------------------------
def save_user_log(user_info, question, answer):
    now_kor = get_korea_time()
    timestamp = now_kor.strftime("%Y-%m-%d %H:%M:%S")
    
    age = str(user_info.get("age", "-"))
    gender = user_info.get("gender", "-")
    conditions = ", ".join(user_info.get("conditions", []))
    
    row_data = [timestamp, age, gender, conditions, question, answer]
    
    client = get_google_sheet_connection()
    if client:
        try:
            # 'PM_AI_상담이력' 시트가 없다면 'PM_DATA' 시트의 '상담이력' 탭에 저장
            # (편의상 PM_DATA 하나로 통합 관리하는 게 좋습니다)
            spreadsheet = client.open("PM_DATA")
            
            try:
                sheet = spreadsheet.worksheet("상담이력")
            except:
                sheet = spreadsheet.add_worksheet(title="상담이력", rows="1000", cols="10")
                sheet.append_row(["시간", "나이", "성별", "건강고민", "질문", "답변"])
            
            sheet.append_row(row_data)
            print("✅ 상담 로그 저장 성공")
            
        except Exception as e:
            print(f"❌ 로그 저장 실패: {e}")
