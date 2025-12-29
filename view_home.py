import streamlit as st
import random
import os
import pandas as pd 
from utils import get_optimized_image
from func import get_sheet_data, get_daily_visitor_count 
from config import FAMILY_IDS 

# --------------------------------------------------------------------------
# [1] 관리자용 로그 확인 함수
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
# [2] 메인 홈 화면 렌더링
# --------------------------------------------------------------------------
def render_home_dashboard(all_sheets):
    
    # [0] 방문자 수
    if "cached_visitor_count" not in st.session_state:
        st.session_state.cached_visitor_count = get_daily_visitor_count()
        
    visitor_count = st.session_state.cached_visitor_count

    st.markdown(f"""
        <div style="text-align:center; padding: 5px 0 15px 0;">
            <span style="color:#2E7D32; font-weight:bold; font-size:13px;">
                🌿 오늘의 방문자 : {visitor_count}명
            </span>
        </div>
    """, unsafe_allow_html=True)

    # [1] 추천인 정보
    if "random_sponsor" not in st.session_state:
        try: st.session_state.random_sponsor = random.choice(FAMILY_IDS)
        except: st.session_state.random_sponsor = {"name": "김피엠", "id": "12345678"}
            
    sponsor = st.session_state.random_sponsor

    st.markdown(f"""
        <div class="sponsor-container">
            <div class="sponsor-top">
                <span class="sponsor-name">✨ 당신의 성공 파트너: {sponsor['name']} ({sponsor['id']})</span>
                <span class="sponsor-desc">PM-International Team Partner</span>
            </div>
            <div class="sponsor-bottom">
                <a href="https://m.pmi-korea.com/member/join/step01.do" target="_blank" class="join-btn">
                    회원가입 바로가기 🔗
                </a>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # [2] 메인 비주얼 배너
    st.markdown("""
        <div class="main-visual">
            <h1>FitLine: 건강한 삶을 위한 최고의 선택</h1>
            <p>독일 프리미엄 건강기능식품의 놀라운 효과를 경험해보세요.</p>
        </div>
    """, unsafe_allow_html=True)

    # [3] 주요 서비스 바로가기 (이미지 클릭 시 이동 기능 복구 완료)
    st.markdown('<div class="section-title">주요 서비스</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    # 1. AI 상담 (이미지 클릭 링크 복구)
    with col1:
        st.markdown("""
            <a href="?page=AI상담" target="_self" class="card-link">
                <div class="safety-card">
                    <div class="safety-img-box">
                        <img src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png" class="safety-img">
                    </div>
                    <div class="safety-title">AI 건강 상담</div>
                </div>
            </a>
        """, unsafe_allow_html=True)
        
    # 2. 수익 시뮬레이션 (이미지 클릭 링크 복구)
    with col2:
        st.markdown("""
            <a href="?page=수익계산" target="_self" class="card-link">
                <div class="safety-card">
                    <div class="safety-img-box">
                        <img src="https://cdn-icons-png.flaticon.com/512/5501/5501360.png" class="safety-img">
                    </div>
                    <div class="safety-title">수익 시뮬레이션</div>
                </div>
            </a>
        """, unsafe_allow_html=True)

    # 3. 액티바이즈 진단 (이미지 클릭 링크 복구)
    with col3:
        st.markdown("""
            <a href="?page=액티증상" target="_self" class="card-link">
                <div class="safety-card">
                    <div class="safety-img-box">
                        <img src="https://cdn-icons-png.flaticon.com/512/8454/8454230.png" class="safety-img">
                    </div>
                    <div class="safety-title">액티바이즈 진단</div>
                </div>
            </a>
        """, unsafe_allow_html=True)


    # ----------------------------------------------------------------------
    # [4] ★ 오늘의 아침 조회 (버튼 기능 유지) ★
    # ----------------------------------------------------------------------
    # 영상은 '더보기' 버튼을 눌러야 이동하는 것이 자연스러우므로 버튼 방식을 유지합니다.
    st.markdown('<div class="section-title">📺 오늘의 아침 조회</div>', unsafe_allow_html=True)

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
                        st.error("영상 링크가 올바르지 않습니다.")
                    
                    # 제목과 더보기 버튼
                    v_col1, v_col2 = st.columns([3, 1])
                    with v_col1:
                        st.write(f"**{v_title}**")
                        st.caption(f"📅 {v_date}")
                    with v_col2:
                        st.write("") 
                        # 여기는 아까 수정해드린 버튼 방식을 유지합니다 (잘 작동하니까요!)
                        if st.button("더보기 >", key="btn_more_videos"):
                            st.session_state.page = "영상자료"
                            st.rerun()
                            
            except Exception as e:
                st.error("영상 정보를 불러오는 중 오류가 발생했습니다.")
        else:
            st.info("등록된 최신 영상이 없습니다.")
    else:
        st.info("아직 '아침방송' 데이터가 없습니다.")


    # [5] 제품 안전성 인증 (이미지 클릭 링크 복구)
    st.markdown('<div class="section-title">제품 안전성 인증</div>', unsafe_allow_html=True)
    
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

                # 예전처럼 <a href> 태그를 사용하여 이미지를 클릭하면 이동하도록 수정
                st.markdown(f"""
                    <a href="?page=안전성" target="_self" class="card-link">
                        <div class="safety-card">
                            <div class="safety-img-box"><img src="{img_src}" class="safety-img"></div>
                            <div class="safety-title">{item.get('인증제목', '인증마크')}</div>
                        </div>
                    </a>
                """, unsafe_allow_html=True)

    # [6] FitLine 인기 제품 (이미지 클릭 링크 복구)
    st.markdown('<div class="section-title">FitLine 인기 제품</div>', unsafe_allow_html=True)
    
    target_prod = get_sheet_data(all_sheets, "제품설명")
    if target_prod is not None:
        df = target_prod.fillna("").head(4) 
        p_cols = st.columns(2)
        for i, (idx, item) in enumerate(df.iterrows()):
            with p_cols[i % 2]:
                img_src = get_optimized_image(item.get('이미지주소', ''))
                # 예전처럼 <a href> 태그를 사용하여 이미지를 클릭하면 이동하도록 수정
                st.markdown(f"""
                    <a href="?page=제품구매" target="_self" class="card-link">
                        <div class="shop-item">
                            <div class="shop-img-box"><img src="{img_src}" class="shop-img"></div>
                            <div class="shop-info">
                                <div class="shop-title">{item.get('제품명','-')}</div>
                                <div class="shop-desc">{item.get('한줄소개','FitLine Premium')}</div>
                            </div>
                        </div>
                    </a>
                """, unsafe_allow_html=True)
                
    # 제품 전체보기 버튼 (이건 버튼이 편하실 것 같아 유지합니다)
    if st.button("제품 전체보기 >", use_container_width=True):
        st.session_state.page = "제품구매"
        st.rerun()
            
    # [7] 고객서비스
    st.markdown('<div class="section-title">고객 서비스</div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="cs-box">
            <a href="https://www.pmi-korea.com/story/company/about/page.do" target="_blank" class="cs-item">
                <span class="cs-icon">🏢</span>
                <span class="cs-text">About PM</span>
            </a>
            <a href="https://www.pmi-korea.com/story/customer/csCenter/page.do" target="_blank" class="cs-item">
                <span class="cs-icon">🎧</span>
                <span class="cs-text">고객센터</span>
            </a>
            <a href="https://www.pmi-korea.com/story/pm/news/list.do" target="_blank" class="cs-item">
                <span class="cs-icon">📰</span>
                <span class="cs-text">보도자료</span>
            </a>
        </div>
    """, unsafe_allow_html=True)

    # [8] 관리자 로그 확인 기능 실행
    render_admin_logs()
