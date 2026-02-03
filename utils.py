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
# [1] 만능 이미지 찾기 함수 (기존 로직 유지)
# --------------------------------------------------------------------------
@st.cache_data
def get_optimized_image(file_path):
    if not file_path or str(file_path) == 'nan' or str(file_path).strip() == "":
        return "https://cdn-icons-png.flaticon.com/512/833/833472.png"
    
    file_str = str(file_path).strip()
    
    if "http" in file_str: 
        return file_str
    
    if "\\" in file_str:
        target_name = file_str.split("\\")[-1]
    elif "/" in file_str:
        target_name = file_str.split("/")[-1]
    else:
        target_name = file_str
        
    target_lower = target_name.lower()

    found_path = None
    for root, dirs, files in os.walk("."): 
        for file in files:
            if file.lower() == target_lower:
                found_path = os.path.join(root, file)
                break
        if found_path: break
    
    if found_path:
        try:
            if HAS_PIL:
                with Image.open(found_path) as img:
                    img.thumbnail((600, 600))
                    buffered = BytesIO()
                    img.save(buffered, format="PNG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    return f"data:image/png;base64,{img_str}"
            else:
                with open(found_path, "rb") as f:
                    data = f.read()
                    return f"data:image/png;base64,{base64.b64encode(data).decode()}"
        except Exception:
            pass

    return "https://cdn-icons-png.flaticon.com/512/833/833472.png"

# --------------------------------------------------------------------------
# [2] 엑셀 파일 로딩 (언어 선택 로직 적용 수정)
# --------------------------------------------------------------------------
# target_file 매개변수를 추가하여 언어별 파일(pm_data_ch.xlsx 등)을 받을 수 있게 함
@st.cache_data(ttl=600) 
def load_excel(target_file="pm_data.xlsx"):
    # 파일명이 정확히 일치하는지 확인 (대소문자 구분 및 경로 확인) 
    if not os.path.exists(target_file):
        # pm_data_en.xlsx 처럼 언어별 파일이 없으면 기본 파일로 복구
        if os.path.exists("pm_data.xlsx"):
            target_file = "pm_data.xlsx"
        else:
            return {}

    try:
        # 시트 데이터를 불러와서 시트명 공백 제거 
        df_dict = pd.read_excel(target_file, sheet_name=None, engine='openpyxl')
        cleaned_dict = {key.strip(): value for key, value in df_dict.items()}
        return cleaned_dict
    except Exception as e:
        st.error(f"Excel Load Error: {e}")
        return {}

# --------------------------------------------------------------------------
# [3] (구버전 호환용) AI 함수 더미 (기존 유지)
# --------------------------------------------------------------------------
def generate_ai_response(prompt, api_key, model_name, all_sheets=None):
    return "AI 기능은 view_ai.py에서 직접 처리됩니다."