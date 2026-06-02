import streamlit as st
from pathlib import Path
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# ── 페이지 설정 ──────────────────────────────────────────────
st.set_page_config(
    page_title="StatQA — 통계 분석 어시스턴트",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

:root {
    --bg:        #eef0fb;
    --bg2:       #e4e7f9;
    --surface:   #ffffff;
    --border:    #e6e8f2;
    --accent:    #6c5ce7;
    --accent-dk: #5546c8;
    --accent2:   #00b894;
    --text:      #1f2233;
    --text2:     #4a4e69;
    --muted:     #8a8fa8;
    --user-bg:   #f3f1fe;
    --ai-bg:     #ffffff;
}

/* reset */
html, body, [class*="css"] { font-family: 'Inter', 'Pretendard', sans-serif; }
.stApp {
    background: linear-gradient(135deg, var(--bg) 0%, var(--bg2) 100%);
    color: var(--text);
}
/* 메인 영역을 흰 카드처럼 */
.block-container {
    max-width: 980px;
    padding: 1.5rem 2.2rem 3rem;
    background: var(--surface);
    border-radius: 18px;
    margin-top: 1.5rem;
    box-shadow: 0 10px 40px rgba(80, 70, 160, 0.08);
}

/* hide streamlit chrome */
#MainMenu, footer { visibility: hidden; }
.stDeployButton { display: none; }

/* 본문 글씨 가독성 — 진한 색 */
.stApp, .stMarkdown, .stMarkdown p, .stMarkdown li {
    color: var(--text) !important;
}
.stMarkdown p, .stMarkdown li { font-size: 0.95rem; line-height: 1.75; }
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: var(--text) !important; }

/* ── header ── */
.site-header {
    display: flex; align-items: center; gap: 0.8rem;
    border-bottom: 1px solid var(--border);
    padding-bottom: 1.1rem; margin-bottom: 1.6rem;
}
.site-title {
    font-weight: 700; font-size: 1.7rem; color: var(--text);
    letter-spacing: -0.02em;
}
.site-badge {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem; color: #fff; background: var(--accent);
    padding: 3px 9px; border-radius: 6px; letter-spacing: 0.06em;
}
.site-sub {
    font-size: 0.82rem; color: var(--muted); margin-left: auto;
}

