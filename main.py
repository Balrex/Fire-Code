import numpy as np

from lib import *

# Таблица синдромов ошибок
#syndrome_table = [ [1, 0, 1], [1, 1, 1], [1, 1, 0], [0, 1, 1],                                                 # // для (7, 4)-кода
#                   [1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 0, 0]
#                 ]

#syndrome_table = [ [1, 0, 0, 1, 1], [1, 1, 0, 1, 0], [0, 1, 1, 0, 0], [1, 0, 1, 0, 1],                         # // для (14, 9)-кода
#                   [1, 1, 0, 0, 1], [1, 1, 1, 1, 1], [1, 1, 1, 0, 0], [0, 1, 1, 1, 1], [0, 0, 1, 1, 1],
#                   [1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]
#                 ]

                                                                                                                # // для (28, 21)-кода
syndrome_table = [ [0, 1, 0, 1, 1, 1, 0], [0, 0, 1, 0, 1, 1, 1], [1, 0, 1, 0, 1, 1, 0], [0, 1, 0, 1, 0, 1, 1], [1, 0, 0, 1, 0, 0, 0], [0, 1, 0, 0, 1, 0, 0], [0, 0, 1, 0, 0, 1, 0], [0, 0, 0, 1, 0, 0, 1], [1, 0, 1, 1, 0, 0, 1],
                   [1, 1, 1, 0, 0, 0, 1], [1, 1, 0, 0, 1, 0, 1], [1, 1, 0, 1, 1, 1, 1], [1, 1, 0, 1, 0, 1, 0], [0, 1, 1, 0, 1, 0, 1], [1, 0, 0, 0, 1, 1, 1], [1, 1, 1, 1, 1, 1, 0], [0, 1, 1, 1, 1, 1, 1], [1, 0, 0, 0, 0, 1, 0],
                   [0, 1, 0, 0, 0, 0, 1], [1, 0, 0, 1, 1, 0, 1], [1, 1, 1, 1, 0, 1, 1], [1, 1, 0, 0, 0, 0, 0], [0, 1, 1, 0, 0, 0, 0], [0, 0, 1, 1, 0, 0, 0], [0, 0, 0, 1, 1, 0, 0], [0, 0, 0, 0, 1, 1, 0], [0, 0, 0, 0, 0, 1, 1]
                 ]

def bit_error(syndrome):
    i = 1
    for element in syndrome_table:
        if syndrome == element:
            return i
        i += 1

if __name__ == "__main__":
    # gX = input("Введите порождающий многочлен: ")
    # gX = "1011"                             #        //  для (7, 4)-кода: t=3, c=0, L=1
    # gX = "100111"                           #       // для (14, 9)-кода: t=3, c=2, L=1
    gX = "10111011"                           #      //  для (28, 21)-кода: t=3, c=4, L=2
    print("Порождающий многочлен:", gX)
    gX = [int(char) for char in gX]

    # L = input("Введите длину пакета ошибок")
    L = 2

    # message = input("Введите сообщение: ")
    # message = "011001110"
    # message = "0010"
    message = "111000111000111000111"
    print("Сообщение:", message)
    message = [int(char) for char in message]
    # err = input("Введите номер искаженного бита: ")
    err = 25
    #print("В каком бите будет ошибка:", err)
    print()

    Code = FireCode(gX)
    full_message = Code.code(message)
    print("В каком бите будет ошибка:", err," - ", err+1)
    match L:
        case 1:
            codedMsg = Code.add_errors(err, full_message)
        case 2:
            codedMsg = Code.add_errors2(err, err, full_message)
    print("Сообщение c дополнительными битами:", full_message)
    print("Полученное сообщение:\t\t   ", np.array(codedMsg))
    error_syndrome = list(Code.decode(codedMsg))
    
    i = bit_error(error_syndrome)
    if i == 8:
        print("Ошибки нет")
    else:
        E = 1
        if L == 1:
            print(f"Ошибка в бите {i}")
            if codedMsg[i-1] == 0:
                codedMsg[i-1] = 1
            else:
                codedMsg[i-1] = 0
        else:
            print(f"Ошибка в битах {i} - {i+1}")
            if codedMsg[i-1] == 0:
                codedMsg[i-1] = 1
                codedMsg[i] = 1
            else:
                codedMsg[i-1] = 0
                codedMsg[i] = 0

    print()

    i = len(gX) - np.min(np.nonzero(gX)) - 1
    answer = codedMsg[:-i]
    print("Оригинальное сообщение: ", message)
    print("Декодированное сообщение: ", answer)
    
