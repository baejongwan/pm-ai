import streamlit as st

# 1. CSS 스타일 (시각적 중앙 정렬 보정)
def apply_custom_styles():
    st.markdown("""
        <style>
        /* [1] 숫자 입력칸 디자인 */
        div[data-testid="stNumberInput"] > div > div {
            background-color: #ffffff !important;
            border: 1px solid #c0c0c0 !important;
            border-radius: 8px !important;
            color: #333333 !important;
            box-shadow: none !important;
            align-items: center !important;
            padding-right: 0 !important;
        }

        /* [2] 숫자 텍스트 */
        div[data-testid="stNumberInput"] input {
            background-color: #ffffff !important;
            color: #333333 !important;
            text-align: center !important;
            font-size: 20px !important;
            font-weight: bold !important;
            padding: 0px !important;
        }

        /* [3] +/- 조절 버튼 */
        div[data-testid="stNumberInput"] button {
            background-color: transparent !important;
            border: none !important;
            color: #555555 !important;
            font-size: 18px !important;
            border-left: 1px solid #f0f0f0 !important;
            width: 30px !important; /* 버튼 너비 강제 고정 (계산을 위해) */
        }
        div[data-testid="stNumberInput"] button:active {
            background-color: #f0f0f0 !important;
        }

        /* [4] ★ 제목(Label) 시각적 중앙 정렬 보정 ★ */
        .custom-label {
            text-align: center !important;
            font-weight: bold;
            font-size: 15px;
            color: #333;
            margin-bottom: 2px !important;
            
            /* 핵심: 오른쪽에 버튼만큼의 여백을 줘서 중심을 왼쪽(흰색칸)으로 당김 */
            padding-right: 65px !important; 
        }

        /* [5] ★ 단위(Unit) 시각적 중앙 정렬 보정 ★ */
        .unit-caption { 
            text-align: center !important;
            font-size: 14px;
            font-weight: 600;
            color: #555;
            margin-top: -2px !important;
            margin-bottom: 10px !important;
            
            /* 핵심: 제목과 동일하게 오른쪽 여백 추가 */
            padding-right: 65px !important; 
        }
        
        /* 모바일에서는 버튼 크기가 조금 달라질 수 있으므로 미세 조정 */
        @media (max-width: 640px) {
            .custom-label, .unit-caption {
                padding-right: 60px !important; /* 모바일 최적화 */
            }
        }
        </style>
    """, unsafe_allow_html=True)


# 2. 숫자 조절 컴포넌트
def number_counter(label, key, default_val, min_val, max_val, unit=""):
    if key not in st.session_state:
        st.session_state[key] = default_val

    # [제목] (오른쪽 여백이 적용된 클래스 사용)
    st.markdown(f"<div class='custom-label'>{label}</div>", unsafe_allow_html=True)
    
    # [숫자 입력칸]
    val = st.number_input(
        label=label,
        label_visibility="collapsed",
        min_value=min_val,
        max_value=max_val,
        value=default_val,
        step=1,
        key=key
    )

    # [단위] (오른쪽 여백이 적용된 클래스 사용)
    if unit:
        st.markdown(f"<div class='unit-caption'>{unit}</div>", unsafe_allow_html=True)
    
    return val
