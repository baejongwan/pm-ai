import streamlit as st
import google.generativeai as genai
from config import MAIN_CONTACT_NAME, MAIN_CONTACT_PHONE
from func import save_user_log

# [1] API 호출 함수 (안전 모드)
def get_safe_response(prompt, api_key, model_name):
    if not api_key:
        return "⚠️ API 키가 설정되지 않았습니다."
    
    try:
        genai.configure(api_key=api_key)
        safe_model_name = model_name.replace("models/", "")
        model = genai.GenerativeModel(safe_model_name)
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"⚠️ AI 연결 오류 발생: {str(e)}\n(모델: {safe_model_name})"

# [2] 메인 화면 및 로직
def render_ai_assistant(api_key, selected_model, all_sheets):
    st.markdown("<h2 style='text-align:center;'>🤖 PM AI 상담</h2>", unsafe_allow_html=True)

    # --- 사용자 정보 입력 폼 ---
    if "user_info" not in st.session_state:
        st.markdown("""
            <div style="background-color:#f8f9fa; padding:20px; border-radius:15px; border:1px solid #eee; margin-bottom:20px;">
                <h4 style="text-align:center; margin-bottom:15px;">📋 맞춤형 상담을 위한 정보 입력</h4>
                <p style="text-align:center; color:#666; font-size:14px;">
                    정보를 입력하시면 고객님의 건강 상태에 딱 맞는 답변을 드립니다.
                </p>
            </div>
        """, unsafe_allow_html=True)

        with st.form("user_info_form"):
            c1, c2 = st.columns(2)
            with c1:
                age = st.number_input("연령대 (세)", min_value=10, max_value=100, step=10, value=40)
            with c2:
                gender = st.radio("성별", ["여성", "남성"], horizontal=True)
            
            st.markdown("**건강 관심사, 상태 (예 : 당뇨/다이어트)**")
            condition_input = st.text_input("label_hidden", placeholder="입력 후 엔터", label_visibility="collapsed")
            
            if st.form_submit_button("상담 시작하기 🚀", use_container_width=True, type="primary"):
                final_condition = condition_input.strip() if condition_input.strip() else "특이사항 없음"
                st.session_state.user_info = {"age": age, "gender": gender, "conditions": [final_condition]}
                st.rerun()
        return

    # --- 채팅 화면 ---
    user_info = st.session_state.user_info
    info_text = f"{user_info['age']}세 {user_info['gender']}, 관심사: {', '.join(user_info['conditions'])}"
    st.info(f"✅ **프로필:** {info_text}")
    
    if "messages" not in st.session_state:
        greeting = f"안녕하세요! {MAIN_CONTACT_NAME} 산하 AI 비서입니다.\n무엇이든 물어보세요!"
        st.session_state.messages = [{"role": "assistant", "content": greeting}]
    
    # 이전 대화 출력
    for message in st.session_state.messages:
        role_icon = "👤" if message["role"] == "user" else "🤖"
        with st.chat_message(message["role"], avatar=role_icon): 
            st.markdown(message["content"])
            
    # --- 질문 입력 및 답변 생성 ---
    if prompt := st.chat_input("질문을 입력하세요..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"): 
            st.markdown(prompt)
        
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("데이터 분석 및 답변 작성 중..."):
                
                # ---------------------------------------------------------
                # [핵심 수정] 엑셀 데이터 문자열로 변환 (Q&A 시트 특별 대우)
                # ---------------------------------------------------------
                context_text = ""
                
                if all_sheets:
                    # 1. 질의응답(Q&A) 시트 먼저 찾아서 강력하게 주입
                    if "질의응답" in all_sheets:
                        qa_df = all_sheets["질의응답"]
                        # Q&A는 중요하니까 최대 100개까지 읽도록 설정 (필요시 조절)
                        qa_text = qa_df.astype(str).head(100).to_string(index=False)
                        context_text += f"\n[🔥🔥 핵심 질의응답 데이터 (선배 사업자 노하우)]\n{qa_text}\n"
                    
                    # 2. 나머지 시트들 (제품, 보상플랜 등) 추가
                    for sheet_name, df in all_sheets.items():
                        if sheet_name == "질의응답": continue # 위에서 이미 넣었으니 건너뜀
                        
                        # 일반 데이터는 30줄 정도만 요약해서 참고
                        summary = df.astype(str).head(30).to_string(index=False)
                        context_text += f"\n--- [{sheet_name} 데이터] ---\n{summary}\n"

                # ---------------------------------------------------------
                # 프롬프트 작성 (지침 강화)
                # ---------------------------------------------------------
                full_prompt = f"""
                당신은 'PM 인터내셔널' 사업을 돕는 유능하고 전문적인 AI 파트너입니다.
                
                [답변 원칙]
                1. **핵심 질의응답 우선:** [🔥🔥 핵심 질의응답 데이터]에 사용자의 질문과 유사한 사례가 있다면, 그 답변 내용을 최우선으로 참고하여 답변하세요. (실제 경험 데이터입니다.)
                2. **내부 데이터 기반:** 질문에 대한 답이 엑셀 데이터에 있다면 정확한 수치와 정보를 인용하세요.
                3. **맞춤형 답변:** 질문자는 {user_info['age']}세 {user_info['gender']}이며, '{', '.join(user_info['conditions'])}'에 관심이 있습니다. 이 정보를 반영해 공감하고 조언하세요.
                4. **스폰서 안내:** 해결되지 않는 전산/개인적인 문제는 스폰서({MAIN_CONTACT_NAME}, {MAIN_CONTACT_PHONE})에게 문의하라고 안내하세요.
                5. 비즈니스와 무관한 질문은 정중히 거절하세요.

                [참고할 엑셀 데이터베이스]
                {context_text}

                [사용자 질문]
                {prompt}
                """
                
                # AI 답변 생성
                response = get_safe_response(full_prompt, api_key, selected_model)
                st.markdown(response)
                
                try: save_user_log(user_info, prompt, response)
                except: pass
                
        st.session_state.messages.append({"role": "assistant", "content": response})
