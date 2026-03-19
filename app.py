import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. 페이지 설정
st.set_page_config(page_title="AI 건강 리포트", page_icon="🩺")

# 2. API 및 모델 설정
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# 제목 및 세련된 문구
st.title("🩺 AI 개인 건강 인사이트")
st.markdown("##### 데이터로 읽는 당신의 건강, AI가 더 명확하게 해석합니다.")
st.write("---")

# 3. 이미지 업로드
uploaded_file = st.file_uploader("검진 결과표 사진을 업로드해 주세요", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='업로드된 검진표 이미지', use_container_width=True)
    
    # 분석 버튼
    if st.button("🔍 데이터 정밀 분석 시작"):
        with st.spinner('AI 컨설턴트가 데이터를 심층 분석 중입니다...'):
            try:
                prompt = """
                너는 건강 관리 전문 컨설턴트야. 20~40대 성인 사용자의 검진표를 분석해 줘.
                말투는 신뢰감 있고 지적인 전문가 스타일로 하되, 가독성을 최우선으로 해줘.

                [출력 양식]
                1. 📋 종합적 건강 분석: 현재 전반적인 상태를 핵심적으로 요약
                2. ⚠️ 집중 관리 지표: 주의가 필요한 수치와 그에 따른 건강 영향
                3. 🏃 라이프스타일 처방: 지속 가능한 식단 및 운동 솔루션 제안

                마지막에 "본 해석은 AI의 데이터 분석 결과이며, 정확한 의학적 진단은 반드시 전문의와 상담하시기 바랍니다." 문구를 포함해 줘.
                """
                
                response = model.generate_content([image, prompt])
                
                # 분석 완료 메시지
                st.success("✅ 리포트 생성이 완료되었습니다!") 
                
                # 결과 출력 (글자 크기 조절 및 가독성 강조)
                st.markdown("#### 📄 맞춤형 정밀 분석 결과")
                
                # 배경색 박스를 사용하여 글자가 선명하게 보이도록 설정
                st.markdown(
                    f"""
                    <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #007bff;">
                        <span style="color: #1e1e1e; font-size: 16px; line-height: 1.6;">
                            {response.text.replace('\n', '<br>')}
                        </span>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                st.markdown("---")

            except Exception as e:
                st.error(f"분석 중 오류가 발생했습니다: {e}")

else:
    st.info("분석을 시작하려면 검진 결과표 이미지를 업로드하세요.")
