import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. 페이지 설정
st.set_page_config(page_title="AI 건강검진 해석기", page_icon="🩺")

# 2. API 및 모델 설정
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

# 타이틀 및 상단 디자인
st.title("🩺 AI 건강검진 리포트")
st.markdown("##### 쉽고 빠르게 확인하는 내 몸 상태")
st.write("---")

# 3. 이미지 업로드 (기존 중앙 방식)
uploaded_file = st.file_uploader("검진 결과표 사진을 업로드하세요", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='업로드된 검진표', use_container_width=True)
    
    # 분석 버튼
    if st.button("🔍 결과 분석 시작"):
        with st.spinner('데이터를 분석 중입니다...'):
            try:
                prompt = """
                너는 건강 관리 컨설턴트야. 20~40대 성인 사용자의 검진표를 분석해 줘.
                말투는 신뢰감 있는 전문가 스타일로 하되, 내용은 이해하기 쉽게 풀어서 설명해 줘.

                [출력 양식]
                1. 📋 종합 분석: 현재 상태에 대한 핵심 요약 3줄
                2. ⚠️ 중점 관리 항목: 정상 범위를 벗어난 수치의 의미 설명
                3. 🏃 생활 습관 가이드: 식단 및 운동 제안 3가지

                마지막에 "본 해석은 AI의 분석 결과이며, 정확한 진료와 처방은 반드시 전문의와 상담하시기 바랍니다." 문구를 포함해 줘.
                """
                
                response = model.generate_content([image, prompt])
                
                # 분석 완료 메시지를 결과 최상단에 배치
                st.success("✅ 분석이 완료되었습니다!") 
                
                st.markdown("### 📄 정밀 분석 결과")
                st.info(response.text)
                st.markdown("---")

            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")

else:
    st.info("해석할 검진표 사진을 먼저 업로드해 주세요.")
