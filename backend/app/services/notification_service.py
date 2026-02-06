from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
from typing import List, Dict, Any


class NotificationChannel(ABC):
    
    @abstractmethod
    def send(self, recipient: str, message: str, context: Dict[str, Any]) -> bool:
        
        pass
    
    @abstractmethod
    def get_channel_name(self) -> str:
        
        pass


class EmailNotification(NotificationChannel):
    
    
    def send(self, recipient: str, message: str, context: Dict[str, Any]) -> bool:
        
        print(f"📧 EMAIL: {recipient}")
        print(f"   Тема: {context.get('subject', 'Оновлення статусу')}")
        print(f"   Повідомлення: {message}")
        print(f"   Час: {datetime.now()}")
        return True
    
    def get_channel_name(self) -> str:
        return "EMAIL"


class SMSNotification(NotificationChannel):
    
    def send(self, recipient: str, message: str, context: Dict[str, Any]) -> bool:
        print(f"📱 SMS: {recipient}")
        print(f"   Повідомлення: {message[:160]}")  # SMS обмежено 160 символів
        print(f"   Час: {datetime.now()}")
        # Здійснити інтеграцію з SMS сервісом
        return True
    
    def get_channel_name(self) -> str:
        return 


class PushNotification(NotificationChannel):
    
    def send(self, recipient: str, message: str, context: Dict[str, Any]) -> bool:
       
        print(f"🔔 PUSH: {recipient}")
        print(f"   Заголовок: {context.get('title', 'Оновлення')}")
        print(f"   Повідомлення: {message}")
        print(f"   Час: {datetime.now()}")
        # Здійснити інтеграцію з push сервісом
        return True
    
    def get_channel_name(self) -> str:
        return 


class TelegramNotification(NotificationChannel):
   
    
    def send(self, recipient: str, message: str, context: Dict[str, Any]) -> bool:
        
        print(f"💬 TELEGRAM: {recipient}")
        print(f"   Повідомлення: {message}")
        print(f"   Час: {datetime.now()}")
        # Здійснити інтеграцію з Telegram Bot API
        return True
    
    def get_channel_name(self) -> str:
        return "TELEGRAM"


class NotificationEventType(str, Enum):
    MEMBERSHIP_ACTIVATED = "MEMBERSHIP_ACTIVATED"
    MEMBERSHIP_EXPIRING = "MEMBERSHIP_EXPIRING"
    MEMBERSHIP_EXPIRED = "MEMBERSHIP_EXPIRED"
    CLASS_REMINDER = "CLASS_REMINDER"
    PAYMENT_RECEIVED = "PAYMENT_RECEIVED"
    TRAINER_ASSIGNED = "TRAINER_ASSIGNED"
    CLASS_CANCELLED = "CLASS_CANCELLED"
    NEW_CLASS_AVAILABLE = "NEW_CLASS_AVAILABLE"


class NotificationService:
    
    def __init__(self):
        self.channels: List[NotificationChannel] = []
        self.subscriptions: Dict[str, List[NotificationChannel]] = {}
    
    def attach_channel(self, channel: NotificationChannel):
        if channel not in self.channels:
            self.channels.append(channel)
            print(f"✅ Канал {channel.get_channel_name()} підписаний")
    
    def detach_channel(self, channel: NotificationChannel):
        if channel in self.channels:
            self.channels.remove(channel)
            print(f"❌ Канал {channel.get_channel_name()} відписаний")
    
    def subscribe_to_event(self, event_type: NotificationEventType, channel: NotificationChannel):
        if event_type not in self.subscriptions:
            self.subscriptions[event_type] = []
        
        if channel not in self.subscriptions[event_type]:
            self.subscriptions[event_type].append(channel)
    
    def notify_all(self, event: NotificationEventType, recipient: str, message: str, context: Dict[str, Any]):
        print(f"\n📢 Розсилка сповіщення: {event.value}")
        for channel in self.channels:
            try:
                channel.send(recipient, message, context)
            except Exception as e:
                print(f"⚠️  Помилка при отправці через {channel.get_channel_name()}: {str(e)}")
    
    def notify_subscribers(self, event: NotificationEventType, recipient: str, message: str, context: Dict[str, Any]):
        """Розіслати сповіщення підписаним каналам для даної події"""
        if event not in self.subscriptions:
            print(f"ℹ️  Немає підписань на подію: {event.value}")
            return
        
        print(f"\n📢 Розсилка сповіщення: {event.value}")
        for channel in self.subscriptions[event]:
            try:
                channel.send(recipient, message, context)
            except Exception as e:
                print(f"⚠️  Помилка при отправці через {channel.get_channel_name()}: {str(e)}")


def example_notifications():
    
    service = NotificationService()
    
    email = EmailNotification()
    sms = SMSNotification()
    push = PushNotification()
    telegram = TelegramNotification()
    
    service.attach_channel(email)
    service.attach_channel(sms)
    service.attach_channel(push)
    service.attach_channel(telegram)
    
    service.notify_all(
        NotificationEventType.MEMBERSHIP_ACTIVATED,
        recipient="user@example.com",
        message="Ваше членство було активовано!",
        context={
            "subject": "Членство активовано",
            "title": "Успіх!",
            "membership_type": "Premium",
            "valid_until": "2025-03-02"
        }
    )
    
    service.subscribe_to_event(NotificationEventType.CLASS_REMINDER, sms)
    service.subscribe_to_event(NotificationEventType.CLASS_REMINDER, push)
    
    service.notify_subscribers(
        NotificationEventType.CLASS_REMINDER,
        recipient="+380501234567",
        message="Нагадування: Ваш клас Йога розпочинається за 1 годину",
        context={
            "title": "Нагадування про клас",
            "class_name": "Йога",
            "start_time": "18:00",
            "trainer": "Марія"
        }
    )
    
    service.notify_all(
        NotificationEventType.MEMBERSHIP_EXPIRING,
        recipient="user@example.com",
        message="Ваше членство закінчується за 7 днів",
        context={
            "subject": "Членство закінчується",
            "title": "Внимание",
            "days_left": 7
        }
    )
