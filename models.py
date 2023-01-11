from sqlalchemy import Column, Integer, String, ForeignKey, Date, Table, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, autoincrement=True)
    fullname = Column(String(100), nullable=False, unique=True)
    born_date = Column(String(20), nullable=True)
    born_location = Column(String(50), nullable=True)
    bio = Column(String(5000), nullable=True)
    quote = relationship('Quote', back_populates='author')


class Quote(Base):
    __tablename__ = "quotes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(100), nullable=False, unique=True)
    author_id = Column(Integer, ForeignKey("authors.id", ondelete='SET NULL'))
    author = relationship("Author", back_populates='quote')
    tags = relationship("Tag", secondary='quote_m2m_tag', back_populates="quotes")


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tagname = Column(String(100), nullable=False, unique=True)
    quotes = relationship("Quote", secondary='quote_m2m_tag', back_populates="tags")


quote_m2m_tag = Table(
    "quote_m2m_tag",
    Base.metadata,
    Column("quote_id", ForeignKey("quotes.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True)
)


engine = create_engine("sqlite:///quotes.db")
Base.metadata.create_all(engine)
Base.metadata.bind = engine
Session = sessionmaker(bind=engine)
