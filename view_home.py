import streamlit as st
import random
import os
import pandas as pd 
from utils import get_optimized_image
from func import get_sheet_data, get_daily_visitor_count 
from config import FAMILY_IDS 

# --------------------------------------------------------------------------
# [0] 페이지 이동 함수 (세션 유지를 위해 st.rerun 활용)
# --------------------------------------------------------------------------
def navigate_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# --------------------------------------------------------------------------
# [1] 관리자용 로그 확인 함수 (기존 유지)
# --------------------------------------------------------------------------
def render_admin_logs():
    import pandas as pd
    from func import get_google_sheet_connection 

    st.markdown("---")
    with st.expander("🔐 관리자 전용: AI 상담 이력 보기 (구글 연동)"):
        password = st.text_input("관리자 비밀번호를 입력하세요", type="password", key="admin_pw_input")
        ADMIN_PASSWORD = "1234"
        
        if password == ADMIN_PASSWORD:
            st.success("✅ 관리자 인증 완료! (구글 시트 로딩 중...)")
            
            try:
                client = get_google_sheet_connection()
                if client:
                    sheet = client.open("PM_AI_상담이력").sheet1
                    data = sheet.get_all_records() 
                    
                    if data:
                        df = pd.DataFrame(data)
                        if "날짜시간" in df.columns:
                            df = df.sort_values(by="날짜시간", ascending=False)
                            
                        st.write(f"📊 총 **{len(df)}건**의 영구 저장된 기록이 있습니다.")
                        st.dataframe(df, use_container_width=True)
                        
                        csv_data = df.to_csv(index=False).encode('utf-8-sig')
                        st.download_button(
                            label="📥 엑셀 파일로 다운로드",
                            data=csv_data,
                            file_name="PM_상담_이력_구글연동.csv",
                            mime="text/csv"
                        )
                    else:
                        st.info("데이터는 연결되었으나, 아직 기록된 내용이 없습니다.")
                else:
                    st.error("구글 시트 연결에 실패했습니다.")
                    
            except Exception as e:
                st.error(f"데이터 로딩 중 오류 발생: {e}")
                
        elif password:
            st.error("⛔ 비밀번호가 틀렸습니다.")

