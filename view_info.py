# view_info.py
import streamlit as st
import pandas as pd
from utils import get_optimized_image

# ----------------------------------------------------------------
# [0] CSS 스타일 (높이 고정 & 디자인 최적화)
# ----------------------------------------------------------------
def apply_custom_styles():
    st.markdown("""
        <style>
        /* 1. 숫자 표시 박스 디자인 (높이 45px 고정) */
        .counter-box {
            display: flex;
            align-items: center;
            justify-content: center;
            height: 45px;          /* 높이 고정 */
            font-size: 20px;
            font-weight: bold;
            color: #333;
            border: 1px solid #d0d0d0;
            border-radius: 8px;
            background-color: #f9f9f9;
            margin: 0;
            width: 100%;
        }
        
        /* 2. 더하기/빼기 버튼 디자인 (높이 45px 강제 고정) */
        div.stButton > button {
            height: 45px !important;      /* 높이 강제 고정 */
            min-height: 45px !important;  
            max-height: 45px !important; 
            padding: 0px !important;
            font-size: 20px !important;
            border-radius: 8px !important;
            line-height: 1 !important;
            width: 100% !important;
            border: 1px solid #d0d0d0 !important;
        }
        
        /* 모바일 텍스트 크기 미세 조정 */
        @media (max-width: 640px) {
            .counter-box { font-size: 18px; }
            div.stButton > button { font-size: 18px !important; }
        }
        </style>
    """, unsafe_allow_html=True)

# ----------------------------------------------------------------
# [1] 호전반응 가이드
# ----------------------------------------------------------------
def render_guide(all_sheets):
    apply_custom_styles() 
    st.markdown("## 💡 호전반응(명현현상) 가이드")
    st.info("몸이 좋아지는 과정에서 나타나는 일시적인 반응입니다.")

    target_sheet = None
    if all_sheets and '호전반응' in all_sheets:
        target_sheet = all_sheets['호전반응']
    
    if target_sheet is not None:
        search_query = st.text_input("🔍 증상을 검색해보세요 (예: 두통, 가려움)", "")
        df = target_sheet.fillna("")
        
        if search_query:
            df = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]

        for index, row in df.iterrows():
            symptom = row.get('증상', '증상명')
            phenomenon = row.get('나타나는현상', '-')
            cause = row.get('발생원인', '-')
            guide = row.get('대처/가이드', '-')
            products = row.get('관련제품', '-')

            with st.expander(f"📌 {symptom}", expanded=False):
                st.markdown(f"**👀 나타나는 현상:**")
                st.write(phenomenon)
                st.markdown(f"**❓ 발생 원인:**")
                st.info(cause)
                st.markdown(f"**💡 대처 가이드:**")
                st.success(guide)
                if products and products != '-':
                    st.markdown(f"**💊 관련 제품:** {products}")
    else:
        st.warning("⚠️ '호전반응' 시트를 찾을 수 없습니다.")

# ----------------------------------------------------------------
# [2] 보상플랜
# ----------------------------------------------------------------
def render_compensation(all_sheets):
    apply_custom_styles()
    st.markdown("## 💰 성공을 부르는 보상플랜")
    
    tab1, tab2 = st.tabs(["📚 보상플랜 핵심요약", "🧮 프리미엄 수익 시뮬레이터"])
    
    with tab1:
        st.markdown("#### PM 사업의 강력한 수익 구조")
        target_sheet = None
        if all_sheets and '보상플랜' in all_sheets:
            target_sheet = all_sheets['보상플랜']
            
        if target_sheet is not None:
            df = target_sheet.fillna("")
            for index, row in df.iterrows():
                title = row.get('제목', f"보상플랜 정보 {index+1}")
                content = row.get('내용', '-')
                youtube_link = row.get('유튜브')
                
                with st.expander(f"💎 {title}", expanded=True):
                    st.write(content)
                    if youtube_link and str(youtube_link).startswith('http'):
                        st.video(str(youtube_link))
                    
                    img_list = []
                    for i in range(1, 5): 
                        col_name = f"이미지{i}"
                        if col_name in row and row[col_name]:
                            img_path = get_optimized_image(row[col_name])
                            if "flaticon" not in img_path:
                                img_list.append(img_path)
                    if img_list:
                        cols = st.columns(len(img_list))
                        for idx, img_src in enumerate(img_list):
                            with cols[idx]:
                                st.image(img_src, use_container_width=True)
        else:
            st.info("보상플랜 데이터가 없습니다.")

    with tab2:
        render_calculator_v2()

