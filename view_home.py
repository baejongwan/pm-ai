import streamlit as st
import random
import os
import pandas as pd 
from utils import get_optimized_image
from func import get_sheet_data, get_daily_visitor_count 
from config import FAMILY_IDS 

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
# [2] 메인 홈 화면 렌더링 (다국어 제목 지원 수정)
# --------------------------------------------------------------------------
def render_home_dashboard(all_sheets):
    # [다국어 지원] 현재 선택된 언어의 메뉴 텍스트 가져오기
    # app.py의 LANG_CONFIG 구조를 활용합니다.
    from config import LANG_CONFIG 
    
    lang_code = st.session_state.get("selected_lang", "KR")
    current_menu = LANG_CONFIG[lang_code]["menu"]
    welcome_text = LANG_CONFIG[lang_code]["welcome"]

    # [0] 방문자 수
    if "cached_visitor_count" not in st.session_state:
        st.session_state.cached_visitor_count = get_daily_visitor_count()
        
    visitor_count = st.session_state.cached_visitor_count

    # 방문자 텍스트 다국어화 (간이)
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

    # 회원가입 텍스트 다국어화
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
    """, unsafe_allow_html=True)

    # [2] 메인 비주얼 배너 (Welcome 문구 적용)
    st.markdown(f"""
        <div class="main-visual">
            <h1>{welcome_text}: FitLine</h1>
            <p>Premium Health & Nutrition from Germany</p>
        </div>
    """, unsafe_allow_html=True)

    # [3] 주요 서비스 바로가기 (제목 다국어화)
    service_label = "주요 서비스" if lang_code == "KR" else "Core Services"
    st.markdown(f'<div class="section-title">{service_label}</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    # 1. AI 상담 (메뉴 리스트 인덱스 1 활용)
    with col1:
        st.markdown(f"""
            <a href="?page={current_menu[1]}" target="_self" class="card-link">
                <div class="safety-card">
                    <div class="safety-img-box">
                        <img src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png" class="safety-img">
                    </div>
                    <div class="safety-title">{current_menu[1]}</div>
                </div>
            </a>
        """, unsafe_allow_html=True)
        
    # 2. 수익 시뮬레이션 (메뉴 리스트 인덱스 2 활용)
    with col2:
        st.markdown(f"""
            <a href="?page={current_menu[2]}" target="_self" class="card-link">
                <div class="safety-card">
                    <div class="safety-img-box">
                        <img src="https://cdn-icons-png.flaticon.com/512/5501/5501360.png" class="safety-img">
                    </div>
                    <div class="safety-title">{current_menu[2]}</div>
                </div>
            </a>
        """, unsafe_allow_html=True)

    # 3. 액티바이즈 진단 (메뉴 리스트 인덱스 6 활용)
    with col3:
        st.markdown(f"""
            <a href="?page={current_menu[6]}" target="_self" class="card-link">
                <div class="safety-card">
                    <div class="safety-img-box">
                        <img src="https://cdn-icons-png.flaticon.com/512/8454/8454230.png" class="safety-img">
                    </div>
                    <div class="safety-title">{current_menu[6]}</div>
                </div>
            </a>
        """, unsafe_allow_html=True)


    # ----------------------------------------------------------------------
    # [4] ★ 오늘의 아침 조회 (제목 다국어화) ★
    # ----------------------------------------------------------------------
    morning_label = current_menu[10] # "영상자료" 또는 "Videos"
    st.markdown(f'<div class="section-title">📺 {morning_label}</div>', unsafe_allow_html=True)

    if all_sheets and "아침방송" in all_sheets:
        video_df = all_sheets["아침방송"]
        
        if not video_df.empty:
            try:
                video_df = video_df.sort_values(by="날짜", ascending=False)
                latest_video = video_df.iloc[0] 
                
                v_link = str(latest_video.get("링크", "")).strip()
                v_title = latest_video.get("설명", "제목 없음")
                v_date = latest_video.get("날짜", "")

                with st.container(border=True):
                    if "http" in v_link:
                        st.video(v_link)
                    else:
                        st.error("Invalid Link")
                    
                    v_col1, v_col2 = st.columns([3, 1])
                    with v_col1:
                        st.write(f"**{v_title}**")
                        st.caption(f"📅 {v_date}")
                    with v_col2:
                        more_text = "더보기 >" if lang_code == "KR" else "More >"
                        if st.button(more_text, key="btn_more_videos"):
                            st.session_state.page = current_menu[10]
                            st.rerun()
                            
            except Exception as e:
                st.error("Error loading video info")
        else:
            st.info("No recent videos")
    else:
        st.info("No data")


    # [5] 제품 안전성 인증 (제목 다국어화)
    safety_label = current_menu[5] # "안전성" 또는 "Safety"
    st.markdown(f'<div class="section-title">{safety_label}</div>', unsafe_allow_html=True)
    
    target_safe = get_sheet_data(all_sheets, "안전성")
    safe_data = []
    
    if target_safe is not None:
        target_safe = target_safe.fillna("")
        safe_data = target_safe.head(3).to_dict('records')
    
    if not safe_data:
        safe_data = [
            {"인증제목": "TÜV SÜD", "이미지": "tuv.png"},
            {"인증제목": "쾰른 리스트", "이미지": "cologne.png"},
            {"인증제목": "GMP 인증", "이미지": "gmp.png"}
        ]

    s_cols = st.columns(3)
    for i, item in enumerate(safe_data):
        if i < 3:
            with s_cols[i]:
                img_src = get_optimized_image(item.get('이미지', ''))
                if "home_logo" in img_src or not img_src:
                      img_src = "https://cdn-icons-png.flaticon.com/512/1156/1156743.png"

                st.markdown(f"""
                    <a href="?page={safety_label}" target="_self" class="card-link">
                        <div class="safety-card">
                            <div class="safety-img-box"><img src="{img_src}" class="safety-img"></div>
                            <div class="safety-title">{item.get('인증제목', 'Certification')}</div>
                        </div>
                    </a>
                """, unsafe_allow_html=True)

    # [6] FitLine 인기 제품 (제목 다국어화)
    popular_label = current_menu[4] # "제품구매" 또는 "Products"
    st.markdown(f'<div class="section-title">FitLine {popular_label}</div>', unsafe_allow_html=True)
    
    target_prod = get_sheet_data(all_sheets, "제품설명")
    if target_prod is not None:
        df = target_prod.fillna("").head(4) 
        p_cols = st.columns(2)
        for i, (idx, item) in enumerate(df.iterrows()):
            with p_cols[i % 2]:
                img_src = get_optimized_image(item.get('이미지주소', ''))
                st.markdown(f"""
                    <a href="?page={popular_label}" target="_self" class="card-link">
                        <div class="shop-item">
                            <div class="shop-img-box"><img src="{img_src}" class="shop-img"></div>
                            <div class="shop-info">
                                <div class="shop-title">{item.get('제품명','-')}</div>
                                <div class="shop-desc">{item.get('한줄소개','FitLine Premium')}</div>
                            </div>
                        </div>
                    </a>
                """, unsafe_allow_html=True)
                
    view_all_text = "전체보기 >" if lang_code == "KR" else "View All >"
    if st.button(view_all_text, use_container_width=True):
        st.session_state.page = popular_label
        st.rerun()
            
    # [7] 고객서비스 (제목 다국어화)
    cs_label = "고객 서비스" if lang_code == "KR" else "Customer Service"
    st.markdown(f'<div class="section-title">{cs_label}</div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="cs-box">
            <a href="https://www.pmi-korea.com/story/company/about/page.do" target="_blank" class="cs-item">
                <span class="cs-icon">🏢</span>
                <span class="cs-text">About PM</span>
            </a>
            <a href="https://www.pmi-korea.com/story/customer/csCenter/page.do" target="_blank" class="cs-item">
                <span class="cs-icon">🎧</span>
                <span class="cs-text">CS Center</span>
            </a>
            <a href="https://www.pmi-korea.com/story/pm/news/list.do" target="_blank" class="cs-item">
                <span class="cs-icon">📰</span>
                <span class="cs-text">News</span>
            </a>
        </div>
    """, unsafe_allow_html=True)

    render_admin_logs()