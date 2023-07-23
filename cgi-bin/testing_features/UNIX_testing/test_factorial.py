import unittest

class FactorialTestCase(unittest.TestCase):
    def test_factorial(self):
        # Входные данные и ожидаемые результаты
        test_cases = [
            (-1, "Sorry, factorial does not exist for negative numbers"),
            (0, "The factorial of 0 is 1"),
            (5, "The factorial of 5 is 120"),
            (7, "The factorial of 7 is 5040")
        ]

        for num, expected_result in test_cases:
            with self.subTest(num=num):
                # Выполнение программы для текущего входного значения
                factorial = 1
                if num < 0:
                    result = "Sorry, factorial does not exist for negative numbers"
                elif num == 0:
                    result = "The factorial of 0 is 1"
                else:
                    for i in range(1, num + 1):
                        factorial = factorial * i
                    result = "The factorial of " + str(num) + " is " + str(factorial)

                # Проверка соответствия полученного результата ожидаемому
                self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
