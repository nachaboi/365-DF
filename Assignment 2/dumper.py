# COMPSCI 365
# Spring 2020
# NATHAN NG
# Assignment 2: Dumper

# Complete the relevant functions.
# Make sure to test your implementations.
# You can import any standard library.
# You can define any new function you want.

import binascii
import math
import codecs

def hex_dump(inputFile):
    """
    Description: Read the input file and return a hexdump of the file,
    # identical in formatting to the `hexdump -Cv` program.
    # The formatted hex bytes can be in upper or lowercase.
    # The first output column is the offset. The second output column
    # contains the file bytes in hex format.
    # The last output column contains the bytes in ASCII-encoded
    # character format. If a byte is not ASCII-printable,
    # the character should be a period ('.'). Each output column is
    # separated by two spaces ('  '), each hex byte is separated
    # by one space (' '), except for the 8th and 9th bytes in each
    # row which are separated by two spaces ('  '), and each line
    # of the ASCII output is surrounded by vertical bars ('|').
    # Note that the input file CAN be EMPTY.
    Input: string inputFile
    Output: string
    Example: Included in prompt.
    """
    arr = []
    with open(inputFile, 'rb') as f:
        for chunk in iter(lambda: f.read(16), b''):
            arr.append(str((binascii.hexlify(chunk)))[2:][:-1])
    theVals = []
    off = ["00000000"]
    row = 0
    ascFull = []
    for i in arr:
        curAsc = ""
        s = ""
        row += int(len(i)/2)
        theHex = str(hex(int(row)))
        toAdd = 8-len(theHex)+2
        finalHexString = ""
        for q in range(0,toAdd):
            finalHexString+="0"
        finalHexString+=theHex[-2:]
        off.append(finalHexString)
        for j in range(0,len(i)):
            if j % 2 == 0:
                s += i[j]
            else:
                curChar = codecs.decode((s+i[j])[-2:], "hex").decode('utf-8')
                if (ord(curChar) < 128 and ord(curChar) > 31):
                    curAsc += curChar
                else:
                    curAsc += "."
                if j == 15:
                    s += i[j] + "  "
                else:
                    s += i[j] + " "
        toAdd = 49 - len(s)
        finalvalString=s
        for p in range(0,toAdd):
            finalvalString+=" "
        finalvalString = finalvalString[:-1]
        # print(len(finalvalString))
        theVals.append(finalvalString)
        ascFull.append(curAsc)
    #     print(s)
    # print(off)
    # print(theVals)
    curString = ""
    for k in range(0, len(theVals)):
        curString += off[k] + "  " + theVals[k] +  "  |" + ascFull[k] + "|" + "\n"
    if len(theVals) < len(off):
        curString += off[len(off)-1]
    else:
        # curString = curString[:-1]
        curString = curString

    return curString
# hex_dump("uuu.txt")

# print(codecs.decode("68", "hex").decode('utf-8'))
# print(len("68 69 0a 64 6a 0a 77 68  61 74 0a 69 73 0a 75 70"))
