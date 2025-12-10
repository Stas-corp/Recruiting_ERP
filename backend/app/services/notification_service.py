from abc import ABC, abstractmethod
from typing import Optional

class NotificationProvider(ABC):
    @abstractmethod
    def send_notification(self, recipient: str, message: str, title: Optional[str] = None,
                         metadata: Optional[dict] = None) -> bool:
        pass

class ConsoleNotificationProvider(NotificationProvider):
    def send_notification(self, recipient: str, message: str, title: Optional[str] = None,
                         metadata: Optional[dict] = None) -> bool:
        print(f"[NOTIFICATION to {recipient}]")
        if title:
            print(f"Title: {title}")
        print(f"Message: {message}")
        if metadata:
            print(f"Metadata: {metadata}")
        return True

class NotificationService:
    def __init__(self, provider: NotificationProvider):
        self.provider = provider
    
    def notify_candidate_confirmed(self, candidate_name: str, position: str, recipient_id: str) -> bool:
        title = "Кандидат подтвержден"
        message = f"Кандидат {candidate_name} подтвержден на должность {position}"
        return self.provider.send_notification(recipient=recipient_id, title=title, message=message,
                                              metadata={"action": "candidate_confirmed"})
