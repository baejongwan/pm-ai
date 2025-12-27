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
        # 모델 이름에서 models/ 접두사 제거 (혹시 있을 경우)
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
    # [방어 로직 1] 이미 입력한 정보가 세션에 있다면 입력 폼을 건너뜁니다.
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
                # 세션에 저장 (페이지 이동해도 유지)
                st.session_state.user_info = {"age": age, "gender": gender, "conditions": [final_condition]}
                st.rerun()
        return

    # --- 채팅 화면 ---
    user_info = st.session_state.user_info
    info_text = f"{user_info['age']}세 {user_info['gender']}, 관심사: {', '.join(user_info['conditions'])}"
    st.info(f"✅ **프로필:** {info_text}")
    
    # [방어 로직 2] 대화 기록이 아예 없을 때만(최초 1회) 생성합니다.
    # 이미 대화 내용이 있다면 이 부분은 무시하고 지나갑니다 (초기화 방지).
    if "messages" not in st.session_state:
        # 최초 1회만 정중하게 인사
        greeting = f"안녕하세요! {MAIN_CONTACT_NAME} 산하 AI 전문 비서입니다.\n건강이나 제품에 대해 궁금한 점을 말씀해 주세요."
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
            with st.spinner("전문 데이터 분석 및 답변 작성 중..."):
                
                # ---------------------------------------------------------
                # 1. 엑셀 데이터 컨텍스트화
                # ---------------------------------------------------------
                context_text = ""
                
                if all_sheets:
                    # 질의응답 시트 우선 처리
                    if "질의응답" in all_sheets:
                        qa_df = all_sheets["질의응답"]
                        qa_text = qa_df.astype(str).head(100).to_string(index=False)
                        context_text += f"\n[🔥🔥 핵심 질의응답 데이터 (우선순위 높음)]\n{qa_text}\n"
                    
                    # 나머지 시트 처리
                    for sheet_name, df in all_sheets.items():
                        if sheet_name == "질의응답": continue
                        summary = df.astype(str).head(30).to_string(index=False)
                        context_text += f"\n--- [{sheet_name} 데이터] ---\n{summary}\n"

                # ---------------------------------------------------------
                # 2. 강력한 시스템 프롬프트 (인사 생략 + 전문성 강화)
                # ---------------------------------------------------------
                full_prompt = f"""
                당신은 'PM 인터내셔널'의 최고위급 건강 컨설턴트입니다.
                
                [사용자 프로필]
                - 연령/성별: {user_info['age']}세 {user_info['gender']}
                - 관심사: {', '.join(user_info['conditions'])}

                [답변 작성 절대 원칙]
                1. **인사말 금지:** "안녕하세요", "반갑습니다" 같은 인사를 **절대** 하지 마세요. 질문에 대한 **결론부터 즉시** 답변하세요.
                2. **전문성 및 구조화:** 답변은 전문가처럼 확신에 찬 어조로 작성하세요. 가독성을 위해 **글머리 기호(Bullets)**나 **볼드체**를 적극 사용하세요.
                3. **데이터 활용:** - 제공된 [내부 데이터베이스]에 답이 있다면 그 수치와 근거를 정확히 인용하세요.
                    - 데이터가 없다면, 당신이 가진 **일반적인 영양학/생리학/비즈니스 전문 지식**을 활용하여 최고 수준의 답변을 제공하세요. "데이터가 없습니다"라고 말하지 말고, 외부 지식으로 해결하세요.
                4. **공감과 맞춤:** 사용자의 연령과 건강 관심사를 고려하여, 그들에게 실질적인 도움이 되는 조언을 덧붙이세요.

                [내부 데이터베이스]
                {context_text}

                [사용자 질문]
                {prompt}
                """
                
                # AI 답변 생성
                raw_response = get_safe_response(full_prompt, api_key, selected_model)
                
                # ---------------------------------------------------------
                # 3. 문의처 강제 부착 (Python 레벨에서 처리)
                # ---------------------------------------------------------
                # AI가 생성한 답변 뒤에 무조건 연락처를 붙입니다.
                footer_msg = f"\n\n---\n📞 **추가 문의 및 상담**: {MAIN_CONTACT_NAME} ({MAIN_CONTACT_PHONE})"
                final_response = raw_response + footer_msg
                
                # 화면 출력
                st.markdown(final_response)
                
                # 로그 저장 및 대화 기록 (한국 시간 함수 적용됨 - func.py에서)
                try: save_user_log(user_info, prompt, final_response)
                except: pass
                
        st.session_state.messages.append({"role": "assistant", "content": final_response})
