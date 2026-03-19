import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API 키 설정 (Streamlit Secrets 사용)
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# 2. 모델 설정 (Gemini 1.5 Flash)
model = genai.GenerativeModel('gemini-2.5-flash')

# 화면 제목 및 서브 타이틀
st.title("🩺 내 손안의 AI 건강검진 해석기")
st.write("복잡한 건강검진 결과표를 업로드하시면, AI가 핵심 내용을 분석하여 이해하기 쉽게 설명해 드립니다.")

# 이미지 업로드 섹션
uploaded_file = st.file_uploader("건강검진 결과표 사진을 업로드하세요 (JPG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 업로드된 이미지 표시
    image = Image.open(uploaded_file)
    st.image(image, caption='업로드된 검진표 이미지', use_container_width=True)

    # 분석 버튼
    if st.button("결과 분석하기"):
        with st.spinner('검진 데이터를 정밀하게 분석 중입니다. 잠시만 기다려 주세요...'):
            try:
                # 성인 대상 전문 코치 스타일 프롬프트
                prompt = """
                너는 20~40대 직장인 및 성인을 대상으로 하는 전문 건강 컨설턴트야.
                첨부된 건강검진 결과표의 수치들을 분석해서 다음 양식에 맞춰 신뢰감 있게 설명해 줘.
                
                [작성 가이드라인]
                - 말투: 전문적이면서도 친절한 구어체 (~입니다, ~하세요).
                - 난이도: 어려운 의학 용어는 일반 성인이 이해할 수 있도록 쉽게 풀어서 설명.
                - 대상: 자기관리에 관심이 많은 2040 세대.

                [출력 양식]
                1. 종합 분석: 현재 전반적인 건강 상태에 대한 3줄 요약.
                2. 중점 관리 항목: 정상 범위를 벗어난 수치와 그 수치가 의미하는 건강 위험 요소. (모두 정상이면 '현재 모든 수치가 양호합니다'라고 출력)
                3. 생활 습관 가이드: 수치 개선을 위한 구체적인 식단 관리 및 운동법 3가지 제안.

                주의사항: 성함, 생년월일 등 개인정보는 절대 언급하지 마. 
                마지막에 "본 해석은 AI의 분석 결과이며, 정확한 진료와 처방은 반드시 전문의와 상담하시기 바랍니다."라는 문구를 반드시 포함해 줘.
                """
                
                # AI 분석 실행
                response = model.generate_content([image, prompt])
                
                # 결과 출력
                st.markdown("---")
                st.subheader("💡 AI 건강 데이터 분석 결과")
                st.write(response.text)
                st.markdown("---")

            except Exception as e:
                st.error(f"분석 과정에서 오류가 발생했습니다: {e}")
