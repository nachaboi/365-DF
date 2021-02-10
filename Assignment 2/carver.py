# COMPSCI 365
# Spring 2020
# NATHAN NG
# Assignment 2: Carver

# Complete the relevant functions.
# Make sure to test your implementations.
# You can import any standard library.
# You can define any new function you want.

# * EXCEPTIONS: You may not use str.encode() OR bytes.decode().
# * This includes directly and indirectly.
# * bin(), chr(), and ord() are not allowed.
# * For example, bytes(chr(codePoint)) calls
# * str.encode() and therefore is not allowed.
# * You need to work with the bits yourself.
# * Work with values of type int; do NOT call
# * bin() to convert to strings and use
# * string manipulation instead.

# import BitArray
# import sys
import string
# import binascii


# def encode(): 

def utf8_search(inputFile, codePoint):
    """
    Description: Read the input file and search for the given
    # code point in UTF-8 format. Only find the FIRST occurrence
    # if there are multiple. Return the offset (the number
    # of bytes into the file, where the first byte starts at 0,
    # ex. the 11th byte is at offset 10) as a string in LOWERCASE
    # hexadecimal format of the first byte where the code point
    # is found, ex. "0x00000094". It should be left-padded with
    # zeroes up to eight characters (represents max. 16^8 bytes).
    # The codePoint will be in UPPERCASE format.
    # If it does not exist in the file, then return an empty string.
    Input: string inputFile, string codePoint
    Output: string
    Example: utf8_search("main.py", "U+0050") = "0x00000076"
    """

    d = {"0":0,"1":1,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"A":10,"B":11,"C":12,"D":13,"E":14,"F":15}

    size = len(codePoint[2:])-1
    theVal = 0
    for i in codePoint[2:]:
        theVal += d[i]*(16**(size))
        size -= 1
    
    data = None

    with open(inputFile, "rb") as file:
        data = file.read()
    # print(data)

    cur = theVal
    binLength = 0
    while cur > 0:
        cur = cur//2
        binLength+=1
    # theVal = 250
    convertedBin = None
    numBytes = 0
    if binLength <=7:
        convertedBin = theVal
        numBytes = 1
    elif binLength <= 11:
        temp = theVal&0b111111
        a = 0b10000000
        convertedBin = temp+a
        # print(bin(convertedBin), 111100)
        mask = 0b11111<<6
        # print(mask,0)
        temp = theVal&mask
        # print(bin(temp))
        temp = temp>>6
        a = 0b1100000000000000
        # print(bin(a+(temp<<8)))
        convertedBin = convertedBin + (temp<<8) + a
        numBytes = 2
    elif binLength <= 16:
        temp = theVal&0b111111
        a = 0b10000000
        convertedBin = temp+a
        mask = 0b111111<<6
        temp = theVal&mask
        temp = temp>>6
        a = 0b1000000000000000
        convertedBin = convertedBin + (temp<<8) + a
        mask = 0b1111<<12
        temp = theVal&mask
        temp = temp>>12
        a = 0b111000000000000000000000
        convertedBin = convertedBin + (temp<<16) + a
        numBytes = 3
    elif binLength <=21:
        temp = theVal&0b111111
        a = 0b10000000
        convertedBin = temp+a
        mask = 0b111111<<6
        temp = theVal&mask
        temp = temp>>6
        a = 0b1000000000000000
        convertedBin = convertedBin + (temp<<8) + a
        mask = 0b111111<<12
        temp = theVal&mask
        temp = temp>>12
        a = 0b100000000000000000000000
        convertedBin = convertedBin + (temp<<16) + a
        mask = 0b111<<18
        temp = theVal&mask
        temp = temp>>18
        a = 0b11110000000000000000000000000000
        convertedBin = convertedBin + (temp<<24) + a
        numBytes = 4
    # print(bin(convertedBin))
    # print(data[1])
    # print(range(0,len(data)-numBytes+1))
    # print(range(0,2))

    for i in range(0, len(data)-numBytes+1):
        curUTF = 0
        for j in range(0,numBytes):
            curUTF = curUTF + (data[i+(numBytes-j-1)]<<(8*j))
        # print(data[i])
        # print(curUTF)
        if curUTF == convertedBin:
            theHex = "0x%x" % i
            theHex = theHex[2:]
            toAdd = 8 - len(theHex)
            finalvalString="0x"
            for p in range(0,toAdd):
                finalvalString+="0"
            finalvalString +=theHex
            # print(finalvalString)
            return finalvalString.lower()
    return ""

    # print(bin(convertedBin))
    #it is an array

    # print(bytearray(data)[0])

    #encode by filling in bits (left pad) into how many it needs

    # if a


  #   to get one place
  #   ---------
  # &  0000001111


    # print(a)


    # if a <= 127:
    #     q = (binascii.a2b_uu("0" + decimalToBinary(a)))
    #     # print(format(q[0],"b"))
    # elif a <=2047:
    #     temp = decimalToBinary(a)
    #     q = binascii.a2b_uu("110" + temp[:5] + "10" + temp[-5:])

    
        # print(format(q[1],"b"))
    # elif a <=65535:

    # elif a <=1114111:

    # print(a)
    # data = None
    # with open(inputFile, "rb") as file:
    #     data = file.read()
    # data.find()
    # print(type(newcodePoint))

    # hexCodePoint = codePoint[2:]
    # # print(hexCodePoint)
    # arr = []
    # with open(inputFile, "rb") as fh:
    #     b = True
    #     while b:
    #         b = fh.read(1)
    #         arr.append(b.hex())
    # # print(int(hexCodePoint, 16) == int(arr[0], 16))

    # offset = 0
    # hexCodePoint = int(hexCodePoint, 16)
    # broken = False
    # # print(arr)
    # for i in arr:
    #     if hexCodePoint == int(i, 16):
    #         broken = True
    #         break
    #         # print()
    #     else:
    #         offset += 1
    # if not broken:
    #     return ""
    # theHex = "0x%x" % offset
    # theHex = theHex[2:]
    # toAdd = 8 - len(theHex)
    # finalvalString="0x"
    # for p in range(0,toAdd):
    #     finalvalString+="0"
    # finalvalString +=theHex
    # return finalvalString
    # return "0x00000076"

    # a = int(codePoint[2:], 16)


