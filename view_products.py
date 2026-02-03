import streamlit as st
import pandas as pd
import re
from utils import get_optimized_image
from func import get_sheet_data
from components import apply_custom_styles
# [추가] 다국어 설정을 위해 config에서 LANG_CONFIG 임포트
from config import LANG_CONFIG

# --------------------------------------------------------------------------
# 1. 제품 소개
# --------------------------------------------------------------------------
def render_products(all_sheets):
    # [다국어 처리] 선택된 언어에 맞는 제목 가져오기
    lang_code = st.session_state.get("selected_lang", "KR")
    menu = LANG_CONFIG[lang_code]["menu"]
    ui = LANG_CONFIG[lang_code]["ui"]
    
    # "📦 FitLine 제품" 대신 메뉴 리스트의 명칭 사용
    st.markdown(f"<h2 style='text-align:center;'>📦 {menu[4]}</h2>", unsafe_allow_html=True)
    
    target = get_sheet_data(all_sheets, "제품설명")
    
    if target is not None:
        df = target.fillna("")
        cols = st.columns(2) 
        for idx, row in df.iterrows():
            with cols[idx%2]:
                with st.container():
                    img = row.get('이미지주소')
                    img_src = get_optimized_image(img)
                    
                    # 한줄소개 줄바꿈 처리
                    raw_desc = str(row.get('한줄소개','-'))
                    formatted_desc = raw_desc.replace('\n', '<br>')
                    
                    st.markdown(f"""
                        <div style="text-align:center; padding-bottom:10px;">
                            <img src="{img_src}" style="width:100%; height:150px; object-fit:contain; border-radius:10px;">
                        </div>
                        <div style="text-align:center; font-weight:bold; font-size:16px; margin-bottom:5px;">{row.get('제품명','-')}</div>
                        <div style="text-align:center; color:#666; font-size:12px; min-height:40px; margin-bottom:10px; line-height:1.4;">
                            {formatted_desc}
                        </div>
                    """, unsafe_allow_html=True)
                    
                    link = row.get('구매링크')
                    # [다국어 처리] 버튼 텍스트 다국어화 (예: 구매하기 -> Shop Now)
                    buy_text = "구매하기" if lang_code == "KR" else "Buy Now"
                    if "http" in str(link): st.link_button(buy_text, link, use_container_width=True)
    else:
        st.info("Data not found.")

