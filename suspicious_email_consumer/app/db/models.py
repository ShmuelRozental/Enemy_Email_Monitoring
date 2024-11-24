from sqlalchemy import JSON, Column, String, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class EmailModel(Base):
    __tablename__ = 'emails'
    
    id = Column(Integer, primary_key=True, autoincrement=True)  
    email = Column(String, nullable=False, unique=True) 
    username = Column(String, nullable=False)
    received_at = Column(DateTime, default=datetime.now)

    hostages = relationship('HostagesModel', backref='email') 
    explosives = relationship('ExplosiveModel', backref='email')


class HostagesModel(Base):
    __tablename__ = 'suspicious_hostage_content'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email_id = Column(Integer, ForeignKey('emails.id')) 
    suspicious_sentence = Column(JSON, nullable=False)
    detected_at = Column(DateTime, default=datetime.now)



class ExplosiveModel(Base):
    __tablename__ = 'suspicious_explosive_content'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email_id = Column(Integer, ForeignKey('emails.id')) 
    suspicious_sentence = Column(JSON, nullable=False)
    detected_at = Column(DateTime, default=datetime.now)
