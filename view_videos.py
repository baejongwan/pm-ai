import streamlit as st
import pandas as pd

def render_video_page(all_sheets):
    st.title("📺 PM 영상 자료실")
    st.caption("매일 아침 조회 및 주요 교육 영상을 확인하세요.")
    st.divider()

    # 1. 엑셀에서 '아침방송' 시트 데이터 가져오기
    # (데이터가 없거나 시트 이름이 틀렸을 때를 대비한 안전장치)
    if all_sheets is None or "아침방송" not in all_sheets:
        st.info("📂 아직 등록된 영상 데이터가 없습니다. (엑셀 '아침방송' 시트 확인)")
        return

    df = all_sheets["아침방송"]

    # 2. 데이터가 비어있는지 확인
    if df.empty:
        st.info("📭 등록된 영상이 없습니다.")
        return

    # 3. 최신 날짜가 위로 오도록 정렬 (날짜 형식이 올바르다면)
    try:
        df = df.sort_values(by="날짜", ascending=False)
    except:
        pass # 날짜 형식이 아니면 그냥 엑셀 순서대로 보여줌

    # 4. 영상 목록 보여주기 (2단 그리드 디자인)
    # 모바일에서도 보기 좋게 2열로 배치합니다.
    cols = st.columns(2) 
    
    for index, row in df.iterrows():
        # 왼쪽, 오른쪽 번갈아가며 배치
        with cols[index % 2]:
            with st.container(border=True): # 깔끔한 카드 디자인
                # 유튜브 영상 플레이어
                video_url = str(row.get("링크", "")).strip()
                
                if "http" in video_url:
                    st.video(video_url)
                else:
                    st.error("잘못된 링크입니다.")

                # 영상 제목 및 날짜
                st.write(f"**{row.get('설명', '제목 없음')}**")
                st.caption(f"📅 {row.get('날짜', '-')}")
