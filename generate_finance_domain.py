# Path: generate_finance_domain.py
import os

def create_file(path, content):
    """파일 생성 및 경로 주석 추가 (UTF-8)"""
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# Path: {path}\n")
        f.write(content.strip())
    print(f"   📄 생성 완료: {path}")

def init_project_structure():
    """AI 금융 비서 프로젝트 필수 인프라 구축"""
    print("🏗️ AI 금융 프로젝트 인프라 구축 시작 (PostgreSQL/Supabase)...")

    # 1. 요구사항: PostgreSQL/Supabase 환경 설정
    db_content = """
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Supabase 또는 로컬 PostgreSQL URL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/finance_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""
    create_file("app/core/database.py", db_content)

    # 2. app/main.py (버전 관리 및 라우터 마커)
    main_content = """
from fastapi import FastAPI
from app.core.database import engine, Base

app = FastAPI(
    title="AI Finance Assistant API",
    description="WP 1~5 통합 금융 비서 백엔드",
    version="1.0.0"
)

# DB 테이블 생성 (최초 실행 시)
Base.metadata.create_all(bind=engine)

@app.get("/")
def health_check():
    return {"status": "running", "project": "AI Finance Assistant"}

# --- [자동 라우터 연동 영역] ---
# --- ROUTERS START ---
# --- ROUTERS END ---
"""
    if not os.path.exists("app/main.py"):
        create_file("app/main.py", main_content)

    # 3. 환경 파일 및 의존성
    create_file(".env.example", "DATABASE_URL=postgresql://user:pass@host:5432/dbname\nOPENAI_API_KEY=sk-...\nGEMINI_API_KEY=...")
    create_file("requirements.txt", "fastapi\nuvicorn\nsqlalchemy\npsycopg2-binary\npgvector\npydantic[email]\npython-dotenv")

def update_main_router(domain_name):
    """라우터 자동 등록 로직"""
    main_path = "app/main.py"
    with open(main_path, "r", encoding="utf-8") as f:
        content = f.read()

    import_line = f"from app.domains.{domain_name}.router import router as {domain_name}_router"
    include_line = f"app.include_router({domain_name}_router)"

    if import_line not in content:
        content = import_line + "\n" + content
    if include_line not in content:
        marker = "# --- ROUTERS END ---"
        content = content.replace(marker, f"{include_line}\n{marker}")

    with open(main_path, "w", encoding="utf-8") as f:
        f.write(content)

def generate_domain(domain_name):
    """현업 수준의 Layered Architecture 도메인 생성"""
    base_dir = f"app/domains/{domain_name}"
    CapName = domain_name.replace("_", " ").title().replace(" ", "")

    # 1. Models (UUID 및 pgvector 고려)
    models_content = f"""
from sqlalchemy import Column, String, DECIMAL, DateTime, ForeignKey, Boolean, text
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from datetime import datetime
from app.core.database import Base

class {CapName}(Base):
    __tablename__ = "{domain_name}s"
    # 금융 데이터 보안 및 확장을 위해 UUID 사용
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    
    # 💡 도메인별 컬럼을 아래에 추가하세요
    # 예: user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
"""

    # 2. Schemas (Pydantic V2)
    schemas_content = f"""
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class {CapName}Base(BaseModel):
    pass

class {CapName}Create({CapName}Base):
    pass

class {CapName}Read({CapName}Base):
    id: UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
"""

    # 3. Repository (데이터 접근 최적화)
    repo_content = f"""
from sqlalchemy.orm import Session
from uuid import UUID
from .models import {CapName}

class {CapName}Repository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, obj_id: UUID):
        return self.db.query({CapName}).filter({CapName}.id == obj_id).first()
"""

    # 4. Services (비즈니스 로직 - AI 에이전트 결합 지점)
    services_content = f"""
from sqlalchemy.orm import Session
from .repository import {CapName}Repository

class {CapName}Service:
    def __init__(self, db: Session):
        self.repo = {CapName}Repository(db)
        
    # WP 관련 핵심 비즈니스 로직 구현 위치
"""

    # 5. Router (API 엔드포인트)
    router_content = f"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from .services import {CapName}Service
from .schemas import {CapName}Read

router = APIRouter(prefix='/{domain_name}', tags=['{CapName}'])

@router.get("/{{id}}", response_model={CapName}Read)
def get_{domain_name}(id, db: Session = Depends(get_db)):
    service = {CapName}Service(db)
    result = service.repo.get_by_id(id)
    if not result:
        raise HTTPException(status_code=404, detail="Not Found")
    return result
"""

    files = {
        f"{base_dir}/__init__.py": "",
        f"{base_dir}/models.py": models_content,
        f"{base_dir}/schemas.py": schemas_content,
        f"{base_dir}/repository.py": repo_content,
        f"{base_dir}/services.py": services_content,
        f"{base_dir}/router.py": router_content,
    }

    for path, content in files.items():
        create_file(path, content)
    update_main_router(domain_name)

if __name__ == "__main__":
    init_project_structure()
    
    # 기획된 핵심 도메인 리스트
    print("\n💡 AI 금융 비서 권장 도메인: users, assets, transactions, fixed_costs, automations, quests")
    user_input = input("👉 생성할 도메인 입력: ").strip()

    if user_input:
        domains = [d.strip() for d in user_input.split(",") if d.strip()]
        for domain in domains:
            print(f"\n🛠️ '{domain}' 도메인 인프라 구축 중...")
            generate_domain(domain)
        print("\n✨ 모든 도메인이 Layered Architecture 구조로 생성되었습니다.")