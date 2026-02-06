from abc import ABC, abstractmethod
from decimal import Decimal
from datetime import datetime, timedelta


class MembershipComponent(ABC):
    """Базовий компонент членства"""
    
    @abstractmethod
    def get_name(self) -> str:
        """Отримати назву"""
        pass
    
    @abstractmethod
    def get_price(self) -> Decimal:
        """Отримати ціну"""
        pass
    
    @abstractmethod
    def get_classes_limit(self) -> int:
        """Отримати ліміт занять"""
        pass
    
    @abstractmethod
    def get_benefits(self) -> list:
        """Отримати переваги"""
        pass
    
    @abstractmethod
    def get_loyalty_multiplier(self) -> float:
        """Отримати множник балів лояльності"""
        pass


class BaseMembership(MembershipComponent):
    """Базове членство"""
    
    def __init__(self, name: str, price: Decimal, classes_limit: int):
        self.name = name
        self.price = price
        self.classes_limit = classes_limit
        self.benefits = ["Доступ до спортзалу"]
    
    def get_name(self) -> str:
        return self.name
    
    def get_price(self) -> Decimal:
        return self.price
    
    def get_classes_limit(self) -> int:
        return self.classes_limit
    
    def get_benefits(self) -> list:
        return self.benefits.copy()
    
    def get_loyalty_multiplier(self) -> float:
        return 1.0


class MembershipDecorator(MembershipComponent):
    """Базовий декоратор для членства"""
    
    def __init__(self, membership: MembershipComponent):
        self.membership = membership
    
    def get_name(self) -> str:
        return self.membership.get_name()
    
    def get_price(self) -> Decimal:
        return self.membership.get_price()
    
    def get_classes_limit(self) -> int:
        return self.membership.get_classes_limit()
    
    def get_benefits(self) -> list:
        return self.membership.get_benefits()
    
    def get_loyalty_multiplier(self) -> float:
        return self.membership.get_loyalty_multiplier()


class PersonalTrainerDecorator(MembershipDecorator):
    """Декоратор для додавання персонального тренера"""
    
    TRAINER_COST = Decimal("50.00")
    
    def __init__(self, membership: MembershipComponent, sessions_per_month: int = 4):
        super().__init__(membership)
        self.sessions_per_month = sessions_per_month
    
    def get_name(self) -> str:
        return f"{self.membership.get_name()} + Тренер"
    
    def get_price(self) -> Decimal:
        total_cost = self.TRAINER_COST * self.sessions_per_month
        return self.membership.get_price() + total_cost
    
    def get_benefits(self) -> list:
        benefits = self.membership.get_benefits()
        benefits.append(f"Персональний тренер ({self.sessions_per_month} занять/місяць)")
        return benefits
    
    def get_loyalty_multiplier(self) -> float:
        return self.membership.get_loyalty_multiplier() * 1.2


class NutritionConsultantDecorator(MembershipDecorator):
    """Декоратор для додавання консультацій з харчування"""
    
    CONSULTATION_COST = Decimal("30.00")
    
    def __init__(self, membership: MembershipComponent, consultations_per_month: int = 2):
        super().__init__(membership)
        self.consultations_per_month = consultations_per_month
    
    def get_name(self) -> str:
        return f"{self.membership.get_name()} + Харчування"
    
    def get_price(self) -> Decimal:
        total_cost = self.CONSULTATION_COST * self.consultations_per_month
        return self.membership.get_price() + total_cost
    
    def get_benefits(self) -> list:
        benefits = self.membership.get_benefits()
        benefits.append(f"Консультації по харчуванню ({self.consultations_per_month} разів/місяць)")
        return benefits
    
    def get_loyalty_multiplier(self) -> float:
        return self.membership.get_loyalty_multiplier() * 1.15


class DiscountDecorator(MembershipDecorator):
    """Декоратор для додавання знижки"""
    
    def __init__(self, membership: MembershipComponent, discount_percent: float):
        super().__init__(membership)
        self.discount_percent = discount_percent
    
    def get_name(self) -> str:
        return f"{self.membership.get_name()} (-{self.discount_percent}%)"
    
    def get_price(self) -> Decimal:
        original_price = self.membership.get_price()
        discount_amount = (original_price * Decimal(str(self.discount_percent / 100)))
        return (original_price - discount_amount).quantize(Decimal("0.01"))
    
    def get_benefits(self) -> list:
        benefits = self.membership.get_benefits()
        benefits.append(f"Знижка {self.discount_percent}% на ціну")
        return benefits
    
    def get_loyalty_multiplier(self) -> float:
        return self.membership.get_loyalty_multiplier() * 1.1


