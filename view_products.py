import streamlit as st
import pandas as pd
import re
from utils import get_optimized_image
from func import get_sheet_data
from components import apply_custom_styles

# --------------------------------------------------------------------------
# 1. 제품 소개
# --------------------------------------------------------------------------
def render_products(all_sheets):
    st.markdown("<h2 style='text-align:center;'>📦 FitLine 제품</h2>", unsafe_allow_html=True)
    
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
                    if "http" in str(link): st.link_button("구매하기", link, use_container_width=True)
    else:
        st.info("제품설명 데이터를 찾을 수 없습니다.")

# --------------------------------------------------------------------------
# 2. 품질 & 안전성
# --------------------------------------------------------------------------
def render_safety(all_sheets):
    st.markdown("<h2 style='text-align:center;'>🛡️ 품질 & 안전성</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background-color:#E8F5E9; padding:20px; border-radius:20px; margin-bottom:30px; border:1px solid #C8E6C9; text-align:center;'>
        <h4 style='color:#2E7D32; margin:0;'>✅ PM 인터내셔널의 타협하지 않는 안전성</h4>
        <p style='color:#333; margin-top:10px; font-size:14px;'>
            국가대표 선수부터 임산부까지 안심하고 섭취할 수 있는 최고의 품질을 약속합니다.
        </p>
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
                if link_url and str(link_url).startswith('http'):
                    st.link_button("공식 홈페이지 확인 🔗", link_url)
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("---")

# --------------------------------------------------------------------------
# 3. 액티바이즈 진단 (수정 완료: 사용자 엑셀 컬럼 '구분,반응,증상,이미지' 반영)
# --------------------------------------------------------------------------
def render_diagnosis(all_sheets):
    try:
        apply_custom_styles()
    except:
        pass

    st.markdown("## 🩺 액티바이즈 반응 분석")
    st.info("💡 신체 부위를 선택하면 나타나는 반응의 원인과 호전 반응을 확인할 수 있습니다.")

    sub1, sub2 = st.tabs(["🤕 부위별 반응", "😋 맛 별 체크"])

    # --- [탭 1] 부위별 반응 ---
    with sub1:
        # 1. 시트 찾기 (액티바이즈, 액티증상 등)
        target_sheet = None
        possible_names = ['액티바이즈', '액티증상', '호전반응', '반응']
        
        for name in possible_names:
            target_sheet = get_sheet_data(all_sheets, name)
            if target_sheet is not None:
                break
        
        if target_sheet is not None:
            df = target_sheet.fillna("")
            
            # 2. 컬럼 매핑 (사장님 파일 구조: 구분, 반응, 증상, 이미지)
            # 만약 '구분' 컬럼이 있으면 그걸 사용하고, 없으면 '부위'를 사용하도록 유연하게 처리
            part_col = '구분' if '구분' in df.columns else ('부위' if '부위' in df.columns else None)
            
            if part_col:
                parts = df[part_col].unique().tolist()
                
                st.write("### 👇 부위를 선택하세요")
                
                # 메뉴바(알약) 스타일
                try:
                    selected_part = st.pills(
                        label="부위 선택",
                        options=parts,
                        default=parts[0] if parts else None,
                        selection_mode="single",
                        label_visibility="collapsed"
                    )
                except AttributeError:
                    selected_part = st.radio(
                        "부위 선택",
                        options=parts,
                        horizontal=True,
                        label_visibility="collapsed"
                    )

                st.markdown("---")

                if selected_part:
                    filtered_df = df[df[part_col] == selected_part]
                    
                    if not filtered_df.empty:
                        for idx, row in filtered_df.iterrows():
                            # [핵심] 컬럼 연결
                            # 반응 -> (UI) 나타나는 반응
                            # 증상 -> (UI) 원인 및 분석
                            symptom = row.get('반응') if '반응' in df.columns else row.get('증상', '-')
                            cause = row.get('증상') if '반응' in df.columns else row.get('원인', '-') 
                            # (설명: '반응' 컬럼이 있으면 그게 증상이고, '증상' 컬럼은 원인/해설로 씁니다)
                            
                            image_url = row.get('이미지') # 이미지 컬럼

                            st.success(f"### 📍 {selected_part}")
                            
                            # 레이아웃: 이미지가 있으면 3단, 없으면 2단
                            has_image = image_url and str(image_url).strip() != ""
                            
                            if has_image:
                                c1, c2, c3 = st.columns([1.5, 2, 2])
                                with c1:
                                    st.image(get_optimized_image(image_url), use_container_width=True)
                                with c2:
                                    st.markdown(f"**🔥 나타나는 반응**")
                                    st.write(symptom)
                                with c3:
                                    st.markdown(f"**🧐 원인 및 분석**")
                                    st.info(cause)
                            else:
                                c1, c2 = st.columns([1, 2])
                                with c1:
                                    st.markdown(f"**🔥 나타나는 반응**")
                                    st.write(symptom)
                                with c2:
                                    st.markdown(f"**🧐 원인 및 분석**")
                                    st.info(cause)
                            
                            # 대처나 호전반응 컬럼이 따로 있다면 추가 표시 (옵션)
                            extra_solution = row.get('대처') or row.get('호전반응')
                            if extra_solution:
                                with st.expander("💡 추가 가이드", expanded=True):
                                    st.write(extra_solution)

                    else:
                        st.warning("해당 부위에 대한 상세 데이터가 없습니다.")
            else:
                st.error(f"엑셀 파일에 '구분' 또는 '부위' 컬럼이 없습니다. (현재 컬럼: {list(df.columns)})")
        else:
            st.error("🚨 엑셀에서 '액티바이즈' 관련 시트를 찾을 수 없습니다.")

    # --- [탭 2] 맛 체크 ---
    with sub2:
        target_taste = None
        possible_taste_names = ['맛', '맛체크', '맛반응']
        
        for name in possible_taste_names:
            target_taste = get_sheet_data(all_sheets, name)
            if target_taste is not None:
                break

        if target_taste is not None:
            df_t = target_taste.fillna("")
            
            if len(df_t.columns) >= 2:
                # 첫 번째 열: 맛, 두 번째 열: 설명
                taste_map = dict(zip(df_t.iloc[:,0], df_t.iloc[:,1]))
                
                cols = st.columns(2)
                for i, (t, s) in enumerate(taste_map.items()):
                    with cols[i%2]:
                        desc = str(s).replace('\n', '\n\n')
                        if st.button(f"😋 {t}", key=f"t_{i}", use_container_width=True): 
                            st.success(f"**{t}** 👉 {desc}")
            else:
                st.warning("엑셀 오류: '맛' 시트에는 최소 2개의 열(맛 종류, 설명)이 필요합니다.")
        else:
            st.info("데이터 없음: 엑셀 시트 이름을 '맛' 또는 '맛체크'로 확인해주세요.")