/* ── sidebar ── */
[data-testid="stSidebar"] {
    background: var(--surface);
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * { color: var(--text2); }
.sb-brand {
    font-weight: 700; font-size: 1.3rem; color: var(--text);
    margin-bottom: 0.2rem;
}
.sb-brand-sub {
    font-size: 0.72rem; color: var(--muted); margin-bottom: 1rem;
    letter-spacing: 0.03em;
}
.sb-section {
    font-size: 0.7rem; font-weight: 600; color: var(--accent);
    text-transform: uppercase; letter-spacing: 0.08em;
    margin: 1.1rem 0 0.5rem;
}
.sb-card {
    background: var(--bg); border: 1px solid var(--border);
    border-radius: 10px; padding: 0.8rem 0.95rem;
    font-size: 0.8rem; line-height: 1.6; color: var(--text2);
    margin-bottom: 0.5rem;
}
.sb-card b { color: var(--text); }
.sb-src {
    display: block; font-size: 0.78rem; color: var(--text2);
    text-decoration: none; padding: 0.35rem 0;
    border-bottom: 1px solid var(--border);
}
.sb-src:hover { color: var(--accent); }
.sb-src span { font-family: 'DM Mono', monospace; color: var(--muted); font-size: 0.7rem; }

/* ── tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px; background: var(--bg); border: 1px solid var(--border);
    border-radius: 10px; padding: 5px; margin-bottom: 1.5rem;
}
.stTabs [data-baseweb="tab"] {
    font-size: 0.85rem !important; font-weight: 500;
    color: var(--muted) !important; background: transparent !important;
    border-radius: 7px; padding: 9px 22px; border: none !important;
    transition: all 0.15s ease;
}
.stTabs [aria-selected="true"] {
    color: #fff !important; background: var(--accent) !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 0; }
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display: none; }

/* ── form elements ── */
.stSelectbox > div > div,
.stTextArea > div > div,
.stTextInput > div > div {
    background: var(--surface) !important;
    border-color: var(--border) !important;
    border-radius: 9px !important; color: var(--text) !important;
}
.stSelectbox label, .stRadio label, .stTextArea label,
.stNumberInput label, .stTextInput label {
    font-size: 0.8rem !important; color: var(--text2) !important;
    font-weight: 600 !important;
}
.stButton > button {
    background: var(--accent) !important; color: #fff !important;
    border: none !important; border-radius: 9px !important;
    font-weight: 600 !important; font-size: 0.85rem !important;
    padding: 0.55rem 1.5rem !important; transition: all 0.15s ease;
    box-shadow: 0 4px 14px rgba(108, 92, 231, 0.25);
}
.stButton > button:hover { background: var(--accent-dk) !important; }

/* ── chat messages (st.chat_message 네이티브) ── */
[data-testid="stChatMessage"] {
    background: var(--ai-bg); border: 1px solid var(--border);
    border-radius: 12px; padding: 0.8rem 1.1rem;
    box-shadow: 0 2px 10px rgba(80, 70, 160, 0.04);
    width: 100%;
    display: flex !important;
    align-items: flex-start !important;
    gap: 0.6rem !important;
}
/* 아바타는 고정 크기, 본문이 나머지 폭을 전부 차지 */
[data-testid="stChatMessage"] > [data-testid="stChatMessageAvatar"],
[data-testid="stChatMessage"] > img:first-child { flex: 0 0 auto !important; }
[data-testid="stChatMessage"] > div:last-child {
    flex: 1 1 auto !important; width: auto !important; min-width: 0 !important;
}
[data-testid="stChatMessageContent"],
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
    width: 100% !important; max-width: 100% !important;
}
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li { word-break: keep-all; overflow-wrap: anywhere; }

/* 디버그 청크(st.code) — 가로 스크롤 대신 자동 줄바꿈으로 한눈에 보이게 */
[data-testid="stExpander"] pre,
[data-testid="stExpander"] code,
pre, code {
    white-space: pre-wrap !important;
    word-break: break-word !important;
    overflow-wrap: anywhere !important;
    overflow-x: hidden !important;
}
[data-testid="stExpander"] pre { max-width: 100% !important; }

/* ── source badge ── */
.source-block {
    margin-top: 0.7rem; padding: 0.55rem 0.9rem;
    background: var(--user-bg); border: 1px solid var(--border);
    border-radius: 9px; font-size: 0.78rem; color: var(--text2);
}
.source-block a { color: var(--accent) !important; text-decoration: none; font-weight: 500; }
.source-block a:hover { text-decoration: underline; }

