import streamlit as st
import google.generativeai as genai
from PIL import Image

# 페이지 설정 (가장 먼저 실행되어야 합니다)
st.set_page_config(page_title="AI 건강검진 해석기", page_icon="🩺", layout="centered")

# 1. API 키 설정
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

# 스타일링 (CSS) - 폰트와 배경을 살짝 만져줍니다
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #007bff;
        color: white;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 메인 타이틀 영역
st.title("🩺 스마트 AI 건강 리포트")
st.subheader("2040 세대를 위한 맞춤형 검진 데이터 해석")
st.write("---")

# 사이드바에 업로드 기능 배치
with st.sidebar:
    st.header("📂 데이터 업로드")
    uploaded_file = st.sidebar.file_uploader("검진표 사진을 올려주세요", type=["jpg", "jpeg", "png"])
    st.info("💡 팁: 글자가 선명하게 보이도록 밝은 곳에서 촬영한 사진이 좋습니다.")

if uploaded_file is not None:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        image = Image.open(uploaded_file)
        st.image(image, caption='📸 업로드된 이미지', use_container_width=True)
    
    with col2:
        st.write("### ⚙️ 분석 준비 완료")
        st.write("업로드하신 데이터를 바탕으로 AI 컨설턴트가 정밀 분석을 시작합니다.")
        analyze_button = st.button("🔍 지금 바로 분석하기")

    if analyze_button:
        with st.status("🚀 데이터를 분석하고 리포트를 생성 중입니다...", expanded=True) as status:
            try:
                prompt = """
                너는 20~40대 성인을 대상으로 하는 전문 건강 컨설턴트야.
                첨부된 건강검진 결과표의 수치들을 분석해서 다음 양식에 맞춰 신뢰감 있게 설명해 줘.
                
                [출력 양식 및 가이드라인]
                - 전체적인 분위기는 신뢰감 있고 명확하게.
                - 1. 📋 **종합 분석**: 현재 상태 요약 (긍정적인 부분과 주의할 점)
                - 2. ⚠️ **중점 관리 항목**: 수치와 의미 풀이 (이해하기 쉽게)
                - 3. 🏃 **생활 습관 가이드**: 식단, 운동, 생활 습관 제안
                
                - 마지막에 반드시 "본 해석은 AI의 분석 결과이며, 정확한 진료와 처방은 반드시 전문의와 상담하시기 바랍니다."라고 적어줘.
                """
                
                response = model.generate_content([image, prompt])
                status.update(label="✅ 분석이 완료되었습니다!", state="complete", expanded=False)
                
                # 결과 출력 영역
                st.markdown("### 📄 AI 정밀 분석 리포트")
                st.success("데이터 해석이 성공적으로 완료되었습니다.")
                
                # 배경색이 있는 박스에 결과 출력
                st.info(response.text)
                
            except Exception as e:
                st.error(f"분석 중 오류가 발생했습니다: {e}")

else:
    # 파일을 올리기 전 안내 화면
    st.warning("👈 왼쪽 사이드바에서 건강검진 결과표 사진을 먼저 업로드해 주세요!")
