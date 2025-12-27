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
# [2] 네비게이션 로직 (기억 유지 + 새로고침 방지)
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
    
    # [★디자인 수정의 핵심★] 겹침 방지 + 자연스러운 줄바꿈 + 중앙 정렬
    st.markdown("""
        <style>
        /* 1. 메뉴 컨테이너: 가로 배치, 줄바꿈 허용, 가운데 정렬 */
        div[data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: wrap !important;      /* 공간 부족하면 다음 줄로 넘어감 */
            justify-content: center !important; /* 버튼들 가운데 모으기 */
            gap: 8px !important;             /* 버튼 사이 간격 */
            padding-bottom: 10px !important;
        }

        /* 2. 기둥(Column): 글자 겹침 방지 및 크기 자동 조절 */
        div[data-testid="column"] {
            flex: 0 0 auto !important;          /* 크기 고정 안함 (내용물에 맞춤) */
            width: auto !important;             /* 가로 100% 금지 */
            min-width: max-content !important;  /* ★핵심★ 글자 크기만큼은 무조건 자리 확보 (겹침 방지) */
        }
        
        /* 3. 버튼 디자인: 알약 모양 */
        div.stButton > button {
            width: auto !important;
            height: auto !important;
            padding: 6px 15px !important;
            border-radius: 50px !important;     /* 둥근 알약 */
            border: 1px solid #ddd;
            background-color: white;
            color: #555;
            font-size: 14px !important;
            font-weight: 600;
            margin: 0 !important;
            white-space: nowrap !important;     /* 버튼 내 줄바꿈 금지 */
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }

        /* 4. 마우스 호버 효과 */
        div.stButton > button:hover {
            border-color: #007bff;
            color: #007bff;
            background-color: #f0f8ff;
        }
        
        /* 5. 클릭 시 강조 */
        div.stButton > button:focus:not(:active) {
            border-color: #007bff;
            color: #007bff;
            background-color: #e7f1ff;
        }
        
        /* 6. 모바일 화면 최적화 */
        @media (max-width: 640px) {
            /* 모바일에서도 강제로 중앙 정렬 유지 */
            div[data-testid="stHorizontalBlock"] {
                justify-content: center !important;
                gap: 6px !important;
            }
            div.stButton > button {
                padding: 5px 12px !important;
                font-size: 13px !important;
            }
        }
        </style>
    """, unsafe_allow_html=True)

    # 컬럼 생성 및 버튼 배치
    cols = st.columns(len(menu_options))
    current_page = st.session_state.page

    for i, option in enumerate(menu_options):
        is_active = (current_page == option)
        btn_type = "primary" if is_active else "secondary"
        
        # 버튼 기능 연결 (새로고침 방지)
        cols[i].button(
            option, 
            key=f"nav_{i}", 
            type=btn_type, 
            on_click=change_page, 
            args=(option,)
        )

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
