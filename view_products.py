import streamlit as st
import pandas as pd
import re
from utils import get_optimized_image
from func import get_sheet_data
from components import apply_custom_styles

# --------------------------------------------------------------------------
# 1. 제품 소개 (기존과 동일)
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
# 2. 품질 & 안전성 (이미지 확대 적용)
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
            
            # [수정 1] 컬럼 비율 조정 (이미지 영역 2 -> 3으로 확대)
            # 기존 [2, 8] -> 변경 [3, 7]
            c1, c2 = st.columns([3, 7])
            
            with c1:
                img = row.get('이미지')
                img_src = get_optimized_image(img)
                
                # [수정 2] 이미지 최대 너비(max-width) 증가
                # 기존 120px -> 변경 180px (필요하면 더 늘려도 됩니다)
                st.markdown(f"""
                    <div style="display:flex; justify-content:center; align-items:center; height:100%;">
                        <img src="{img_src}" style="width:100%; max-width:180px; object-fit:contain;">
                    </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown(f'<div class="cert-title">{row.get("인증제목", "")}</div>', unsafe_allow_html=True)
                
                # (지난번 적용한 줄바꿈 마법 코드 유지)
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

# view_products.py의 맨 마지막 함수(render_diagnosis)를 이걸로 바꾸세요

# --------------------------------------------------------------------------
# 3. 액티바이즈 진단 (시트 이름 자동 탐지 기능 추가)
# --------------------------------------------------------------------------
def render_diagnosis(all_sheets):
    apply_custom_styles()
    st.markdown("## 🩺 액티바이즈 반응 분석")
    st.info("💡 신체 부위를 선택하면 나타나는 반응의 원인과 호전 반응을 확인할 수 있습니다.")

    # 1. 데이터 로드
    target_sheet = all_sheets.get('액티증상')
    
    if target_sheet is not None:
        df = target_sheet.fillna("")
        
        # 2. 부위 목록 추출 (중복 제거)
        # 엑셀에 '부위'라는 컬럼이 있다고 가정합니다.
        if '부위' in df.columns:
            parts = df['부위'].unique().tolist()
            
            # 3. [핵심 수정] 부위 선택 UI 변경 (selectbox -> pills)
            # pills는 메뉴바처럼 항목을 나열해줍니다.
            # 만약 Streamlit 버전이 낮아 pills가 안 된다면 radio(가로형)을 쓰도록 예외처리함
            st.write("### 👇 부위를 선택하세요")
            
            try:
                # 최신 디자인 (알약 버튼 형태)
                selected_part = st.pills(
                    label="부위 선택",
                    options=parts,
                    default=parts[0] if parts else None,
                    selection_mode="single",
                    label_visibility="collapsed" # 라벨 숨김 (깔끔하게)
                )
            except AttributeError:
                # 구버전 호환용 (가로형 라디오 버튼)
                selected_part = st.radio(
                    "부위 선택",
                    options=parts,
                    horizontal=True,
                    label_visibility="collapsed"
                )

            st.markdown("---")

            # 4. 선택된 부위 상세 정보 표시
            if selected_part:
                # 선택된 부위의 데이터 필터링
                filtered_df = df[df['부위'] == selected_part]
                
                if not filtered_df.empty:
                    for idx, row in filtered_df.iterrows():
                        symptom = row.get('증상', '증상 정보 없음')
                        cause = row.get('원인', '-')
                        solution = row.get('대처', '-')
                        
                        # 카드 형태로 예쁘게 표시
                        st.success(f"### 📍 {selected_part}")
                        
                        c1, c2 = st.columns([1, 2])
                        with c1:
                            st.markdown(f"**🔥 나타나는 증상**")
                            st.write(symptom)
                        with c2:
                            st.markdown(f"**🧐 원인 및 분석**")
                            st.info(cause)
                            
                        if solution and solution != '-':
                            with st.expander("💡 호전 반응 및 대처 가이드", expanded=True):
                                st.write(solution)
                else:
                    st.warning("해당 부위에 대한 상세 데이터가 없습니다.")
        else:
            st.error("엑셀 파일에 '부위' 컬럼이 없습니다.")
    else:
        st.error("'액티증상' 시트를 찾을 수 없습니다. 엑셀 파일을 확인해주세요.")
    # --- [탭 2] 맛 체크 ---
    with sub2:
        # 2. 시트 이름 찾기 (맛 또는 맛체크)
        target_taste = get_sheet_data(all_sheets, "맛")
        if target_taste is None:
            target_taste = get_sheet_data(all_sheets, "맛체크") # 혹시 이름이 다를까봐 한 번 더 찾음

        if target_taste is not None:
            df_t = target_taste.fillna("")
            
            # 데이터가 2열 이상인지 확인
            if len(df_t.columns) >= 2:
                # 첫 번째 열은 '맛', 두 번째 열은 '설명'으로 자동 인식
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


