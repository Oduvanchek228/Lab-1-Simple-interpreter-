def interpreter(string):
    tokens = []
    i = 0

    while i < len(string):
        sym = string[i]

        # Игнорируем пробелы
        if sym.isspace():
            i += 1
        # Начинается лексический анализ
        elif sym.isdigit():
            start = i
            points = 0

            while i < len(string) and (string[i] in '0123456789.'):
                if string[i] == '.':
                    points += 1
                    if points > 1:
                        raise ValueError
                i += 1

            number = string[start:i]

            if number.endswith('.'):
                raise ValueError

            tokens.append(float(number) if points else int(number))

        elif sym.isalpha():
            start = i

            while i < len(string) and (string[i].isalpha()):
                i += 1

            name = string[start:i]

            if name != 'pow':
                raise ValueError

            tokens.append(name)

        elif string[i:i + 2] == '>>':
            tokens.append(string[i:i + 2])
            i += 2

        elif sym in '+-*/(),':
            tokens.append(sym)
            i += 1

        else:
            raise ValueError

    tokens.append(None)  # Элемент, обозначающий конец выражения

    pos = 0

    # Получает на вход токен, проверяет, соотв. ли он expected, возращает текущий токен и переходит к следующему
    def consume(expected=None):
        nonlocal pos

        token = tokens[pos]

        if token is None or (expected is not None and token != expected):
            raise ValueError

        pos += 1

        return token

    # Обработка сложения и вычитания
    def expression():
        result = term()

        while tokens[pos] in ('+', '-'):
            sign = consume()
            right = term()

            if sign == '+':
                result += right
            else:
                result -= right
        return result

    # Обработка умножения и деления
    def term():
        result = factor()

        while tokens[pos] in ('*', '/'):
            sign = consume()
            right = factor()

            if sign == '*':
                result *= right
            else:
                if right == 0:
                    raise ZeroDivisionError
                result /= right

        return result

    # Обработка чисел, скобок, унарных плюса/минуса и функции pow() (Вариант 7)
    def factor():
        token = tokens[pos]

        if token == '+':
            consume('+')
            return factor()

        if token == '-':
            consume('-')
            return -factor()

        if token == '(':
            consume('(')
            result = shift_expression()
            consume(')')
            return result

        if token == 'pow':
            consume('pow')
            consume('(')
            x = shift_expression()
            consume(',')
            y = shift_expression()
            consume(')')

            return x ** y

        if isinstance(token, (int, float)):
            return consume()
        raise ValueError  # Если не выполнилось ни одно из условий

    # Обработка побитового сдвига вправо (Вариант 7)
    def shift_expression():
        result = expression()

        while tokens[pos] == '>>':
            consume('>>')
            right = expression()

            if type(result) is not int or type(right) is not int:
                raise TypeError

            if right < 0:
                raise ValueError

            result >>= right

        return result

    if tokens[pos] is None:
        raise ValueError

    result = shift_expression()

    if tokens[pos] is not None:
        raise ValueError

    return result


try:
    print(interpreter('64 >> 2 + 1'))  # В качестве аргумента принимается строка с арифметическим выражением
except ValueError:
    print('Некорректное арифметическое выражение.')
except TypeError:
    print('Побитовый сдвиг вправо (>>) возможен только с целыми числами.')  # Это правила Python, я ничего не выдумал
except ZeroDivisionError:
    print('Деление на ноль недопустимо.')
