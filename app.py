import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. 페이지 설정
st.set_page_config(page_title="AI 건강 리포트", page_icon="🩺")

# 2. API 및 모델 설정
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

# 제목 및 문구 (가장 처음의 친절한 느낌 유지)
st.title("🩺 내 손안의 AI 건강검진 해석기")
st.markdown("##### 건강검진 결과표 사진을 올리면, AI가 쉽게 설명해 주고 관리 방법을 알려줍니다.")
st.write("---")

# 3. 이미지 업로드
uploaded_file = st.file_uploader("건강검진 결과표 사진을 업로드하세요 (JPG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='업로드된 결과표', use_container_width=True)
    
    # 분석 버튼
    if st.button("🔍 결과 분석하기"):
        with st.spinner('AI가 검진표를 꼼꼼히 읽고 분석 중입니다... 잠시만 기다려주세요!'):
            try:
                # [가장 처음의 프롬프트 내용으로 복구]
                prompt = """
                너는 친절하고 전문적인 건강 관리사야. 
                첨부된 건강검진 결과표 이미지를 읽고 다음 양식에 맞춰서 설명해 줘. 
                어려운 의학 용어는 초등학생도 이해할 수 있게 쉽게 풀어서 설명해야 해.

                1. 요약: 현재 건강 상태에 대한 3줄 요약
                2. 주의 항목: 정상 수치를 벗어난 항목과 그 의미 (없으면 '모두 정상입니다' 출력)
                3. 맞춤 관리법: 수치를 개선하기 위한 식습관과 운동 방법 3가지 추천

                주의사항: 개인정보(이름, 생년월일 등)가 보여도 절대 언급하지 마. 
                의료적 진단이 아니라는 점을 마지막에 꼭 명시해 줘.
                """
                
                response = model.generate_content([image, prompt])
                
                # 분석 완료 메시지
                st.success("✅ 분석이 완료되었습니다!") 
                
                # 결과 출력 (가독성 좋은 박스 디자인 유지)
                st.markdown("#### 💡 AI 건강 분석 결과")
                
                # 글자 크기와 가독성을 고려한 디자인 박스
                st.markdown(
                    f"""
                    <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #007bff;">
                        <div style="color: #1e1e1e; font-size: 16px; line-height: 1.8; white-space: pre-wrap;">
                            {response.text}
                        </div>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                st.markdown("---")

            except Exception as e:
                st.error(f"분석 중 오류가 발생했습니다: {e}")

else:
    st.info("검진표 사진을 업로드하시면 분석을 시작합니다.")