# --------------------------------------------------------------------------
# 2. 품질 & 안전성
# --------------------------------------------------------------------------
def render_safety(all_sheets):
    from config import LANG_CONFIG # 순환 참조 방지를 위해 함수 내부에서 임포트 권장
    
    lang_code = st.session_state.get("selected_lang", "KR")
    
    # 해당 언어의 UI 설정 가져오기
    lang_info = LANG_CONFIG.get(lang_code, LANG_CONFIG["KR"])
    ui = lang_info.get("ui", {})
    
    # safety_title 키가 없을 경우를 대비해 기본값 설정
    page_title = ui.get("safety_title", "Quality & Safety")
    
    st.markdown(f"<h2 style='text-align:center;'>🛡️ {page_title}</h2>", unsafe_allow_html=True)    
    # 상단 안내 문구 다국어 처리
    safety_info = {
        "KR": "국가대표 선수부터 임산부까지 안심하고 섭취할 수 있는 최고의 품질을 약속합니다.",
        "EN": "We guarantee the highest quality that anyone from national athletes to pregnant women can consume with confidence.",
        "CH": "我们保证从国家运动员到孕妇都可以放心食用的最高品质。",
        "TH": "เรารับประกันคุณภาพสูงสุดที่ทุกคนตั้งแต่บริโภคได้อย่างมั่นใจ"
    }
    sub_text = safety_info.get(lang_code, safety_info["EN"])

    st.markdown(f"""
    <div style='background-color:#E8F5E9; padding:20px; border-radius:20px; margin-bottom:30px; border:1px solid #C8E6C9; text-align:center;'>
        <h4 style='color:#2E7D32; margin:0;'>✅ PM International Quality</h4>
        <p style='color:#333; margin-top:10px; font-size:14px;'>{sub_text}</p>
    </div>
    """, unsafe_allow_html=True)

    target = get_sheet_data(all_sheets, "안전성")
    if target is not None:
        df = target.fillna("")
        if "순서" in df.columns: df = df.sort_values(by="순서")
        
        for idx, row in df.iterrows():
            st.markdown(f'<div class="cert-box">', unsafe_allow_html=True)
            
            c1, c2 = st.columns([3, 7])
            
            with c1:
                img = row.get('이미지')
                img_src = get_optimized_image(img)
                
                st.markdown(f"""
                    <div style="display:flex; justify-content:center; align-items:center; height:100%;">
                        <img src="{img_src}" style="width:100%; max-width:180px; object-fit:contain;">
                    </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown(f'<div class="cert-title">{row.get("인증제목", "")}</div>', unsafe_allow_html=True)
                
                raw_content = str(row.get("상세내용", ""))
                temp_content = raw_content.replace('\n', '<br>')
                formatted_content = re.sub(r'(\d+\.)', r'<br>\1', temp_content)
                if formatted_content.startswith("<br>"):
                    formatted_content = formatted_content[4:]

                st.markdown(f'<div class="cert-desc" style="line-height:1.6; margin-top:5px;">{formatted_content}</div>', unsafe_allow_html=True)
                
                link_url = row.get('링크')
                btn_label = "공식 홈페이지 확인 🔗" if lang_code == "KR" else "Official Website 🔗"
                if link_url and str(link_url).startswith('http'):
                    st.link_button(btn_label, link_url)
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("---")

# --------------------------------------------------------------------------
# 3. 액티바이즈 진단
# --------------------------------------------------------------------------
def render_diagnosis(all_sheets):
    try:
        apply_custom_styles()
    except:
        pass

    # [다국어 처리]
    lang_code = st.session_state.get("selected_lang", "KR")
    ui = LANG_CONFIG[lang_code]["ui"]
    
    st.markdown(f"## 🩺 {ui['act_title']}")
    
    info_msg = {
        "KR": "💡 신체 부위를 선택하면 나타나는 반응의 원인과 호전 반응을 확인할 수 있습니다.",
        "EN": "💡 Select a body part to check the cause of the reaction and the recovery response.",
        "CH": "💡 选择身体部位以检查反应的原因和好转反应。",
        "TH": "💡 เลือกส่วนของร่างกายเพื่อตรวจสอบสาเหตุของการตอบสนอง"
    }
    st.info(info_msg.get(lang_code, info_msg["EN"]))

    tab_labels = {
        "KR": ["🤕 부위별 반응", "😋 맛 별 체크"],
        "EN": ["🤕 By Body Part", "😋 By Taste"],
        "CH": ["🤕 按部位", "😋 按味道"],
        "TH": ["🤕 ตามส่วนร่างกาย", "😋 ตามรสชาติ"]
    }
    current_tabs = tab_labels.get(lang_code, tab_labels["EN"])
    sub1, sub2 = st.tabs(current_tabs)

    # --- [탭 1] 부위별 반응 ---
    with sub1:
        target_sheet = None
        possible_names = ['액티바이즈', '액티증상', '호전반응', '반응']
        
        for name in possible_names:
            target_sheet = get_sheet_data(all_sheets, name)
            if target_sheet is not None:
                break
        
        if target_sheet is not None:
            df = target_sheet.fillna("")
            part_col = '구분' if '구분' in df.columns else ('부위' if '부위' in df.columns else None)
            
            if part_col:
                parts = df[part_col].unique().tolist()
                sel_msg = "### 👇 부위를 선택하세요" if lang_code == "KR" else "### 👇 Select Body Part"
                st.write(sel_msg)
                
                try:
                    selected_part = st.pills(label="Part", options=parts, default=parts[0] if parts else None, selection_mode="single", label_visibility="collapsed")
                except AttributeError:
                    selected_part = st.radio("Part", options=parts, horizontal=True, label_visibility="collapsed")

                st.markdown("---")

                if selected_part:
                    filtered_df = df[df[part_col] == selected_part]
                    if not filtered_df.empty:
                        first_row = filtered_df.iloc[0]
                        rep_image = first_row.get('이미지')
                        if rep_image and str(rep_image).strip() != "":
                            c_img1, c_img2, c_img3 = st.columns([1, 2, 1])
                            with c_img2:
                                st.image(get_optimized_image(rep_image), use_container_width=True)
                        
                        detail_msg = "상세 분석" if lang_code == "KR" else "Detailed Analysis"
                        st.markdown(f"### 📍 {selected_part} {detail_msg}")
                        
                        label_reaction = "**🔥 나타나는 반응**" if lang_code == "KR" else "**🔥 Reaction**"
                        label_cause = "**🧐 원인 및 분석**" if lang_code == "KR" else "**🧐 Cause & Analysis**"
                        label_extra = "💡 추가 가이드" if lang_code == "KR" else "💡 Extra Guide"

                        for idx, row in filtered_df.iterrows():
                            symptom = row.get('반응') if '반응' in df.columns else row.get('증상', '-')
                            cause = row.get('증상') if '반응' in df.columns else row.get('원인', '-') 
                            
                            with st.container():
                                c1, c2 = st.columns([1, 2])
                                with c1:
                                    st.markdown(label_reaction)
                                    st.warning(symptom)
                                with c2:
                                    st.markdown(label_cause)
                                    st.info(cause)
                                
                                extra_solution = row.get('대처') or row.get('호전반응')
                                if extra_solution:
                                    with st.expander(label_extra, expanded=False):
                                        st.write(extra_solution)
                                st.divider()
                    else:
                        st.warning("No detail data found.")
            else:
                st.error("Column Error")
        else:
            st.error("Sheet Error")

    # --- [탭 2] 맛 체크 ---
    with sub2:
        target_taste = None
        possible_taste_names = ['맛', '맛체크', '맛반응']
        for name in possible_taste_names:
            target_taste = get_sheet_data(all_sheets, name)
            if target_taste is not None: break

        if target_taste is not None:
            df_t = target_taste.fillna("")
            if len(df_t.columns) >= 2:
                taste_map = dict(zip(df_t.iloc[:,0], df_t.iloc[:,1]))
                cols = st.columns(2)
                for i, (t, s) in enumerate(taste_map.items()):
                    with cols[i%2]:
                        desc = str(s).replace('\n', '\n\n')
                        if st.button(f"😋 {t}", key=f"t_{i}", use_container_width=True): 
                            st.success(f"**{t}** 👉 {desc}")
        else:
            st.info("No data found.")