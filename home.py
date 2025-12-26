# app.py
import streamlit as st
import random
import os
import warnings

warnings.filterwarnings("ignore")

try:
    import google.generativeai as genai
except ImportError:
    genai = None

from config import *
from styles import apply_custom_css
from utils import load_excel
import tabs

if os.path.exists(LOGO_FILE_PATH):
    icon_setting = LOGO_FILE_PATH
else:
    icon_setting = "💙"

st.set_page_config(
    page_title="PM 파트너스 허브", 
    page_icon=icon_setting,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 1. 초기 상태 설정 ('홈 화면'이 기본)
if 'page' not in st.session_state:
    st.session_state.page = "🏠 홈 화면"

apply_custom_css()
all_sheets = load_excel()

if all_sheets is None:
    st.error(f"🚨 '{EXCEL_FILE_PATH}' 파일을 찾을 수 없습니다.")
    st.stop()

# ---------------------------------------------------------
# [상단 헤더 영역]
# ---------------------------------------------------------
def render_header():
    if "random_sponsor" not in st.session_state:
        st.session_state.random_sponsor = random.choice(FAMILY_IDS)
    sponsor = st.session_state.random_sponsor
    
    # [수정] '홈 화면' 메뉴 부활
    menu_options = [
        "🏠 홈 화면", "🤖 AI 비서", "📦 FitLine 제품", "🛡️ 제품 안전성", 
        "🔥 액티바이즈 진단", "💡 호전반응", "💰 보상플랜", 
        "💬 제품체험사례", "🏆 사업성공사례"
    ]
    
    try:
        current_index = menu_options.index(st.session_state.page)
    except ValueError:
        current_index = 0

    col_left, col_right = st.columns([3, 7])

    with col_left:
        c1, c2 = st.columns([1, 2.2]) 
        with c1:
            if os.path.exists(LOGO_FILE_PATH):
                st.image(LOGO_FILE_PATH, width=80)
            else:
                st.write("PM Logo")
        with c2:
            st.markdown(f"""
                <div class="sponsor-top">
                    <div class="sponsor-label">✨ 추천인 (꾹 눌러서 복사)</div>
                    <div class="sponsor-name">{sponsor['name']}</div>
                </div>
            """, unsafe_allow_html=True)
            st.text_input("hidden_label", value=sponsor['id'], key="sponsor_id_input", label_visibility="collapsed")
            st.markdown("""
                <div class="sponsor-bottom">
                    <a href="https://www.pmi-korea.com/member/join/step01.do" target="_blank" class="join-btn">
                        회원가입 이동 🚀
                    </a>
                </div>
            """, unsafe_allow_html=True)

    with col_right:
        st.write("") 
        selected_menu = st.radio(
            "메뉴", 
            menu_options, 
            index=current_index, 
            horizontal=True, 
            label_visibility="collapsed", 
            key="header_menu"
        )

    if selected_menu != st.session_state.page:
        st.session_state.page = selected_menu
        st.rerun()

    st.markdown("---")

render_header()

# AI 설정
api_key = GOOGLE_API_KEY
selected_model = "gemini-pro"
if api_key and genai:
    try:
        genai.configure(api_key=api_key)
        all_models = list(genai.list_models())
        valid_models = [m.name for m in all_models if 'generateContent' in m.supported_generation_methods]
        if valid_models:
            if "models/gemini-1.5-flash" in valid_models: selected_model = "models/gemini-1.5-flash"
            elif "models/gemini-1.5-pro" in valid_models: selected_model = "models/gemini-1.5-pro"
            else: selected_model = valid_models[0]
    except: pass

# ---------------------------------------------------------
# 화면 라우팅
# ---------------------------------------------------------
if st.session_state.page == "🏠 홈 화면":
    # [NEW] 소꼴 디자인을 적용한 메인 대시보드 함수 호출
    tabs.render_home_dashboard(all_sheets)

elif st.session_state.page == "🤖 AI 비서":
    tabs.render_ai_assistant(api_key, selected_model, all_sheets)

elif st.session_state.page == "📦 FitLine 제품":
    tabs.render_products(all_sheets)

elif st.session_state.page == "🛡️ 제품 안전성":
    tabs.render_safety(all_sheets)

elif st.session_state.page == "🔥 액티바이즈 진단":
    tabs.render_diagnosis(all_sheets)

elif st.session_state.page == "💡 호전반응":
    tabs.render_guide(all_sheets)

elif st.session_state.page == "💰 보상플랜":
    tabs.render_compensation(all_sheets)

elif st.session_state.page == "💬 제품체험사례":
    tabs.render_experience(all_sheets)

elif st.session_state.page == "🏆 사업성공사례":
    tabs.render_success(all_sheets)