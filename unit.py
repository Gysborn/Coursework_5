from __future__ import annotations
from abc import ABC, abstractmethod
from equipment import Weapon, Armor, Equipment
from classes import UnitClass, WarriorClass, ThiefClass
from random import randint
from typing import Optional


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """

    def __init__(self, name: str, unit_class: UnitClass):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = None
        self.armor = None
        self.skill_name = unit_class.skill.name
        self.skill_stamina = unit_class.skill.stamina
        self.skill_damage = unit_class.skill.damage
        self._is_skill_used = False

    @property
    def health_points(self) -> float:
        # TODO возвращаем аттрибут hp в красивом виде
        return round(self.hp, 1)

    @property
    def stamina_points(self) -> float:
        # TODO возвращаем аттрибут stamina в красивом виде
        return round(self.stamina, 1)

    def equip_weapon(self, weapon: Weapon) -> str:
        # TODO присваиваем нашему герою новое оружие
        self.weapon = weapon
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor) -> str:
        # TODO одеваем новую броню
        self.armor = armor
        return f"{self.name} экипирован броней {self.armor.name}"

    def count_damage(self, target: BaseUnit) -> int:
        # TODO Эта функция должна содержать:
        #  логику расчета урона игрока
        #  логику расчета брони цели
        #  здесь же происходит уменьшение выносливости атакующего при ударе
        #  и уменьшение выносливости защищающегося при использовании брони
        #  если у защищающегося нехватает выносливости - его броня игнорируется
        #  после всех расчетов цель получает урон - target.get_damage(damage)
        #  и возвращаем предполагаемый урон для последующего вывода пользователю в текстовом виде

        damage = self.weapon.damage * self.unit_class.attack
        self.stamina -= self.weapon.stamina_per_hit

        if self.stamina < 0:
            self.stamina = 0

        if target.armor.stamina_per_turn > target.stamina:
            target._get_damage(damage)
            return round(damage, 1)
        else:
            damage -= target.armor.defence * target.unit_class.armor
            if damage > 0:
                target._get_damage(damage)
        target.stamina -= target.armor.stamina_per_turn

        if target.stamina < 0:
            target.stamina = 0
        return round(damage, 1)

    def _get_damage(self, damage: int):
        # TODO получение урона целью
        #      присваиваем новое значение для аттрибута self.hp
        self.hp -= damage

    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        """
        этот метод будет переопределен ниже
        """
        pass

    def use_skill(self, target: BaseUnit) -> str:
        """
        метод использования умения.
        если умение уже использовано возвращаем строку
        Навык использован
        Если же умение не использовано тогда выполняем функцию
        self.unit_class.skill.use(user=self, target=target)
        и уже эта функция вернем нам строку которая характеризует выполнение умения
        """
        if not self._is_skill_used:
            self._is_skill_used = True
            return self.unit_class.skill.use(self, user=self, target=target)

        else:
            return "Навык использован"


class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        функция удар игрока:
        здесь происходит проверка достаточно ли выносливости для нанесения удара.
        вызывается функция self._count_damage(target)
        а также возвращается результат в виде строки
        """
        if self.stamina < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."
        damage = self.count_damage(target)
        if damage > 0:
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит {damage} урона."
        else:
            f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} cоперника его останавливаеt"

        # TODO результат функции должен возвращать следующие строки:



class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        функция удар соперника
        должна содержать логику применения соперником умения
        (он должен делать это автоматически и только 1 раз за бой).
        Например, для этих целей можно использовать функцию randint из библиотеки random.
        Если умение не применено, противник наносит простой удар, где также используется
        функция _count_damage(target
        """
        rand_int = randint(0, 9)
        if rand_int < 1:
            return self.use_skill(target)
        if self.stamina < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."
        damage = self.count_damage(target)
        if damage > 0:
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} и наносит Вам {damage} урона"
        else:
            return f"{self.name} используя {self.weapon.name} наносит удар, но Ваш(а) {target.armor.name} его останавливает."

        # TODO результат функции должен возвращать результат функции skill.use или же следующие строки:
        # f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} и наносит Вам {damage} урона."
        # f"{self.name} используя {self.weapon.name} наносит удар, но Ваш(а) {target.armor.name} его останавливает."
        # f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

