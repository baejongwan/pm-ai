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
if os.path.exists("app_icon.png"): icon_path = "app_icon.png"
elif os.path.exists("home_logo.png"): icon_path = "home_logo.png"
elif os.path.exists("PMAILOGO.png"): icon_path = "PMAILOGO.png"
else: icon_path = "💙"

st.set_page_config(
    page_title="PM 파트너스 허브", 
    page_icon=icon_path, 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------------------------------
# [2] 네비게이션 로직 (URL 기준 - 뒤로 가기 해결)
# --------------------------------------------------------------------------
current_url_page = st.query_params.get("page", "홈")

if "page" not in st.session_state:
    st.session_state.page = current_url_page

# --------------------------------------------------------------------------
# [3] 스타일 및 데이터 로딩
# --------------------------------------------------------------------------
styles.apply_custom_css()
all_sheets = load_excel()

# --------------------------------------------------------------------------
# [4] 화면 구성 함수들
# --------------------------------------------------------------------------
def render_home_logo():
    if current_url_page == "홈":
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
    html_nav = '<div class="nav-container">'
    for option in menu_options:
        active_class = "active" if option == current_url_page else ""
        html_nav += f'<a href="?page={option}" target="_self" class="nav-link {active_class}">{option}</a>'
    html_nav += '</div>'
    st.markdown(html_nav, unsafe_allow_html=True)

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
        
# [1] 팝업용 도구 가져오기
import streamlit.components.v1 as components
import streamlit as st # st가 없을 경우를 대비해 import

# [2] 7주년 행사 포스터 주소 (이미지 확인 완료됨)
EVENT_IMAGE_URL = "https://raw.githubusercontent.com/baejongwan/pm-ai/main/event_01.jpg"

# [3] 팝업 HTML 코드 직접 작성 (utils.py 의존 X)
def show_popup_directly():
    # 팝업 디자인 및 기능 (높이 문제 해결됨)
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        /* 팝업 배경 */
        .popup-overlay {{
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background-color: rgba(0, 0, 0, 0.5);
            z-index: 999999; /* 제일 위에 뜨도록 */
            display: flex; justify-content: center; align-items: center;
        }}
        /* 팝업 내용 박스 */
        .popup-content {{
            background: white; padding: 0; border-radius: 10px;
            box-shadow: 0 0 15px rgba(0,0,0,0.3);
            text-align: center; width: 350px; max-width: 90%;
            overflow: hidden;
        }}
        .popup-img {{ width: 100%; display: block; }}
        .btn-area {{ padding: 10px; background: #f1f1f1; display: flex; justify-content: space-between; }}
        button {{ border: none; background: none; cursor: pointer; font-size: 14px; }}
    </style>
    </head>
    <body>
    
    <div id="myPopup" class="popup-overlay">
        <div class="popup-content">
            <img src="{EVENT_IMAGE_URL}" class="popup-img">
            <div class="btn-area">
                <button onclick="closeToday()" style="color:#666; font-weight:bold;">🚫 오늘만 닫기</button>
                <button onclick="closePopup()">❌ 닫기</button>
            </div>
        </div>
    </div>

    <script>
        // 1. 날짜 체크
        const todayStr = new Date().toISOString().slice(0, 10); // YYYY-MM-DD
        const hiddenDate = localStorage.getItem("pm_popup_hide_date");

        if (hiddenDate === todayStr) {{
            // 오늘 안보기로 했으면 숨김 (Javascript로 숨김)
            document.getElementById("myPopup").style.display = "none";
            // 중요: 부모창(Streamlit)의 iframe 높이도 줄여줌
            toggleFrame(false);
        }} else {{
            // 보여줘야 하면 높이 확보
            toggleFrame(true);
        }}

        // 2. 닫기 버튼
        function closePopup() {{
            document.getElementById("myPopup").style.display = "none";
            toggleFrame(false);
        }}

        // 3. 오늘 하루 닫기
        function closeToday() {{
            localStorage.setItem("pm_popup_hide_date", todayStr);
            document.getElementById("myPopup").style.display = "none";
            toggleFrame(false);
        }}

        // 4. Streamlit iframe 높이 조절 트릭
        function toggleFrame(show) {{
            // 팝업이 닫힐 때 iframe 높이를 줄여서 화면을 가리지 않게 함
            try {{
                const frame = window.frameElement;
                if (frame) {{
                    frame.style.height = show ? '100vh' : '0px'; 
                    // 100vh = 화면 전체 높이
                }}
            }} catch(e) {{ console.log(e); }}
        }}
    </script>
    </body>
    </html>
    """
    
    # [핵심] 높이를 1000 이상 줘서 일단 화면에 공간을 확보합니다.
    # (자바스크립트가 로딩되면서 닫히거나 조절됩니다)
    components.html(html_code, height=1000)

# [4] 실행 (무조건 실행)
show_popup_directly()

# [5] 나머지 화면 렌더링
render_home_logo()      
render_top_navigation()
# --------------------------------------------------------------------------
# [6] 페이지 내용 표시
# --------------------------------------------------------------------------
target_page = current_url_page

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










