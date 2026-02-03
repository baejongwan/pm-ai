# view_stories.py (체험사례 및 성공사례)
import streamlit as st
from utils import get_optimized_image
from config import LANG_CONFIG

# 1. 제품 체험 사례
def render_experience(all_sheets):
    lang_code = st.session_state.get("selected_lang", "KR")
    ui = LANG_CONFIG[lang_code]["ui"]
    
    st.markdown(f"## 💬 {ui['story_title']}")
    
    # 데이터 가져오기
    target_sheet = all_sheets.get('체험사례') if all_sheets else None
    
    if target_sheet is not None:
        # [수정] target_sheet를 df라는 변수로 정의 (오류 해결 핵심)
        df = target_sheet.fillna("")
        
        # 카테고리 목록 생성 ("All" 추가)
        categories = ["All"] + list(df['카테고리'].unique()) if '카테고리' in df.columns else ["All"]
        
        # 선택박스 (작은 글씨 다국어화)
        selected_cat = st.selectbox(ui['story_sub'], categories)
        
        # 필터링 로직 (All이 아닐 경우에만 필터링)
        if selected_cat != "All":
            df = df[df['카테고리'] == selected_cat]

        # 사례 리스트 출력
        for _, row in df.iterrows():
            with st.container():
                st.markdown(f"""
                <div style="border:1px solid #e0e0e0; border-radius:10px; padding:20px; margin-bottom:20px; background-color:white;">
                    <div style="color:#2E7D32; font-weight:bold; font-size:14px; margin-bottom:5px;">[{row.get('카테고리','-')}] {row.get('질병/증상','-')}</div>
                    <h3 style="margin-top:0;">{row.get('제목','-')}</h3>
                    <div style="color:#666; font-size:14px; margin-bottom:15px;">👤 {row.get('국가/나이/성별','-')} | 💊 {row.get('섭취제품','-')}</div>
                    <div style="background-color:#f9f9f9; padding:15px; border-radius:5px; margin-bottom:15px;">{row.get('내용/후기','-')}</div>
                </div>""", unsafe_allow_html=True)
                
                # 유튜브 영상이 있는 경우 출력
                v_url = row.get('유튜브')
                if v_url and str(v_url).startswith('http'):
                    st.video(str(v_url))
    else:
        # 데이터 없을 때 다국어 안내
        no_data_msg = "체험 사례 데이터가 없습니다." if lang_code == "KR" else "No experience stories found."
        st.info(no_data_msg)

# 2. 명예의 전당 (성공 사례)
def render_success(all_sheets):
    lang_code = st.session_state.get("selected_lang", "KR")
    ui = LANG_CONFIG[lang_code]["ui"]
    
    st.markdown(f"## 🏆 {ui['success_title']}")
    st.caption(ui['success_sub'])
    
    target_sheet = all_sheets.get('성공사례') if all_sheets else None
    
    if target_sheet is not None:
        df = target_sheet.fillna("")
        
        # 레이블 다국어화
        label_period = "달성 기간" if lang_code == "KR" else "Period"
        label_job = "전직업" if lang_code == "KR" else "Former Job"
        label_motive = "동기" if lang_code == "KR" else "Motive"
        label_difficulty = "애로사항" if lang_code == "KR" else "Challenges"
        label_knowhow = "노하우" if lang_code == "KR" else "Know-how"

        for _, row in df.iterrows():
            with st.expander(f"👑 {row.get('이름')} {row.get('직급')} ({row.get('전직업')})", expanded=True):
                c1, c2 = st.columns(2)
                with c1:
                    st.write(f"**⏱ {label_period}:** {row.get('달성기간')}")
                    st.write(f"**💼 {label_job}:** {row.get('전직업')}")
                with c2:
                    st.write(f"**🚀 {label_motive}:** {row.get('시작동기')}")
                
                st.write("---")
                st.write(f"**😥 {label_difficulty}:**\n{row.get('애로사항')}")
                st.write(f"**💡 {label_knowhow}:**\n{row.get('극복노하우')}")
                
                v_url = row.get('유튜브')
                if v_url and str(v_url).startswith('http'):
                    st.video(str(v_url))
    else:
        no_data_msg = "성공 사례 데이터가 없습니다." if lang_code == "KR" else "No success stories found."
        st.info(no_data_msg)