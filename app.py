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
# [1] 기본 페이지 설정
# --------------------------------------------------------------------------
if os.path.exists("app_icon.png"): icon_path = "app_icon.png"
elif os.path.exists("home_logo.png"): icon_path = "home_logo.png"
elif os.path.exists("PMAILOGO.png"): icon_path = "PMAILOGO.png"
else: icon_path = "💙"

st.set_page_config(
    page_title="PM 파트너스 허브", 
    page_icon=icon_path, 
    layout="wide", 
    initial_sidebar_state="collapsed"
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
# [4] 화면 구성 함수들
# --------------------------------------------------------------------------
def render_home_logo():
    if current_url_page == "홈":
        logo_path = None
        if os.path.exists("home_logo.png"): logo_path = "home_logo.png"
        elif os.path.exists("PMAILOGO.png"): logo_path = "PMAILOGO.png"
        
        if logo_path:
            with open(logo_path, "rb") as f:
                img_b64 = base64.b64encode(f.read()).decode()
            st.markdown(f"""
                <div style="display: flex; justify-content: center; padding-top: 10px; padding-bottom: 5px;">
                    <img src="data:image/png;base64,{img_b64}" style="width: 120px; object-fit: contain;">
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <h3 style='text-align:center; color:#003057; margin-top:10px; margin-bottom:5px;'>
                    PM Partners
                </h3>
            """, unsafe_allow_html=True)

def render_top_navigation():
    menu_options = [
        "홈", "AI상담", "수익계산", "보상플랜", "제품구매",
        "안전성", "액티증상", "호전반응", "체험사례", "성공사례", "자료실"
    ]
    html_nav = '<div class="nav-container">'
    for option in menu_options:
        active_class = "active" if option == current_url_page else ""
        html_nav += f'<a href="?page={option}" target="_self" class="nav-link {active_class}">{option}</a>'
    html_nav += '</div>'
    st.markdown(html_nav, unsafe_allow_html=True)

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
        
# [1] 팝업 함수 가져오기
from utils import show_event_popup

# [2] 7주년 행사 포스터 주소 (사장님 깃허브 파일명: event_01.jpg)
# 주의: 깃허브 저장소가 'Public(공개)' 상태여야 이 이미지가 보입니다.
EVENT_IMAGE_URL = "https://raw.githubusercontent.com/baejongwan/pm-final-v1/main/event_01.jpg"

# [3] 팝업 실행
# 조건: 'page' 파라미터가 없거나(첫 접속), '홈 대시보드'일 때만 실행
if "page" not in st.query_params or st.query_params["page"] == "🏠 홈 대시보드":
    show_event_popup(EVENT_IMAGE_URL)

# [4] 나머지 화면 렌더링 (이 부분은 들여쓰기 없이 벽에 붙어야 합니다)
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





