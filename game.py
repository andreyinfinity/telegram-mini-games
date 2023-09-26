import json
import random


class Cities:
    miss_char = ["й", "ь", "ы", "ъ", "ё"]
    used_cities = []

    def __init__(self):
        self.cities = self.load_cities()

    def random_city(self) :
        city = random.choice(self.cities)
        self.cities.remove(city)
        return city

    def load_cities(self):
        with open("data/cities.json", "r", encoding="utf-8") as file:
            return json.load(file)

    def get_last_char(self, word: str):
        if word[-1] in self.miss_char:
            return word[-2]
        return word[-1]

    # def check_city(self, city: str):
    #     if city.capitalize() in self.used_cities:
    #         print("Такой город уже назывался")
    #     elif city.capitalize() in self.cities


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
