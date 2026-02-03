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
    from config import LANG_CONFIG
    lang_code = st.session_state.get("selected_lang", "KR")
    ui = LANG_CONFIG[lang_code]["ui"]

    st.markdown(f"<h2 style='text-align:center;'>🤖 {ui['ai_title']}</h2>", unsafe_allow_html=True)

    # --- [단계 1] 사용자 정보 입력 폼 ---
    if "user_info" not in st.session_state:
        st.markdown(f"""
            <div style="background-color:#f8f9fa; padding:20px; border-radius:15px; border:1px solid #eee; margin-bottom:20px;">
                <h4 style="text-align:center; margin-bottom:15px;">{ui['ai_sub']}</h4>
                <p style="text-align:center; color:#666; font-size:14px;">{ui['ai_desc']}</p>
            </div>
        """, unsafe_allow_html=True)

        with st.form("user_info_form"):
            c1, c2 = st.columns(2)
            with c1:
                age = st.number_input(ui["age"], min_value=10, max_value=100, step=1, value=40)
            with c2:
                gender = st.radio(ui["gender"], [ui["gen_f"], ui["gen_m"]], horizontal=True)
            
            st.markdown(f"**{ui['search']}**")
            condition_input = st.text_input("label_hidden", placeholder="Enter...", label_visibility="collapsed")
            
            if st.form_submit_button(ui["start_ai"], use_container_width=True, type="primary"):
                final_condition = condition_input.strip() if condition_input.strip() else "-"
                # 세션에 정보 저장 (현재 선택된 언어 코드도 함께 저장)
                st.session_state.user_info = {
                    "age": age, 
                    "gender": gender, 
                    "conditions": [final_condition],
                    "language": lang_code  # 현재 앱 언어 설정을 따름
                }
                st.rerun()
        return

    # --- [단계 2] 채팅 화면 ---
    user_info = st.session_state.user_info
    
    # [수정 포인트] .get()을 사용하여 language가 없어도 에러가 나지 않게 방어
    u_lang = user_info.get("language", lang_code)
    u_age = user_info.get("age", "-")
    u_gender = user_info.get("gender", "-")
    u_cond = ", ".join(user_info.get("conditions", []))
    
    # 프로필 정보 표시 (다국어 대응)
    profile_label = "프로필" if lang_code == "KR" else "Profile"
    info_text = f"{u_age} | {u_gender} | {u_cond} ({u_lang})"
    st.info(f"✅ **{profile_label}:** {info_text}")
    
    # 대화 기록 초기화
    if "messages" not in st.session_state:
        greetings = {
            "KR": f"안녕하세요! {MAIN_CONTACT_NAME} 산하 AI 비서입니다. 궁금한 점을 말씀해 주세요.",
            "EN": f"Hello! I am the AI assistant for {MAIN_CONTACT_NAME}. How can I help you?",
            "CH": f"你好！我是 {MAIN_CONTACT_NAME} 旗下的 AI 助手。有什么可以帮您的？",
            "TH": f"สวัสดีครับ ผมคือผู้ช่วย AI ของคุณ {MAIN_CONTACT_NAME} มีอะไรให้ช่วยไหมครับ?"
        }
        greeting = greetings.get(lang_code, greetings["EN"])
        st.session_state.messages = [{"role": "assistant", "content": greeting}]
    
    # 대화 기록 출력
    for message in st.session_state.messages:
        role_icon = "👤" if message["role"] == "user" else "🤖"
        with st.chat_message(message["role"], avatar=role_icon): 
            st.markdown(message["content"])
            
    # 질문 입력 및 AI 답변 생성
    chat_placeholder = ui.get("search", "Enter your question...")
    if prompt := st.chat_input(chat_placeholder):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"): 
            st.markdown(prompt)
        
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Analyzing..."):
                # 1. 엑셀 데이터 컨텍스트 생성
                context_text = ""
                if all_sheets:
                    for sheet_name, df in all_sheets.items():
                        # 데이터가 너무 크면 모델 토큰 제한에 걸릴 수 있으므로 50행으로 제한
                        summary = df.astype(str).head(50).to_string(index=False)
                        context_text += f"\n--- [{sheet_name}] ---\n{summary}\n"

                # 2. 강력한 시스템 프롬프트 구성 (요청사항 반영)
                full_prompt = f"""
                당신은 'PM 인터내셔널'의 최고위급 건강 컨설턴트입니다.
                
                [사용자 프로필]
                - 연령/성별: {user_info['age']}세 {user_info['gender']}
                - 관심사: {', '.join(user_info['conditions'])}

                [답변 작성 절대 원칙]
                1. **인사말 금지:** "안녕하세요", "반갑습니다", "감사합니다" 같은 모든 인사말을 **절대** 하지 마세요. 질문에 대한 **결론부터 즉시** 답변하세요.
                2. **전문성 및 구조화:** 답변은 전문가처럼 확신에 찬 어조로 작성하세요. 가독성을 위해 **글머리 기호(Bullets)**나 **볼드체**를 적극 사용하세요.
                3. **데이터 활용:** - 제공된 [내부 데이터베이스]에 답이 있다면 그 수치와 근거를 정확히 인용하세요.
                    - 데이터에 직접적인 답이 없다면, 당신이 가진 **일반적인 영양학/생리학/비즈니스 전문 지식**을 활용하여 최고 수준의 답변을 제공하세요. 
                    - "데이터가 없습니다"라고 말하지 말고, 외부 지식으로 해결하세요.
                4. **공감과 맞춤:** 사용자의 연령과 건강 관심사를 고려하여, 그들에게 실질적인 도움이 되는 조언을 덧붙이세요.
                5. **언어 준수:** 사용자가 선택한 언어({user_info.get('language', 'KR')})로 답변하세요.

                [내부 데이터베이스]
                {context_text}

                [사용자 질문]
                {prompt}
                """
                
                # AI 답변 생성
                raw_response = get_safe_response(full_prompt, api_key, selected_model)
                
                # 하단에 연락처 정보만 깔끔하게 추가
                footer_msg = f"\n\n---\n📞 **Contact**: {MAIN_CONTACT_NAME} ({MAIN_CONTACT_PHONE})"
                final_response = raw_response + footer_msg
                
                st.markdown(final_response)
                
                # 로그 저장 (선택 사항)
                try:
                    save_user_log(user_info, prompt, final_response)
                except:
                    pass
                
        # 대화 기록에 저장
        st.session_state.messages.append({"role": "assistant", "content": final_response})