/* ── recommender cards ── */
.rec-card {
    background: var(--bg); border: 1px solid var(--border);
    border-radius: 12px; padding: 1.2rem 1.4rem; margin-bottom: 0.8rem;
}
.rec-card-title { font-weight: 700; font-size: 1.15rem; color: var(--text); margin-bottom: 0.4rem; }
.rec-card-sub { font-size: 0.85rem; color: var(--text2); margin-bottom: 0.7rem; }
.tag {
    display: inline-block; font-family: 'DM Mono', monospace;
    font-size: 0.68rem; letter-spacing: 0.04em; padding: 3px 9px;
    border-radius: 6px; margin-right: 6px; margin-top: 4px;
}
.tag-method { background: #ede9ff; color: var(--accent); border: 1px solid #d6ccff; }
.tag-warn   { background: #fff4d6; color: #b8860b; border: 1px solid #f0d98a; }
.tag-ok     { background: #d6f5ec; color: var(--accent2); border: 1px solid #a3e6d2; }

/* ── section label ── */
.section-label {
    font-size: 0.72rem; font-weight: 600; letter-spacing: 0.08em;
    text-transform: uppercase; color: var(--accent); margin-bottom: 0.6rem;
}

/* ── divider ── */
hr { border-color: var(--border) !important; margin: 1.3rem 0; }

/* spinner */
.stSpinner > div { border-top-color: var(--accent) !important; }

/* ── 인쇄(PDF 저장) 전용 — 사이드바 숨기고 본문을 종이 전체로 ── */
@media print {
    /* 사이드바·헤더·툴바 등 인쇄 불필요 요소 숨김 */
    [data-testid="stSidebar"],
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="stToolbar"],
    header { display: none !important; }

    /* 본문이 종이 폭 전체를 쓰도록 */
    [data-testid="stAppViewContainer"] > .main,
    .main .block-container {
        max-width: 100% !important;
        width: 100% !important;
        margin: 0 !important;
        padding: 0.5cm !important;
        box-shadow: none !important;
        border-radius: 0 !important;
    }
    .stApp { background: #ffffff !important; }

    /* 채팅 메시지가 페이지 중간에서 잘리지 않게 */
    [data-testid="stChatMessage"] { break-inside: avoid; page-break-inside: avoid; }
    [data-testid="stExpander"] { break-inside: avoid; page-break-inside: avoid; }
}
</style>
""", unsafe_allow_html=True)


# ── 유틸: LangChain + FAISS 로딩 ────────────────────────────
@st.cache_resource(show_spinner=False)
def load_vectorstore(db_path: str):
    try:
        from langchain_openai import OpenAIEmbeddings
        from langchain_community.vectorstores import FAISS
        embeddings = OpenAIEmbeddings(api_key=st.session_state.get("api_key", os.getenv("OPENAI_API_KEY", "")))
        vs = FAISS.load_local(db_path, embeddings, allow_dangerous_deserialization=True)
        return vs
    except Exception as e:
        return None


def get_rag_answer(question: str, history: list, api_key: str) -> tuple[str, list[str]]:
    """RAG 답변 생성. (answer, sources) 반환"""
    from langchain_openai import ChatOpenAI, OpenAIEmbeddings
    from langchain_community.vectorstores import FAISS
    

    db_path = "vector_db/faiss_stat_integrated_db"
    if not Path(db_path).exists():
        db_path = "vector_db/faiss_stat501_db"
    if not Path(db_path).exists():
        return "⚠️ 벡터 DB를 찾을 수 없습니다. `vector_db/` 폴더가 있는지 확인해 주세요.", []

    embeddings = OpenAIEmbeddings(api_key=api_key)
    vs = FAISS.load_local(db_path, embeddings, allow_dangerous_deserialization=True)
    retriever = vs.as_retriever(search_kwargs={"k": 4})

    llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key, temperature=0.2, streaming=False)

    system_prompt = """당신은 Penn State STAT 501(회귀분석)과 STAT 504(이산형 데이터 분석) 강의 자료를 기반으로 통계 가이드라인을 제공하는 전문 어시스턴트입니다.

규칙:
1. [가장 중요] 오직 아래 제공된 컨텍스트(벡터 DB 검색 결과)에 실제로 적혀 있는 내용만으로 답변하세요. 컨텍스트에 없는 공식·수치·정의·예시·기법 이름은 당신이 알고 있더라도 절대 지어내거나 보충하지 마세요. 사전 학습 지식·일반 상식은 사용 금지입니다.
   - 특히 다음을 금지합니다: 컨텍스트에 등장하지 않는 검정/기법/모델 이름을 언급하는 것 (예: 컨텍스트에 없는데 "Breusch-Pagan 검정", "Levene 검정", "ARIMA", "Lasso 회귀", "주성분 회귀", "조건수" 등을 답변에 추가하면 안 됨).
   - 컨텍스트에 부분적으로만 있으면 그 부분까지만 설명하고, 나머지는 "제공된 자료에는 이 부분에 대한 추가 설명이 없습니다"라고 솔직히 밝히세요.
2. 답변하기 전에 먼저 판단하세요: "이 질문이 컨텍스트의 통계 주제(회귀분석·이산자료 분석)와 실제로 관련이 있는가?"
   - 질문이 통계 분석과 무관하거나(예: 날씨·일상 잡담·코딩·일반 시사), 컨텍스트가 질문과 명백히 다른 분야(예: 의사결정 트리·딥러닝·랜덤포레스트·XGBoost)이면, 컨텍스트에 우연히 비슷한 단어가 있더라도 억지로 답하지 말고 정확히 다음 문장만 출력하세요:
   "제공된 자료에서 해당 내용을 찾을 수 없습니다. STAT 501(회귀분석) 또는 STAT 504(이산자료 분석) 범위 안의 질문을 주세요."
   - 거절 시에는 어떤 보충 설명·추측·일반 지식도 절대 추가하지 마세요.
   - 회귀분석·로지스틱회귀·분산분석·카이제곱·오즈비·잔차·상관·다중공선성·MLE 등 명백한 통계 주제는 거절하지 말고 컨텍스트 근거로 답하세요.
3. 답변은 한국어로 작성하되, 통계 용어는 영어 병기(예: 다중공선성(Multicollinearity))하세요. 영어 원문은 자연스러운 한국어로 풀어 설명하세요.
4. 핵심 가정, 검정 방법, 위반 시 조치를 제시하되, 반드시 컨텍스트에 있는 내용에 한해서만 제시하세요. 컨텍스트에 없으면 만들어내지 마세요.
5. 출처 URL은 별도 박스에 자동 표시되므로 답변 본문에 URL을 직접 쓰지 마세요.
6. 이미지는 답변에 절대 포함하지 마세요. `![설명](url)` 형식의 markdown 이미지 문법을 사용하지 마세요.
   - 이유: 외부 사이트(Penn State)의 이미지가 hotlink 차단되어 어차피 화면에 표시되지 않습니다.
   - 시각적 그래프 설명이 필요하면 "잔차 플롯에서는 점들이 0을 중심으로 무작위로 흩어진 모습을 확인할 수 있다" 같은 텍스트 묘사로만 표현하세요.
7. 수식은 LaTeX 문법으로 작성하세요. 인라인은 `$수식$`, 블록 수식은 `$$수식$$`. 단순한 변수도 LaTeX로 감싸 일관되게 표기하세요."""
  
    from langchain_core.prompts import PromptTemplate
    qa_prompt = PromptTemplate.from_template(
        system_prompt + "\n\n컨텍스트:\n{context}\n\n질문: {question}\n\n답변:"
    )

    # ── 검색용 영어 쿼리 생성 ──
    # 자료는 영어(Penn State)인데 질문은 한국어라 임베딩 매칭이 약함.
    # 검색 전에 한국어 질문을 영어 통계 키워드로 번역·확장해서 검색 정확도를 높인다.
    import openai
    _client = openai.OpenAI(api_key=api_key)
    try:
        _tr = _client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            messages=[
                {"role": "system", "content": "You translate Korean statistics questions into concise English search queries using standard statistical terminology (e.g., '오즈비' → 'odds ratio'). Output ONLY the English query, no explanation."},
                {"role": "user", "content": question},
            ],
        )
        search_query = _tr.choices[0].message.content.strip()
    except Exception:
        search_query = question  # 번역 실패 시 원문으로 폴백

    # 한국어 원문 + 영어 번역 둘 다로 검색 (양쪽 매칭 보강)
    docs = retriever.invoke(f"{search_query} {question}")
    context_text = "\n\n---\n\n".join([d.page_content for d in docs])

    # 출처: 각 청크의 metadata['source']에서 추출 (DB 빌드 시 단원별로 부착됨)
    urls = set()
    for d in docs:
        url = d.metadata.get("source", "")
        if url:
            urls.add(url)
    sources = sorted(urls)
    

    messages = [
        {"role": "system", "content": system_prompt},
    ]
    for h in history[-6:]:
        messages.append({"role": "user",      "content": h["user"]})
        messages.append({"role": "assistant", "content": h["assistant"]})
    messages.append({"role": "user", "content": f"컨텍스트:\n{context_text}\n\n질문: {question}"})

    import openai
    client = openai.OpenAI(api_key=api_key)
    resp = client.chat.completions.create(model="gpt-4o-mini", messages=messages, temperature=0.2)
    answer = resp.choices[0].message.content

    # 디버그용: 검색된 원문 청크 본문도 함께 반환
    retrieved_chunks = [d.page_content for d in docs]

    return answer, sources, retrieved_chunks


# ── 통계 기법 추천 로직 ──────────────────────────────────────
METHODS = {
    ("연속형", "연속형", "단순 관계 파악"): {
        "name": "단순 선형 회귀 (Simple Linear Regression)",
        "desc": "연속형 독립변수 1개로 연속형 종속변수를 예측합니다.",
        "assumptions": ["선형성(Linearity)", "오차의 정규성", "등분산성(Homoscedasticity)", "독립성"],
        "tags": ["STAT 501", "Regression"],
        "url": "https://online.stat.psu.edu/stat501/lesson/1",
    },
    ("연속형", "연속형", "다중 예측/설명"): {
        "name": "다중 선형 회귀 (Multiple Linear Regression)",
        "desc": "여러 연속형 독립변수로 연속형 종속변수를 예측합니다.",
        "assumptions": ["선형성", "다중공선성 없음(No Multicollinearity)", "오차의 정규성", "등분산성"],
        "tags": ["STAT 501", "Regression", "VIF 확인 필요"],
        "url": "https://online.stat.psu.edu/stat501/lesson/5",
    },
    ("범주형(2개)", "연속형", "단순 관계 파악"): {
        "name": "독립표본 t-검정 (Independent t-test)",
        "desc": "두 집단의 평균을 비교합니다.",
        "assumptions": ["정규성", "등분산성(Levene 검정)", "독립성"],
        "tags": ["STAT 501", "t-test"],
        "url": "https://online.stat.psu.edu/stat501/lesson/2",
    },
    ("범주형(2개)", "이항형(0/1)", "다중 예측/설명"): {
        "name": "로지스틱 회귀 (Logistic Regression)",
        "desc": "이항형 종속변수의 확률을 모델링합니다.",
        "assumptions": ["선형 로짓 관계", "다중공선성 없음", "충분한 표본 크기", "이상치 없음"],
        "tags": ["STAT 504", "Logistic", "이항형 종속변수"],
        "url": "https://online.stat.psu.edu/stat504/lesson/3",
    },
    ("이항형(0/1)", "이항형(0/1)", "단순 관계 파악"): {
        "name": "카이제곱 검정 (Chi-Square Test)",
        "desc": "두 범주형 변수 간의 독립성을 검정합니다.",
        "assumptions": ["기대 빈도 ≥ 5", "독립적인 관측치"],
        "tags": ["STAT 504", "Chi-Square", "범주형"],
        "url": "https://online.stat.psu.edu/stat504/lesson/2",
    },
    ("범주형(3개+)", "연속형", "다중 예측/설명"): {
        "name": "일원 분산분석 (One-Way ANOVA)",
        "desc": "3개 이상 집단의 평균을 동시에 비교합니다.",
        "assumptions": ["정규성", "등분산성", "독립성"],
        "tags": ["STAT 501", "ANOVA"],
        "url": "https://online.stat.psu.edu/stat501/lesson/10",
    },
}

DEFAULT_REC = {
    "name": "추가 정보가 필요합니다",
    "desc": "선택한 조합에 대한 특정 추천이 없습니다. Tab 2의 챗봇에 더 자세히 설명해 주세요.",
    "assumptions": [],
    "tags": ["챗봇 문의 권장"],
    "url": "",
}


# ── 세션 초기화 ──────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "api_key" not in st.session_state:
    st.session_state.api_key = os.getenv("OPENAI_API_KEY", "")


# ── 헤더 ─────────────────────────────────────────────────────
st.markdown("""
<div class="site-header">
    <span class="site-title">StatQA</span>
    <span class="site-badge">RAG v1.0</span>
    <span class="site-sub">Penn State STAT 501 · 504 기반</span>
</div>
""", unsafe_allow_html=True)

# ── 사이드바 (제안서 2.1: 프로젝트 개요 + 사용 가이드 + 출처 + 설정) ──
with st.sidebar:
    st.markdown('<div class="sb-brand">📐 StatQA</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-brand-sub">통계 가이드라인 RAG 어시스턴트</div>', unsafe_allow_html=True)

    # 프로젝트 개요
    st.markdown('<div class="sb-section">프로젝트 개요</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sb-card">검증된 통계 전공 자료(<b>Penn State</b>)만을 근거로 답하는 RAG 챗봇입니다. '
        'AI가 자료에 없는 내용을 지어내는 <b>환각(Hallucination)</b>을 차단하도록 설계되었습니다.</div>',
        unsafe_allow_html=True,
    )

    # 사용 가이드
    st.markdown('<div class="sb-section">사용 가이드</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sb-card">① <b>기법 추천</b> 탭: 데이터 유형을 고르면 적합한 분석법을 추천<br>'
        '② <b>통계 검증 챗봇</b> 탭: 통계 개념·가정·방법론을 자연어로 질문<br>'
        '③ 답변 하단에서 참고한 <b>출처 단원</b>을 확인</div>',
        unsafe_allow_html=True,
    )

    # 참고 자료 출처
    st.markdown('<div class="sb-section">참고 자료 (Data Source)</div>', unsafe_allow_html=True)
    st.markdown(
        '<a class="sb-src" href="https://online.stat.psu.edu/stat501/" target="_blank">'
        'Penn State STAT 501 <span>회귀분석</span></a>'
        '<a class="sb-src" href="https://online.stat.psu.edu/stat504/" target="_blank">'
        'Penn State STAT 504 <span>이산자료 분석</span></a>',
        unsafe_allow_html=True,
    )

    # 설정
    st.markdown('<div class="sb-section">설정</div>', unsafe_allow_html=True)
    api_input = st.text_input(
        "OpenAI API Key",
        value=st.session_state.api_key,
        type="password",
        placeholder="sk-proj-...",
        help=".env 파일에 OPENAI_API_KEY가 있으면 자동으로 로드됩니다.",
    )
    if api_input:
        st.session_state.api_key = api_input
    st.caption("키는 세션 내에서만 사용되며 저장되지 않습니다.")

    debug_mode = st.checkbox("🔧 디버그 모드 (검색 청크·raw 답변 표시)", value=False)
    st.session_state["debug_mode"] = debug_mode


# ── 탭 ───────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["01 · 기법 추천", "02 · 통계 검증 챗봇"])


# ══════════════════════════════════════════════════════════════
# TAB 1 — 통계 기법 추천 시뮬레이터
# ══════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-label">Methodology Recommender</div>', unsafe_allow_html=True)
    st.markdown("데이터 특성을 입력하면 적합한 통계 분석 기법과 확인해야 할 가정을 추천해 드립니다.")
    st.markdown("")

    col1, col2, col3 = st.columns([1, 1, 1], gap="medium")

    with col1:
        iv_type = st.selectbox(
            "독립변수(X) 유형",
            ["연속형", "범주형(2개)", "범주형(3개+)", "이항형(0/1)"],
            help="예측하거나 설명하는 변수의 유형"
        )
    with col2:
        dv_type = st.selectbox(
            "종속변수(Y) 유형",
            ["연속형", "이항형(0/1)", "범주형(3개+)", "카운트형"],
            help="예측 대상 변수의 유형"
        )
    with col3:
        purpose = st.selectbox(
            "분석 목적",
            ["단순 관계 파악", "다중 예측/설명", "집단 간 비교", "시계열/반복 측정"],
        )

    st.markdown("")
    run_btn = st.button("기법 추천 받기 →", use_container_width=False)

    if run_btn:
        key = (iv_type, dv_type, purpose)
        rec = METHODS.get(key, DEFAULT_REC)

        st.markdown("---")
        st.markdown('<div class="section-label">추천 결과</div>', unsafe_allow_html=True)

        tags_html = "".join([f'<span class="tag tag-method">{t}</span>' for t in rec["tags"]])
        url_html = f'<a href="{rec["url"]}" target="_blank">📎 Penn State 원문 →</a>' if rec["url"] else ""

        st.markdown(f"""
        <div class="rec-card">
            <div class="rec-card-title">{rec["name"]}</div>
            <div class="rec-card-sub">{rec["desc"]}</div>
            {tags_html}
        </div>
        """, unsafe_allow_html=True)

        if rec["assumptions"]:
            st.markdown("")
            st.markdown('<div class="section-label">확인해야 할 가정 (Assumptions)</div>', unsafe_allow_html=True)
            for i, a in enumerate(rec["assumptions"], 1):
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:0.7rem;padding:0.5rem 0;border-bottom:1px solid var(--border)">
                    <span style="font-family:'DM Mono',monospace;font-size:0.7rem;color:var(--accent);min-width:1.5rem">{i:02d}</span>
                    <span style="font-size:0.88rem">{a}</span>
                </div>
                """, unsafe_allow_html=True)

        if url_html:
            st.markdown(f'<div class="source-block">출처: {url_html}</div>', unsafe_allow_html=True)

        st.markdown("")
        st.info("💬 더 구체적인 상황(표본 크기, 정규성 검정 결과 등)은 **Tab 02 챗봇**에 질문하세요.")


# ══════════════════════════════════════════════════════════════
# TAB 2 — RAG 기반 통계 검증 챗봇
# ══════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-label">Stat Validator Chatbot</div>', unsafe_allow_html=True)
    st.markdown("통계 분석 아이디어, 가정 검토, 방법론 적절성 등을 질문하세요. Penn State 강의 자료를 근거로 답변합니다.")
    st.markdown("")

    # 대화 히스토리 출력
    # Streamlit 네이티브 st.chat_message 사용 → markdown·LaTeX·이미지 자동 렌더링
    if st.session_state.chat_history:
        import re as _re

        # Penn State 이미지가 hotlink 차단되어 표시 불가 — 모든 markdown 이미지 제거
        _any_img_pattern = _re.compile(r'!\[[^\]]*\]\([^)]*\)')
        # URL → 사람이 읽기 좋은 라벨 변환용 패턴들
        _src_pat_501_sub = _re.compile(r'/stat(\d+)/lesson/(\d+)/\d+\.(\d+)')
        _src_pat_501_main = _re.compile(r'/stat(\d+)/lesson/(\d+)/?$')
        _src_pat_504 = _re.compile(r'/stat(\d+)/Lesson(\d+)')
        _img_url_exts = ('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp')

        def clean_assistant_text(text: str) -> str:
            # 이미지 markdown 전부 제거 (Penn State hotlink 차단으로 어차피 표시 불가)
            text = _any_img_pattern.sub("", text)
            # KaTeX가 모르는 LaTeX 명령 보정 (\mbox → \text 등)
            text = text.replace(r"\mbox", r"\text")
            return text

        def format_source(url: str) -> tuple[str, str]:
            """URL을 (라벨, 실제 링크 URL) 튜플로 변환.
            STAT 501: 사이트 개편으로 lesson URL이 404 → 메인 페이지로 폴백
            STAT 504: lesson URL이 살아있음 → 그대로 사용
            반환: (사람이 읽기 좋은 라벨, 실제 클릭하면 열릴 URL)
            """
            m = _src_pat_501_sub.search(url)
            if m:
                label = f"STAT {m.group(1)} · Lesson {m.group(2)}.{m.group(3)}"
                return label, f"https://online.stat.psu.edu/stat{m.group(1)}/"
            m = _src_pat_501_main.search(url)
            if m:
                label = f"STAT {m.group(1)} · Lesson {m.group(2)}"
                return label, f"https://online.stat.psu.edu/stat{m.group(1)}/"
            m = _src_pat_504.search(url)
            if m:
                label = f"STAT {m.group(1)} · Lesson {int(m.group(2))}"
                return label, url  # STAT 504는 원본 URL 그대로
            return url, url

        def is_valid_source(url: str) -> bool:
            if "base64" in url or "data:" in url or len(url) > 200:
                return False
            if url.lower().endswith(_img_url_exts):
                return False
            if "/assets/" in url or "/files/" in url:
                return False
            return True

        debug_mode = st.session_state.get("debug_mode", False)

        for turn in st.session_state.chat_history:
            with st.chat_message("user", avatar="🧑"):
                st.markdown(turn["user"])

            with st.chat_message("assistant", avatar="📐"):
                cleaned = clean_assistant_text(turn["assistant"])
                st.markdown(cleaned)

                # 디버그 모드: 검색된 원문 청크 + LLM 답변
                if debug_mode:
                    chunks = turn.get("chunks", [])
                    with st.expander(f"🔧 디버그 ① 검색된 원문 청크 ({len(chunks)}개) — DB에서 가져온 근거"):
                        for ci, chunk in enumerate(chunks, 1):
                            st.markdown(f"**[청크 {ci}]**")
                            st.code(chunk, language="markdown")
                    with st.expander("🔧 디버그 ② LLM 원본 답변 (가공 전)"):
                        st.code(turn["assistant"], language="markdown")

                # 출처 표시 (한 번 더 필터링 + 사람이 읽기 좋은 라벨 + 죽은 링크 폴백)
                if turn.get("sources"):
                    valid_sources = [s for s in turn["sources"] if is_valid_source(s)]
                    if valid_sources:
                        # 중복 라벨 제거 (예: 같은 단원 청크 여러 개 매칭됐을 때)
                        seen_labels = set()
                        unique_pairs = []
                        for s in valid_sources:
                            label, link = format_source(s)
                            if label not in seen_labels:
                                seen_labels.add(label)
                                unique_pairs.append((label, link))

                        src_links = " &nbsp;·&nbsp; ".join(
                            f'<a href="{link}" target="_blank">{label}</a>'
                            for label, link in unique_pairs
                        )
                        st.markdown(
                            f'<div class="source-block">📎 출처: {src_links}</div>',
                            unsafe_allow_html=True,
                        )

    # 입력 영역
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_area(
            "질문 입력",
            placeholder="예: 종속변수가 0과 1인데 선형회귀를 써도 될까요?\n예: 잔차 플롯에서 팬 모양이 보이는데 어떻게 해야 하나요?",
            height=100,
            label_visibility="collapsed",
        )
        col_send, col_clear, _ = st.columns([1.2, 1, 5])
        with col_send:
            send = st.form_submit_button("전송 →", use_container_width=True)
        with col_clear:
            clear = st.form_submit_button("초기화", use_container_width=True)

    if clear:
        st.session_state.chat_history = []
        st.rerun()

    if send and user_input.strip():
        if not st.session_state.api_key:
            st.error("사이드바에서 OpenAI API Key를 입력해 주세요.")
        else:
            with st.spinner("Penn State 자료를 검색하는 중..."):
                try:
                    answer, sources, retrieved_chunks = get_rag_answer(
                        user_input.strip(),
                        st.session_state.chat_history,
                        st.session_state.api_key,
                    )
                    st.session_state.chat_history.append({
                        "user": user_input.strip(),
                        "assistant": answer,
                        "sources": sources,
                        "chunks": retrieved_chunks,
                    })
                    st.rerun()
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")

    if not st.session_state.chat_history:
        st.markdown("""
        <div style="padding:2rem;text-align:center;color:var(--muted);font-size:0.85rem;border:1px dashed var(--border);border-radius:8px;margin-top:1rem">
            <div style="font-size:1.5rem;margin-bottom:0.5rem">📐</div>
            질문을 입력하면 Penn State STAT 501·504 자료를 검색하여 답변합니다.<br>
            <span style="font-family:'DM Mono',monospace;font-size:0.75rem">vector_db/ 폴더와 API Key가 필요합니다.</span>
        </div>
        """, unsafe_allow_html=True)
