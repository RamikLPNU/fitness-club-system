from decimal import Decimal
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# Імпортуємо паттерни
from app.services.membership_builder import MembershipBuilder
from app.services.payment_strategy import (
    PaymentFactory, PaymentProcessor, PaymentMethodEnum
)
from app.services.notification_service import (
    NotificationService, NotificationEventType,
    EmailNotification, SMSNotification, PushNotification
)
from app.services.membership_decorator import (
    BaseMembership, PersonalTrainerDecorator,
    NutritionConsultantDecorator, DiscountDecorator,
    UnlimitedClassesDecorator, ParkingDecorator
)

# Імпортуємо моделі і schemas
from app.models.dim_membership import DimMembership
from app.models.dim_client import DimClient
from app.database import get_db
from app.schemas.membership_schema import MembershipCreate


router = APIRouter(prefix="/api/v1", tags=["patterns-demo"])


# ============================================================================
# 1. BUILDER PATTERN ПРИКЛАД
# ============================================================================

class MembershipBuildRequest:
    """Request модель для побудови членства"""
    name: str
    price: float
    duration_days: int
    max_classes_per_week: int = None
    includes_trainer: bool = False
    includes_nutrition: bool = False


@router.post("/memberships/build")
def create_membership_with_builder(request: MembershipBuildRequest, db: Session = Depends(get_db)):
    """
    Приклад использування Builder для створення членства
    
    Замість передачі всіх параметрів одночасно, будуємо поетапно.
    """
    # Используємо Builder для поетапного конструювання
    builder = MembershipBuilder()
    builder.set_name(request.name)
    builder.set_price(Decimal(str(request.price)))
    builder.set_duration(request.duration_days)
    
    if request.max_classes_per_week:
        builder.set_classes_limit(request.max_classes_per_week)
    
    if request.includes_trainer:
        builder.with_trainer()
    
    if request.includes_nutrition:
        builder.with_nutrition()
    
    # Отримуємо готовий об'єкт
    membership_data = builder.build()
    
    # Зберігаємо в БД
    db_membership = DimMembership(
        name=membership_data["name"],
        duration_days=membership_data["duration_days"],
        price=membership_data["price"]
    )
    db.add(db_membership)
    db.commit()
    db.refresh(db_membership)
    
    return {
        "status": "success",
        "membership": membership_data,
        "id": db_membership.membership_id
    }


@router.get("/memberships/templates")
def get_membership_templates():
    """Отримати готові шаблони членств створені через Builder"""
    from app.services.membership_builder import example_builders
    
    basic, premium, vip = example_builders()
    
    return {
        "templates": [
            {"type": "Basic", "data": basic},
            {"type": "Premium", "data": premium},
            {"type": "VIP", "data": vip}
        ]
    }


# ============================================================================
# 2. STRATEGY + FACTORY PATTERN ПРИКЛАД
# ============================================================================

class PaymentRequest:
    """Request модель для обробки платежу"""
    method: str  # CARD, CASH, MOBILE, BANK_TRANSFER
    amount: float
    payment_data: dict  # Залежить від методу


@router.post("/payments/process")
def process_payment_with_strategy(request: PaymentRequest):
    """
    Приклад використання Strategy + Factory для обробки платежів
    
    Factory динамічно створює потрібну стратегію на основі типу платежу.
    """
    try:
        # Фабрика створює відповідну стратегію
        method = PaymentMethodEnum[request.method]
        strategy = PaymentFactory.create_payment_strategy(method)
        
        # Процесор застосовує стратегію
        processor = PaymentProcessor().set_strategy(strategy)
        result = processor.process(
            Decimal(str(request.amount)),
            request.payment_data
        )
        
        return {
            "status": "success",
            "payment_result": result
        }
    
    except ValueError as e:
        return {
            "status": "error",
            "message": str(e),
            "available_methods": PaymentFactory.get_available_methods()
        }


@router.get("/payments/methods")
def get_available_payment_methods():
    """Отримати доступні методи оплати"""
    methods = PaymentFactory.get_available_methods()
    
    methods_info = {
        "CARD": {"commission": "2%", "description": "Оплата кредитною карткою"},
        "CASH": {"commission": "0%", "description": "Готівкова оплата"},
        "MOBILE": {"commission": "1.5%", "description": "Мобільна оплата"},
        "BANK_TRANSFER": {"commission": "1%", "description": "Банківський переклад"}
    }
    
    return {
        "available_methods": [
            {
                "method": method,
                **methods_info.get(method, {})
            }
            for method in methods
        ]
    }


