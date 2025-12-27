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
# (수정사항: 매번 실행되어 깜빡이는 것을 방지하기 위해 한 번만 실행되도록 설정)
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
# [2] 네비게이션 로직 (수정사항: URL 방식 제거 -> 내부 기억 장치 사용)
# --------------------------------------------------------------------------
# URL(?page=...)을 쓰면 새로고침이 되므로, session_state로 페이지를 기억합니다.
if "page" not in st.session_state:
    st.session_state.page = "홈"

# 페이지 변경 함수 (새로고침 없이 화면만 바꿈)
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
    # 로고는 현재 페이지가 '홈'일 때만 나오거나, 항상 나오거나 설정 가능
    # (기존 로직 유지하되 session_state 기준)
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
    
    # [디자인 수정] 버튼을 기존 메뉴바처럼 보이게 하는 CSS
    # 알약 모양이나 세로 리스트가 되지 않도록, 최대한 깔끔한 가로형 버튼으로 스타일링
    st.markdown("""
        <style>
        /* 버튼 간격 조절 */
        div[data-testid="column"] { padding: 0 !important; margin: 0 !important; min-width: 0px !important;}
        
        /* 버튼 스타일 평면화 (링크처럼 보이게) */
        div.stButton > button {
            width: 100%;
            border: none;
            border-radius: 0px;
            background-color: transparent;
            color: #555;
            font-size: 14px;
            font-weight: 600;
            padding: 10px 0;
            margin: 0;
            border-bottom: 3px solid transparent;
            transition: all 0.2s;
        }
        
        /* 마우스 올렸을 때 */
        div.stButton > button:hover {
            color: #007bff;
            background-color: #f8f9fa;
        }

        /* 모바일 화면 대응 (글자 크기 자동 조절) */
        @media (max-width: 768px) {
            div.stButton > button { 
                font-size: 11px; 
                padding: 5px 0; 
            }
        }
        </style>
    """, unsafe_allow_html=True)

    # 메뉴 개수만큼 컬럼 생성 (가로 배열 유지)
    cols = st.columns(len(menu_options))
    current_page = st.session_state.page

    for i, option in enumerate(menu_options):
        # 현재 선택된 메뉴인지 확인
        is_active = (current_page == option)
        btn_type = "primary" if is_active else "secondary"
        
        # [핵심] a 태그(링크) 대신 button(버튼) 사용 -> 새로고침 방지!
        cols[i].button(
            option, 
            key=f"nav_{i}", 
            type=btn_type, 
            use_container_width=True,
            on_click=change_page, # 클릭 시 페이지 변경 함수 실행
            args=(option,)
        )

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
@st.dialog("🎉 7주년 액티바이즈 프로모션", width="large")
def show_promo_window():
    st.image(EVENT_IMAGE_URL)
    st.caption("💡 창 밖의 어두운 부분을 클릭하거나, 오른쪽 위 X를 누르면 닫힙니다.")
    if st.button("닫기", type="primary", use_container_width=True):
        st.rerun()

# [3] 팝업 실행 로직 (접속 시 한 번만 뜨도록 설정)
if "home_popup_shown" not in st.session_state:
    if st.session_state.page == "홈":
        show_promo_window()
        st.session_state["home_popup_shown"] = True

# [4] 나머지 화면 렌더링
render_home_logo()      
render_top_navigation()

# --------------------------------------------------------------------------
# [6] 페이지 내용 표시
# --------------------------------------------------------------------------
# URL 파라미터가 아닌 session_state의 페이지를 바라봅니다.
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
