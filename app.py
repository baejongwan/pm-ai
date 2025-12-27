import streamlit as st
import os
import warnings
import base64

# --- 파일 임포트 ---
import styles
import view_home
import view_ai
import view_products
import view_pdf
import view_guide
import view_compensation
import view_stories
from func import move_to_page 
from utils import load_excel

warnings.filterwarnings("ignore")
try: import google.generativeai as genai
except: genai = None

from config import *

# --------------------------------------------------------------------------
# [1] 기본 페이지 설정 (Manifest 방식 적용)
# --------------------------------------------------------------------------

# 1. 아이콘 및 매니페스트 주소
ICON_URL = "https://raw.githubusercontent.com/baejongwan/pm-ai/main/app_icon.png"
MANIFEST_URL = "https://raw.githubusercontent.com/baejongwan/pm-ai/main/manifest.json"

# 2. 페이지 기본 설정
st.set_page_config(
    page_title="PM 파트너스 허브", 
    page_icon=ICON_URL, 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 3. [최종 병기] 아이콘 및 매니페스트 강제 주입
# 스마트폰에게 "왕관 말고 이 명찰(manifest)을 봐!"라고 강력하게 요청하는 코드입니다.
st.markdown(
    f"""
    <link rel="manifest" href="{MANIFEST_URL}">
    <link rel="apple-touch-icon" href="{ICON_URL}">
    <link rel="apple-touch-icon" sizes="180x180" href="{ICON_URL}">
    <link rel="shortcut icon" href="{ICON_URL}">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black">
    <meta name="apple-mobile-web-app-title" content="PM Hub">
    """,
    unsafe_allow_html=True
)
# --------------------------------------------------------------------------
# [2] 네비게이션 로직 (URL 기준 - 뒤로 가기 해결)
# --------------------------------------------------------------------------
current_url_page = st.query_params.get("page", "홈")

if "page" not in st.session_state:
    st.session_state.page = current_url_page

# --------------------------------------------------------------------------
# [3] 스타일 및 데이터 로딩
# --------------------------------------------------------------------------
styles.apply_custom_css()
all_sheets = load_excel()

# --------------------------------------------------------------------------
# [4] 화면 구성 함수들 (수정됨: 새로고침 방지 네비게이션)
# --------------------------------------------------------------------------
def render_top_navigation():
    # 메뉴 목록
    menu_options = [
        "홈", "AI상담", "수익계산", "보상플랜", "제품구매",
        "안전성", "액티증상", "호전반응", "체험사례", "성공사례", "자료실"
    ]
    
    # CSS: 버튼을 메뉴바처럼 예쁘게 꾸미기
    st.markdown("""
        <style>
        /* 버튼 사이 간격 조절 */
        div[data-testid="column"] { padding: 0 !important; margin: 0 !important; }
        
        /* 버튼 기본 스타일 (투명하고 깔끔하게) */
        div.stButton > button {
            width: 100%;
            border-radius: 0px;
            border: none;
            background-color: transparent;
            color: #555;
            font-weight: 600;
            padding: 10px 0;
            border-bottom: 3px solid transparent; /* 밑줄 효과 준비 */
            transition: all 0.3s;
        }
        
        /* 마우스 올렸을 때 */
        div.stButton > button:hover {
            color: #007bff;
            background-color: #f8f9fa;
        }
        
        /* 모바일 화면 대응 (글자 크기 조절) */
        @media (max-width: 768px) {
            div.stButton > button { font-size: 12px; padding: 5px 0; }
        }
        </style>
    """, unsafe_allow_html=True)

    # 메뉴 개수만큼 칸 나누기
    cols = st.columns(len(menu_options))
    
    # 현재 보고 있는 페이지 확인
    current_page = st.session_state.get("page", "홈")

    for i, option in enumerate(menu_options):
        # 현재 선택된 메뉴인지 확인
        is_active = (current_page == option)
        
        # 버튼 그리기
        # (type="primary"를 쓰면 선택된 메뉴가 붉은색/테마색으로 강조됩니다)
        btn_type = "primary" if is_active else "secondary"
        
        # 버튼을 클릭하면? -> 페이지 이동 (새로고침 없이!)
        if cols[i].button(option, key=f"nav_{i}", type=btn_type, use_container_width=True):
            st.session_state.page = option   # 1. 내부 기억 장치에 페이지 저장
            st.query_params["page"] = option # 2. 주소창 주소 변경
            st.rerun()                       # 3. 화면만 살짝 다시 그리기

# --------------------------------------------------------------------------
# [5] 실행 (서버 목록에 있는 확실한 모델 이름 사용)
# --------------------------------------------------------------------------
api_key = GOOGLE_API_KEY
selected_model = "gemini-flash-latest"

if api_key:
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
    except Exception as e:
        print(f"모델 설정 오류: {e}")
        
# [1] 7주년 행사 포스터 주소
EVENT_IMAGE_URL = "https://raw.githubusercontent.com/baejongwan/pm-ai/main/event_01.jpg"

# [2] 정식 팝업창 기능 (st.dialog 사용)
# 이 기능은 스트림릿이 직접 관리하는 '진짜 윈도우 창'을 띄웁니다.
@st.dialog("🎉 7주년 액티바이즈 프로모션", width="large")
def show_promo_window():
    # 1. 이미지 출력
    st.image(EVENT_IMAGE_URL)
    
    # 2. 설명 문구
    st.caption("💡 창 밖의 어두운 부분을 클릭하거나, 오른쪽 위 X를 누르면 닫힙니다.")
    
    # 3. 닫기 버튼 (빨간색)
    if st.button("닫기", type="primary", use_container_width=True):
        st.rerun()

# [3] 팝업 실행 로직 (접속 시 한 번만 뜨도록 설정)
# 'home_popup_shown'이라는 이름표가 없으면 -> 팝업을 띄우고 -> 이름표를 붙임
if "home_popup_shown" not in st.session_state:
    # 홈 화면일 때만 띄우기
    if "page" not in st.query_params or st.query_params["page"] == "🏠 홈 대시보드":
        show_promo_window()
        st.session_state["home_popup_shown"] = True

# [4] 나머지 화면 렌더링
render_home_logo()      
render_top_navigation()
# --------------------------------------------------------------------------
# [6] 페이지 내용 표시
# --------------------------------------------------------------------------
target_page = current_url_page

if target_page == "홈": view_home.render_home_dashboard(all_sheets)
elif target_page == "AI상담": view_ai.render_ai_assistant(api_key, selected_model, all_sheets)
elif target_page == "수익계산": view_compensation.render_calculator_v2()
elif target_page == "보상플랜": view_compensation.render_compensation(all_sheets)
elif target_page == "제품구매": view_products.render_products(all_sheets)
elif target_page == "안전성": view_products.render_safety(all_sheets)
elif target_page == "액티증상": view_products.render_diagnosis(all_sheets)
elif target_page == "자료실": view_pdf.render_pdf_viewer("catalog.pdf")
elif target_page == "호전반응": view_guide.render_guide(all_sheets)
elif target_page == "체험사례": view_stories.render_experience(all_sheets)
elif target_page == "성공사례": view_stories.render_success(all_sheets)




