import asyncio
import time
from aiokafka import AIOKafkaConsumer
import json
import os
import re
from db.conn import AsyncSessionLocal
from db.models import  EmailModel, HostagesModel, ExplosiveModel
from sqlalchemy.future import select


KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
DATABASE_URL = "postgresql+asyncpg://postgres:1234@postgres/email_monitor"
suspicious_keywords = {'hostage': 'hostage', 'explosive': 'explosive'}


async def process_message(session, message, keyword):
    try:
        email_data = message.value  
        
        print(f"Received message: {email_data}")
        sentences = email_data.get('sentences', [])

        model_mapping = {
            'hostage': HostagesModel,
            'explosive': ExplosiveModel
        }
        if keyword not in model_mapping:
            raise ValueError(f"Unsupported keyword: {keyword}")

 
        email_address = email_data.get('email')
        stmt = select(EmailModel).filter(EmailModel.email == email_address)
        result = await session.execute(stmt)
        email_obj = result.scalars().first()
        
        if not email_obj:
            print(f"Email not found for {email_address}")
            return

        # for sentence in sentences:
        #     if re.search(rf'\b{re.escape(keyword)}\b', sentence, re.IGNORECASE):
        content = model_mapping[keyword](email_id=email_obj.id, suspicious_sentence=sentences)
        session.add(content)

        await session.commit()
        print(f"Processed and saved {keyword} content.")
    except Exception as e:
        await session.rollback()
        print(f"Error processing message: {e}")

async def consume_topic_for_keyword(keyword):
    print(f"Consumer for {keyword} started...")
    consumer = AIOKafkaConsumer(
        "suspicious_emails", 
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=f"suspicious_emails_group_{keyword}",  
        key_deserializer=lambda k: k.decode('utf-8'),
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )
    await consumer.start()

    try:
        async with AsyncSessionLocal() as session:
            async for message in consumer:
                if message.key == keyword:
                    print(f"Message with keyword {keyword} received.")  
                    await process_message(session, message, keyword)
    finally:
        await consumer.stop()

async def main():
    tasks = []
    for keyword in suspicious_keywords.keys(): 
        tasks.append(asyncio.create_task(consume_topic_for_keyword(keyword)))  

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    time.sleep(60)  
    asyncio.run(main())
