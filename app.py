import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. 페이지 설정
st.set_page_config(page_title="AI 건강 리포트", page_icon="🩺")

# 2. API 및 모델 설정
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

# 타이틀 및 문구
st.title("🩺 내 손안의 AI 건강검진 해석기")
st.markdown("##### 건강검진 결과표 사진을 올리면, AI가 쉽게 설명해 주고 관리 방법을 알려줍니다.")
st.write("---")

# 3. 이미지 업로드
uploaded_file = st.file_uploader("건강검진 결과표 사진을 업로드하세요", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='업로드된 결과표', use_container_width=True)
    
    if st.button("🔍 결과 분석하기"):
        with st.spinner('AI가 검진표를 분석 중입니다...'):
            try:
                prompt = """
                너는 친절한 건강 관리사야. 
                건강검진 결과를 읽고 다음 양식에 맞춰서 설명해 줘. 
                초등학생도 이해할 수 있게 아주 쉽게 풀어서 설명해야 해.

                1. 요약: 현재 상태 3줄 요약
                2. 주의 항목: 수치의 의미 설명
                3. 맞춤 관리법: 식습관과 운동 방법 추천

                마지막에 의료적 진단이 아니라는 점을 명시해 줘.
                """
                
                response = model.generate_content([image, prompt])
                
                st.success("✅ 분석이 완료되었습니다!") 
                st.markdown("#### 💡 AI 건강 분석 결과")
                
                # [수정된 부분] 간격 최적화 디자인 박스
                st.markdown(
                    f"""
                    <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #007bff; color: #1e1e1e; font-size: 16px; line-height: 1.5;">
                        {response.text}
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                st.markdown("---")

            except Exception as e:
                st.error(f"분석 중 오류가 발생했습니다: {e}")

else:
    st.info("검진표 사진을 업로드하시면 분석을 시작합니다.")
