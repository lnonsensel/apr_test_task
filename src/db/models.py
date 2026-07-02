from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    DateTime,
    String,
)
from sqlalchemy.orm import relationship

from src.db.session import Base
from datetime import datetime


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    text = Column(String)
    created_date = Column(DateTime, default=datetime.now)

    rubrics_objs = relationship("Rubric", back_populates="post", cascade="all")

    def __repr__(self):
        return f"<Post(id={self.id}, text='{self.text}', created_date='{self.created_date})>"


class Rubric(Base):
    __tablename__ = "rubrics"
    id = Column(Integer, primary_key=True)
    vk_id = Column(String)
    post_id = Column(Integer, ForeignKey("posts.id"))

    post = relationship("Post", back_populates="rubrics_objs")
