import streamlit as st
import google.generativeai as genai
from PIL import Image

# 화면 제목 설정
st.title("🩺 내 손안의 AI 건강검진 해석기")
st.write("건강검진 결과표 사진을 올리면, AI가 쉽게 설명해 주고 관리 방법을 알려줍니다.")

# 발급받은 API 키 입력 (여기에 구글 AI 스튜디오에서 받은 키를 넣으세요)
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# 사용할 AI 모델 설정
model = genai.GenerativeModel('gemini-2.5-flash')

# 이미지 업로드 버튼 만들기
uploaded_file = st.file_uploader("건강검진 결과표 사진을 업로드하세요 (JPG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='업로드된 결과표', use_container_width=True)

    if st.button("결과 분석하기"):
        with st.spinner('AI가 검진표를 꼼꼼히 읽고 분석 중입니다... 잠시만 기다려주세요!'):
            try:
                prompt = """
                너는 친절하고 전문적인 건강 관리사야. 
                첨부된 건강검진 결과표 이미지를 읽고 다음 양식에 맞춰서 설명해 줘.
                어려운 의학 용어는 초등학생도 이해할 수 있게 쉽게 풀어서 설명해야 해.
                
                1. 요약: 현재 건강 상태에 대한 3줄 요약
                2. 주의 항목: 정상 수치를 벗어난 항목과 그 의미 (없으면 '모두 정상입니다' 출력)
                3. 맞춤 관리법: 수치를 개선하기 위한 식습관과 운동 방법 3가지 추천
                
                주의사항: 개인정보(이름, 생년월일 등)가 보여도 절대 언급하지 마. 의료적 진단이 아니라는 점을 마지막에 꼭 명시해 줘.
                """
                response = model.generate_content([image, prompt])
                st.subheader("💡 AI 건강 분석 결과")
                st.write(response.text)
            except Exception as e:
                st.error(f"분석 중 오류가 발생했습니다: {e}")
import streamlit as st
import google.generativeai as genai

# 직접 키를 적는 대신 Secrets에서 가져오도록 수정
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
