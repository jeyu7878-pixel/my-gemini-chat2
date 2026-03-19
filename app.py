import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API 키 설정
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# 2. 모델 설정 (안정적인 최신 버전)
model = genai.GenerativeModel('gemini-2.5-flash')

# 화면 제목 및 설명
st.title("🩺 내 손안의 AI 건강검진 해석기")
st.write("건강검진 결과표 사진을 올리면, AI가 쉽게 설명해 줍니다.")

# 이미지 업로드 버튼
uploaded_file = st.file_uploader("건강검진 결과표 사진을 업로드하세요 (JPG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 업로드된 이미지 표시
    image = Image.open(uploaded_file)
    st.image(image, caption='업로드된 결과표', use_container_width=True)

    # 분석 버튼
    if st.button("결과 분석하기"):
        with st.spinner('AI가 검진표를 분석 중입니다. 잠시만 기다려주세요!'):
            try:
                # AI에게 보낼 요청 메시지
                prompt = """
                너는 친절하고 전문적인 건강 관리사야.
                첨부된 이미지의 수치들을 읽고 다음 양식에 맞춰서 설명해 줘.
                초등학생도 이해할 수 있게 쉽게 풀어써야 해.

                1. 요약: 현재 상태에 대한 3줄 요약
                2. 주의 항목: 정상 수치를 벗어난 항목과 그 의미 (없으면 '모두 정상입니다' 출력)
                3. 맞춤 관리법: 수치 개선을 위한 식습관과 운동 방법 3가지 추천
                
                주의사항: 이름, 생년월일 등 개인정보는 절대 언급하지 마. 
                의료적 진단이 아니라는 점을 마지막에 반드시 명시해 줘.
                """
                
                # AI 분석 실행 및 결과 출력
                response = model.generate_content([image, prompt])
                st.subheader("💡 AI 건강 분석 결과")
                st.markdown("---")
                st.write(response.text)
                st.markdown("---")
                st.info("💡 팁: 결과를 카톡으로 공유하려면 화면의 글자를 길게 눌러 복사해서 전달해 보세요!")

            except Exception as e:
                st.error(f"분석 중 오류가 발생했습니다: {e}")
