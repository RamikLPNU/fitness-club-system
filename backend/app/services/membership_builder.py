from datetime import datetime, timedelta
from decimal import Decimal


class MembershipBuilder:
    
    def __init__(self):
        self.name = None
        self.duration_days = 30
        self.price = Decimal("0.00")
        self.max_classes_per_week = None
        self.classes_list = []
        self.includes_trainer = False
        self.includes_nutrition = False
        self.created_date = datetime.now()
        
    def set_name(self, name: str):
        """Встановити назву членства"""
        self.name = name
        return self
    
    def set_duration(self, days: int):
        """Встановити тривалість членства в днях"""
        self.duration_days = days
        return self
    
    def set_price(self, price: Decimal):
        """Встановити ціну"""
        self.price = price
        return self
    
    def set_classes_limit(self, limit: int):
        """Встановити максимум занять на тиждень"""
        self.max_classes_per_week = limit
        return self
    
    def add_class(self, class_id: int):
        """Додати конкретний клас до членства"""
        self.classes_list.append(class_id)
        return self
    
    def with_trainer(self):
        """Включити персонального тренера"""
        self.includes_trainer = True
        return self
    
    def with_nutrition(self):
        """Включити консультацію по харчуванню"""
        self.includes_nutrition = True
        return self
    
    def build(self):
        """Побудувати фінальний об'єкт членства"""
        if not self.name:
            raise ValueError("Назва членства обов'язкова")
        if self.price < 0:
            raise ValueError("Ціна не може бути негативною")
        
        return {
            "name": self.name,
            "duration_days": self.duration_days,
            "price": self.price,
            "max_classes_per_week": self.max_classes_per_week,
            "classes_list": self.classes_list,
            "includes_trainer": self.includes_trainer,
            "includes_nutrition": self.includes_nutrition,
            "created_date": self.created_date
        }


# Приклади використання:
def example_builders():
    """Приклади побудови різних типів членств"""
    
    # Базове членство
    basic = (MembershipBuilder()
             .set_name("Базове")
             .set_price(Decimal("50.00"))
             .set_duration(30)
             .build())
    
    # Преміум членство з тренером
    premium = (MembershipBuilder()
               .set_name("Преміум")
               .set_price(Decimal("150.00"))
               .set_duration(30)
               .set_classes_limit(12)
               .with_trainer()
               .with_nutrition()
               .build())
    
    # VIP членство з обмеженнями
    vip = (MembershipBuilder()
           .set_name("VIP")
           .set_price(Decimal("300.00"))
           .set_duration(90)
           .set_classes_limit(None)  # Необмежено
           .add_class(1)
           .add_class(2)
           .add_class(3)
           .with_trainer()
           .with_nutrition()
           .build())
    
    return basic, premium, vip
