# 경매 알림 SaaS - FastAPI 백엔드

경매 사이트를 크롤링하여 사용자가 등록한 키워드와 매칭되는 경매 물건을 찾고 알림을 보내는 SaaS 백엔드 API

## 🚀 기술 스택

- **FastAPI** - 현대적이고 빠른 웹 프레임워크
- **PostgreSQL** - Supabase 호스팅 데이터베이스
- **SQLAlchemy** - ORM
- **Alembic** - 데이터베이스 마이그레이션
- **BeautifulSoup** - 웹 크롤링
- **Render** - 배포 플랫폼

## 📁 프로젝트 구조

```
auction-crawler-back/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 앱
│   ├── config.py            # 설정
│   ├── database.py          # DB 연결
│   ├── models/              # SQLAlchemy 모델
│   │   ├── keyword.py
│   │   ├── detected_item.py
│   │   └── alert.py
│   ├── schemas/             # Pydantic 스키마
│   ├── crud/                # CRUD 작업
│   ├── api/                 # API 라우터
│   ├── crawler/             # 크롤링 모듈
│   ├── services/            # 비즈니스 로직
│   └── utils/
├── alembic/                 # DB 마이그레이션
├── requirements.txt
├── .env.example
└── README.md
```

## 🛠️ 로컬 개발 환경 설정

### 1. 프로젝트 클론 및 의존성 설치

```bash
git clone <repository-url>
cd auction-crawler-back

# 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### 2. 환경 변수 설정

```bash
cp .env.example .env
```

`.env` 파일을 편집하여 Supabase 연결 정보를 입력:

```env
# Database
DATABASE_URL=postgresql://postgres:password@db.project-ref.supabase.co:5432/postgres

# Supabase
SUPABASE_URL=https://project-ref.supabase.co
SUPABASE_ANON_KEY=your_anon_key_here
SUPABASE_SERVICE_KEY=your_service_role_key_here

# Environment
ENVIRONMENT=development
```

### 3. 데이터베이스 마이그레이션

```bash
# 마이그레이션 파일 생성
alembic revision --autogenerate -m "Initial migration"

# 마이그레이션 실행
alembic upgrade head
```

### 4. 서버 실행

```bash
# 개발 서버 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 또는
python app/main.py
```

## 📖 API 사용법

### 기본 URL

- 개발: `http://localhost:8000`
- 프로덕션: `https://your-app-name.onrender.com`

### API 문서

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 주요 엔드포인트

#### 1. 키워드 관리

```bash
# 키워드 목록 조회
GET /keywords?user_id=temp-user-id

# 키워드 등록
POST /keywords
{
  "user_id": "temp-user-id",
  "keyword": "송파구"
}

# 키워드 삭제
DELETE /keywords/{keyword_id}
```

#### 2. 감지된 경매 물건

```bash
# 전체 목록 조회
GET /detected

# 키워드로 검색
GET /detected?keyword=아파트&limit=10

# 상세 조회
GET /detected/{item_id}
```

#### 3. 알림 기록

```bash
# 사용자별 알림 조회
GET /alerts?user_id=temp-user-id

# 알림 상세 조회
GET /alerts/{alert_id}
```

#### 4. 크롤링

```bash
# 수동 크롤링 실행
POST /crawler/run?pages=3

# 크롤러 상태 확인
GET /crawler/status
```

## 🗄️ 데이터베이스 스키마

### Supabase에서 실행할 SQL

```sql
-- keywords 테이블
CREATE TABLE keywords (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,
    keyword VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- detected_items 테이블
CREATE TABLE detected_items (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    appraisal_value BIGINT,
    bid_date DATE,
    url TEXT NOT NULL,
    keywords JSONB,
    source_site VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- alerts 테이블
CREATE TABLE alerts (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,
    item_id INT NOT NULL,
    message TEXT,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES detected_items(id)
);

-- 인덱스 생성
CREATE INDEX idx_keywords_user_id ON keywords(user_id);
CREATE INDEX idx_detected_items_created_at ON detected_items(created_at);
CREATE INDEX idx_detected_items_keywords ON detected_items USING GIN(keywords);
CREATE INDEX idx_alerts_user_id ON alerts(user_id);
```

## 🚀 배포 (Render)

### 1. GitHub 연결

1. 코드를 GitHub에 푸시
2. Render 대시보드에서 새 Web Service 생성
3. GitHub 리포지토리 연결

### 2. 배포 설정

- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 3. 환경 변수 설정

Render 대시보드에서 다음 환경 변수 추가:

```
DATABASE_URL=postgresql://postgres:<password>@db.<project-ref>.supabase.co:5432/postgres
SUPABASE_URL=https://<project-ref>.supabase.co
SUPABASE_ANON_KEY=<anon-key>
SUPABASE_SERVICE_KEY=<service-role-key>
ENVIRONMENT=production
```

## 🕷️ 크롤링 기능

### 지원하는 사이트

- **대법원 경매정보** (`http://www.courtauction.go.kr`)

### 크롤링 방법

1. **수동 실행**: API 엔드포인트 호출
2. **자동 실행**: 스케줄러 (향후 구현)

### 키워드 매칭

- 경매 물건 제목에서 키워드 검색
- 지역명, 물건 유형 자동 추출
- 사용자 등록 키워드와 매칭 시 알림 생성

## 🔧 개발 팁

### 테스트 데이터 생성

```bash
# 테스트 키워드 등록
curl -X POST "http://localhost:8000/keywords" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test-user", "keyword": "송파구"}'

# 크롤링 실행
curl -X POST "http://localhost:8000/crawler/run?pages=1"
```

### 로그 확인

```bash
# 개발 서버 로그
tail -f logs/app.log

# 크롤링 로그는 콘솔에 출력됨
```

## 🐛 문제 해결

### 데이터베이스 연결 오류

```bash
# 연결 정보 확인
python -c "from app.database import test_database_connection; import asyncio; asyncio.run(test_database_connection())"
```

### 크롤링 실패

- User-Agent 변경
- 요청 간격 조절
- 대상 사이트 구조 변경 확인

## 📝 TODO

- [ ] 이메일 알림 기능
- [ ] 웹훅 알림 기능
- [ ] 스케줄러 구현 (Celery)
- [ ] 다중 크롤링 사이트 지원
- [ ] API 키 인증
- [ ] 모니터링 시스템

## 📄 라이선스

MIT License

## 📞 지원

문의사항이나 버그 리포트는 GitHub Issues를 이용해 주세요. 