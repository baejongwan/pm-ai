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

if "icon_fixed" not in st.session_state:
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
    st.session_state.icon_fixed = True

# --------------------------------------------------------------------------
# [2] 네비게이션 로직
# --------------------------------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "홈"

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
    if st.session_state.page == "홈":
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

    # CSS로 라디오를 '가로형 알약 버튼 + 자동 줄바꿈 + 가운데 정렬'로 변환
    st.markdown("""
        <style>
        /* 전체 라디오 그룹을 플렉스 컨테이너로 */
        div[data-testid="stRadio"] div[role="radiogroup"] {
            display: flex !important;
            flex-wrap: wrap !important;         /* 공간 부족하면 줄바꿈 */
            justify-content: center !important; /* 가운데 정렬 */
            gap: 8px !important;                /* 버튼 간격 */
        }
        /* 각 옵션을 pill 버튼처럼 */
        div[data-testid="stRadio"] label {
            display: inline-flex !important;
            align-items: center !important;
            padding: 6px 14px !important;
            border-radius: 50px !important;
            border: 1px solid #ddd !important;
            background-color: #fff !important;
            color: #555 !important;
            font-size: 14px !important;
            font-weight: 600 !important;
            white-space: nowrap !important;
            cursor: pointer !important;
        }
        /* 선택된 옵션 강조 */
        div[data-testid="stRadio"] input:checked + div {
            border-color: #007bff !important;
            color: #007bff !important;
            background-color: #e7f1ff !important;
        }
        /* 호버 효과 */
        div[data-testid="stRadio"] label:hover {
            border-color: #007bff !important;
            color: #007bff !important;
            background-color: #f0f8ff !important;
        }
        /* 기본 라디오 점 숨김 */
        div[data-testid="stRadio"] input {
            display: none !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # 라디오로 현재 페이지 선택
    current = st.radio(
        label="메뉴", 
        options=menu_options,
        index=menu_options.index(st.session_state.page),
        horizontal=False,  # CSS가 가로/랩핑을 처리하므로 False 유지
        key="nav_radio"
    )

    # 세션 상태만 변경 (리로드 없이 상태 유지)
    if current != st.session_state.page:
        change_page(current)


# --------------------------------------------------------------------------
# [5] 실행 설정
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

# [2] 정식 팝업창 기능
@st.dialog("🎉 7주년 액티바이즈 프로모션", width="large")
def show_promo_window():
    st.image(EVENT_IMAGE_URL)
    st.caption("💡 창 밖의 어두운 부분을 클릭하거나, 오른쪽 위 X를 누르면 닫힙니다.")
    if st.button("닫기", type="primary", use_container_width=True):
        st.rerun()

# [3] 팝업 실행 로직
if "home_popup_shown" not in st.session_state:
    if st.session_state.page == "홈":
        show_promo_window()
        st.session_state["home_popup_shown"] = True

# [4] 화면 렌더링
render_home_logo()      
render_top_navigation()

# --------------------------------------------------------------------------
# [6] 페이지 내용 표시
# --------------------------------------------------------------------------
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

