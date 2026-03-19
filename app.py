import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API 키 설정 (금고에서 가져오기)
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# 2. 모델 설정
model = genai.GenerativeModel('gemini-2.5-flash')

# 화면 제목
st.title("🩺 내 손안의 AI 건강검진 해석기")
st.write("건강검진 결과표 사진을 올리면, AI가 쉽게 설명해 줍니다.")

# 이미지 업로드
uploaded_file = st.file_uploader("건강검진 결과표 사진을 업로드하세요 (JPG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='업로드된 결과표', use_container_width=True)

    if st.button("결과 분석하기"):
        with st.spinner('AI가 꼼꼼히 읽고 분석 중입니다...'):
            try:
                prompt = """
                너는 친절하고 전문적인 건강 관리사야.
                첨부된 이미지의 수치들을 읽고 다음 양식에 맞춰서 설명해 줘.
                초등학생도 이해할 수 있게 쉽게 풀어써야 해.

                1. 요약: 현재 상태에 대한 3줄 요약
                2. 주의 항목: 정상 수치를 벗어난 항목과 그 의미 (없으면 '모두 정상입니다' 출력)
                3. 맞춤 관리법: 수치 개선을 위한 식습관과 운동 방법 3가지 추천
                
                주의사항: 이름, 생년월일 등 개인정보는 절대 언급하지 마. 
                의료적 진단이 아니라는 점을 마지막에 꼭 명시해 줘.
                """
                
                # AI 분석 실행
                response = model.generate_content([image, prompt])
                st.subheader("💡 AI 건강 분석 결과")
                st.write(response.text)

                # --- 여기서부터 카톡 공유용 복사 기능 ---
                summary_text = f"🩺 AI 건강검진 해석 결과\n\n{response.text[:100]}...\n\n자세한 내용은 사이트에서 확인하세요!"
                # 기존 에러 난 줄을 지우고 아래 내용을 넣으세요
                st.text_area("카톡 공유용 요약 문구 (아래 내용을 복사하세요)", value=summary_text, height=100)
                st.info("위 박스의 내용을 복사해서 카톡에 붙여넣으세요! 📋")
                st.success("✅ 분석 완료! 카톡 공유용 요약 문구가 자동으로 복사되었습니다.")
                # ------------------------------------

            except Exception as e:
                st.error(f"분석 중 오류가 발생했습니다: {e}")