def utf8_carve(inputFile):
    """
    Description: Read the input file and extract all valid
    # UTF-8 characters that are in any of the following planes:
    # U+0000 to U+FFFF, U+10000 to U+1FFFF, U+20000 to U+2FFFF
    # If a character is valid and in one of those planes, but
    # is not defined, you still treat it as a character and
    # extract it. Each valid UTF-8 character extracted
    # should be represented with a (offset, codePoint) format.
    # The output should be a list of those formats (i.e. a list
    # of tuples). The offset string should be in the same format
    # as specified in the utf8_search function. The codePoint
    # string should be in the Unicode code format, i.e. "U+XXXX"
    # or "U+XXXXX" (number of X's depends on the plane it is in).
    # The ordering of the output list does not matter. The codePoint
    # should be in UPPERCASE, but the offset should be in LOWERCASE.
    # If there are no valid characters, return an empty list.
    # NOTE: REMEMBER THAT WE ARE CARVING FOR CHARACTERS THAT CAN BE
    # ANYWHERE BETWEEN 1 AND 4 BYTES. MAKE SURE YOU COVER ALL OF THOSE
    # CASES.
    Input: string inputFile
    Output: list of tuples (string offset, string codePoint)
    Example: utf8_carve("main.py") = [("0x00000000", "U+0069"),
    # ("0x00000001", "U+006D"), ("0x00000002", "U+0070"), ... ]
    """

    #0-65535
    #65536-131071
    #131072-196607
    d = {"0":0,"1":1,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"A":10,"B":11,"C":12,"D":13,"E":14,"F":15}
    nums = {}
    for i in range(0,196608):
        # theVal = str(i)
        theVal = i

        # size = len(codePoint)-1
        # theVal = 0
        # for i in codePoint:
        #     theVal += d[i]*(16**(size))
        #     size -= 1
        
        data = None

        with open(inputFile, "rb") as file:
            data = file.read()
        # print(data)

        cur = theVal
        binLength = 0
        while cur > 0:
            cur = cur//2
            binLength+=1
        # theVal = 250
        convertedBin = None
        numBytes = 0
        if binLength <=7:
            convertedBin = theVal
            numBytes = 1
        elif binLength <= 11:
            temp = theVal&0b111111
            a = 0b10000000
            convertedBin = temp+a
            # print(bin(convertedBin), 111100)
            mask = 0b11111<<6
            # print(mask,0)
            temp = theVal&mask
            # print(bin(temp))
            temp = temp>>6
            a = 0b1100000000000000
            # print(bin(a+(temp<<8)))
            convertedBin = convertedBin + (temp<<8) + a
            numBytes = 2
        elif binLength <= 16:
            temp = theVal&0b111111
            a = 0b10000000
            convertedBin = temp+a
            mask = 0b111111<<6
            temp = theVal&mask
            temp = temp>>6
            a = 0b1000000000000000
            convertedBin = convertedBin + (temp<<8) + a
            mask = 0b1111<<12
            temp = theVal&mask
            temp = temp>>12
            a = 0b111000000000000000000000
            convertedBin = convertedBin + (temp<<16) + a
            numBytes = 3
        elif binLength <=21:
            temp = theVal&0b111111
            a = 0b10000000
            convertedBin = temp+a
            mask = 0b111111<<6
            temp = theVal&mask
            temp = temp>>6
            a = 0b1000000000000000
            convertedBin = convertedBin + (temp<<8) + a
            mask = 0b111111<<12
            temp = theVal&mask
            temp = temp>>12
            a = 0b100000000000000000000000
            convertedBin = convertedBin + (temp<<16) + a
            mask = 0b111<<18
            temp = theVal&mask
            temp = temp>>18
            a = 0b11110000000000000000000000000000
            convertedBin = convertedBin + (temp<<24) + a
            numBytes = 4
        if numBytes == 0:
           continue
        else:
            nums[convertedBin] = numBytes
    # print(nums[196607])
    data = None

    # print(0b01101101 in nums)

    with open(inputFile, "rb") as file:
        data = file.read()

    fullList = []
    for numBytes in range(1,5):
        for i in range(0, len(data)-numBytes+1):
            curUTF = 0
            for j in range(0,numBytes):
                curUTF = curUTF + (data[i+(numBytes-j-1)]<<(8*j))
            # print(data[i])
            if curUTF in nums:
                theHex = "0x%x" % i
                theHex = theHex[2:]
                toAdd = 8 - len(theHex)
                finalvalString="0x"
                for p in range(0,toAdd):
                    finalvalString+="0"
                finalvalString +=theHex
                finalvalString = finalvalString.lower()

                # convertedFinal
                theNumBytes = nums[curUTF]
                if theNumBytes == 1:
                    convertedBin = curUTF
                elif theNumBytes == 2:
                    convertedBin = curUTF&0b111111
                    toAdd = (curUTF&(0b11111<<8))>>8
                    toAdd = toAdd<<6
                    convertedBin = (toAdd+convertedBin)
                elif theNumBytes == 3:
                    convertedBin = curUTF&0b111111
                    # print(convertedBin)
                    toAdd = (curUTF&(0b111111<<8))>>8
                    toAdd = toAdd<<6
                    # print(toAdd)
                    convertedBin = (toAdd+convertedBin)
                    toAdd = (curUTF&(0b1111<<16))>>16
                    toAdd = toAdd<<12
                    # print(toAdd)
                    convertedBin = (toAdd+convertedBin)
                elif theNumBytes == 4:
                    convertedBin = curUTF&0b111111
                    toAdd = (curUTF&(0b111111<<8))>>8
                    toAdd = toAdd<<6
                    convertedBin = (toAdd+convertedBin)
                    toAdd = (curUTF&(0b111111<<16))>>16
                    toAdd = toAdd<<12
                    convertedBin = (toAdd+convertedBin)
                    toAdd = (curUTF&(0b111)<<24)>>24
                    toAdd = toAdd<<18
                    convertedBin = (toAdd+convertedBin)
                
                curUTF = convertedBin
                # print(curUTF)
                theUTF = "0x%x" % curUTF
                # print(theUTF)
                theUTF = theUTF[2:]
                toAdd = 4 - len(theUTF)
                finalUTF = "U+"
                if len(theUTF) <= 3:
                    for p in range(0,toAdd):
                        finalUTF += "0"
                finalUTF+=theUTF
                finalUTF = finalUTF.upper()
                #convert curUTF back into codePoint
                #make mask with only chracters u need

                # print(finalvalString)
                fullList.append((str(finalvalString),str(finalUTF)))

    return fullList
# print((utf8_search("hahacopy.txt", "U+20AC")))
# print((utf8_search("hahacopy.txt", "U+00E2")))
# print((utf8_search("hahacopy.txt", "U+0082")))
# print((utf8_search("hahacopy.txt", "U+00AC")))

# curUTF = 49826
# convertedBin = curUTF&0b111111
# toAdd = (curUTF&(0b11111<<8))>>8
# toAdd = toAdd<<6
# convertedBin = (toAdd+convertedBin)
# # print(convertedBin)

# print(utf8_carve("hahacopy.txt"))
