from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from unit import BaseUnit


class Skill(ABC):
    """
    Базовый класс умения
    """
    user = None
    target = None

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def stamina(self):
        pass

    @property
    @abstractmethod
    def damage(self):
        pass

    @abstractmethod
    def skill_effect(self) -> str:
        pass

    def _is_stamina_enough(self):
        return self.user.stamina >= self.user.unit_class.skill.stamina

    def use(self, user: BaseUnit, target: BaseUnit) -> str:
        """
        Проверка, достаточно ли выносливости у игрока для применения умения.
        Для вызова скилла везде используем просто use
        """
        self.user = user
        self.target = target
        if Skill._is_stamina_enough(self):
            return self.user.unit_class.skill.skill_effect(self)
        return f"{self.user.name} попытался использовать {self.user.unit_class.skill.name} но у него не хватило выносливости."


class FuryPunch(Skill):
    name = "Свирепый Пинокио"
    stamina = 6
    damage = 12

    def skill_effect(self) -> str:
        self.target.hp -= FuryPunch.damage
        self.user.stamina -= FuryPunch.stamina
        return f"{self.user.name} использует {FuryPunch.name} " \
               f"и дамажит на {FuryPunch.damage} урона соперника."
        # TODO логика использования скилла -> return str
        # TODO в классе нам доступны экземпляры user и target - можно использовать любые их методы
        # TODO именно здесь происходит уменшение стамины у игрока применяющего умение и
        # TODO уменьшение здоровья цели.
        # TODO результат применения возвращаем строкой


class HardShot(Skill):
    name = "Мощный укор"
    stamina = 5
    damage = 15

    def skill_effect(self) -> str:
        self.target.hp -= HardShot.damage
        self.user.stamina -= HardShot.stamina
        return f"{self.user.name} использует {HardShot.name} " \
               f"и дамажит на {HardShot.damage} урона соперника."
