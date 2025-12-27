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
ICON_URL = "https://raw.githubusercontent.com/baejongwan/pm-ai/main/app_icon.png"
MANIFEST_URL = "https://raw.githubusercontent.com/baejongwan/pm-ai/main/manifest.json"

st.set_page_config(
    page_title="PM 파트너스 허브", 
    page_icon=ICON_URL, 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# [핵심] 아이콘 깜빡임/새로고침 방지 (최초 1회만 실행)
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
# [2] 네비게이션 로직 (내부 기억 장치 사용)
# --------------------------------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "홈"

# 페이지 변경 함수
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
    # 홈 화면일 때만 로고 표시 (선택 사항)
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
    
    # [디자인 해결] 세로 정렬 방지 + 알약 모양 CSS
    st.markdown("""
        <style>
        /* 1. 기둥(Column) 강제 가로 정렬 */
        div[data-testid="column"] {
            padding: 0 !important;
            margin: 0 !important;
            min-width: 0px !important; /* 이게 없으면 좁은 화면에서 세로로 바뀜 */
        }
        
        /* 2. 버튼 스타일 (알약 모양) */
        div.stButton > button {
            width: 100%;
            border-radius: 50px;       /* 둥근 알약 모양 */
            border: 1px solid #eee;
            background-color: white;
            color: #555;
            font-size: 13px;           /* 글자 크기 조정 */
            font-weight: 600;
            padding: 6px 0;
            margin: 2px 0;
            white-space: nowrap;       /* 글자 줄바꿈 방지 */
            transition: all 0.2s;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        /* 3. 마우스 올렸을 때 */
        div.stButton > button:hover {
            background-color: #f0f8ff;
            color: #007bff;
            border-color: #007bff;
            transform: translateY(-1px);
        }
        
        /* 4. 클릭 효과 */
        div.stButton > button:active {
            transform: translateY(0);
        }

        /* 5. 모바일 화면 미세 조정 */
        @media (max-width: 768px) {
            div.stButton > button { 
                font-size: 10px; 
                padding: 4px 0; 
            }
        }
        </style>
    """, unsafe_allow_html=True)

    # 11개 메뉴를 위한 좁은 간격의 기둥 생성
    cols = st.columns(len(menu_options), gap="small")
    current_page = st.session_state.page

    for i, option in enumerate(menu_options):
        is_active = (current_page == option)
        
        # 활성화된 버튼 시각적 강조 (Primary)
        btn_type = "primary" if is_active else "secondary"
        
        # [기능 해결] button + on_click 사용 (새로고침 방지)
        cols[i].button(
            option, 
            key=f"nav_{i}", 
            type=btn_type, 
            use_container_width=True,
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

# [3] 팝업 실행 로직 (접속 시 한 번만)
if "home_popup_shown" not in st.session_state:
    if st.session_state.page == "홈":
        show_promo_window()
        st.session_state["home_popup_shown"] = True

# [4] 화면 렌더링
render_home_logo()      
render_top_navigation()

# --------------------------------------------------------------------------
# [6] 페이지 내용 표시 (기억된 페이지 보여주기)
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
