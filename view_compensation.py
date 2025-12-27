import streamlit as st
from utils import get_optimized_image
from components import apply_custom_styles

# 1. 보상플랜 핵심요약 (기존 유지)
def render_compensation(all_sheets):
    apply_custom_styles()
    st.markdown("## 📚 보상플랜 핵심요약")
    
    target_sheet = all_sheets.get('보상플랜') if all_sheets else None
    if target_sheet is not None:
        df = target_sheet.fillna("")
        for index, row in df.iterrows():
            title = row.get('제목', f"보상플랜 정보 {index+1}")
            content = row.get('내용', '-')
            youtube_link = row.get('유튜브')
            with st.expander(f"💎 {title}", expanded=True):
                st.write(content)
                if youtube_link and str(youtube_link).startswith('http'): st.video(str(youtube_link))
                img_list = []
                for i in range(1, 5): 
                    if f"이미지{i}" in row and row[f"이미지{i}"]:
                        img_path = get_optimized_image(row[f"이미지{i}"])
                        if "flaticon" not in img_path: img_list.append(img_path)
                if img_list:
                    cols = st.columns(len(img_list))
                    for idx, img_src in enumerate(img_list):
                        with cols[idx]: st.image(img_src, use_container_width=True)
    else: st.info("보상플랜 데이터가 없습니다.")

