import streamlit as st
import os
import base64
# func 임포트 제거됨 (render_return_home_button 안씀)

def render_pdf_viewer(file_name):
    # 홈 버튼 제거됨
    st.markdown("<h2 style='text-align:center;'>📄 BA 자료실</h2>", unsafe_allow_html=True)
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, file_name)

    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
            
        st.download_button(
            label="📥 PDF 파일 다운로드 받기",
            data=base64.b64decode(base64_pdf),
            file_name=file_name,
            mime="application/pdf",
            use_container_width=True
        )
        
        st.write("") 
        st.markdown("---")
        
        try:
            import fitz  # pymupdf
            doc = fitz.open(file_path)
            for page in doc:
                pix = page.get_pixmap(dpi=150)
                st.image(pix.tobytes(), use_container_width=True)
                
        except ImportError:
             st.error("pymupdf 라이브러리가 필요합니다.")
        except Exception as e:
            st.error("뷰어 로딩 중 오류가 발생했습니다.")
            st.warning("모바일에서 화면이 보이지 않는다면 위 [다운로드] 버튼을 이용해주세요.")

    else:
        st.error(f"🚨 파일을 찾을 수 없습니다: {file_name}")
        st.info(f"💡 팁: '{file_name}' 파일을 app.py 파일이 있는 폴더에 넣어주세요.")
