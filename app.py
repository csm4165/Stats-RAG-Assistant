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
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=DM+Mono:wght@400;500&family=Pretendard:wght@300;400;500;600&display=swap');

:root {
    --bg:       #0f0f11;
    --surface:  #18181c;
    --border:   #2a2a32;
    --accent:   #7c6aff;
    --accent2:  #00e5b0;
    --text:     #e8e8f0;
    --muted:    #6b6b80;
    --user-bg:  #1e1e28;
    --ai-bg:    #141420;
}

/* reset */
html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; }
.stApp { background: var(--bg); color: var(--text); }
.block-container { max-width: 900px; padding: 2rem 1.5rem; }

/* hide streamlit chrome */
#MainMenu, footer { visibility: hidden; }
.stDeployButton { display: none; }

/* ── header ── */
.site-header {
    display: flex; align-items: baseline; gap: 1rem;
    border-bottom: 1px solid var(--border);
    padding-bottom: 1.2rem; margin-bottom: 2rem;
}
.site-title {
    font-family: 'Instrument Serif', serif;
    font-size: 2.1rem; color: var(--text); letter-spacing: -0.02em;
}
.site-badge {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem; color: var(--accent2);
    border: 1px solid var(--accent2);
    padding: 2px 8px; border-radius: 4px; letter-spacing: 0.08em;
}
.site-sub {
    font-size: 0.85rem; color: var(--muted); margin-left: auto;
}

/* ── tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0; background: var(--surface);
    border: 1px solid var(--border); border-radius: 8px;
    padding: 4px; margin-bottom: 1.5rem;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.78rem !important; letter-spacing: 0.04em;
    color: var(--muted) !important;
    background: transparent !important;
    border-radius: 5px; padding: 8px 20px;
    border: none !important;
    transition: all 0.15s ease;
}
.stTabs [aria-selected="true"] {
    color: var(--text) !important;
    background: var(--border) !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 0; }
.stTabs [data-baseweb="tab-highlight"] { display: none; }
.stTabs [data-baseweb="tab-border"] { display: none; }

/* ── form elements ── */
.stSelectbox > div > div,
.stRadio > div,
.stTextArea > div > div {
    background: var(--surface) !important;
    border-color: var(--border) !important;
    border-radius: 6px !important;
    color: var(--text) !important;
}
.stSelectbox label, .stRadio label, .stTextArea label,
.stNumberInput label, .stSlider label {
    font-size: 0.82rem !important; color: var(--muted) !important;
    font-weight: 500 !important; letter-spacing: 0.03em;
    text-transform: uppercase;
}
.stButton > button {
    background: var(--accent) !important;
    color: #fff !important; border: none !important;
    border-radius: 6px !important; font-family: 'DM Mono', monospace !important;
    font-size: 0.78rem !important; letter-spacing: 0.05em;
    padding: 0.55rem 1.4rem !important;
    transition: opacity 0.15s ease;
}
.stButton > button:hover { opacity: 0.85; }

/* ── chat messages ── */
.msg-wrap { display: flex; flex-direction: column; gap: 1rem; margin-bottom: 1.5rem; }
.msg { padding: 1rem 1.2rem; border-radius: 8px; line-height: 1.65; font-size: 0.92rem; }
.msg-user { background: var(--user-bg); border-left: 2px solid var(--accent); }
.msg-ai   { background: var(--ai-bg);   border-left: 2px solid var(--accent2); }
.msg-role {
    font-family: 'DM Mono', monospace; font-size: 0.68rem;
    letter-spacing: 0.08em; text-transform: uppercase;
    margin-bottom: 0.4rem;
}
.msg-user .msg-role { color: var(--accent); }
.msg-ai   .msg-role { color: var(--accent2); }

/* ── source badge ── */
.source-block {
    margin-top: 0.8rem; padding: 0.6rem 0.9rem;
    background: #0f0f18; border: 1px solid var(--border);
    border-radius: 6px; font-size: 0.78rem;
    font-family: 'DM Mono', monospace; color: var(--muted);
}
.source-block a { color: var(--accent2) !important; text-decoration: none; }
.source-block a:hover { text-decoration: underline; }

