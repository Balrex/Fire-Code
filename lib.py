import numpy as np

class FireCode(object): # Класс для кода Файра
    def __init__(self, polynomial): # Принимаем на вход неприводимый многочлен, который выражен в виде последовательности бит
        self.polynomial = polynomial # Сохраняем многочлен в переменную
        self.r = len(polynomial) - np.min(np.nonzero(polynomial)) - 1 # Вычисляем максимальную степень многочлена
        self.booleanMapper = np.vectorize(get_zero_and_one)

    def code(self, message):
        print("Начальное сообщение:", np.array(message))
        cx = np.array(message)
        cx = np.append(cx, [0] * self.r) # Дополняем к начальному сообщению нули, то есть получаем длину полного сообщения (с проверочными битами)
        cx = self.get_module(cx, self.polynomial) # Делим начальное сообщение на порождающий многочлен, для получения проверочных бит
        dif = self.r - len(cx)
        print("Дополнительные биты:", cx)
        print()
        if dif != 0: # Проверка разницы между длиной многочлена и сообщением
            cx = np.append([0] * dif, cx) # Если есть разница, дополняем иx нулями до длины многочлена
        return np.append(message, cx) # Возвращаем сообщение с проверочными битами

    def add_errors(self, err, message): # Метод для внесения ошибки в сообщение
        if err == 0:                # Если ввести 0 бит на изменение, будем считать, что в сообщение не будет вноситься ошибка
            return message
        message = np.array(message) 
        if message[err-1] == 0:     # Изменяем по указанному месту бит на противоположный
            message[err-1] = 1
        else:
            message[err-1] = 0
        return message # Возвращаем испорченное сообщение

    def decode(self, err_message): # Метод декодирования сообщения
        cx = self.get_module(err_message, self.polynomial) # Вычисляем синдром ошибки
        dif = len(err_message[-self.r:]) - len(cx)
        cx = np.append(dif * [0], cx)                      # Добавляем в начало синдрома нули, увеличивая его до необходимого размера
        print("\nСиндром ошибки:", np.array(list(map(int, cx)))) 
        return cx # Возвращаем синдром ошибки

    def get_module(self, p, module): # Метод вычисления остатков (последовательностей по модулю)
        if len(np.nonzero(p)[0]) == 0: # Проверка на отсутствие не нулевых элементов
            return [0] # Если вся последовательность состоит из 0, возвращаем 0
        p = np.array(p)
        module = np.array(module)
        p_deg = len(p) - np.min(np.nonzero(p)) - 1
        mod_deg = len(module) - np.min(np.nonzero(module)) - 1
        p = np.delete(p, range(0, np.min(np.nonzero(p))))
        module = np.delete(module, range(0, np.min(np.nonzero(module))))
        try:
            while p_deg >= mod_deg:
                deg = p_deg - mod_deg
                tmp_module = np.append(module, [0] * deg)
                p = np.logical_xor(p, tmp_module)
                p_deg = len(p) - np.min(np.nonzero(p)) - 1
                p = np.delete(p, range(0, np.min(np.nonzero(p))))
            v_func = np.vectorize(get_zero_and_one)
            return v_func(p)
        except ValueError: # Если деление невозможно, возвращаем ошибку
            return [0]

def get_zero_and_one(y):
    if y == 1:
        return 1
    else:
        return 0
