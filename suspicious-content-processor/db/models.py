from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import os

Base = declarative_base()


class EmailModel(Base):
    __tablename__ = 'emails'
    
    email_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    received_at = Column(DateTime, default=datetime.now)

    hostage_contents = relationship('HostagesModel', back_populates='email_details')
    explosive_contents = relationship('ExplosiveModel', back_populates='email_details')


class HostagesModel(Base):
    __tablename__ = 'suspicious_hostage_content'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email_id = Column(Integer, ForeignKey('emails.email_id'))
    suspicious_sentence = Column(String, nullable=False)
    detected_at = Column(DateTime, default=datetime.now)
    
    email_details = relationship('EmailModel', back_populates='hostage_contents')

class ExplosiveModel(Base):
    __tablename__ = 'suspicious_explosive_content'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email_id = Column(Integer, ForeignKey('emails.email_id'))
    suspicious_sentence = Column(String, nullable=False)
    detected_at = Column(DateTime, default=datetime.now)
    
    email_details = relationship('EmailModel', back_populates='explosive_contents')
