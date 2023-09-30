import json
import random
from pathlib import Path


class Cities:
    miss_char = ["й", "ь", "ы", "ъ", "ё", "ц"]

    def __init__(self, level: str):
        self.cities: list[dict] = self.load_cities()
        self.used_cities = []
        self.population = self.set_population(level)
        self.last_char: str = random.choice("абвгдежзиклмнопрстуфхчшщэюя")

    def set_population(self, level):
        """Минимальное население для поиска города зависит от уровня сложности"""
        if level == "1":
            return 200_000
        elif level == "2":
            return 20_000
        elif level == "3":
            return 0
        else:
            return 500_000

    def random_city(self, char: str) -> str:
        """Перемешиваем список городов, находим город с населением больше level"""
        random.shuffle(self.cities)
        for item in self.cities:
            city = item.get('name')
            if self.population < item.get('population') and city[0].upper() == char.upper():
                self.cities.remove(item)
                self.used_cities.append(city)
                self.last_char = self.get_last_char(city).lower()
                return city

    def load_cities(self):
        with open(Path.joinpath(Path(__file__).parent, "data", "russian-cities.json"), "r", encoding="utf-8") as file:
            return json.load(file)

    def get_last_char(self, word: str) -> str:
        if word[-1] in self.miss_char:
            return word[-2]
        return word[-1]

    def check_city(self, city: str) -> tuple[bool, str]:
        if city.lower()[0] != self.last_char:
            return False, f"Нужно назвать город на букву {self.last_char.upper()}"
        if city.lower() in self.used_cities:
            return False, "Такой город уже назывался"
        else:
            for item in self.cities:
                if item.get('name').lower() == city.lower().strip():
                    self.used_cities.append(item.get('name').lower())
                    self.cities.remove(item)
                    return True, (f"Верно, местонахождение города - {item.get('subject')}\n"
                                  f"В нем проживает примерно {round(item.get('population'), -3)} человек")
            return False, "К сожалению я не знаю такого города в России"


class BullsCows:
    __digits = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    def __init__(self, num_digits: str):
        self.num_digits = int(num_digits)
        self.__number = self._generate_number()
        self.attempts = 0
        # self.game()

    def _generate_number(self) -> list:
        """Генератор n-значного числа. Первая цифра не должна быть 0, все цифры в числе должны быть разными."""
        n = 0
        number = []
        while n < self.num_digits:
            if n == 0:
                digit = random.choice(self.__digits[1:])
            else:
                digit = random.choice(self.__digits)
            self.__digits.remove(digit)
            number.append(digit)
            n += 1
        return number

    def check_bulls_cows(self, number: str):
        bulls = 0
        cows = 0
        n = 0
        for digit in number:
            if int(digit) in self.__number:
                if int(digit) == self.__number[n]:
                    bulls += 1
                else:
                    cows += 1
            n += 1
        self.attempts += 1
        return bulls, cows

    def check_number(self, number: str) -> tuple[bool, str]:
        """Проверки на корректность введенного числа"""
        try:
            int(number)
        except ValueError:
            return False, f"Необходимо ввести целое число"

        if number[0] == '0':
            return False, f"Число не должно начинаться с 0"

        if len(number) == self.num_digits:
            for digit in number:
                if number.count(digit) > 1:
                    return False, f"Число должно содержать разные цифры"
            return True, f"Все ок"
        else:
            print()
            return False, f"Число должно быть {self.num_digits}-значное"

    def game(self):
        while True:
            num: str = input(f"Введите число, состоящее из {self.num_digits} цифр: ")
            if self.check_number(num):
                b, c = self.check_bulls_cows(num)
                print(f"{b} - bulls, {c} - cows")
                if b == self.num_digits:
                    print("Поздравляю, вы выйграли!")
                    print(f"Вы угадали число за {self.attempts} попыток.")
                    break


if __name__ == "__main__":
    cities = Cities()
    print(cities.get_last_char("Азей"))
    # bc = BullsCows('3')
    # while True:
    #     num = input("Введите число, состоящее из 3 цифр: ")
    #     b, c = bc.equation_numbers(num)
    #     print(f"{b} - bulls, {c} - cows")
    #     if b == 4:
    #         print("Поздравляю, вы выйграли!")
    #         break
