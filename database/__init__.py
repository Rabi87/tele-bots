from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from config import Config

# تهيئة اتصال PostgreSQL
engine = create_engine(
    Config.DATABASE_URL,
    pool_size=20,
    max_overflow=0,
    pool_pre_ping=True
)

# جلسة قاعدة البيانات
SessionFactory = sessionmaker(bind=engine)
db_session = scoped_session(SessionFactory)

# القاعدة التصريحية للجداول
Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)