# ----------------------------------------------------------------
# [보조 함수] 숫자 조절 버튼 (비율 최적화 & 넘침 방지)
# ----------------------------------------------------------------
def number_counter(label, key, default_val, min_val, max_val, unit=""):
    if key not in st.session_state:
        st.session_state[key] = default_val

    st.markdown(f"<div style='text-align:center; font-weight:bold; font-size:15px; margin-bottom:8px; color:#555;'>{label}</div>", unsafe_allow_html=True)
    
    # [수정] 스마트폰에서 꽉 차게 보이도록 비율 설정 [1, 2, 1]
    # 모바일에서는 이 컬럼들이 화면 전체 너비를 쓰므로 충분히 넓어서 줄바꿈이 안 일어납니다.
    c_minus, c_val, c_plus = st.columns([1, 2, 1])
    
    with c_minus:
        if st.button("－", key=f"dec_{key}", use_container_width=True):
            if st.session_state[key] > min_val:
                st.session_state[key] -= 1
                st.rerun()
                
    with c_val:
        st.markdown(f"""
            <div class="counter-box">
                {st.session_state[key]}
            </div>
        """, unsafe_allow_html=True)
        
    with c_plus:
        if st.button("＋", key=f"inc_{key}", type="primary", use_container_width=True):
            if st.session_state[key] < max_val:
                st.session_state[key] += 1
                st.rerun()

    if unit:
        st.markdown(f"<div style='text-align:center; font-size:12px; color:#888; margin-top:5px;'>{unit}</div>", unsafe_allow_html=True)
    
    return st.session_state[key]

