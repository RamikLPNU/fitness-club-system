from abc import ABC, abstractmethod
from decimal import Decimal
from datetime import datetime
from enum import Enum


class PaymentStrategy(ABC):
    """Абстрактна стратегія оплати"""
    
    @abstractmethod
    def process_payment(self, amount: Decimal) -> dict:
        """Обробити платіж"""
        pass
    
    @abstractmethod
    def get_commission(self, amount: Decimal) -> Decimal:
        """Отримати комісію"""
        pass
    
    @abstractmethod
    def validate(self, payment_data: dict) -> bool:
        """Валідувати дані платежу"""
        pass


class CardPaymentStrategy(PaymentStrategy):
    """Стратегія оплати картою"""
    
    COMMISSION_RATE = Decimal("0.02")  # 2% комісія
    
    def process_payment(self, amount: Decimal) -> dict:
        total = amount + self.get_commission(amount)
        return {
            "method": "CARD",
            "amount": amount,
            "commission": self.get_commission(amount),
            "total": total,
            "timestamp": datetime.now(),
            "status": "COMPLETED"
        }
    
    def get_commission(self, amount: Decimal) -> Decimal:
        return (amount * self.COMMISSION_RATE).quantize(Decimal("0.01"))
    
    def validate(self, payment_data: dict) -> bool:
        required = ["card_number", "expiry", "cvv"]
        return all(field in payment_data for field in required)


class CashPaymentStrategy(PaymentStrategy):
    """Стратегія оплати готівкою"""
    
    COMMISSION_RATE = Decimal("0.00")  # Без комісії
    
    def process_payment(self, amount: Decimal) -> dict:
        return {
            "method": "CASH",
            "amount": amount,
            "commission": Decimal("0.00"),
            "total": amount,
            "timestamp": datetime.now(),
            "status": "PENDING_VERIFICATION"
        }
    
    def get_commission(self, amount: Decimal) -> Decimal:
        return Decimal("0.00")
    
    def validate(self, payment_data: dict) -> bool:
        # Готівка не потребує додаткових даних
        return "amount" in payment_data


class MobilePaymentStrategy(PaymentStrategy):
    """Стратегія оплати мобільним платежем"""
    
    COMMISSION_RATE = Decimal("0.015")  # 1.5% комісія
    
    def process_payment(self, amount: Decimal) -> dict:
        total = amount + self.get_commission(amount)
        return {
            "method": "MOBILE",
            "amount": amount,
            "commission": self.get_commission(amount),
            "total": total,
            "timestamp": datetime.now(),
            "status": "PROCESSING"
        }
    
    def get_commission(self, amount: Decimal) -> Decimal:
        return (amount * self.COMMISSION_RATE).quantize(Decimal("0.01"))
    
    def validate(self, payment_data: dict) -> bool:
        required = ["phone_number", "provider"]
        return all(field in payment_data for field in required)


class BankTransferStrategy(PaymentStrategy):
    """Стратегія банківського переводу"""
    
    COMMISSION_RATE = Decimal("0.01")  # 1% комісія
    
    def process_payment(self, amount: Decimal) -> dict:
        total = amount + self.get_commission(amount)
        return {
            "method": "BANK_TRANSFER",
            "amount": amount,
            "commission": self.get_commission(amount),
            "total": total,
            "timestamp": datetime.now(),
            "status": "PENDING_CONFIRMATION"
        }
    
    def get_commission(self, amount: Decimal) -> Decimal:
        return (amount * self.COMMISSION_RATE).quantize(Decimal("0.01"))
    
    def validate(self, payment_data: dict) -> bool:
        required = ["iban", "account_holder"]
        return all(field in payment_data for field in required)


class PaymentMethodEnum(str, Enum):
    """Типи методів оплати"""
    CARD = "CARD"
    CASH = "CASH"
    MOBILE = "MOBILE"
    BANK_TRANSFER = "BANK_TRANSFER"


class PaymentFactory:
    """Factory для створення стратегій оплати"""
    
    _strategies = {
        PaymentMethodEnum.CARD: CardPaymentStrategy,
        PaymentMethodEnum.CASH: CashPaymentStrategy,
        PaymentMethodEnum.MOBILE: MobilePaymentStrategy,
        PaymentMethodEnum.BANK_TRANSFER: BankTransferStrategy,
    }
    
    @staticmethod
    def create_payment_strategy(method: PaymentMethodEnum) -> PaymentStrategy:
        """Отримати стратегію оплати за типом"""
        strategy_class = PaymentFactory._strategies.get(method)
        if not strategy_class:
            raise ValueError(f"Невідомий метод оплати: {method}")
        return strategy_class()
    
    @staticmethod
    def get_available_methods():
        """Отримати список доступних методів"""
        return list(PaymentFactory._strategies.keys())


class PaymentProcessor:
    """Процесор платежів з використанням стратегій"""
    
    def __init__(self):
        self.strategy = None
    
    def set_strategy(self, strategy: PaymentStrategy):
        """Встановити стратегію оплати"""
        self.strategy = strategy
        return self
    
    def process(self, amount: Decimal, payment_data: dict) -> dict:
        """Обробити платіж"""
        if not self.strategy:
            raise RuntimeError("Стратегія оплати не встановлена")
        
        if not self.strategy.validate(payment_data):
            raise ValueError("Невалідні дані платежу")
        
        result = self.strategy.process_payment(amount)
        result["payment_data"] = payment_data
        return result


# Приклади використання:
def example_payment_factory():
    """Приклади використання payment factory"""
    
    processor = PaymentProcessor()
    
    # Оплата картою
    card_strategy = PaymentFactory.create_payment_strategy(PaymentMethodEnum.CARD)
    card_payment = (processor
                    .set_strategy(card_strategy)
                    .process(Decimal("100.00"), {
                        "card_number": "1234567890123456",
                        "expiry": "12/25",
                        "cvv": "123"
                    }))
    
    # Оплата готівкою
    cash_strategy = PaymentFactory.create_payment_strategy(PaymentMethodEnum.CASH)
    cash_payment = (processor
                    .set_strategy(cash_strategy)
                    .process(Decimal("100.00"), {"amount": 100}))
    
    # Мобільний платіж
    mobile_strategy = PaymentFactory.create_payment_strategy(PaymentMethodEnum.MOBILE)
    mobile_payment = (processor
                      .set_strategy(mobile_strategy)
                      .process(Decimal("100.00"), {
                          "phone_number": "+380501234567",
                          "provider": "Kyivstar"
                      }))
    
    return card_payment, cash_payment, mobile_payment
