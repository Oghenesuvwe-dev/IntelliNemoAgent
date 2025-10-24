"""Mailgun service module for email functionality."""

import os
import requests
from typing import Dict, Any, Optional

class MailgunService:
    def __init__(self):
        self.api_key = os.getenv('MAILGUN_API_KEY')
        self.domain = os.getenv('MAILGUN_DOMAIN')
        self.base_url = f"https://api.mailgun.net/v3/{self.domain}"
    
    def send_email(self, to: str, subject: str, text: str, html: Optional[str] = None) -> Dict[str, Any]:
        """Send email via Mailgun API."""
        if not self.api_key or not self.domain:
            return {"status": "error", "message": "Mailgun not configured"}
        
        data = {
            "from": f"noreply@{self.domain}",
            "to": to,
            "subject": subject,
            "text": text
        }
        
        if html:
            data["html"] = html
        
        try:
            response = requests.post(
                f"{self.base_url}/messages",
                auth=("api", self.api_key),
                data=data,
                timeout=10
            )
            return {"status": "success", "response": response.json()}
        except Exception as e:
            return {"status": "error", "message": str(e)}

# Create instance for import
mailgun_service = MailgunService()