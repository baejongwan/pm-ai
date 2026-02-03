import streamlit as st
import os
import warnings
import base64
from datetime import datetime 
from streamlit_option_menu import option_menu 

# --- 파일 임포트 ---
import styles
import view_home
import view_ai
import view_products
import view_pdf
import view_guide
import view_compensation
import view_stories
import view_videos
from utils import load_excel

# [설정] 경고 무시 및 설정 파일 로드
from config import *
warnings.filterwarnings("ignore")
from config import LANG_CONFIG

# --------------------------------------------------------------------------
# [1] 기본 페이지 및 세션 설정
# --------------------------------------------------------------------------
ICON_URL = "https://raw.githubusercontent.com/baejongwan/pm-ai/main/app_icon.png"
MANIFEST_URL = "https://raw.githubusercontent.com/baejongwan/pm-ai/main/manifest.json"

st.set_page_config(
    page_title="PM AI PARTNER", 
    page_icon=ICON_URL, 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------------------------------
# [핵심 수정] 1단계: 언어 선택 화면 (로고 + Welcome 문구 추가)
# --------------------------------------------------------------------------
if "selected_lang" not in st.session_state:
    st.session_state.selected_lang = None

if st.session_state.selected_lang is None:
    # 1. 로고 출력 (home_logo.png)
    logo_path = "home_logo.png"
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()
        st.markdown(f"""
            <div style="display: flex; justify-content: center; padding-top: 50px;">
                <img src="data:image/png;base64,{img_b64}" style="width: 180px; object-fit: contain;">
            </div>
        """, unsafe_allow_html=True)
    
    # 2. 환영 문구
    st.markdown("<h1 style='text-align:center; color:#003057; margin-top:20px;'>Welcome</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#666;'>Please select your language / 언어를 선택해주세요</p>", unsafe_allow_html=True)
    
    # 3. 언어 선택 버튼
    st.write("")
    lang_cols = st.columns(4)
    for i, (code, info) in enumerate(LANG_CONFIG.items()):
        with lang_cols[i]:
            if st.button(info["name"], key=f"lang_{code}", use_container_width=True):
                st.session_state.selected_lang = code
                st.rerun()
    st.stop()

# --------------------------------------------------------------------------
# [핵심 수정] 2단계: 선택된 언어 데이터 및 다국어 텍스트 로드
# --------------------------------------------------------------------------
lang_code = st.session_state.selected_lang
lang_info = LANG_CONFIG[lang_code]
all_sheets = load_excel(lang_info["file"]) # 언어별 엑셀 파일 로드
menu_options = lang_info["menu"]           # 해당 언어의 메뉴 리스트

# --------------------------------------------------------------------------
# [2] URL 쿼리 파라미터 및 세션 페이지 관리
# --------------------------------------------------------------------------
if "page" in st.query_params:
    st.session_state.page = st.query_params["page"]
    st.query_params.clear()

if "page" not in st.session_state:
    st.session_state.page = menu_options[0]

# 아이콘 및 메타태그
if "head_set" not in st.session_state:
    st.markdown(f"""
        <link rel="manifest" href="{MANIFEST_URL}">
        <link rel="apple-touch-icon" href="{ICON_URL}">
        <meta name="apple-mobile-web-app-capable" content="yes">
    """, unsafe_allow_html=True)
    st.session_state.head_set = True

styles.apply_custom_css()

# --------------------------------------------------------------------------
# [3] 화면 구성 함수 (로고 렌더링)
# --------------------------------------------------------------------------
def render_home_logo():
    if st.session_state.get("page") == menu_options[0]:
        logo_path = "PMAILOGO.png" if os.path.exists("PMAILOGO.png") else "home_logo.png"
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as f:
                img_b64 = base64.b64encode(f.read()).decode()
            st.markdown(f"""
                <div style="display: flex; justify-content: center; padding-top: 10px;">
                    <img src="data:image/png;base64,{img_b64}" style="width: 120px; object-fit: contain;">
                </div>
            """, unsafe_allow_html=True)

# --------------------------------------------------------------------------
# [4] 상단 다국어 메뉴바
# --------------------------------------------------------------------------
def render_top_navigation():
    menu_icons = ["house", "robot", "calculator", "diagram-3", "cart", 
                  "shield-check", "activity", "heart-pulse", "people", "trophy", "collection-play", "file-earmark-pdf"]

    current_page = st.session_state.get("page", menu_options[0])
    try:
        current_index = menu_options.index(current_page)
    except ValueError:
        current_index = 0

    selected = option_menu(
        menu_title=None, 
        options=menu_options,
        icons=menu_icons,
        default_index=current_index, 
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#ffffff", "margin": "0"},
            "nav-link": {"font-size": "13px", "text-align": "center", "color": "#444", "white-space": "nowrap", "padding": "10px 5px"},
            "nav-link-selected": {"background-color": "#007bff", "color": "white"},
        }
    )
    return selected

# --------------------------------------------------------------------------
# [5] 화면 렌더링 및 페이지 라우팅
# --------------------------------------------------------------------------
api_key = GOOGLE_API_KEY
selected_model = "gemini-2.0-flash"

render_home_logo()
selected_page = render_top_navigation()

if selected_page != st.session_state.page:
    st.session_state.page = selected_page
    st.rerun()

# 페이지별 렌더링 (인덱스 기반 매칭으로 다국어 완벽 지원)
target_page = st.session_state.page

if target_page == menu_options[0]: view_home.render_home_dashboard(all_sheets)
elif target_page == menu_options[1]: view_ai.render_ai_assistant(api_key, selected_model, all_sheets)
elif target_page == menu_options[2]: view_compensation.render_calculator_v2()
elif target_page == menu_options[3]: view_compensation.render_compensation(all_sheets)
elif target_page == menu_options[4]: view_products.render_products(all_sheets)
elif target_page == menu_options[5]: view_products.render_safety(all_sheets)
elif target_page == menu_options[6]: view_products.render_diagnosis(all_sheets)
elif target_page == menu_options[7]: view_guide.render_guide(all_sheets)
elif target_page == menu_options[8]: view_stories.render_experience(all_sheets)
elif target_page == menu_options[9]: view_stories.render_success(all_sheets)
elif target_page == menu_options[10]: view_videos.render_video_page(all_sheets)
elif target_page == menu_options[11]: view_pdf.render_pdf_viewer("catalog.pdf")