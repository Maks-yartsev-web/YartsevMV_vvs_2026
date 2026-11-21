class Calculator:
    '''Калькулятор с четырьмя базовыми операциями'''
    def calculate(self, x, y, op):
        '''Вернуть результат действия с двумя числами'''
        if op == '+': return x + y
        if op == '-': return x - y
        if op == '*': return x * y
        return x / y