# ============================================================================
# 3. OBSERVER PATTERN ПРИКЛАД
# ============================================================================

@router.post("/memberships/{membership_id}/activate")
def activate_membership_with_notifications(membership_id: int, db: Session = Depends(get_db)):
    """
    Приклад використання Observer для розсилання сповіщень
    
    Коли активується членство, сервіс Observer повідомляє всі підписані канали.
    """
    # Отримуємо членство і клієнта з БД
    membership = db.query(DimMembership).filter(
        DimMembership.membership_id == membership_id
    ).first()
    
    if not membership:
        return {"status": "error", "message": "Членство не знайдено"}
    
    # Ініціалізуємо Observer сервіс
    notif_service = NotificationService()
    
    # Підписуємо канали на сповіщення
    notif_service.attach_channel(EmailNotification())
    notif_service.attach_channel(SMSNotification())
    notif_service.attach_channel(PushNotification())
    
    # Розсилаємо сповіщення всім каналам
    notif_service.notify_all(
        NotificationEventType.MEMBERSHIP_ACTIVATED,
        recipient="member@example.com",
        message=f"Вітаємо! Ваше членство '{membership.name}' було активовано!",
        context={
            "subject": "Членство активовано",
            "title": "Добро пожалувати!",
            "membership_type": membership.name,
            "valid_until": "2025-03-02"
        }
    )
    
    return {
        "status": "success",
        "message": "Членство активовано, сповіщення розіслано"
    }


@router.post("/memberships/{membership_id}/expiring-reminder")
def send_membership_expiring_reminder(membership_id: int, db: Session = Depends(get_db)):
    """Надіслати нагадування про закінчення членства"""
    
    notif_service = NotificationService()
    
    # Підписуємо різні канали на різні события
    notif_service.subscribe_to_event(
        NotificationEventType.MEMBERSHIP_EXPIRING,
        EmailNotification()
    )
    notif_service.subscribe_to_event(
        NotificationEventType.MEMBERSHIP_EXPIRING,
        SMSNotification()
    )
    
    # Розсилаємо тільки підписаним каналам
    notif_service.notify_subscribers(
        NotificationEventType.MEMBERSHIP_EXPIRING,
        recipient="+380501234567",
        message="Ваше членство закінчується за 7 днів. Поновіть його зараз!",
        context={
            "days_left": 7,
            "renewal_link": "/api/v1/memberships/renew"
        }
    )
    
    return {"status": "success", "message": "Нагадування розіслано"}


# ============================================================================
# 4. DECORATOR PATTERN ПРИКЛАД
# ============================================================================

@router.get("/memberships/compositions/{composition_type}")
def get_membership_composition(composition_type: str):
    """
    Приклад використання Decorator для композиції послуг
    
    Динамічно комбінуємо базове членство з різними послугами.
    """
    
    # Базове членство
    base = BaseMembership("Базове", Decimal("50.00"), 10)
    
    # Застосовуємо декоратори на основі типу
    if composition_type == "basic":
        result = base
    
    elif composition_type == "with_trainer":
        result = PersonalTrainerDecorator(base, 2)
    
    elif composition_type == "premium":
        result = (DiscountDecorator(
            NutritionConsultantDecorator(
                PersonalTrainerDecorator(base, 3),
                2
            ),
            10  # 10% знижка
        ))
    
    elif composition_type == "vip":
        result = (ParkingDecorator(
            DiscountDecorator(
                NutritionConsultantDecorator(
                    PersonalTrainerDecorator(
                        UnlimitedClassesDecorator(base),
                        8
                    ),
                    4
                ),
                25  # 25% знижка для VIP
            )
        ))
    
    else:
        return {"error": f"Невідомий тип: {composition_type}"}
    
    # Повертаємо інформацію про членство
    return {
        "composition_type": composition_type,
        "name": result.get_name(),
        "price": str(result.get_price()),
        "classes_limit": result.get_classes_limit(),
        "loyalty_multiplier": result.get_loyalty_multiplier(),
        "benefits": result.get_benefits()
    }