# 2. 수익 시뮬레이션 (수정됨: 디자인 유지 + 오류 해결)
def render_calculator_v2():
    apply_custom_styles()
    st.markdown("## 💸 수익 & 직급 시뮬레이션")
    
    with st.container():
        st.info("""
        **📌 시뮬레이션 기준 (현실적인 사업 모델 적용)**
        1. **1인당 소비:** 오토십(103GV) + 액티바이즈(37GV) = **총 140GV**
        2. **보상 기준:** 직추천 10%, 레벨보너스(5~3%) 적용
        3. 실제소득은 **월 예상 수령액**보다 더 높은 수익을 받습니다.
        """)
    st.markdown("---")
    
    # ----------------------------------------------------------------------
    # [수정된 부분] 오류 해결을 위한 세션 초기화 및 디자인 적용
    # ----------------------------------------------------------------------
    
    # 1. 세션 상태 초기화 (값이 없을 때만 초기값 3, 3, 4 설정 -> 오류 원인 차단)
    if "my_partners_val" not in st.session_state: st.session_state["my_partners_val"] = 3
    if "duplication_val" not in st.session_state: st.session_state["duplication_val"] = 3
    if "generations_val" not in st.session_state: st.session_state["generations_val"] = 4

    # 2. 3단 컬럼 레이아웃 (모바일 최적화 디자인 유지)
    c1, c2, c3 = st.columns(3)
    
    # 1️⃣ 직대 파트너 (위: 라벨, 중간: 입력창, 아래: 단위)
    with c1:
        st.markdown("<div style='text-align: center; font-weight: bold;'>1️⃣ 직대 파트너</div>", unsafe_allow_html=True)
        # value 옵션을 제거하여 충돌 방지
        my_partners = st.number_input("직대 파트너", min_value=1, max_value=50, key="my_partners_val", label_visibility="collapsed")
        st.markdown("<div style='text-align: center; font-size: 0.9em;'>명</div>", unsafe_allow_html=True)

    # 2️⃣ 파트너당 복제
    with c2:
        st.markdown("<div style='text-align: center; font-weight: bold;'>2️⃣ 파트너당 복제</div>", unsafe_allow_html=True)
        duplication = st.number_input("파트너당 복제", min_value=1, max_value=10, key="duplication_val", label_visibility="collapsed")
        st.markdown("<div style='text-align: center; font-size: 0.9em;'>명씩 소개</div>", unsafe_allow_html=True)

    # 3️⃣ 계산 깊이
    with c3:
        st.markdown("<div style='text-align: center; font-weight: bold;'>3️⃣ 계산 깊이</div>", unsafe_allow_html=True)
        generations = st.number_input("계산 깊이", min_value=1, max_value=6, key="generations_val", label_visibility="collapsed")
        st.markdown("<div style='text-align: center; font-size: 0.9em;'>세대(Level)</div>", unsafe_allow_html=True)
        
    st.markdown("---")
    
    # ----------------------------------------------------------------------
    # [기존 로직 유지] 140GV 기준 계산
    # ----------------------------------------------------------------------
    UNIT_PRICE = 179700  # 1인당 월 평균 구매액
    UNIT_GV = 140        # 1인당 월 평균 포인트 (103 + 37)
    
    level_rates = [0.05, 0.03, 0.03, 0.03, 0.05, 0.05] # 레벨별 지급률
    
    # 1. 직추천 보너스
    direct_income = (my_partners * UNIT_PRICE) * 0.10
    
    level_income = 0
    total_partners = 0
    total_gv = 0
    partners_on_level = my_partners
    details_text = []

    # 2. 레벨 보너스 계산
    for i in range(generations):
        current_partners = my_partners if i == 0 else partners_on_level * duplication
        partners_on_level = current_partners
        
        current_sales = current_partners * UNIT_PRICE
        current_gv = current_partners * UNIT_GV
        
        rate = level_rates[i] if i < len(level_rates) else 0.02
        current_bonus = current_sales * rate
        
        total_partners += current_partners
        total_gv += current_gv
        level_income += current_bonus
        
        details_text.append(f"- **{i+1}대:** {current_partners:,}명 x {int(rate*100)}% = {int(current_bonus):,}원")

    total_income = direct_income + level_income
    
    # 3. 직급 및 보너스 산정
    rank, car_bonus, travel, badge_color = "매니저", 0, "없음", "gray"
    
    if total_gv >= 100000: rank, car_bonus, travel, badge_color = "PT", 650000, "✈️ 월드 투어 풀패키지", "#FFD700"
    elif total_gv >= 50000: rank, car_bonus, travel, badge_color = "EVP", 520000, "✈️ 윈터 리더십 여행", "#C0C0C0"
    elif total_gv >= 25000: rank, car_bonus, travel, badge_color = "VP", 288600, "✈️ 윈터 리더십 여행", "#CD7F32"
    elif total_gv >= 10000: rank, car_bonus, travel, badge_color = "IMM", 169000, "✈️ 유럽 여행 (초대)", "#2196F3"
    elif total_gv >= 5000: rank, badge_color = "MM", "#4CAF50"
    elif total_gv >= 2500: rank, badge_color = "SM", "#8BC34A"

    # 화면 표시
    st.markdown(f"#### 🏆 예상 달성 직급: <span style='color:{badge_color}; font-size:24px; font-weight:bold;'>{rank}</span>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f"<div style='border:1px solid #ddd; padding:10px; border-radius:10px; text-align:center;'><div style='font-size:14px; color:#666;'>🚗 카 보너스</div><div style='font-size:20px; font-weight:bold; color:#E91E63;'>{int(car_bonus):,} 원</div></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div style='border:1px solid #ddd; padding:10px; border-radius:10px; text-align:center;'><div style='font-size:14px; color:#666;'>✈️ 여행 보너스</div><div style='font-size:16px; font-weight:bold; color:#3F51B5;'>{travel}</div></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div style='border:1px solid #ddd; padding:10px; border-radius:10px; text-align:center; background-color:#E8F5E9;'><div style='font-size:14px; color:#666;'>💰 월 예상 수령액</div><div style='font-size:20px; font-weight:bold; color:#2E7D32;'>{int(total_income + car_bonus):,} 원</div></div>", unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3)
    with m1: st.metric("총 산하 파트너", f"{total_partners:,} 명")
    with m2: st.metric("총 예상 매출", f"{total_gv:,} P (GV)")
    with m3: st.metric("기본 후원 수당", f"{int(total_income):,} 원")
    
    with st.expander("🔍 수당 계산 상세 내역 보기 (기준: 140GV)"):
        st.write(f"**💡 1인당 기준:** 오토십(103GV) + 액티바이즈(37GV) = **140GV**")
        st.write(f"**(1) 직추천 보너스(10%):** {int(direct_income):,} 원")
        st.write(f"**(2) 레벨 보너스:** {int(level_income):,} 원")
        st.write("---")
        for line in details_text: st.write(line)
