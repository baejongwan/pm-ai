import streamlit as st
import pandas as pd
import datetime
import os
import base64
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# [1] 배경 이미지 설정 (기존 유지)
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

# [2] 엑셀 데이터 가져오기 (기존 유지)
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

# [3] 방문자 수 카운트 (구글 시트 연동 버전)
def get_daily_visitor_count():
    import datetime
    from func import get_google_sheet_connection # 연결 함수 재사용
    
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    
    # 세션 상태 확인 (새로고침 시 카운트 증가 방지)
    if "visited" not in st.session_state:
        st.session_state.visited = True
        
        try:
            client = get_google_sheet_connection()
            if client:
                # 1. '방문자수' 시트 열기 (없으면 생성해야 함)
                try:
                    sheet = client.open("PM_AI_상담이력").worksheet("방문자수")
                except:
                    # 시트가 없으면 기본 시트(sheet1)를 쓰거나 에러 처리
                    # 여기서는 편의상 상담이력 시트의 맨 마지막 셀을 쓴다고 가정하거나
                    # 가장 좋은 건 구글 시트에 '방문자수' 탭을 하나 추가하는 것입니다.
                    return 1

                # 2. 오늘 날짜 데이터 찾기
                # A열: 날짜, B열: 카운트 라고 가정
                cell = sheet.find(today_str)
                
                if cell:
                    # 이미 오늘 날짜가 있으면 -> 카운트 +1
                    current_count = int(sheet.cell(cell.row, 2).value)
                    new_count = current_count + 1
                    sheet.update_cell(cell.row, 2, new_count)
                    return new_count
                else:
                    # 오늘 날짜가 없으면 -> 새로 한 줄 추가
                    sheet.append_row([today_str, 1])
                    return 1
            else:
                return 1 # 연결 실패 시 1명으로 표시
        except Exception as e:
            print(f"방문자 카운트 오류: {e}")
            return 1
            
    else:
        # 이미 방문한 상태라면 카운트 늘리지 않고 조회만 시도
        try:
            client = get_google_sheet_connection()
            if client:
                sheet = client.open("PM_AI_상담이력").worksheet("방문자수")
                cell = sheet.find(today_str)
                if cell:
                    return int(sheet.cell(cell.row, 2).value)
        except:
            pass
        return 1

# [4] 페이지 이동 (기존 유지)
def move_to_page(page_name):
    st.session_state.page = page_name
    st.query_params["page"] = page_name
    st.rerun()

# [5] 구글 시트 연결 헬퍼 함수 (신규 추가)
def get_google_sheet_connection():
    try:
        # Streamlit Secrets에서 키 정보 가져오기
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds_dict = st.secrets["gcp_service_account"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        print(f"구글 시트 연결 실패: {e}")
        return None

# [6] ★ 사용자 로그 저장 (구글 시트로 변경됨) ★
def save_user_log(user_info, question, answer):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    age = str(user_info.get("age", "-"))
    gender = user_info.get("gender", "-")
    conditions = ", ".join(user_info.get("conditions", []))
    
    # 저장할 데이터 한 줄
    row_data = [timestamp, age, gender, conditions, question, answer]
    
    try:
        # 1. 구글 시트 연결
        client = get_google_sheet_connection()
        if client:
            # 2. 스프레드시트 열기 (이름: PM_AI_상담이력)
            # 주의: 구글 드라이브에 이 이름의 시트가 있어야 하고, 봇에게 공유되어 있어야 함
            sheet = client.open("PM_AI_상담이력").sheet1
            
            # 3. 데이터 추가 (append_row)
            sheet.append_row(row_data)
            print("✅ 구글 시트 저장 성공")
        else:
            print("❌ 구글 시트 클라이언트 없음")
            
    except Exception as e:
        print(f"❌ 구글 시트 저장 중 오류: {e}")
        # 실패 시 비상용으로 로컬 파일에도 시도 (백업)
        import csv
        file_name = "backup_logs.csv"
        with open(file_name, mode='a', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(row_data)

