# view_guide.py (호전반응 가이드)
import streamlit as st
from components import apply_custom_styles
# [추가] 다국어 설정을 위해 config에서 LANG_CONFIG 임포트
from config import LANG_CONFIG

def render_guide(all_sheets):
    apply_custom_styles()
    
    # [다국어 처리] 현재 선택된 언어 설정 및 UI 텍스트 가져오기
    lang_code = st.session_state.get("selected_lang", "KR")
    ui = LANG_CONFIG[lang_code]["ui"]
    menu = LANG_CONFIG[lang_code]["menu"]
    
    # 1. 페이지 제목 (메뉴 리스트의 "호전반응" 인덱스 활용)
    st.markdown(f"## 💡 {menu[7]}")
    
    # 2. 상단 안내 문구 다국어 처리
    guide_info = {
        "KR": "몸이 좋아지는 과정에서 나타나는 일시적인 반응입니다.",
        "EN": "This is a temporary reaction that occurs as your body improves.",
        "CH": "这是身体好转过程中出现的暂时性反应。",
        "TH": "นี่คือปฏิกิริยาชั่วคราวที่เกิดขึ้นเมื่อร่างกายของคุณดีขึ้น"
    }
    st.info(guide_info.get(lang_code, guide_info["EN"]))
    
    target_sheet = all_sheets.get('호전반응') if all_sheets else None
    if target_sheet is not None:
        # 3. 검색창 라벨 다국어 처리
        search_label = "🔍 증상을 검색해보세요" if lang_code == "KR" else "🔍 Search symptoms"
        search_query = st.text_input(search_label, "")
        
        df = target_sheet.fillna("")
        if search_query: 
            df = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
        
        # 4. 상세 내용 항목(현상, 원인, 대처) 다국어 레이블 설정
        labels = {
            "KR": {"phenomenon": "현상", "cause": "원인", "solution": "대처", "product": "제품"},
            "EN": {"phenomenon": "Phenomenon", "cause": "Cause", "solution": "Action", "product": "Product"},
            "CH": {"phenomenon": "现象", "cause": "原因", "solution": "对策", "product": "产品"},
            "TH": {"phenomenon": "ปรากฏการณ์", "cause": "สาเหตุ", "solution": "การรับมือ", "product": "ผลิตภัณฑ์"}
        }
        curr_labels = labels.get(lang_code, labels["EN"])

        for _, row in df.iterrows():
            with st.expander(f"📌 {row.get('증상', 'Symptom')}", expanded=False):
                st.write(f"**👀 {curr_labels['phenomenon']}:** {row.get('나타나는현상','-')}")
                st.info(f"**❓ {curr_labels['cause']}:** {row.get('발생원인','-')}")
                st.success(f"**💡 {curr_labels['solution']}:** {row.get('대처/가이드','-')}")
                
                # 관련 제품 텍스트 처리
                product_val = row.get('관련제품')
                if product_val and product_val != '-':
                    st.write(f"**💊 {curr_labels['product']}:** {product_val}")
    else: 
        # 5. 에러 메시지 다국어 처리
        error_msg = "호전반응 시트가 없습니다." if lang_code == "KR" else "Recovery guide data not found."
        st.warning(error_msg)