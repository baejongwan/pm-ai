import streamlit as st
import os

# -----------------------------------------------------------
# [보안] API 키 설정
# -----------------------------------------------------------
if "GOOGLE_API_KEY" in st.secrets:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
else:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# -----------------------------------------------------------
# 기타 기본 설정
# -----------------------------------------------------------
MAIN_CONTACT_NAME = "배종완 사장님"
MAIN_CONTACT_PHONE = "010-5089-1615"
LOGO_FILE_PATH = "home_logo.png"

# 추천인 ID 리스트
FAMILY_IDS = [
    {"role": "아내", "name": "전은영", "id": "8486455"},
    {"role": "어머니", "name": "김월선", "id": "10057772"},
    {"role": "누나", "name": "배정하", "id": "21287855"},
    {"role": "친구", "name": "이송호", "id": "20207931"},
    {"role": "친구", "name": "김영애(호기웅)", "id": "20405088"},
    {"role": "친구", "name": "조재현", "id": "21870233"},
    {"role": "친구", "name": "Yongho Hong", "id": "21869248"}
]

# -----------------------------------------------------------
# [통합 다국어 설정] LANG_CONFIG 하나로 모든 것을 관리합니다.
# -----------------------------------------------------------
# -----------------------------------------------------------
# [통합 다국어 설정] 수익 시뮬레이션 세부 키값 보완 버전
# -----------------------------------------------------------
LANG_CONFIG = {
    "KR": {
        "name": "한국어", 
        "file": "pm_data.xlsx", 
        "welcome": "환영합니다",
        "menu": ["홈", "AI상담", "수익계산", "보상플랜", "제품구매", "안전성", "액티증상", "호전반응", "체험사례", "성공사례", "영상자료", "자료실"],
        "ui": {
            "ai_title": "PM AI 상담", 
            "ai_sub": "📋 맞춤형 상담을 위한 정보 입력", 
            "ai_desc": "정보를 입력하시면 건강 상태에 딱 맞는 답변을 드립니다.",
            "calc_title": "수익 & 직급 시뮬레이션", 
            "calc_sub": "📌 시뮬레이션 기준 (현실적인 사업 모델 적용)",
            "label_partners": "1️⃣ 직대 파트너",
            "label_duplication": "2️⃣ 파트너당 복제",
            "label_depth": "3️⃣ 계산 깊이",
            "unit_person": "명",
            "unit_intro": "명씩 소개",
            "unit_level": "세대(Level)",
            "unit_gen": "대",
            "res_rank_title": "🏆 예상 달성 직급",
            "res_car_bonus": "🚗 카 보너스",
            "res_travel_bonus": "✈️ 여행 보너스",
            "res_monthly_income": "💰 월 예상 수령액",
            "res_total_partners": "총 산하 파트너",
            "res_total_gv": "총 예상 매출",
            "res_base_bonus": "기본 후원 수당",
            "res_direct_bonus": "직추천 보너스",
            "res_level_bonus": "레벨 보너스",
            "detail_view": "🔍 수당 계산 상세 내역 보기",
            "calc_unit_info": "1인당 기준",
            "story_title": "제품 체험 사례", 
            "story_sub": "증상별/제품별 모아보기",
            "success_title": "명예의 전당", 
            "success_sub": "성공 스토리",
            "video_title": "PM 영상 자료실", 
            "video_sub": "매일 아침 조회 및 주요 교육 영상을 확인하세요.",
            "pdf_title": "📄 BA 자료실",
            "pdf_download": "📥 PDF 파일 다운로드 받기",
            "search": "🔍 검색어 입력", 
            "age": "연령대 (세)", 
            "gender": "성별", 
            "gen_f": "여성", 
            "gen_m": "남성", 
            "start_ai": "상담 시작하기 🚀",
            "safety_title": "품질 & 안전성", 
            "act_title": "액티바이즈 반응 분석", 
            "guide_title": "호전반응 가이드"
        }
    },
    "CH": {
        "name": "中文", 
        "file": "pm_data_ch.xlsx", 
        "welcome": "欢迎光临",
        "menu": ["首页", "AI咨询", "收益计算", "奖励计划", "产品购买", "安全性", "反应诊断", "好转反应", "见证案例", "成功案例", "视频资料", "资料室"],
        "ui": {
            "ai_title": "PM AI 咨询", 
            "ai_sub": "📋 输入信息以获得定制化咨询", 
            "ai_desc": "输入您的信息，我们将为您提供量身定制的健康建议。",
            "calc_title": "收益与职级模拟", 
            "calc_sub": "📌 模拟标准 (适用于现实业务模型)",
            "label_partners": "1️⃣ 直系伙伴",
            "label_duplication": "2️⃣ 每位伙伴复制",
            "label_depth": "3️⃣ 计算深度",
            "unit_person": "人",
            "unit_intro": "人推荐",
            "unit_level": "层级(Level)",
            "unit_gen": "代",
            "res_rank_title": "🏆 预计达成等级",
            "res_car_bonus": "🚗 购车补贴",
            "res_travel_bonus": "✈️ 旅游奖金",
            "res_monthly_income": "💰 预计月收入",
            "res_total_partners": "旗下伙伴总数",
            "res_total_gv": "预计总销售额",
            "res_base_bonus": "基本提成",
            "res_direct_bonus": "直接推荐奖金",
            "res_level_bonus": "层级奖金",
            "detail_view": "🔍 查看奖금计算详情",
            "calc_unit_info": "人均标准",
            "story_title": "产品见证案例", 
            "story_sub": "按症状/产品查看",
            "success_title": "名人堂", 
            "success_sub": "成功故事",
            "video_title": "PM 视频资料室", 
            "video_sub": "查看每日早会及主要培训视频。",
            "pdf_title": "📄 BA 资料室",
            "pdf_download": "📥 下载 PDF 文件",
            "search": "🔍 输入搜索词", 
            "age": "年龄 (岁)", 
            "gender": "性别", 
            "gen_f": "女性", 
            "gen_m": "男性", 
            "start_ai": "开始咨询 🚀",
            "safety_title": "品质与安全性", 
            "act_title": "Activize 反应分析", 
            "guide_title": "好转反应指南"
        }
    },
    "TH": {
        "name": "ไทย", 
        "file": "pm_data_th.xlsx", 
        "welcome": "ยินดีต้อนรับ",
        "menu": ["หน้าแรก", "AI ปรึกษา", "คำนวณรายได้", "แผนการชดเชย", "ซื้อผลิตภัณฑ์", "ความปลอดภัย", "การวินิจฉัย", "ปฏิกิริยาดีขึ้น", "กรณีศึกษา", "ความสำเร็จ", "วิดีโอ", "ห้องสมุด"],
        "ui": {
            "ai_title": "PM AI ปรึกษา", 
            "ai_sub": "📋 ข้อมูลสำหรับการให้คำปรึกษาเฉพาะบุคคล", 
            "ai_desc": "กรอกข้อมูลของคุณเพื่อรับคำตอบที่เหมาะสมกับสภาพสุขภาพของคุณ",
            "calc_title": "การจำลองรายได้และตำแหน่ง", 
            "calc_sub": "📌 เกณฑ์การจำลอง (ใช้รูปแบบธุรกิจจริง)",
            "label_partners": "1️⃣ พาร์ทเนอร์สายตรง",
            "label_duplication": "2️⃣ การคัดลอกต่อพาร์ทเนอร์",
            "label_depth": "3️⃣ ความลึกในการคำนวณ",
            "unit_person": "คน",
            "unit_intro": "คนต่อการแนะนำ",
            "unit_level": "ลำดับชั้น(Level)",
            "unit_gen": "ชั้น",
            "res_rank_title": "🏆 ตำแหน่งที่คุณจะได้รับ",
            "res_car_bonus": "🚗 โบนัสรถยนต์",
            "res_travel_bonus": "✈️ โบนัสท่องเที่ยว",
            "res_monthly_income": "💰 รายได้ต่อเดือนโดยประมาณ",
            "res_total_partners": "พาร์ทเนอร์ภายใต้สายงานทั้งหมด",
            "res_total_gv": "ยอดขายโดยประมาณทั้งหมด",
            "res_base_bonus": "ค่าคอมมิชชั่นพื้นฐาน",
            "res_direct_bonus": "โบนัสแนะนำตรง",
            "res_level_bonus": "โบนัสตามชั้น",
            "detail_view": "🔍 ดูรายละเอียดการคำนวณรายได้",
            "calc_unit_info": "เกณฑ์ต่อคน",
            "story_title": "กรณีศึกษาผลิตภัณฑ์", 
            "story_sub": "ดูตามอาการ/ผลิตภัณฑ์",
            "success_title": "หอเกียรติยศ", 
            "success_sub": "เรื่องราวความสำเร็จ",
            "video_title": "คลังวิดีโอ PM", 
            "video_sub": "ตรวจสอบการประชุมเช้าและวิดีโอการฝึกอบรมหลัก",
            "pdf_title": "📄 คลังเอกสาร BA",
            "pdf_download": "📥 ดาวน์โหลดไฟล์ PDF",
            "search": "🔍 ใส่คำค้นหา", 
            "age": "อายุ (ปี)", 
            "gender": "เพศ", 
            "gen_f": "หญิง", 
            "gen_m": "ชาย", 
            "start_ai": "เริ่มปรึกษา 🚀",
            "safety_title": "คุณภาพและความปลอดภัย", 
            "act_title": "การวิเคราะห์ผลลัพธ์ Activize", 
            "guide_title": "คู่มือปฏิกิริยาดีขึ้น"
        }
    },
    "EN": {
        "name": "English", 
        "file": "pm_data_en.xlsx", 
        "welcome": "Welcome",
        "menu": ["Home", "AI Chat", "Income Calc", "Comp Plan", "Products", "Safety", "Symptoms", "Guide", "Stories", "Success", "Videos", "Library"],
        "ui": {
            "ai_title": "PM AI Consulting", 
            "ai_sub": "📋 Information for Customized Counseling", 
            "ai_desc": "Enter your info to get answers tailored to your health status.",
            "calc_title": "Income & Rank Simulation", 
            "calc_sub": "📌 Simulation Criteria (Realistic Business Model)",
            "label_partners": "1️⃣ Direct Partners",
            "label_duplication": "2️⃣ Duplication per Partner",
            "label_depth": "3️⃣ Calculation Depth",
            "unit_person": "Pax",
            "unit_intro": "Referrals each",
            "unit_level": "Generation (Level)",
            "unit_gen": "Gen",
            "res_rank_title": "🏆 Estimated Rank",
            "res_car_bonus": "🚗 Car Bonus",
            "res_travel_bonus": "✈️ Travel Bonus",
            "res_monthly_income": "💰 Estimated Monthly Income",
            "res_total_partners": "Total Downline Partners",
            "res_total_gv": "Total Estimated Sales (GV)",
            "res_base_bonus": "Basic Commission",
            "res_direct_bonus": "Direct Bonus",
            "res_level_bonus": "Level Bonus",
            "detail_view": "🔍 View Detailed Calculation",
            "calc_unit_info": "Per Person Criteria",
            "story_title": "Product Experience Stories", 
            "story_sub": "View by symptoms/products",
            "success_title": "Hall of Fame", 
            "success_sub": "Success Stories",
            "video_title": "PM Video Library", 
            "video_sub": "Check daily morning meetings and major training videos.",
            "pdf_title": "📄 BA Resource Center",
            "pdf_download": "📥 Download PDF File",
            "search": "🔍 Search", 
            "age": "Age", 
            "gender": "Gender", 
            "gen_f": "Female", 
            "gen_m": "Male", 
            "start_ai": "Start Counseling 🚀",
            "safety_title": "Quality & Safety", 
            "act_title": "Activize Analysis", 
            "guide_title": "Recovery Guide"
        }
    }
}