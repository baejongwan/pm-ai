import streamlit as st
import os
import base64
from config import LANG_CONFIG

def render_pdf_viewer(file_name):
    # 1. 언어 설정 가져오기
    lang_code = st.session_state.get("selected_lang", "KR")
    ui = LANG_CONFIG[lang_code]["ui"]
    
    # 2. [오류 해결] ui에 'pdf_title'이 없을 경우를 대비한 안전 장치
    # 만약 config.py에 'pdf_title'이 없으면 기본값 "BA 자료실"을 사용합니다.
    page_title = ui.get('pdf_title', "📄 BA 자료실")
    download_label = ui.get('pdf_download', "📥 PDF 파일 다운로드 받기")
    
    st.markdown(f"<h2 style='text-align:center;'>{page_title}</h2>", unsafe_allow_html=True)
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, file_name)

    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            pdf_data = f.read()
            
        st.download_button(
            label=download_label,
            data=pdf_data,
            file_name=file_name,
            mime="application/pdf",
            use_container_width=True
        )
        
        st.write("") 
        st.markdown("---")
        
        # PDF 미리보기 (이미지 변환 출력)
        try:
            import fitz  # pymupdf
            doc = fitz.open(file_path)
            for page in doc:
                pix = page.get_pixmap(dpi=150)
                st.image(pix.tobytes(), use_container_width=True)
                
        except ImportError:
            st.warning("PDF 미리보기를 위해 'pymupdf' 라이브러리가 필요합니다.")
        except Exception as e:
            st.error(f"미리보기를 불러오는 중 오류가 발생했습니다: {e}")
            
    else:
        no_file_msg = "파일을 찾을 수 없습니다." if lang_code == "KR" else "File not found."
        st.error(f"🚨 {file_name} {no_file_msg}")