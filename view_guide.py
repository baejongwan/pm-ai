# view_guide.py (호전반응 가이드)
import streamlit as st
from components import apply_custom_styles

def render_guide(all_sheets):
    apply_custom_styles()
    st.markdown("## 💡 호전반응(명현현상) 가이드")
    st.info("몸이 좋아지는 과정에서 나타나는 일시적인 반응입니다.")
    
    target_sheet = all_sheets.get('호전반응') if all_sheets else None
    if target_sheet is not None:
        search_query = st.text_input("🔍 증상을 검색해보세요", "")
        df = target_sheet.fillna("")
        if search_query: df = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
        
        for _, row in df.iterrows():
            with st.expander(f"📌 {row.get('증상', '증상명')}", expanded=False):
                st.write(f"**👀 현상:** {row.get('나타나는현상','-')}")
                st.info(f"**❓ 원인:** {row.get('발생원인','-')}")
                st.success(f"**💡 대처:** {row.get('대처/가이드','-')}")
                if row.get('관련제품') != '-': st.write(f"**💊 제품:** {row.get('관련제품')}")
    else: st.warning("호전반응 시트가 없습니다.")
