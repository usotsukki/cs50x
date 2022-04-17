import sys
import csv
from collections import Counter
from itertools import repeat, chain


def main():
    # check for main() arguments
    if len(sys.argv) != 3:
        sys.exit('Usage: python dna.py data.csv, sequence.txt')

    # read database to memory
    data = list(csv.reader(open(sys.argv[1])))

    # STRs
    # for i in range(1, len(data[0])):
    # print(data[0][i])

    # names
    # for j in range(1, len(data)):
    # print(data[j][0])

    # read sequence to memory
    with open(sys.argv[2]) as file:
        sequence = file.read()

    # count consecutive strings in sequence
    result_list = []
    for j in range(1, len(data)):
        for i in range(1, len(data[0])):

            n = 1
            if (i-n) < 1:
                n = -1
            # seqv and seqv2 are specific strs for person like (24 times AGAT etc.)
            seqv = listToString(data[0][i])
            intv = int(data[j][i])
            seqr = seqv * intv

            seqv2 = listToString(data[0][i-n])
            intv2 = int(data[j][i-n])
            seqr2 = seqv2 * intv2

            if (sequence.find(seqr) != -1) and (sequence.find(seqr2) != -1) and (sequence.find(seqv*(intv+1)) == -1) and (sequence.find(seqv2*(intv2+1)) == -1):
                result_list.append(data[j][0])

    # sorted matches by frequency of matches (in reverse order)
    result = list(chain.from_iterable(repeat(i, c)
                  for i, c in Counter(result_list).most_common()))

    # print(result)
    # output matching results

    if (len(result) > 7):

        if (result[0] == result[7]):
            print(result[0])

        else:
            print('No match')

    elif len(result) > 2:
        print(result[0])
        
    else:
        print('No match')


def listToString(s):

    # initialize an empty string
    string = ""

    # traverse in the string
    for element in s:
        string += element

    # return string
    return string


if __name__ == "__main__":
    main()