@router.post("/memberships/custom-composition")
def create_custom_membership_composition(services: dict):
    """
    Дозволяє клієнту створити власну комбінацію послуг
    
    services: {
        "base": "базове" або "преміум",
        "add_trainer": true/false,
        "add_nutrition": true/false,
        "add_parking": true/false,
        "unlimited_classes": true/false,
        "discount": 0-50
    }
    """
    
    # Вибираємо базове членство
    if services.get("base") == "premium":
        membership = BaseMembership("Преміум Базис", Decimal("150.00"), 15)
    else:
        membership = BaseMembership("Базис", Decimal("50.00"), 10)
    
    # Послідовно додаємо декоратори
    if services.get("unlimited_classes"):
        membership = UnlimitedClassesDecorator(membership)
    
    if services.get("add_trainer"):
        membership = PersonalTrainerDecorator(membership, 4)
    
    if services.get("add_nutrition"):
        membership = NutritionConsultantDecorator(membership, 2)
    
    if services.get("add_parking"):
        membership = ParkingDecorator(membership)
    
    if services.get("discount", 0) > 0:
        membership = DiscountDecorator(membership, services["discount"])
    
    return {
        "composition": {
            "name": membership.get_name(),
            "price": str(membership.get_price()),
            "classes_limit": membership.get_classes_limit(),
            "loyalty_multiplier": membership.get_loyalty_multiplier(),
            "benefits": membership.get_benefits()
        }
    }


# ============================================================================
# КОМБІНОВАНИЙ ПРИКЛАД: Всі паттерни разом
# ============================================================================

@router.post("/complete-workflow")
def complete_workflow_example():
    """
    Демонструє використання всіх паттернів разом:
    1. Builder - створює членство
    2. Decorator - додає послуги
    3. Strategy - обробляє платіж
    4. Observer - розсилає сповіщення
    """
    
    # 1. BUILDER: Побудувати членство
    member_builder = MembershipBuilder()
    member_builder.set_name("Преміум Пакет")
    member_builder.set_price(Decimal("150.00"))
    member_builder.set_duration(30)
    member_builder.with_trainer()
    membership_data = member_builder.build()
    
    # 2. DECORATOR: Додати послуги
    base = BaseMembership(
        membership_data["name"],
        membership_data["price"],
        12
    )
    decorated_membership = (DiscountDecorator(
        PersonalTrainerDecorator(base, 3),
        15
    ))
    
    # 3. STRATEGY: Обробити платіж
    payment_strategy = PaymentFactory.create_payment_strategy(
        PaymentMethodEnum.CARD
    )
    processor = PaymentProcessor().set_strategy(payment_strategy)
    payment_result = processor.process(
        decorated_membership.get_price(),
        {
            "card_number": "1234567890123456",
            "expiry": "12/25",
            "cvv": "123"
        }
    )
    
    # 4. OBSERVER: Розіслати сповіщення
    notif_service = NotificationService()
    notif_service.attach_channel(EmailNotification())
    notif_service.notify_all(
        NotificationEventType.PAYMENT_RECEIVED,
        "user@example.com",
        f"Платіж отримано! Ваше членство активовано.",
        {"amount": str(decorated_membership.get_price())}
    )
    
    return {
        "workflow_status": "completed",
        "membership": {
            "name": decorated_membership.get_name(),
            "price": str(decorated_membership.get_price()),
            "benefits": decorated_membership.get_benefits()
        },
        "payment": {
            "method": payment_result["method"],
            "total": str(payment_result["total"]),
            "status": payment_result["status"]
        },
        "notifications_sent": ["EMAIL"]
    }


if __name__ == "__main__":
    # Для тестування локально
    print("✅ Design Patterns примери завантажені")
    print("Доступні endpoints:")
    print("  POST /api/v1/memberships/build")
    print("  GET  /api/v1/memberships/templates")
    print("  POST /api/v1/payments/process")
    print("  GET  /api/v1/payments/methods")
    print("  POST /api/v1/memberships/{id}/activate")
    print("  GET  /api/v1/memberships/compositions/{type}")
    print("  POST /api/v1/complete-workflow")
