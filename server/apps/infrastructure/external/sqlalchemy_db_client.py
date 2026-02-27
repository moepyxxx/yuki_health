from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager


class SqlAlchemyDBClient:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url, echo=False)
        self._SessionLocal = sessionmaker(
            bind=self.engine, autocommit=False, autoflush=False
        )
        self.session: Session = self._SessionLocal()

    @contextmanager
    def get_transaction_session(self):
        """リポジトリが使うセッションを提供するコンテキストマネージャ"""
        session: Session = self._SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
