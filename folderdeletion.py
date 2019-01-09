import os
def main():
    MAX = 2
    DIR = "/home/zsamora/Descargas/labcronobiologia/"
    BUFFER = []
    cont = 0
    index = 0
    while True:
        print(BUFFER, cont, index)
        if not os.path.isdir(DIR + str(cont)):
            if len(BUFFER) == MAX:
                os.rmdir(DIR + BUFFER[index])
                BUFFER[index] = str(cont)
                index = (index + 1) % MAX
            else:
                BUFFER.append(str(cont))
            try:
                os.makedirs(DIR + str(cont))
            except OSError:
                raise
        cont += 1

if __name__ == '__main__':
    main()
