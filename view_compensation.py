import streamlit as st
from utils import get_optimized_image
from components import apply_custom_styles
from config import LANG_CONFIG

# --------------------------------------------------------------------------
# [1] 보상플랜 핵심요약 페이지 (제목 번역 수정 완료)
# --------------------------------------------------------------------------
def render_compensation(all_sheets):
    apply_custom_styles()
    
    # 세션에서 언어 코드를 가져와 해당 언어의 UI 설정을 로드합니다.
    lang_code = st.session_state.get("selected_lang", "KR")
    ui = LANG_CONFIG.get(lang_code, LANG_CONFIG["KR"])["ui"]
    
    # [수정] "보상플랜 핵심요약" 글자를 삭제하고 변수를 넣습니다.
    page_title = ui.get("comp_title", "Compensation Plan Summary") 
    st.markdown(f"## 📚 {page_title}")
    
    target_sheet = all_sheets.get('보상플랜') if all_sheets else None
    
    if target_sheet is not None:
        df = target_sheet.fillna("")
        for index, row in df.iterrows():
            title = row.get('제목', f"Info {index+1}")
            content = row.get('내용', '-')
            youtube_link = row.get('유튜브')
            
            with st.expander(f"💎 {title}", expanded=True):
                st.write(content)
                if youtube_link and str(youtube_link).startswith('http'): 
                    st.video(str(youtube_link))
                
                img_list = []
                for i in range(1, 5): 
                    if f"이미지{i}" in row and row[f"이미지{i}"]:
                        img_path = get_optimized_image(row[f"이미지{i}"])
                        if "flaticon" not in img_path: 
                            img_list.append(img_path)
                
                if img_list:
                    cols = st.columns(len(img_list))
                    for idx, img_src in enumerate(img_list):
                        with cols[idx]: 
                            st.image(img_src, use_container_width=True)
    else:
        st.info("No data found.")

