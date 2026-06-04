# 📐 Stats-RAG-Assistant (StatQA)

**검증된 통계 강의 자료(Penn State STAT 501·504)만을 근거로 답하는 RAG 기반 통계 질의응답 챗봇.**
일반 LLM의 **환각(Hallucination)** — 자료에 없는 내용을 그럴듯하게 지어내는 문제 — 을 차단하는 데 초점을 맞췄습니다. 자료에 없으면 **정직하게 거절**하고, 모든 답변에 **근거 출처**를 표시합니다.

> 📚 데이터 출처: [Penn State STAT 501 — Regression Methods](https://online.stat.psu.edu/stat501/) · [STAT 504 — Analysis of Discrete Data](https://online.stat.psu.edu/stat504/)

---

## 📑 목차

1. [주요 기능](#-주요-기능)
2. [빠른 시작 (로컬)](#-빠른-시작-로컬-실행) · [Docker](#-docker로-실행-선택)
3. [이렇게 동작합니다](#-이렇게-동작합니다)
4. [시스템 개요](#️-시스템-개요)
5. [동작 원리 자세히](#-동작-원리-자세히) — 준비 단계 / 실행 단계
6. [핵심 구현 디테일](#-핵심-구현-디테일)
7. [설정 바꾸기](#️-설정-바꾸기-커스터마이징) · [문제 해결](#️-문제-해결-troubleshooting)
8. [폴더 구조](#-폴더-구조) · [처음부터 빌드](#-처음부터-다시-빌드하고-싶다면) · [평가 결과](#-평가-결과)

---

## ✨ 주요 기능

- **🔍 근거 기반 답변(RAG)** — 답하기 전 검증된 강의 자료를 먼저 검색해 그 범위 안에서만 답변
- **🚫 환각 차단 3중 장치** — ①검증 자료만 DB화 ②"없으면 거절" 시스템 프롬프트 ③출처 표기로 사용자 검증
- **🌏 한국어 ↔ 영어** — 한국어로 질문하면 영어로 번역해 검색하고, 답변은 다시 한국어로 (Query Translation)
- **📎 출처 표시** — 모든 답변에 근거가 된 STAT 501·504 단원을 함께 표시
- **🔧 디버그 모드** — 답변의 근거가 된 실제 검색 청크를 화면에서 직접 확인 가능
- **🧭 두 개의 탭** — ① 규칙 기반 기법 추천 시뮬레이터 ② RAG 통계 검증 챗봇(핵심)

---

## 🚀 빠른 시작 (로컬 실행)

> 빌드된 벡터 DB(`vector_db/faiss_stat_integrated_db/`)가 저장소에 포함되어 있어, **OpenAI API 키만 설정하면 바로 실행**됩니다. 크롤링·DB 빌드를 다시 할 필요가 없습니다.

### 1. 클론
```bash
git clone https://github.com/csm4165/Stats-RAG-Assistant.git
cd Stats-RAG-Assistant
```

### 2. 가상환경 + 의존성 설치 (Python 3.11 이상, 3.12 권장)
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. OpenAI API 키 설정
`.env.example`을 복사해 `.env`를 만들고 **본인의** OpenAI 키를 넣습니다. (키는 [platform.openai.com](https://platform.openai.com/api-keys)에서 발급)
```bash
cp .env.example .env        # Windows: copy .env.example .env
```
```
OPENAI_API_KEY=sk-proj-여기에_본인의_키
```
> ⚠️ `.env`는 `.gitignore`로 제외되어 GitHub에 올라가지 않습니다. 앱 사이드바에서 직접 입력할 수도 있습니다.

### 4. 앱 실행
```bash
streamlit run app.py
```
브라우저에서 `http://localhost:8501` 이 자동으로 열립니다. **Tab 2 — 통계 검증 챗봇**에 한국어로 질문해 보세요.
예: `"오즈비가 뭐고 어떻게 해석해?"`, `"종속변수가 0/1인데 선형회귀 써도 돼?"`

---

## 🐳 Docker로 실행 (선택)

`.env`를 만든 뒤(위 3단계), 한 줄이면 됩니다.
```bash
docker compose up --build
```
→ `http://localhost:8501` 접속. 종료는 `docker compose down`.

---

## 💬 이렇게 동작합니다

| 질문 유형 | 동작 |
|---|---|
| 자료 안 질문 (예: "오즈비가 뭐야?") | 강의 자료 근거로 답변 + 출처 표시 |
| 부분만 있는 질문 | 있는 부분만 답하고 "추가 설명 없음" 명시 |
| 자료 밖 질문 (예: "딥러닝 학습법", "오늘 날씨") | **"제공된 자료에서 찾을 수 없습니다"** 로 거절 |

---

## 🏗️ 시스템 개요

```
[사용자 질문 (한국어)]
        ↓
[Streamlit Web UI]  ── Tab 1: 기법 추천 / Tab 2: RAG 챗봇
        ↓
[GPT-4o-mini 질의 번역]  한국어 → 영어 검색어
        ↓
[FAISS 벡터 검색]  의미상 가까운 상위 4개 청크 + 출처
        ↓
[GPT-4o-mini + 환각 차단 시스템 프롬프트]  청크 근거로만 답변
        ↓
[한국어 답변 + 출처(단원) + (디버그 시) 검색 청크]
```

| 계층 | 기술 | 역할 |
|---|---|---|
| 표현 (UI) | Streamlit, KaTeX | 채팅 화면·사이드바·탭, 수식 렌더링 |
| 로직 | Python, LangChain | RAG 파이프라인 연결·제어 |
| AI 모델 | GPT-4o-mini, OpenAI Embeddings(ada-002, 1536차원) | 번역·답변 생성 / 임베딩 |
| 데이터 검색 | FAISS (로컬 벡터 DB) | 벡터 저장·유사도 검색 |
| 전처리 | requests, BeautifulSoup4, markdownify, TextSplitter | 크롤링→변환→청킹 |
| 배포·환경 | Docker, docker-compose, python-dotenv | 컨테이너 실행·키 관리 |

---

## 🔬 동작 원리 자세히

이 시스템은 **두 개의 흐름**으로 나뉩니다. (A) 자료를 미리 검색 가능하게 만드는 **준비 단계**와, (B) 질문마다 실시간으로 도는 **실행 단계**입니다.

### (A) 준비 단계 — 벡터 DB 구축 (최초 1회, `notebooks/`)

> 비유하자면 "도서관에 책을 의미별로 정리해 꽂아 두는 작업". 이미 빌드된 결과(`vector_db/`)가 포함돼 있어 사용자는 다시 할 필요 없습니다.

1. **크롤링** (`notebooks/crawling/`) — `requests`로 Penn State 강의 페이지에 접속하고 `BeautifulSoup4`로 **본문만** 추출. `markdownify`로 HTML→Markdown 변환. (단순 텍스트가 아닌 Markdown을 쓰는 이유: 통계 강의의 핵심인 **표·수식 구조**를 보존하기 위해)
2. **정제** — 원본에 섞인 잡음 제거. ① 본문에 박힌 base64 이미지 문자열(약 58,623자) 정규식 제거 ② SAS 통계 SW가 만든 깨진 ASCII 그래프 제거. → 검색 오염 방지.
3. **청킹** — `RecursiveCharacterTextSplitter`로 긴 텍스트를 **1,500자** 단위로 분할(이웃끼리 **200자 겹침**). 문단→문장→단어 순으로 "의미가 덜 끊기는 경계"부터 자릅니다. → 총 **1,551개 청크**.
4. **임베딩** — 각 청크를 OpenAI `text-embedding-ada-002` 모델로 **1,536차원 벡터**(의미 좌표)로 변환.
5. **저장** — `FAISS`에 벡터 + 원문 + **출처 메타데이터(`source`=단원 URL)**를 함께 저장. (`index.faiss`=벡터, `index.pkl`=원문·출처)

### (B) 실행 단계 — 질문 처리 (질문마다, `app.py`의 `get_rag_answer()`)

> "손님(질문)이 오면 사서가 관련 책을 찾아 읽고 답해 주는 작업".

1. **질문 입력** — 사용자가 한국어로 질문. 최근 3턴(질문·답변 6개)의 대화 맥락도 함께 챙김.
2. **질의 번역** — `GPT-4o-mini`(`temperature=0`)가 한국어 질문을 영어 통계 검색어로 변환. 예: `"오즈비가 뭐야?"` → `"What is odds ratio?"` (자료가 영어라, 한국어 그대로 검색하면 정확도가 떨어지기 때문)
3. **검색** — 검색어를 같은 임베딩 모델로 벡터화하고, FAISS에서 **L2 거리**가 가장 가까운 **상위 4개 청크(top-k=4)**를 가져옴. 각 청크엔 출처가 딸려 옴.
4. **답변 생성** — `[시스템 프롬프트]+[최근 대화]+[청크 4개+질문]`을 `GPT-4o-mini`(`temperature=0.2`)에 전달. 시스템 프롬프트가 "청크에 있는 내용만으로 답하고, 없으면 거절하라"고 강제.
5. **후처리** — 답변에서 표시 불가능한 이미지·잡음 제거, 수식 보정. 검색에 쓰인 청크의 출처를 중복 제거 후 `"STAT 504 · Lesson 3"` 같은 라벨로 변환.
6. **표시** — `st.chat_message`로 답변·출처 표시. 디버그 모드면 근거 청크도 함께 펼쳐 보여 사용자가 검증 가능.

---

## 🧩 핵심 구현 디테일

`app.py`에서 각 기능이 실제로 어떻게 구현됐는지 정리합니다.

| 기능 | 어디에 / 어떻게 |
|---|---|
| **벡터 DB 로드** | `@st.cache_resource`로 1회만 로드해 메모리 캐싱 → 질문마다 다시 안 읽음 |
| **검색기** | `vs.as_retriever(search_kwargs={"k": 4})` — 상위 4개 청크 |
| **질의 번역** | `openai` 클라이언트로 GPT 호출(`temperature=0`), 실패 시 원문으로 폴백(`try/except`). 검색은 `"영어쿼리 + 원문"` 둘 다로 수행 |
| **출처 추출** | 검색 청크의 `d.metadata["source"]`를 `set`으로 중복 제거 → `format_source()`로 라벨 변환. STAT 501은 사이트 개편으로 세부 URL이 404라 메인 페이지로 폴백, 504는 원본 URL 유지 |
| **대화 맥락** | `history[-6:]`(최근 3턴)만 메시지에 포함 → 토큰 절약 + 오래된 맥락 오염 방지 |
| **환각 차단 프롬프트** | 시스템 프롬프트 7규칙: ①컨텍스트 내에서만 답변 ②없으면 거절 ③일반지식 보충 금지 ④없는 기법명(Lasso·ARIMA 등) 금지 ⑤한국어+영어 병기 ⑥이미지 금지 ⑦수식 LaTeX |
| **수식 렌더링** | `clean_assistant_text()`에서 `\(...\)`→`$...$`, `\[...\]`→`$$...$$` 변환 후 KaTeX 렌더 |
| **이미지 차단** | Penn State 이미지가 hotlink(403) 차단되어 안 뜨므로, 프롬프트 + 정규식 후처리로 이미지 markdown 제거 |
| **상태 유지** | 대화는 `st.session_state.chat_history`에 저장, 전송 시 `st.rerun()`으로 전체 대화 다시 렌더 |
| **인쇄(PDF)** | `@media print` CSS로 Ctrl+P 시 사이드바 숨김 + 본문 종이 폭 100% |

### 환각 차단 3중 장치
1. **데이터 통제** — 검증된 Penn State 자료만 DB화. 애초에 엉뚱한 출처가 존재하지 않음.
2. **시스템 프롬프트** — "검색된 청크에 없으면 지어내지 말고 거절하라" 강제.
3. **출처 표기** — 모든 답에 근거 단원 표시 → 사용자가 원문으로 사후 검증 가능.

---

## ⚙️ 설정 바꾸기 (커스터마이징)

| 바꾸고 싶은 것 | 방법 |
|---|---|
| 검색 청크 개수(top-k) | `app.py`의 `search_kwargs={"k": 4}` 값 수정 |
| 답변 모델 | `app.py`의 `ChatOpenAI(model="gpt-4o-mini", ...)` 변경 |
| 답변의 창의성 | `temperature` 값 조정 (0=일관적, 높을수록 자유로움) |
| 청크 크기/겹침 | `notebooks/build_db/`에서 `chunk_size`·`chunk_overlap` 수정 후 **DB 재빌드** 필요 |
| 임베딩 모델 | 변경 가능하나, 바꾸면 **DB 전체를 다시 임베딩(재빌드)**해야 함 (좌표계가 달라지므로) |
| 새 통계 자료 추가 | 새 텍스트를 `data/`에 넣고 `notebooks/build_db/`로 재빌드 |

---

## 🛠️ 문제 해결 (Troubleshooting)

| 증상 | 해결 |
|---|---|
| `⚠️ 벡터 DB를 찾을 수 없습니다` | `vector_db/faiss_stat_integrated_db/` 폴더가 있는지 확인 (클론 시 포함됨) |
| API 키 오류 / 답변 안 됨 | `.env`에 `OPENAI_API_KEY`가 올바른지, 또는 사이드바에 키를 입력했는지 확인. OpenAI 잔액도 확인 |
| 수식이 `\(...\)` 날것으로 보임 | 최신 코드(수식 후처리 포함)인지 확인 후 브라우저 새로고침 |
| `langchain` import 에러 | `pip install -r requirements.txt`로 **고정 버전** 그대로 설치 (버전이 다르면 API가 깨질 수 있음) |
| Python 버전 충돌 | Python **3.11 이상** 사용 (3.12 권장). 전용 가상환경(.venv) 사용 권장 |
| 출처 링크가 404 | STAT 501은 사이트 개편으로 세부 단원 URL이 죽어 메인으로 연결됨 (정상 동작) |

---

## 📁 폴더 구조

```
Stats-RAG-Assistant/
├── app.py                          # ⭐ 메인 — Streamlit 챗봇 + RAG 파이프라인(get_rag_answer)
├── data/                           # 크롤링·정제된 강의 텍스트
│   ├── stat501_full_data.txt
│   └── stat504_full_data.txt
├── vector_db/
│   ├── faiss_stat_integrated_db/   # ⭐ 앱이 사용하는 통합 벡터 DB (1,551개 청크)
│   └── faiss_stat501_db/           # STAT 501 단독 DB (참고용)
├── notebooks/
│   ├── crawling/                   # Penn State 사이트 크롤링
│   └── build_db/                   # 텍스트 → 벡터 DB 구축
├── tests/
│   ├── eval_questions.json         # 평가 질문 23개 (5범주)
│   └── eval_result.md              # 채점 결과 (95.7%)
├── .env.example                    # 환경 변수 템플릿
├── requirements.txt                # 의존성 (핵심 8개 버전 고정)
├── Dockerfile / docker-compose.yml # 컨테이너 실행
└── README.md
```

---

## 🔄 처음부터 다시 빌드하고 싶다면

> ⚠️ 보통은 필요 없습니다 — 빌드된 DB가 이미 포함돼 있습니다.

1. **크롤링**: `notebooks/crawling/`의 두 노트북 실행 → `data/`에 텍스트 생성
2. **DB 빌드**: `notebooks/build_db/build_integrated_db.ipynb` 실행 → `vector_db/faiss_stat_integrated_db/` 생성 (청킹 `chunk_size=1500`, `chunk_overlap=200`)
3. **실행**: `streamlit run app.py`

---

## 📊 평가 결과

실제 챗봇에 5범주 23개 질문을 입력하고, **디버그 모드로 검색된 청크와 답변을 1:1 대조**하여 수동 채점했습니다.

| 항목 | 결과 |
|---|---|
| 전체 정답률 | **22 / 23 ≈ 95.7%** (제안서 목표 70% 크게 상회) |
| 범위 밖 질문 거절 | **4 / 4 (100%)** — 환각 차단 작동 확인 |
| 출처 표시 | **23 / 23 (100%)** |

| 범주 | 점수 |
|---|---|
| A. 기본 개념 | 7 / 7 |
| B. 가정 검토 | 5 / 5 |
| C. 방법론 적절성 | 5 / 5 |
| D. 실전 시나리오 | 1.5 / 2 |
| E. 범위 밖 거절 | 4 / 4 |

자세한 채점 내역은 [`tests/eval_result.md`](tests/eval_result.md) 참고.

---

## 📝 라이선스 및 데이터 출처

- **코드**: 학습·연구용 오픈소스
- **데이터**: Penn State Eberly College of Science 공개 강의 자료
  - [STAT 501: Regression Methods](https://online.stat.psu.edu/stat501/)
  - [STAT 504: Analysis of Discrete Data](https://online.stat.psu.edu/stat504/)

---

## 🔗 참고 자료

- [LangChain Documentation](https://python.langchain.com/) · [FAISS](https://faiss.ai/) · [Streamlit](https://docs.streamlit.io/)
- RAG 개념: Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*, NeurIPS 2020
