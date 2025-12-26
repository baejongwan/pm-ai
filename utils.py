import streamlit as st
import pandas as pd
import os
import base64
from io import BytesIO
import glob

# (1) 이미지 처리 라이브러리 (Pillow) 확인
try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# --------------------------------------------------------------------------
# [1] 만능 이미지 찾기 함수 (이게 없어서 오류가 난 것입니다)
# --------------------------------------------------------------------------
@st.cache_data
def get_optimized_image(file_path):
    # 1. 값이 없으면 하트 아이콘 반환
    if not file_path or str(file_path) == 'nan' or str(file_path).strip() == "":
        return "https://cdn-icons-png.flaticon.com/512/833/833472.png"
    
    file_str = str(file_path).strip()
    
    # 2. 인터넷 주소(http)라면 바로 반환
    if "http" in file_str: 
        return file_str
    
    # 3. 경로 떼고 '파일 이름'만 추출
    if "\\" in file_str:
        target_name = file_str.split("\\")[-1]
    elif "/" in file_str:
        target_name = file_str.split("/")[-1]
    else:
        target_name = file_str
        
    target_lower = target_name.lower() # 소문자로 변환해서 비교

    # 4. 현재 폴더를 뒤져서 실제 파일 찾기
    found_path = None
    for root, dirs, files in os.walk("."): 
        for file in files:
            if file.lower() == target_lower:
                found_path = os.path.join(root, file)
                break
        if found_path: break
    
    # 5. 파일을 찾았다면 이미지로 변환 (Base64)
    if found_path:
        try:
            if HAS_PIL:
                with Image.open(found_path) as img:
                    img.thumbnail((600, 600))  # 용량 최적화
                    buffered = BytesIO()
                    img.save(buffered, format="PNG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    return f"data:image/png;base64,{img_str}"
            else:
                # PIL이 없으면 그냥 파일 읽기
                with open(found_path, "rb") as f:
                    data = f.read()
                    return f"data:image/png;base64,{base64.b64encode(data).decode()}"
        except Exception:
            pass # 변환 실패 시 하트로

    # 6. 끝까지 못 찾으면 하트 반환
    return "https://cdn-icons-png.flaticon.com/512/833/833472.png"

# --------------------------------------------------------------------------
# [2] 엑셀 파일 로딩 (pm_data.xlsx 지정 및 캐시 최적화)
# --------------------------------------------------------------------------
# ttl=600 : 10분마다 엑셀 파일을 새로 읽어오라는 뜻입니다 (캐시 갱신)
@st.cache_data(ttl=600) 
def load_excel():
    # 1. 파일 이름 지정 (pm_data.xlsx)
    target_file = "pm_data.xlsx"
    
    # 2. 파일이 없으면 다른 엑셀이라도 찾기
    if not os.path.exists(target_file):
        excel_files = glob.glob("*.xlsx")
        if excel_files:
            target_file = excel_files[0]
        else:
            return {} # 파일이 아예 없으면 빈 딕셔너리 반환

    # 3. 엑셀 읽기
    try:
        # sheet_name=None으로 하면 모든 시트를 다 읽어옵니다.
        df_dict = pd.read_excel(target_file, sheet_name=None, engine='openpyxl')
        
        # [중요] 시트 이름의 앞뒤 공백 제거 (실수 방지)
        # 예: " 제품포인트 " -> "제품포인트" 로 자동 수정
        cleaned_dict = {}
        for key, value in df_dict.items():
            cleaned_dict[key.strip()] = value
            
        return cleaned_dict
        
    except Exception as e:
        st.error(f"엑셀 파일 로딩 실패 ({target_file}): {e}")
        return {}

# --------------------------------------------------------------------------
# [3] (구버전 호환용) AI 함수 더미
# --------------------------------------------------------------------------
# view_ai.py가 이제 스스로 AI를 처리하므로, 여기서는 빈 껍데기만 남겨둡니다.
# 혹시 다른 파일에서 이 함수를 찾을까봐 남겨두는 안전 장치입니다.
def generate_ai_response(prompt, api_key, model_name, all_sheets=None):
    return "AI 기능은 view_ai.py에서 직접 처리됩니다."