# ----------------------------------------------------------------
# 수익 계산기 V2
# ----------------------------------------------------------------
def render_calculator_v2():
    st.markdown("### 💸 나의 미래 직급과 수익 미리보기")
    
    with st.container():
        st.info("""
        **📌 시뮬레이션 기준 (매니저 CA 달성, 오토십 기준)**
        * **1인당 매출:** 오토십 137,100원 (약 103점/GV)
        * **직추천 보너스:** 10%
        * **레벨 보너스:** 1대(5%), 2~4대(3%), 5~6대(5%) 적용
        """)

    st.markdown("---")

    # --- 입력 컨트롤 ---
    # 여기서 st.columns(3)을 쓰면 웹에서는 3단, 모바일에서는 자동으로 1단(세로)으로 바뀝니다.
    # 이전 코드의 nowrap 강제를 삭제했으므로 모바일 화면 밖으로 안 나갑니다.
    c1, c2, c3 = st.columns(3)
    
    with c1:
        my_partners = number_counter("1️⃣ 직대 파트너", "my_partners_val", 3, 1, 50, "명")
        
    with c2:
        duplication = number_counter("2️⃣ 파트너당 복제", "duplication_val", 3, 1, 10, "명씩 소개")
        
    with c3:
        generations = number_counter("3️⃣ 계산 깊이", "generations_val", 4, 1, 6, "세대(Level)")

    st.markdown("---")

    # --- 계산 로직 ---
    PRICE_PER_USER = 137100
    GV_PER_USER = 103
    level_rates = [0.05, 0.03, 0.03, 0.03, 0.05, 0.05] 
    
    total_partners = 0
    total_sales = 0
    total_gv = 0
    
    direct_income = (my_partners * PRICE_PER_USER) * 0.10
    level_income = 0
    partners_on_level = my_partners 
    details_text = [] 

    for i in range(generations):
        if i == 0:
            current_partners = my_partners
        else:
            current_partners = partners_on_level * duplication
            partners_on_level = current_partners
            
        current_sales = current_partners * PRICE_PER_USER
        current_gv = current_partners * GV_PER_USER
        
        rate = level_rates[i] if i < len(level_rates) else 0.02
        current_bonus = current_sales * rate
        
        total_partners += current_partners
        total_sales += current_sales
        total_gv += current_gv
        level_income += current_bonus
        
        details_text.append(f"- **{i+1}대:** {current_partners:,}명 x {int(rate*100)}% = {int(current_bonus):,}원")

    total_income = direct_income + level_income

    # --- 직급 예측 ---
    rank_name = "매니저 (Manager)"
    car_bonus = 0
    travel_bonus = "없음"
    badge_color = "gray"
    
    if total_gv >= 100000:
        rank_name = "PT (President's Team)"
        car_bonus = 650000 
        travel_bonus = "✈️ 월드 투어, 윈터 리더십 등 풀패키지"
        badge_color = "#FFD700"
    elif total_gv >= 50000:
        rank_name = "EVP (Executive VP)"
        car_bonus = 520000 
        travel_bonus = "✈️ 윈터 리더십 여행"
        badge_color = "#C0C0C0"
    elif total_gv >= 25000:
        rank_name = "VP (Vice President)"
        car_bonus = 288600
        travel_bonus = "✈️ 윈터 리더십 여행"
        badge_color = "#CD7F32"
    elif total_gv >= 10000:
        rank_name = "IMM (International MM)"
        car_bonus = 169000
        travel_bonus = "✈️ 유럽 여행 (초대)"
        badge_color = "#2196F3"
    elif total_gv >= 5000:
        rank_name = "MM (Marketing Manager)"
        badge_color = "#4CAF50"
    elif total_gv >= 2500:
        rank_name = "SM (Sales Manager)"
        badge_color = "#8BC34A"

    # --- 결과 화면 ---
    st.markdown(f"#### 🏆 예상 달성 직급: <span style='color:{badge_color}; font-size:24px; font-weight:bold;'>{rank_name}</span>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div style="border:1px solid #ddd; padding:10px; border-radius:10px; text-align:center;">
            <div style="font-size:14px; color:#666;">🚗 카 보너스</div>
            <div style="font-size:20px; font-weight:bold; color:#E91E63;">{int(car_bonus):,} 원</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div style="border:1px solid #ddd; padding:10px; border-radius:10px; text-align:center;">
            <div style="font-size:14px; color:#666;">✈️ 여행 보너스</div>
            <div style="font-size:16px; font-weight:bold; color:#3F51B5;">{travel_bonus}</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div style="border:1px solid #ddd; padding:10px; border-radius:10px; text-align:center; background-color:#E8F5E9;">
            <div style="font-size:14px; color:#666;">💰 월 예상 수령액</div>
            <div style="font-size:20px; font-weight:bold; color:#2E7D32;">{int(total_income + car_bonus):,} 원</div>
        </div>
        """, unsafe_allow_html=True)
        st.caption("* 카보너스 포함 합계")

    m1, m2, m3 = st.columns(3)
    with m1: st.metric("총 산하 파트너", f"{total_partners:,} 명")
    with m2: st.metric("총 예상 매출 포인트", f"{total_gv:,} P (GV)")
    with m3: st.metric("기본 후원 수당", f"{int(total_income):,} 원")
    
    with st.expander("🔍 수당 계산 상세 내역 보기"):
        st.markdown(f"**(1) 직추천 보너스 (10%)** : {int(direct_income):,} 원")
        st.markdown(f"**(2) 레벨 보너스 (1~{generations}대 합계)** : {int(level_income):,} 원")
        for line in details_text:
            st.write(line)
        st.markdown("---")
        st.info("※ 본 시뮬레이션은 이해를 돕기 위한 예상치이며, 실제 수당은 달라질 수 있습니다.")

# ----------------------------------------------------------------
# [3] 제품 체험 사례 (기존 기능 유지)
# ----------------------------------------------------------------
def render_experience(all_sheets):
    apply_custom_styles()
    st.markdown("## 💬 생생한 제품 체험 사례")
    
    target_sheet = None
    if all_sheets and '체험사례' in all_sheets:
        target_sheet = all_sheets['체험사례']
    
    if target_sheet is not None:
        df = target_sheet.fillna("")
        categories = ["전체"]
        if '카테고리' in df.columns:
            categories += list(df['카테고리'].unique())
            
        selected_cat = st.selectbox("증상별/제품별 모아보기", categories)
        if selected_cat != "전체":
            df = df[df['카테고리'] == selected_cat]

        for index, row in df.iterrows():
            category = row.get('카테고리', '일반')
            title = row.get('제목', '체험 사례')
            symptom = row.get('질병/증상', '-')
            profile = row.get('국가/나이/성별', '정보 없음')
            content = row.get('내용/후기', '-')
            products = row.get('섭취제품', '-')
            youtube_link = row.get('유튜브')

            with st.container():
                st.markdown(f"""
                <div style="border:1px solid #e0e0e0; border-radius:10px; padding:20px; margin-bottom:20px; background-color:white;">
                    <div style="color:#2E7D32; font-weight:bold; font-size:14px; margin-bottom:5px;">[{category}] {symptom}</div>
                    <h3 style="margin-top:0;">{title}</h3>
                    <div style="color:#666; font-size:14px; margin-bottom:15px;">
                        👤 <strong>프로필:</strong> {profile} <br>
                        💊 <strong>섭취제품:</strong> {products}
                    </div>
                    <div style="background-color:#f9f9f9; padding:15px; border-radius:5px; margin-bottom:15px;">
                        {content}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if youtube_link and str(youtube_link).startswith('http'):
                    st.video(str(youtube_link))
    else:
        st.info("체험 사례 데이터가 없습니다.")

# ----------------------------------------------------------------
# [4] 사업 성공 사례 (기존 기능 유지)
# ----------------------------------------------------------------
def render_success(all_sheets):
    apply_custom_styles()
    st.markdown("## 🏆 명예의 전당 (성공 스토리)")
    
    target_sheet = None
    if all_sheets and '성공사례' in all_sheets:
        target_sheet = all_sheets['성공사례']

    if target_sheet is not None:
        df = target_sheet.fillna("")
        
        for index, row in df.iterrows():
            name = row.get('이름', '이름 없음')
            ex_job = row.get('전직업', '-')
            motive = row.get('시작동기', '-')
            rank = row.get('직급', '-')
            period = row.get('달성기간', '-')
            difficulty = row.get('애로사항', '-')
            knowhow = row.get('극복노하우', '-')
            youtube_link = row.get('유튜브')
            
            with st.expander(f"👑 {name} {rank} ({ex_job})", expanded=True):
                c1, c2 = st.columns([1, 1])
                with c1:
                    st.markdown(f"**⏱ 달성 기간:** {period}")
                    st.markdown(f"**💼 전직업:** {ex_job}")
                with c2:
                    st.markdown(f"**🚀 시작 동기:** {motive}")

                st.markdown("---")
                st.markdown(f"**😥 애로사항:**\n {difficulty}")
                st.write("")
                st.markdown(f"**💡 극복 노하우:**\n {knowhow}")
                
                if youtube_link and str(youtube_link).startswith('http'):
                    st.write("")
                    st.markdown("**📺 인터뷰 영상 보기**")
                    st.video(str(youtube_link))
    else:
        st.info("성공 사례 데이터가 없습니다.")

    # [진단 도구]
    with st.expander("🛠 [관리자용] 엑셀 데이터 진단"):
        st.write("엑셀 파일 시트 목록:")
        if all_sheets:
            st.write(list(all_sheets.keys()))
            selected_sheet = st.selectbox("확인할 시트", list(all_sheets.keys()))
            if selected_sheet:
                st.dataframe(all_sheets[selected_sheet].head())
                st.write(list(all_sheets[selected_sheet].columns))
        else:
            st.error("엑셀 파일 로드 실패")