# --------------------------------------------------------------------------
# [2] 수익 시뮬레이터 (유럽 여행 및 모든 문구 다국어화)
# --------------------------------------------------------------------------
def render_calculator_v2():
    apply_custom_styles()
    
    # [다국어 설정 로드]
    lang_code = st.session_state.get("selected_lang", "KR")
    lang_info = LANG_CONFIG.get(lang_code, LANG_CONFIG["KR"])
    ui = lang_info.get("ui", {})
    
    # UI 텍스트 변수 바인딩
    page_title = ui.get("calc_title", "Income Simulation")
    calc_sub = ui.get("calc_sub", "Simulation Criteria")
    
    label_partners = ui.get("label_partners", "1️⃣ Direct Partners")
    label_duplication = ui.get("label_duplication", "2️⃣ Duplication")
    label_depth = ui.get("label_depth", "3️⃣ Depth")
    
    unit_person = ui.get("unit_person", "명")
    unit_intro = ui.get("unit_intro", "명씩 소개")
    unit_level = ui.get("unit_level", "세대(Level)")
    
    res_rank_title = ui.get("res_rank_title", "🏆 Target Rank")
    res_car_bonus = ui.get("res_car_bonus", "🚗 Car Bonus")
    res_travel_bonus = ui.get("res_travel_bonus", "✈️ Travel Bonus")
    res_monthly_income = ui.get("res_monthly_income", "💰 Estimated Monthly Income")
    
    res_total_partners = ui.get("res_total_partners", "Total Partners")
    res_total_gv = ui.get("res_total_gv", "Total Sales")
    res_base_bonus = ui.get("res_base_bonus", "Base Bonus")
    detail_view = ui.get("detail_view", "🔍 Detailed Breakdown")
    
    currency = "원" if lang_code == "KR" else "KRW"

    st.markdown(f"## 💸 {page_title}")
    
    # 가이드 문구 상세 처리
    guide_info = {
        "KR": """
        1. **1인당 소비:** 오토십(103GV) + 액티바이즈(37GV) = **총 140GV**
        2. **보상 기준:** 직추천 10%, 레벨보너스(5~3%) 적용
        3. **실제 소득은 월 예상 수령액보다 더 높은 수익을 받습니다.**
        """,
        "CH": """
        1. **每人消费:** ABO(103GV) + Activize(37GV) = **总计 140GV**
        2. **奖励标准:** 直接推荐 10%, 层级奖金 (5~3%)
        3. **实际收入会比预计月收入更高。**
        """,
        "TH": """
        1. **การบริโภคต่อคน:** ออโต้ชิป(103GV) + แอคทิไวซ์(37GV) = **รวม 140GV**
        2. **เกณฑ์การตอบแทน:** แนะนำตรง 10%, โบนัสตามชั้น (5~3%)
        3. **รายได้จริงจะสูงกว่ารายได้ต่อเดือนโดยประมาณ**
        """,
        "EN": """
        1. **Consumption per person:** Autoship(103GV) + Activize(37GV) = **Total 140GV**
        2. **Compensation:** 10% Direct referral, Level bonus (5~3%)
        3. **Actual income is higher than the estimated monthly amount.**
        """
    }
    
    # 안내창 출력
    st.info(f"**{calc_sub}**\n\n{guide_info.get(lang_code, guide_info['EN'])}")
    st.markdown("---")
    # 입력창 레이아웃
    label_style = "text-align: center; font-weight: 800; font-size: 1.0em; color: #000; padding-right: 4rem; margin-bottom: -3px;"
    unit_style = "text-align: center; font-weight: 800; font-size: 0.80em; color: #444; padding-right: 4rem; margin-top: -25px;"

    if "my_partners_val" not in st.session_state: st.session_state["my_partners_val"] = 3
    if "duplication_val" not in st.session_state: st.session_state["duplication_val"] = 3
    if "generations_val" not in st.session_state: st.session_state["generations_val"] = 4

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"<div style='{label_style}'>{label_partners}</div>", unsafe_allow_html=True)
        my_partners = st.number_input("P1", min_value=1, max_value=20, key="my_partners_val", label_visibility="collapsed")
        st.markdown(f"<div style='{unit_style}'>{unit_person}</div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div style='{label_style}'>{label_duplication}</div>", unsafe_allow_html=True)
        duplication = st.number_input("P2", min_value=1, max_value=10, key="duplication_val", label_visibility="collapsed")
        st.markdown(f"<div style='{unit_style}'>{unit_intro}</div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div style='{label_style}'>{label_depth}</div>", unsafe_allow_html=True)
        generations = st.number_input("P3", min_value=1, max_value=6, key="generations_val", label_visibility="collapsed")
        st.markdown(f"<div style='{unit_style}'>{unit_level}</div>", unsafe_allow_html=True)
    
    st.markdown("---")

    # [계산 로직]
    UNIT_PRICE = 179700 
    UNIT_GV = 140       
    level_rates = [0.05, 0.03, 0.03, 0.03, 0.05, 0.05]
    
    direct_income = (my_partners * UNIT_PRICE) * 0.10
    level_income, total_partners, total_gv = 0, 0, 0
    partners_on_level = my_partners
    details_html = ""

    for i in range(generations):
        current_partners = my_partners if i == 0 else partners_on_level * duplication
        partners_on_level = current_partners
        rate = level_rates[i] if i < 6 else 0.02
        current_bonus = (current_partners * UNIT_PRICE) * rate
        total_partners += current_partners
        total_gv += (current_partners * UNIT_GV)
        level_income += current_bonus
        details_html += f"<li>{i+1}{ui.get('unit_gen', '대')}: {current_partners:,}{unit_person} x {int(rate*100)}% = {int(current_bonus):,} {currency}</li>"

    total_income = direct_income + level_income

    # [결과 판정 및 "유럽 여행" 번역]
    rank_names = ui.get("rank_names", {"PT": "PT", "EVP": "EVP", "VP": "VP", "IMM": "IMM", "MM": "MM", "SM": "SM", "M": "Manager"})
    
    travel_info = {
        "KR": {"WT": "✈️ 월드 투어", "WLC": "✈️ 윈터 리더십", "EURO": "✈️ 유럽 여행", "NONE": "없음"},
        "CH": {"WT": "✈️ 世界巡回赛", "WLC": "✈️ 冬季领导力", "EURO": "✈️ 欧洲之旅", "NONE": "无"},
        "TH": {"WT": "✈️ เวิลด์ทัวร์", "WLC": "✈️ วินเทอร์ ลีดเดอร์ชิพ", "EURO": "✈️ ยุโรปทัวร์", "NONE": "ไม่มี"},
        "EN": {"WT": "✈️ World Tour", "WLC": "✈️ Winter Leadership", "EURO": "✈️ Europe Tour", "NONE": "None"}
    }
    curr_travel = travel_info.get(lang_code, travel_info["EN"])

    rank, car_bonus, travel, badge_color = rank_names["M"], 0, curr_travel["NONE"], "gray"
    if total_gv >= 100000: rank, car_bonus, travel, badge_color = rank_names["PT"], 650000, curr_travel["WT"], "#FFD700"
    elif total_gv >= 50000: rank, car_bonus, travel, badge_color = rank_names["EVP"], 520000, curr_travel["WLC"], "#C0C0C0"
    elif total_gv >= 25000: rank, car_bonus, travel, badge_color = rank_names["VP"], 288600, curr_travel["WLC"], "#CD7F32"
    elif total_gv >= 10000: rank, car_bonus, travel, badge_color = rank_names["IMM"], 169000, curr_travel["EURO"], "#2196F3"
    elif total_gv >= 5000: rank, badge_color = rank_names["MM"], "#4CAF50"
    elif total_gv >= 2500: rank, badge_color = rank_names["SM"], "#8BC34A"

    # [결과 카드 섹션 출력]
    st.markdown(f"#### {res_rank_title}: <span style='color:{badge_color}; font-size:24px; font-weight:bold;'>{rank}</span>", unsafe_allow_html=True)
    
    col_card = st.columns(3)
    with col_card[0]:
        st.markdown(f"""<div style='border:1px solid #ddd; padding:10px; border-radius:10px; text-align:center;'>
                        <div style='font-size:13px; color:#666;'>{res_car_bonus}</div>
                        <div style='font-size:18px; font-weight:bold; color:#E91E63;'>{int(car_bonus):,} {currency}</div>
                        </div>""", unsafe_allow_html=True)
    with col_card[1]:
        st.markdown(f"""<div style='border:1px solid #ddd; padding:10px; border-radius:10px; text-align:center;'>
                        <div style='font-size:13px; color:#666;'>{res_travel_bonus}</div>
                        <div style='font-size:14px; font-weight:bold; color:#3F51B5; min-height:21px;'>{travel}</div>
                        </div>""", unsafe_allow_html=True)
    with col_card[2]:
        st.markdown(f"""<div style='border:1px solid #ddd; padding:10px; border-radius:10px; text-align:center; background-color:#E8F5E9;'>
                        <div style='font-size:13px; color:#666;'>{res_monthly_income}</div>
                        <div style='font-size:18px; font-weight:bold; color:#2E7D32;'>{int(total_income + car_bonus):,} {currency}</div>
                        </div>""", unsafe_allow_html=True)

    st.write("") 
    m_cols = st.columns(3)
    m_cols[0].metric(res_total_partners, f"{total_partners:,} {unit_person}")
    m_cols[1].metric(res_total_gv, f"{total_gv:,} P (GV)")
    m_cols[2].metric(res_base_bonus, f"{int(total_income):,} {currency}")
    
    with st.expander(detail_view):
        direct_label = ui.get('res_direct_bonus', 'Direct Referral Bonus')
        level_label = ui.get('res_level_bonus', 'Level Bonus')
        st.markdown(f"""
        <div style="font-size:14px; line-height:1.6;">
            <b>(1) {direct_label}(10%):</b> {int(direct_income):,} {currency}<br>
            <b>(2) {level_label}:</b> {int(level_income):,} {currency}
            <hr style="margin:10px 0;"><ul>{details_html}</ul>
        </div>""", unsafe_allow_html=True)