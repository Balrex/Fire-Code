import numpy as np

from lib import *

# Таблица синдромов ошибок
syndrome_table = [ [1, 0, 1], [1, 1, 1], [1, 1, 0], [0, 1, 1],
                   [1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 0, 0]
                 ]

#syndrome_table = [ [1, 0, 0, 1, 1], [1, 1, 0, 1, 0], [0, 1, 1, 0, 0], [1, 0, 1, 0, 1],
#                   [1, 1, 0, 0, 1], [1, 1, 1, 1, 1], [1, 1, 1, 0, 0], [0, 1, 1, 1, 1], [0, 0, 1, 1, 1],
#                   [1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]
#                 ]

def bit_error(syndrome):
    i = 1
    for element in syndrome_table:
        if syndrome == element:
            return i
        i += 1

if __name__ == "__main__":
    # gX = input("Введите порождающий многочлен: ")
    # gX = "100111"                           #       // для (14, 9)-кода      
    gX = "1011"                               #      //  дляm (7, 4)-кода
    print("Порождающий многочлен:", gX)
    gX = [int(char) for char in gX]

    # message = input("Введите сообщение: ")
    # message = "011001110"
    message = "0010"
    print("Сообщение:", message)
    message = [int(char) for char in message]
    # err = input("Введите номер искаженного бита: ")
    err = 2
    print("В каком бите будет ошибка:", err)
    print()

    Code = FireCode(gX)   
    full_message = Code.code(message)
    codedMsg = Code.add_errors(err, full_message)
    print("Сообщение с дополнительными битами:", full_message)
    print("Полученное сообщение:\t\t   ", np.array(codedMsg))
    error_syndrome = list(Code.decode(codedMsg))

    i = bit_error(error_syndrome)
    if i == 8:
        print("Ошибки нет")
    else:
        E = 1
        print(f"Ошибка в бите {i}")
        if codedMsg[i-1] == 0:
            codedMsg[i-1] = 1
        else:
            codedMsg[i-1] = 0
    print()
    
    i = len(gX) - np.min(np.nonzero(gX)) - 1
    answer = codedMsg[:-i]
    print("Оригинальное сообщение: ", message)
    print("Декодированное сообщение: ", answer)
    