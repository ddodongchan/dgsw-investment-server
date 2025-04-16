from logging.config import fileConfig
import os

from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# .env 불러오기
load_dotenv()

# Alembic 설정 객체
config = context.config

# 환경변수에서 DB URL 읽어서 설정에 주입
config.set_main_option("sqlalchemy.url", os.getenv("MIGRATION_DATABASE_URL"))

# 로깅 설정
fileConfig(config.config_file_name)

# 모델 import
from auth_models.user_credentials import Base

target_metadata = Base.metadata

def run_migrations_offline():
    """오프라인 모드 (sql 스크립트 생성)"""
    context.configure(
        url=os.getenv("MIGRATION_DATABASE_URL"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """온라인 모드 (DB에 직접 실행)"""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with connection.begin():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