/* ── recommender cards ── */
.rec-card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 8px; padding: 1.2rem 1.4rem; margin-bottom: 0.8rem;
}
.rec-card-title {
    font-family: 'Instrument Serif', serif;
    font-size: 1.1rem; color: var(--text); margin-bottom: 0.4rem;
}
.rec-card-sub { font-size: 0.82rem; color: var(--muted); margin-bottom: 0.6rem; }
.tag {
    display: inline-block;
    font-family: 'DM Mono', monospace; font-size: 0.68rem;
    letter-spacing: 0.06em; padding: 2px 8px;
    border-radius: 4px; margin-right: 6px; margin-top: 4px;
}
.tag-method  { background: #1a1a3a; color: var(--accent); border: 1px solid var(--accent); }
.tag-warn    { background: #1a1200; color: #f5c542; border: 1px solid #f5c542; }
.tag-ok      { background: #001a12; color: var(--accent2); border: 1px solid var(--accent2); }

/* ── section label ── */
.section-label {
    font-family: 'DM Mono', monospace; font-size: 0.7rem;
    letter-spacing: 0.1em; text-transform: uppercase;
    color: var(--muted); margin-bottom: 0.6rem;
}

/* ── divider ── */
hr { border-color: var(--border) !important; margin: 1.5rem 0; }

/* spinner */
.stSpinner > div { border-top-color: var(--accent) !important; }
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
1. 제공된 컨텍스트(벡터 DB 검색 결과)에 근거해 답변하세요. 컨텍스트에 부분적으로라도 관련된 정보가 있다면 그것을 활용해 충실히 설명하세요.
2. 컨텍스트가 질문과 완전히 무관한 주제(예: 컨텍스트는 선형회귀인데 질문은 의사결정 트리·딥러닝 등 다른 분야)일 때만 거절하세요. 거절할 때는 정확히 다음 문장만 출력하세요:
   "제공된 자료에서 해당 내용을 찾을 수 없습니다. STAT 501(회귀분석) 또는 STAT 504(이산자료 분석) 범위 안의 질문을 주세요."
   거절 시에는 어떤 보충 설명·일반 지식도 절대 추가하지 마세요.
3. 답변은 한국어로 작성하되, 통계 용어는 영어 병기(예: 다중공선성(Multicollinearity))하세요. 영어 원문은 자연스러운 한국어로 풀어 설명하세요.
4. 핵심 가정, 검정 방법, 위반 시 조치를 구체적으로 제시하세요.
5. 출처 URL은 별도 박스에 자동 표시되므로 답변 본문에 URL을 직접 쓰지 마세요.
6. 이미지는 답변에 절대 포함하지 마세요. `![설명](url)` 형식의 markdown 이미지 문법을 사용하지 마세요.
   - 이유: 외부 사이트(Penn State)의 이미지가 hotlink 차단되어 어차피 화면에 표시되지 않습니다.
   - 시각적 그래프 설명이 필요하면 "잔차 플롯에서는 점들이 0을 중심으로 무작위로 흩어진 모습을 확인할 수 있다" 같은 텍스트 묘사로만 표현하세요.
7. 수식은 LaTeX 문법으로 작성하세요. 인라인은 `$수식$`, 블록 수식은 `$$수식$$`. 단순한 변수도 LaTeX로 감싸 일관되게 표기하세요."""
  
    from langchain_core.prompts import PromptTemplate
    qa_prompt = PromptTemplate.from_template(
        system_prompt + "\n\n컨텍스트:\n{context}\n\n질문: {question}\n\n답변:"
    )

    docs = retriever.invoke(question)
    context_text = "\n\n---\n\n".join([d.page_content for d in docs])

    # 청크 본문에서 Penn State 강의 URL만 추출 (이미지 파일 URL 제외)
    import re
    url_pattern = re.compile(r'https?://online\.stat\.psu\.edu/[^\s\n\)"\']+')
    image_exts = ('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.bmp')
    urls = set()
    for d in docs:
        for m in url_pattern.finditer(d.page_content):
            url = m.group(0).rstrip(').,;:')
            # 1) base64/data 잡음 제외
            if "data:" in url or "base64" in url or len(url) > 200:
                continue
            # 2) 이미지 파일 URL 제외 (출처는 강의 페이지여야 함)
            if url.lower().endswith(image_exts):
                continue
            # 3) /assets/ 같은 정적 파일 경로 제외
            if "/assets/" in url or "/files/" in url:
                continue
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

    return answer, sources


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

# API Key 입력 (사이드바)
with st.sidebar:
    st.markdown("### ⚙️ 설정")
    api_input = st.text_input(
        "OpenAI API Key",
        value=st.session_state.api_key,
        type="password",
        placeholder="sk-proj-...",
        help=".env 파일에 OPENAI_API_KEY가 있으면 자동으로 로드됩니다."
    )
    if api_input:
        st.session_state.api_key = api_input
    st.caption("키는 세션 내에서만 사용되며 저장되지 않습니다.")
    st.markdown("---")
    st.markdown("**벡터 DB 경로**")
    st.code("vector_db/faiss_stat_integrated_db", language=None)
    st.caption("폴더가 없으면 faiss_stat501_db로 폴백합니다.")


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
            return _any_img_pattern.sub("", text)

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

        # 디버그 토글 (사이드바)
        with st.sidebar:
            st.markdown("---")
            debug_mode = st.checkbox("🔧 디버그 모드 (raw 답변·검색 청크 표시)", value=False)

        for turn in st.session_state.chat_history:
            with st.chat_message("user", avatar="🧑"):
                st.markdown(turn["user"])

            with st.chat_message("assistant", avatar="📐"):
                cleaned = clean_assistant_text(turn["assistant"])
                st.markdown(cleaned)

                # 디버그 모드: LLM 원본 답변과 정제 후 텍스트 비교
                if debug_mode:
                    with st.expander("🔧 디버그 — LLM 원본 답변"):
                        st.code(turn["assistant"], language="markdown")
                    with st.expander("🔧 디버그 — 정제(clean) 후 텍스트"):
                        st.code(cleaned, language="markdown")

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
                    answer, sources = get_rag_answer(
                        user_input.strip(),
                        st.session_state.chat_history,
                        st.session_state.api_key,
                    )
                    st.session_state.chat_history.append({
                        "user": user_input.strip(),
                        "assistant": answer,
                        "sources": sources,
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
