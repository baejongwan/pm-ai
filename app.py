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

# 아이콘 깜빡임 방지 (최초 1회만 설정)
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
# [2] 네비게이션 로직 (버튼 방식 -> 세션 유지 필수!)
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
    
    # [★ 디자인 해결의 핵심 CSS ★]
    # 이 CSS는 Streamlit이 모바일에서 세로로 강제 정렬하는 것을 '무력화'시킵니다.
    # flex-direction: row !important; 명령어가 핵심입니다.
    st.markdown("""
        <style>
        /* 1. 메뉴 컨테이너: 무조건 가로 배치 + 줄바꿈 허용 + 중앙 정렬 */
        div[data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-direction: row !important; /* 모바일에서도 가로 유지 */
            flex-wrap: wrap !important;     /* 공간 없으면 다음 줄로 */
            align-items: center !important;
            justify-content: center !important;
            gap: 6px !important;            /* 버튼 사이 간격 */
            padding-bottom: 10px !important;
        }

        /* 2. 개별 버튼 기둥: 100% 폭 차지 금지, 내용물 크기만큼만! */
        div[data-testid="column"] {
            flex: 0 1 auto !important;  
            width: auto !important;
            min-width: auto !important; 
        }

        /* 3. 모바일(좁은 화면) 강제 적용 사항 - 여기가 제일 중요합니다 */
        @media (max-width: 640px) {
            div[data-testid="stHorizontalBlock"] {
                flex-direction: row !important; /* 세로 정렬 절대 금지 */
                display: flex !important;
                flex-wrap: wrap !important;
            }
            div[data-testid="column"] {
                width: auto !important;
                min-width: auto !important;
                flex: 0 1 auto !important;
            }
        }

        /* 4. 버튼 디자인 (HTML 메뉴와 똑같은 알약 모양) */
        div.stButton > button {
            width: auto !important;
            height: auto !important;
            padding: 6px 14px !important;
            border-radius: 50px !important;
            border: 1px solid #ddd;
            background-color: white;
            color: #555;
            font-size: 14px !important;
            font-weight: 600;
            margin: 0 !important;
            white-space: nowrap !important; /* 글자 줄바꿈 금지 */
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }

        /* 5. 마우스 호버 효과 */
        div.stButton > button:hover {
            border-color: #007bff;
            color: #007bff;
            background-color: #f0f8ff;
        }

        /* 6. 선택된 버튼 강조 */
        div.stButton > button:focus:not(:active) {
            border-color: #007bff;
            color: #007bff;
            background-color: #e7f1ff;
        }
        
        /* 7. 아주 작은 폰트 대응 */
        @media (max-width: 400px) {
            div.stButton > button {
                padding: 4px 10px !important;
                font-size: 12px !important;
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
        
        # [핵심] st.button 사용 -> 새로고침 없음 -> 세션 유지됨 -> 상담/방문자수 보호
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
        pass

# 팝업 로직 (세션 유지되므로 홈 버튼 눌러도 다시 안 뜸)
EVENT_IMAGE_URL = "https://raw.githubusercontent.com/baejongwan/pm-ai/main/event_01.jpg"

@st.dialog("🎉 7주년 액티바이즈 프로모션", width="large")
def show_promo_window():
    st.image(EVENT_IMAGE_URL)
    st.caption("💡 창 밖의 어두운 부분을 클릭하거나, 오른쪽 위 X를 누르면 닫힙니다.")
    if st.button("닫기", type="primary", use_container_width=True):
        st.rerun()

if "home_popup_shown" not in st.session_state:
    if st.session_state.page == "홈":
        show_promo_window()
        st.session_state["home_popup_shown"] = True

# 화면 그리기
render_home_logo()      
render_top_navigation()

# --------------------------------------------------------------------------
# [6] 페이지 연결 (세션 state 기준)
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
