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

# [핵심 수정] 아이콘 코드가 매번 실행되지 않도록 '한 번만' 실행하게 막습니다.
if "icon_fixed" not in st.session_state:
    st.markdown(
        f"""
        <head>
            <link rel="manifest" href="{MANIFEST_URL}">
            <link rel="apple-touch-icon" href="{ICON_URL}">
            <link rel="shortcut icon" href="{ICON_URL}">
        </head>
        """,
        unsafe_allow_html=True
    )
    st.session_state.icon_fixed = True  # "나 이제 설정 했어!" 하고 깃발 꽂기

# --------------------------------------------------------------------------
# [2] 네비게이션 로직 (기억 유지)
# --------------------------------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "홈"

# 페이지 변경 함수 (콜백)
def change_page(page_name):
    st.session_state.page = page_name

# --------------------------------------------------------------------------
# [3] 스타일 및 데이터 로딩
# --------------------------------------------------------------------------
styles.apply_custom_css()
all_sheets = load_excel()

# --------------------------------------------------------------------------
# [4] 화면 구성 함수들
# --------------------------------------------------------------------------
def render_home_logo():
    logo_path = None
    if os.path.exists("app_icon.png"): logo_path = "app_icon.png"
    elif os.path.exists("home_logo.png"): logo_path = "home_logo.png"
    
    if logo_path:
        with open(logo_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()
        st.markdown(f"""
            <div style="display: flex; justify-content: center; padding-top: 10px; padding-bottom: 5px;">
                <img src="data:image/png;base64,{img_b64}" style="width: 120px; object-fit: contain;">
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<h3 style='text-align:center; color:#003057;'>PM Partners</h3>", unsafe_allow_html=True)

def render_top_navigation():
    menu_options = [
        "홈", "AI상담", "수익계산", "보상플랜", "제품구매",
        "안전성", "액티증상", "호전반응", "체험사례", "성공사례", "자료실"
    ]
    
    st.markdown("""
        <style>
        div[data-testid="column"] { padding: 0 !important; margin: 0 !important; }
        div.stButton > button {
            width: 100%; border-radius: 0px; border: none;
            background-color: transparent; color: #555; font-weight: 600;
            padding: 10px 0; border-bottom: 3px solid transparent;
            transition: all 0.3s;
        }
        div.stButton > button:hover { color: #007bff; background-color: #f8f9fa; }
        div.stButton > button:focus:not(:active) { border-color: transparent; color: #555; }
        @media (max-width: 768px) { div.stButton > button { font-size: 12px; padding: 5px 0; } }
        </style>
    """, unsafe_allow_html=True)

    cols = st.columns(len(menu_options))
    current_page = st.session_state.page

    for i, option in enumerate(menu_options):
        is_active = (current_page == option)
        btn_type = "primary" if is_active else "secondary"
        
        # 버튼 클릭 시 change_page 함수만 조용히 실행 (새로고침 최소화)
        cols[i].button(
            option, 
            key=f"nav_{i}", 
            type=btn_type, 
            use_container_width=True,
            on_click=change_page,
            args=(option,)
        )

# --------------------------------------------------------------------------
# [5] 팝업창 설정
# --------------------------------------------------------------------------
EVENT_IMAGE_URL = "https://raw.githubusercontent.com/baejongwan/pm-ai/main/event_01.jpg"

@st.dialog("🎉 7주년 액티바이즈 프로모션", width="large")
def show_promo_window():
    st.image(EVENT_IMAGE_URL)
    st.caption("💡 창 밖의 어두운 부분을 클릭하거나, 오른쪽 위 X를 누르면 닫힙니다.")
    if st.button("닫기", type="primary", use_container_width=True):
        st.rerun()

# 팝업 로직 (홈 화면 진입 시 1회만)
if "home_popup_shown" not in st.session_state:
    if st.session_state.page == "홈":
        show_promo_window()
        st.session_state.home_popup_shown = True

# --------------------------------------------------------------------------
# [6] 화면 렌더링 실행
# --------------------------------------------------------------------------
render_home_logo()      
render_top_navigation()

target_page = st.session_state.page 

# API 키 설정
api_key = GOOGLE_API_KEY
selected_model = "gemini-flash-latest"

# 페이지 연결
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
