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
        
# [1] 7주년 행사 포스터 주소
EVENT_IMAGE_URL = "https://raw.githubusercontent.com/baejongwan/pm-ai/main/event_01.jpg"

# [2] 팝업창 코드 (줄바꿈 오류 해결됨)
import streamlit as st

# 아래 코드는 절대 줄바꿈을 임의로 넣지 마세요! (한 줄로 이어져야 작동합니다)
popup_code = f"""
<style>
    /* 팝업 스타일 (CSS) - 파이썬 f-string 때문에 중괄호를 두 번 {{ }} 씁니다 */
    #pm-popup-overlay {{
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background-color: rgba(0, 0, 0, 0.6);
        z-index: 999999;
        display: flex; justify-content: center; align-items: center;
        backdrop-filter: blur(3px);
    }}
    #pm-popup-content {{
        background: white; padding: 0; border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        width: 400px; max-width: 90%;
        text-align: center; overflow: hidden; position: relative;
        animation: popupFadeIn 0.3s ease-out;
    }}
    .popup-img {{ width: 100%; height: auto; display: block; }}
    .popup-btn-area {{
        display: flex; justify-content: space-between; padding: 12px 20px;
        background-color: #f8f9fa; border-top: 1px solid #eee;
    }}
    .btn-today {{ background: none; border: none; color: #555; font-size: 13px; cursor: pointer; font-weight: 600; }}
    .btn-close {{ background: #333; color: white; border: none; padding: 5px 15px; border-radius: 5px; font-size: 13px; cursor: pointer; }}
    @keyframes popupFadeIn {{ from {{ opacity: 0; transform: translateY(-20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
</style>

<div id="pm-popup-overlay">
    <div id="pm-popup-content">
        <img src="{EVENT_IMAGE_URL}" class="popup-img">
        <div class="popup-btn-area">
            <button class="btn-today" onclick="var t=new Date().toISOString().slice(0,10); localStorage.setItem('pm_popup_v4', t); document.getElementById('pm-popup-overlay').style.display='none';">🚫 오늘 하루 보지 않기</button>
            <button class="btn-close" onclick="document.getElementById('pm-popup-overlay').style.display='none';">닫기</button>
        </div>
    </div>
</div>

<script>
    /* 페이지 로딩 시 체크 */
    var t = new Date().toISOString().slice(0, 10);
    if (localStorage.getItem("pm_popup_v4") === t) {{
        document.getElementById("pm-popup-overlay").style.display = "none";
    }}
</script>
"""

st.markdown(popup_code, unsafe_allow_html=True)

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













