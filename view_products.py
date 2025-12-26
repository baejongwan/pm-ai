import streamlit as st
import re
from utils import get_optimized_image
from func import get_sheet_data

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
    st.markdown("<h2 style='text-align:center;'>🔥 액티바이즈 진단</h2>", unsafe_allow_html=True)
    sub1, sub2 = st.tabs(["🔴 신체 반응", "👅 맛 체크"])
    
    # --- [탭 1] 신체 반응 ---
    with sub1:
        # 1. 시트 이름 찾기 (액티바이즈 또는 액티증상)
        target = get_sheet_data(all_sheets, "액티바이즈")
        if target is None:
            target = get_sheet_data(all_sheets, "액티증상") # 혹시 이름이 다를까봐 한 번 더 찾음
            
        if target is not None:
            df = target.ffill() # 빈칸 채우기
            
            # 필수 컬럼 확인 ('구분' 컬럼이 있어야 작동)
            if "구분" in df.columns:
                parts = [x for x in df["구분"].unique() if str(x).strip() != ""]
                part = st.selectbox("어느 부위가 빨개지셨나요?", parts)
                
                if part:
                    subset = df[df["구분"] == part]
                    
                    # 이미지 찾기 (컬럼명이 '이미지'여도 되고 '참고이미지'여도 됨)
                    img_name = subset.iloc[0].get("이미지") or subset.iloc[0].get("참고이미지")
                    img_src = get_optimized_image(img_name)
                    
                    st.markdown(f"""<div style="text-align:center; margin:20px 0;"><img src="{img_src}" style="max-width:200px; border-radius:15px;"></div>""", unsafe_allow_html=True)
                    
                    for idx, row in subset.iterrows():
                        # 줄바꿈 처리 적용
                        symptom = str(row.get('증상','-')).replace('\n', '<br>')
                        reaction = row.get('반응', '-')
                        
                        st.markdown(f"""
                            <div style="background:#fff; border-left: 5px solid #d9534f; padding:15px; border-radius:10px; margin-bottom:10px;">
                                <div style="color:#d9534f; font-weight:bold;">🔥 {reaction}</div>
                                <div style="color:#333; font-size:14px; margin-top:5px; line-height:1.5;">🩺 {symptom}</div>
                            </div>
                        """, unsafe_allow_html=True)
            else:
                st.error("엑셀 오류: '액티바이즈' 시트에 '구분'이라는 제목의 열(Column)이 꼭 있어야 합니다.")
        else:
            st.info("데이터 없음: 엑셀 시트 이름을 '액티바이즈' 또는 '액티증상'으로 확인해주세요.")

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
