from cs50 import get_int

card = 0


def main():

    ccnum = get_int("Number: ")

    real = checksum(ccnum)

    if real == 1 and card == 1:
        print("AMEX")
    elif real == 1 and card == 2:
        print("MASTERCARD")
    elif real == 1 and card == 3:
        print("VISA")
    else:
        print("INVALID")


def checksum(ccnum):
    global card
    total = 0
    i = 0
    if ccnum < 1000000000000 or ccnum > 9999999999999999:
        return 0
    else:
        for i in range(16):
            notdblnum = 0
            dblnum = 0
            if (i % 2 == 0):
                notdblnum = ccnum % 10
                total += notdblnum
            elif (i % 2 == 1):
                dblnum = ccnum % 10
                dblnum *= 2
                if (dblnum > 9):
                    dblnum = dblnum - 9
                total += dblnum
            ccnum = ccnum // 10
            if (ccnum == 34 or ccnum == 37):
                card = 1
            if (ccnum > 50 and ccnum < 56):
                card = 2
            if (ccnum == 4):
                card = 3
        if (total % 10 == 0):
            return 1
        else:
            return 0


if __name__ == "__main__":
    main()