# --------------------------------------------------------------------------
# [2] 메인 홈 화면 렌더링 (디자인 무조건 유지 + 언어 풀림 방지)
# --------------------------------------------------------------------------
def render_home_dashboard(all_sheets):
    from config import LANG_CONFIG 
    
    lang_code = st.session_state.get("selected_lang", "KR")
    current_menu = LANG_CONFIG[lang_code]["menu"]
    welcome_text = LANG_CONFIG[lang_code]["welcome"]

    # [0] 방문자 수
    if "cached_visitor_count" not in st.session_state:
        st.session_state.cached_visitor_count = get_daily_visitor_count()
    visitor_count = st.session_state.cached_visitor_count

    visitor_label = "오늘의 방문자" if lang_code == "KR" else "Daily Visitors"
    st.markdown(f"""
        <div style="text-align:center; padding: 5px 0 15px 0;">
            <span style="color:#2E7D32; font-weight:bold; font-size:13px;">
                🌿 {visitor_label} : {visitor_count}
            </span>
        </div>
    """, unsafe_allow_html=True)

    # [1] 추천인 정보
    if "random_sponsor" not in st.session_state:
        try: st.session_state.random_sponsor = random.choice(FAMILY_IDS)
        except: st.session_state.random_sponsor = {"name": "김피엠", "id": "12345678"}
    sponsor = st.session_state.random_sponsor

    join_text = "회원가입 바로가기" if lang_code == "KR" else "Join Now"
    partner_label = "당신의 성공 파트너" if lang_code == "KR" else "Your Success Partner"

    st.markdown(f"""
        <div class="sponsor-container">
            <div class="sponsor-top">
                <span class="sponsor-name">✨ {partner_label}: {sponsor['name']} ({sponsor['id']})</span>
                <span class="sponsor-desc">PM-International Team Partner</span>
            </div>
            <div class="sponsor-bottom">
                <a href="https://m.pmi-korea.com/member/join/step01.do" target="_blank" class="join-btn">
                    {join_text} 🔗
                </a>
            </div>
        </div>
        <div class="main-visual">
            <h1>{welcome_text}: FitLine</h1>
            <p>Premium Health & Nutrition from Germany</p>
        </div>
    """, unsafe_allow_html=True)

    # [3] 주요 서비스 바로가기 (디자인 유지 + 클릭 방식 수정)
    service_label = "주요 서비스" if lang_code == "KR" else "Core Services"
    st.markdown(f'<div class="section-title">{service_label}</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    # 1. AI 상담
    with col1:
        st.markdown(f"""
            <div class="safety-card">
                <div class="safety-img-box">
                    <img src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png" class="safety-img">
                </div>
                <div class="safety-title">{current_menu[1]}</div>
            </div>
        """, unsafe_allow_html=True)
        # 카드 아래에 투명하지 않지만 클릭하면 세션을 유지해주는 버튼 배치
        if st.button("CLICK 👆", key="btn_go_ai", use_container_width=True):
            navigate_to(current_menu[1])
        
    # 2. 수익 시뮬레이션
    with col2:
        st.markdown(f"""
            <div class="safety-card">
                <div class="safety-img-box">
                    <img src="https://cdn-icons-png.flaticon.com/512/5501/5501360.png" class="safety-img">
                </div>
                <div class="safety-title">{current_menu[2]}</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("CLICK 👆", key="btn_go_calc", use_container_width=True):
            navigate_to(current_menu[2])

    # 3. 액티바이즈 진단
    with col3:
        st.markdown(f"""
            <div class="safety-card">
                <div class="safety-img-box">
                    <img src="https://cdn-icons-png.flaticon.com/512/8454/8454230.png" class="safety-img">
                </div>
                <div class="safety-title">{current_menu[6]}</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("CLICK 👆", key="btn_go_act", use_container_width=True):
            navigate_to(current_menu[6])

    # [4] 오늘의 아침 조회 (기존 유지)
    morning_label = current_menu[10]
    st.markdown(f'<div class="section-title">📺 {morning_label}</div>', unsafe_allow_html=True)
    if all_sheets and "아침방송" in all_sheets:
        video_df = all_sheets["아침방송"]
        if not video_df.empty:
            try:
                video_df = video_df.sort_values(by="날짜", ascending=False)
                latest_video = video_df.iloc[0] 
                v_link = str(latest_video.get("링크", "")).strip()
                with st.container(border=True):
                    if "http" in v_link: st.video(v_link)
                    st.write(f"**{latest_video.get('설명', '제목 없음')}**")
                    if st.button("CLICK 👆 >", key="btn_more_videos"):
                        navigate_to(current_menu[10])
            except: pass

    # [5] 제품 안전성 인증 (카드 디자인 유지 + 세션 유지)
    safety_label = current_menu[5]
    st.markdown(f'<div class="section-title">{safety_label}</div>', unsafe_allow_html=True)
    target_safe = get_sheet_data(all_sheets, "안전성")
    safe_data = target_safe.head(3).to_dict('records') if target_safe is not None else []
    
    s_cols = st.columns(3)
    for i, item in enumerate(safe_data):
        with s_cols[i]:
            img_src = get_optimized_image(item.get('이미지', ''))
            st.markdown(f"""
                <div class="safety-card">
                    <div class="safety-img-box"><img src="{img_src}" class="safety-img"></div>
                    <div class="safety-title">{item.get('인증제목', 'Certification')}</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("CLICK 👆", key=f"btn_safe_{i}", use_container_width=True):
                navigate_to(safety_label)

    # [6] FitLine 인기 제품 (카드 디자인 유지 + 세션 유지)
    popular_label = current_menu[4] 
    st.markdown(f'<div class="section-title">FitLine {popular_label}</div>', unsafe_allow_html=True)
    target_prod = get_sheet_data(all_sheets, "제품설명")
    if target_prod is not None:
        df = target_prod.fillna("").head(4) 
        p_cols = st.columns(2)
        for i, (idx, item) in enumerate(df.iterrows()):
            with p_cols[i % 2]:
                img_src = get_optimized_image(item.get('이미지주소', ''))
                st.markdown(f"""
                    <div class="shop-item">
                        <div class="shop-img-box"><img src="{img_src}" class="shop-img"></div>
                        <div class="shop-info">
                            <div class="shop-title">{item.get('제품명','-')}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("CLICK 👆", key=f"btn_prod_{i}", use_container_width=True):
                    navigate_to(popular_label)
                
    render_admin_logs()
