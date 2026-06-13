# 프로젝트 실행 방법

이 문서는 백엔드(FastAPI)와 프론트엔드(SvelteKit)를 함께 실행하는 방법을 정리합니다.

## 사전 준비
- Node.js + npm
- Python

## 백엔드 실행
PowerShell 기준입니다.

```powershell
cd D:\projects\digital_mental_medicalAI\back
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

- 기본 DB: `sqlite:///./app.db` (작업 디렉터리 기준)
- 환경변수(선택): `DATABASE_URL`, `PROJECT_NAME`
- API 베이스: `http://127.0.0.1:8000/api/v1`

## 프론트엔드 실행
다른 터미널에서 실행합니다.

```powershell
cd D:\projects\digital_mental_medicalAI\front
npm install
npm run dev
```

- 접속: `http://127.0.0.1:5173`
- 개발 서버 프록시: `/api` → `http://localhost:8000` (`front/vite.config.js`)

## 선택: 프로덕션 빌드/미리보기
```powershell
cd D:\projects\digital_mental_medicalAI\front
npm run build
npm run preview
```
