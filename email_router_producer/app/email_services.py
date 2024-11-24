from db.models import EmailModel
from sqlalchemy.orm import Session

class EmailService:
    @staticmethod
    def get_suspicious_content_by_email(session: Session, email_address: str):
        email = session.query(EmailModel).filter(EmailModel.email == email_address).first()
        if not email:
            raise ValueError(f"No email found for address {email_address}")
        
        suspicious_content = {
            "hostages": [hostage.suspicious_sentence for hostage in email.hostages],
            "explosives": [explosive.suspicious_sentence for explosive in email.explosives]
        }

        return suspicious_content
