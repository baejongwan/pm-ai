# view_stories.py (체험사례 및 성공사례)
import streamlit as st
from utils import get_optimized_image

def render_experience(all_sheets):
    st.markdown("## 💬 생생한 제품 체험 사례")
    target_sheet = all_sheets.get('체험사례') if all_sheets else None
    if target_sheet is not None:
        df = target_sheet.fillna("")
        categories = ["전체"] + list(df['카테고리'].unique()) if '카테고리' in df.columns else ["전체"]
        selected_cat = st.selectbox("증상별/제품별 모아보기", categories)
        if selected_cat != "전체": df = df[df['카테고리'] == selected_cat]

        for _, row in df.iterrows():
            with st.container():
                st.markdown(f"""
                <div style="border:1px solid #e0e0e0; border-radius:10px; padding:20px; margin-bottom:20px; background-color:white;">
                    <div style="color:#2E7D32; font-weight:bold; font-size:14px; margin-bottom:5px;">[{row.get('카테고리','-')}] {row.get('질병/증상','-')}</div>
                    <h3 style="margin-top:0;">{row.get('제목','-')}</h3>
                    <div style="color:#666; font-size:14px; margin-bottom:15px;">👤 {row.get('국가/나이/성별','-')} | 💊 {row.get('섭취제품','-')}</div>
                    <div style="background-color:#f9f9f9; padding:15px; border-radius:5px; margin-bottom:15px;">{row.get('내용/후기','-')}</div>
                </div>""", unsafe_allow_html=True)
                if row.get('유튜브') and str(row['유튜브']).startswith('http'): st.video(str(row['유튜브']))
    else: st.info("체험 사례 데이터가 없습니다.")

def render_success(all_sheets):
    st.markdown("## 🏆 명예의 전당 (성공 스토리)")
    target_sheet = all_sheets.get('성공사례') if all_sheets else None
    if target_sheet is not None:
        df = target_sheet.fillna("")
        for _, row in df.iterrows():
            with st.expander(f"👑 {row.get('이름')} {row.get('직급')} ({row.get('전직업')})", expanded=True):
                c1, c2 = st.columns(2)
                with c1: st.write(f"**⏱ 달성:** {row.get('달성기간')}"); st.write(f"**💼 전직업:** {row.get('전직업')}")
                with c2: st.write(f"**🚀 동기:** {row.get('시작동기')}")
                st.write("---"); st.write(f"**😥 애로사항:**\n{row.get('애로사항')}"); st.write(f"**💡 노하우:**\n{row.get('극복노하우')}")
                if row.get('유튜브') and str(row['유튜브']).startswith('http'): st.video(str(row['유튜브']))
    else: st.info("성공 사례 데이터가 없습니다.")
