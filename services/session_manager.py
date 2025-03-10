from contextlib import contextmanager
from database import db_session

@contextmanager
def session_scope():
    """إدارة جلسات قاعدة البيانات بشكل آمن"""
    try:
        yield db_session
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise e
    finally:
        db_session.remove()

# مثال للاستخدام:
with session_scope() as session:
    user = session.query(User).filter_by(id=user_id).first()
    user.balance += 100