class UnlimitedClassesDecorator(MembershipDecorator):
    """Декоратор для необмежених занять"""
    
    UNLIMITED_COST = Decimal("40.00")
    
    def get_name(self) -> str:
        return f"{self.membership.get_name()} Unlimited"
    
    def get_price(self) -> Decimal:
        return self.membership.get_price() + self.UNLIMITED_COST
    
    def get_classes_limit(self) -> int:
        return float('inf')  # Необмежено
    
    def get_benefits(self) -> list:
        benefits = self.membership.get_benefits()
        benefits.append("Необмежені заняття")
        return benefits
    
    def get_loyalty_multiplier(self) -> float:
        return self.membership.get_loyalty_multiplier() * 1.3


class ParkingDecorator(MembershipDecorator):
    """Декоратор для припаркування"""
    
    PARKING_COST = Decimal("10.00")
    
    def get_name(self) -> str:
        return f"{self.membership.get_name()} + Паркування"
    
    def get_price(self) -> Decimal:
        return self.membership.get_price() + self.PARKING_COST
    
    def get_benefits(self) -> list:
        benefits = self.membership.get_benefits()
        benefits.append("Безплатне паркування")
        return benefits
    
    def get_loyalty_multiplier(self) -> float:
        return self.membership.get_loyalty_multiplier() * 1.05


class FreeDeliveryDecorator(MembershipDecorator):
    """Декоратор для безплатної доставки речей"""
    
    def get_name(self) -> str:
        return f"{self.membership.get_name()} + Доставка"
    
    def get_price(self) -> Decimal:
        # Доставка може бути включена без додаткової вартості
        return self.membership.get_price()
    
    def get_benefits(self) -> list:
        benefits = self.membership.get_benefits()
        benefits.append("Безплатна доставка спортзалу")
        return benefits
    
    def get_loyalty_multiplier(self) -> float:
        return self.membership.get_loyalty_multiplier() * 1.25


# Приклади використання:
def example_decorators():
    """Приклади створення різних членств через декоратори"""
    
    # Базове членство
    basic = BaseMembership("Базове", Decimal("50.00"), 10)
    print_membership_info(basic)
    
    # Базове + персональний тренер
    with_trainer = PersonalTrainerDecorator(basic, 2)
    print_membership_info(with_trainer)
    
    # Базове + харчування + тренер
    enhanced = NutritionConsultantDecorator(with_trainer, 1)
    print_membership_info(enhanced)
    
    # Преміум комбо: Unlimited + Тренер + Харчування + Знижка + Паркування
    premium = (FreeDeliveryDecorator(
        ParkingDecorator(
            DiscountDecorator(
                NutritionConsultantDecorator(
                    PersonalTrainerDecorator(
                        UnlimitedClassesDecorator(basic),
                        3
                    ),
                    2
                ),
                15  # 15% знижка
            ),
            1
        )
    ))
    print_membership_info(premium)
    
    # VIP членство з максимумом переваг
    vip = (FreeDeliveryDecorator(
        ParkingDecorator(
            DiscountDecorator(
                NutritionConsultantDecorator(
                    PersonalTrainerDecorator(
                        UnlimitedClassesDecorator(
                            BaseMembership("VIP", Decimal("200.00"), float('inf'))
                        ),
                        8
                    ),
                    4
                ),
                25  # 25% знижка для VIP
            )
        )
    ))
    print_membership_info(vip)


def print_membership_info(membership: MembershipComponent):
    """Вивести інформацію про членство"""
    print(f"\n{'='*60}")
    print(f"📝 {membership.get_name()}")
    print(f"{'='*60}")
    print(f"💰 Ціна: {membership.get_price()} USD")
    print(f"📊 Ліміт занять: {membership.get_classes_limit() if membership.get_classes_limit() != float('inf') else 'Необмежено'}")
    print(f"⭐ Множник балів лояльності: {membership.get_loyalty_multiplier()}x")
    print(f"\n✨ Переваги:")
    for i, benefit in enumerate(membership.get_benefits(), 1):
        print(f"   {i}. {benefit}")
