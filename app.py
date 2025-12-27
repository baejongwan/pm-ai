import streamlit as st
import os
import warnings
import base64
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
from utils import load_excel

# [진짜 수정 완료] 이제 두 줄로 확실히 나눴습니다.
from config 
import * warnings.filterwarnings("ignore")

# --------------------------------------------------------------------------
# [1] 기본 페이지 및 세션 설정
# --------------------------------------------------------------------------
ICON_URL = "https://raw.githubusercontent.com/baejongwan/pm-ai/main/app_icon.png"
MANIFEST_URL = "https://raw.githubusercontent.com/baejongwan/pm-ai/main/manifest.json"

st.set_page_config(
    page_title="PM 파트너스 허브", 
    page_icon=ICON_URL, 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 세션 초기화 (가장 먼저 실행)
if "page" not in st.session_state:
    st.session_state.page = "홈"

# 아이콘 및 메타태그
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
# [2] 스타일 및 데이터 로딩
# --------------------------------------------------------------------------
styles.apply_custom_css()
all_sheets = load_excel()

# --------------------------------------------------------------------------
# [3] 화면 구성 함수들
# --------------------------------------------------------------------------
def render_home_logo():
    if st.session_state.get("page", "홈") == "홈":
        logo_path = None
        if os.path.exists("home_logo.png"): logo_path = "home_logo.png"
        elif os.path.exists("PMAILOGO.png"): logo_path = "PMAILOGO.png"
        
        if logo_path:
            with open(logo_path, "rb") as f:
                img_b64 = base64.b64encode(f.read()).decode()
            st.markdown(f"""
                <div style="display: flex; justify-content: center; padding-top: 10px; padding-bottom: 0px;">
                    <img src="data:image/png;base64,{img_b64}" style="width: 120px; object-fit: contain;">
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <h3 style='text-align:center; color:#003057; margin-top:10px; margin-bottom:5px;'>
                    PM Partners
                </h3>
            """, unsafe_allow_html=True)

# --------------------------------------------------------------------------
# [4] 상단 고정형 메뉴바 (인덱스 자동 추적)
# --------------------------------------------------------------------------
def render_top_navigation():
    menu_options = [
        "홈", "AI상담", "수익계산", "보상플랜", "제품구매",
        "안전성", "액티증상", "호전반응", "체험사례", "성공사례", "자료실"
    ]
    
    menu_icons = ["house", "robot", "calculator", "diagram-3", "cart", 
                  "shield-check", "activity", "heart-pulse", "people", "trophy", "file-earmark-pdf"]

    current_page = st.session_state.get("page", "홈")
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
            "icon": {"color": "#666", "font-size": "14px"}, 
            "nav-link": {
                "font-size": "14px", 
                "text-align": "center", 
                "margin": "0px", 
                "color": "#444",
                "white-space": "nowrap",
            },
            "nav-link-selected": {"background-color": "#007bff", "color": "white"},
        }
    )
    return selected

# --------------------------------------------------------------------------
# [5] 팝업창 및 AI 설정
# --------------------------------------------------------------------------
api_key = GOOGLE_API_KEY
selected_model = "gemini-2.5-flash" # [확인] 최신 모델 적용됨

if api_key:
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
    except Exception as e:
        pass

EVENT_IMAGE_URL = "https://raw.githubusercontent.com/baejongwan/pm-ai/main/event_01.jpg"

@st.dialog("🎉 7주년 액티바이즈 프로모션", width="large")
def show_promo_window():
    st.image(EVENT_IMAGE_URL)
    st.caption("💡 창 밖의 어두운 부분을 클릭하거나, 오른쪽 위 X를 누르면 닫힙니다.")
    if st.button("닫기", type="primary", use_container_width=True):
        st.rerun()

# --------------------------------------------------------------------------
# [6] 화면 렌더링 및 페이지 연결
# --------------------------------------------------------------------------

render_home_logo()
selected_page = render_top_navigation()

if selected_page != st.session_state.page:
    st.session_state.page = selected_page
    st.rerun()

if "home_popup_shown" not in st.session_state:
    if st.session_state.page == "홈":
        show_promo_window()
        st.session_state["home_popup_shown"] = True

target_page = st.session_state.page

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


