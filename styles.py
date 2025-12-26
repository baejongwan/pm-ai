import streamlit as st

def apply_custom_css():
    st.markdown("""
    <style>
        /* [1] 기본 폰트 및 설정 */
        html, body, p, h1, h2, h3, h4, h5, h6, li, a, input, label, textarea, button {
            font-family: "Pretendard", "Malgun Gothic", "Apple SD Gothic Neo", sans-serif !important;
        }
        section[data-testid="stSidebar"] { display: none !important; }
        div[data-testid="collapsedControl"] { display: none !important; }
        div[data-testid="stAppViewContainer"] > section[data-testid="stMain"] > div[data-testid="stVerticalBlock"] {
            padding-top: 0rem;
        }

        /* [2] 상단 고정 네비게이션 바 (HTML 방식) */
        .nav-container {
            position: sticky; top: 0; z-index: 999;
            background-color: rgba(255, 255, 255, 0.95);
            padding: 15px 0; border-bottom: 1px solid #eee;
            backdrop-filter: blur(5px); margin-bottom: 20px;
            display: flex; justify-content: center; flex-wrap: wrap; gap: 8px;
        }

        /* 메뉴 링크 버튼 스타일 */
        .nav-link {
            text-decoration: none;
            background-color: #fff; 
            border: 1px solid #ddd;
            padding: 8px 16px; 
            border-radius: 20px;
            font-size: 14px; 
            font-weight: 600; 
            color: #555 !important;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05); 
            transition: all 0.2s;
            display: inline-block;
            margin-bottom: 5px;
        }

        .nav-link:hover {
            background-color: #f8f9fa; 
            border-color: #0d47a1;
            color: #0d47a1 !important; 
            transform: translateY(-2px);
        }

        /* 선택된 메뉴 스타일 (파란색 강조) */
        .nav-link.active {
            background-color: #0d47a1 !important; 
            color: white !important;
            border-color: #0d47a1 !important; 
            box-shadow: 0 4px 6px rgba(13, 71, 161, 0.3);
        }

        /* [삭제됨] 여기에 있던 라디오 버튼 스타일 코드가 성별 버튼을 망가뜨리고 있었습니다. 삭제 완료! */


        /* [3] 추천인 박스 */
        .sponsor-container { 
            background: white; border-radius: 15px; overflow: hidden; 
            box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 20px; border: 1px solid #eee;
        }
        .sponsor-top { background-color: #004494; padding: 20px; text-align: center; color: white; }
        .sponsor-name { font-size: 18px; font-weight: bold; color: white; display: block; margin-bottom: 5px; }
        .sponsor-desc { font-size: 13px; color: #bdcee8; }
        .sponsor-bottom { background-color: #f8f9fa; padding: 15px; text-align: center; border-top: 1px solid #eee; }
        .join-btn { 
            background-color: #00306b; color: white !important; 
            padding: 10px 25px; border-radius: 25px; 
            font-size: 14px; font-weight: bold; text-decoration: none; 
            display: inline-block; transition: all 0.2s; 
            box-shadow: 0 2px 5px rgba(0,48,107,0.2);
        }
        .join-btn:hover { transform: scale(1.05); background-color: #00224f; }

        /* [4] 메인 비주얼 */
        .main-visual {
            width: 100%;
            background: linear-gradient(90deg, #003057 0%, #0056b3 100%);
            color: white !important; padding: 25px 20px;
            text-align: center; border-radius: 15px; margin-bottom: 30px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }
        .main-visual h1 { font-size: 22px !important; font-weight: 700 !important; margin-bottom: 8px; color: white !important; }
        .main-visual p { color: #e0e0e0 !important; font-size: 14px; margin: 0; }

        /* [5] 카드 공통 스타일 */
        a.card-link { text-decoration: none; color: inherit; display: block; }
        
        .safety-card {
            background-color: #ffffff;
            border: 1px solid #e0e0e0; border-radius: 15px;
            padding: 20px 5px; text-align: center;
            height: 260px;
            display: flex; flex-direction: column;
            align-items: center; justify-content: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.03);
            margin-bottom: 15px; transition: transform 0.2s;
            cursor: pointer;
        }
        .safety-card:hover {
            transform: translateY(-5px); border-color: #004494;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        /* 이미지 박스 */
        .safety-img-box {
            width: 150px; height: 150px; margin-bottom: 15px;
            border-radius: 50%; background: #fff;
            display: flex; align-items: center; justify-content: center;
            border: 1px solid #f0f0f0; overflow: hidden;
            padding: 0px !important; 
        }
        .safety-img { 
            width: 95% !important; 
            height: 95% !important; 
            object-fit: contain; 
        }
        
        .safety-title { 
            font-size: 16px; font-weight: bold; color: #333; 
            height: 40px; display: flex; align-items: center; justify-content: center; 
        }

        /* [6] 섹션 제목 */
        .section-title { 
            font-size: 22px !important; font-weight: 800 !important; 
            margin: 40px 0 20px 0; border-left: 6px solid #003057; 
            padding-left: 15px; color: #333 !important; 
        }
        
        /* [7] 쇼핑 아이템 */
        .shop-item { border: 1px solid #eee; border-radius: 12px; overflow: hidden; background: white; margin-bottom: 20px; }
        .shop-img-box { width: 100%; height: 200px; display: flex; align-items: center; justify-content: center; border-bottom: 1px solid #f0f0f0; padding: 10px; }
        .shop-img { max-width: 100%; max-height: 100%; object-fit: contain; }
        .shop-info { padding: 15px; text-align: center; }
        .shop-title { font-size: 15px; font-weight: bold; margin-bottom: 5px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; color: #333; }
        .shop-desc { font-size: 13px; color: #888; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

        /* [8] 고객센터 */
        .cs-box { display: flex; justify-content: space-around; background-color: #f8f9fa; border-radius: 15px; padding: 20px; border: 1px solid #eee; }
        .cs-item { text-align: center; flex: 1; text-decoration: none; color: #333; transition: 0.2s; }
        .cs-item:hover { transform: scale(1.05); }
        .cs-icon { font-size: 30px; display: block; margin-bottom: 5px; }
        .cs-text { font-size: 14px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)
