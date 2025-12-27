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
ICON_URL = "https://raw.githubusercontent.com/baejongwan/pm-ai/main/app_icon.png"
MANIFEST_URL = "https://raw.githubusercontent.com/baejongwan/pm-ai/main/manifest.json"

st.set_page_config(
    page_title="PM 파트너스 허브", 
    page_icon=ICON_URL, 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 아이콘 및 메타태그 (최초 1회만 설정)
if "head_set" not in st.session_state:
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
    st.session_state.head_set = True

# --------------------------------------------------------------------------
# [2] 네비게이션 로직 (HTML 방식)
# --------------------------------------------------------------------------
# HTML <a> 태그로 전달된 ?page=... 값을 읽어옵니다.
query_params = st.query_params
current_page = query_params.get("page", "홈")

# --------------------------------------------------------------------------
# [3] 스타일 및 데이터 로딩
# --------------------------------------------------------------------------
styles.apply_custom_css()
all_sheets = load_excel()

# --------------------------------------------------------------------------
# [4] 화면 구성 함수들
# --------------------------------------------------------------------------
def render_home_logo():
    if current_page == "홈":
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
    
    # [디자인 복구] 예전의 HTML/CSS 방식 (가로 정렬, 줄바꿈 자연스러움)
    html_nav = """
    <style>
    .nav-container {
        display: flex;
        flex-wrap: wrap;        /* 공간 부족시 자동 줄바꿈 */
        justify-content: center; /* 가운데 정렬 */
        gap: 6px;
        padding-bottom: 10px;
    }
    .nav-link {
        text-decoration: none;
        color: #555;
        background-color: white;
        padding: 6px 14px;
        border-radius: 50px;    /* 알약 모양 */
        border: 1px solid #ddd;
        font-size: 14px;
        font-weight: 600;
        transition: all 0.3s;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        white-space: nowrap;
    }
    .nav-link:hover {
        background-color: #f0f8ff;
        color: #007bff;
        border-color: #007bff;
    }
    .nav-link.active {
        background-color: #007bff;
        color: white;
        border-color: #007bff;
    }
    /* 모바일 반응형 글자 크기 */
    @media (max-width: 400px) {
        .nav-link { font-size: 12px; padding: 5px 10px; }
    }
    </style>
    <div class="nav-container">
    """
    
    for option in menu_options:
        active_class = "active" if option == current_page else ""
        # target="_self"를 사용해 현재 창에서 페이지 이동 (새로고침 발생)
        html_nav += f'<a href="?page={option}" target="_self" class="nav-link {active_class}">{option}</a>'
    
    html_nav += '</div>'
    st.markdown(html_nav, unsafe_allow_html=True)

# --------------------------------------------------------------------------
# [5] 팝업창 및 기본 실행
# --------------------------------------------------------------------------
api_key = GOOGLE_API_KEY
selected_model = "gemini-flash-latest"

if api_key:
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
    except Exception as e:
        pass

# 팝업 로직 (홈 화면일 때 1회만)
EVENT_IMAGE_URL = "https://raw.githubusercontent.com/baejongwan/pm-ai/main/event_01.jpg"

@st.dialog("🎉 7주년 액티바이즈 프로모션", width="large")
def show_promo_window():
    st.image(EVENT_IMAGE_URL)
    st.caption("💡 창 밖의 어두운 부분을 클릭하거나, 오른쪽 위 X를 누르면 닫힙니다.")
    if st.button("닫기", type="primary", use_container_width=True):
        st.rerun()

if "home_popup_shown" not in st.session_state:
    if current_page == "홈":
        show_promo_window()
        st.session_state["home_popup_shown"] = True

# 화면 그리기
render_home_logo()      
render_top_navigation()

# --------------------------------------------------------------------------
# [6] 페이지 연결
# --------------------------------------------------------------------------
target_page = current_page

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
