# COMPSCI 365
# Spring 2020
# NATHAN NG
# Assignment 3: JPEG Manipulation

# Complete the relevant functions.
# Make sure to test your implementations.
# You can import any standard library.
# You can define any new function you want.

import tags
import struct

def carve_jpeg(inputFile):
    """
    Description: Read the input file and extract ANY/ALL valid
    # sequences of bytes that conform to the JPEG standard.
    # The function should return a list of bytes objects, where each
    # bytes object is the extracted sequence of bytes corresponding
    # to one JPEG file. The ordering of the list does not matter. For
    # example, if l_1 = b'\xff\xd8\xff\xe0\x00\x10\x4a...', then
    # the list returned would be [l_1, l_2, ...]. If there is
    # just one valid JPEG file, then it would be [l_1]. If there are
    # no valid JPEG files, return an empty list.
    Input: string inputFile
    Output: list of bytes objects
    Example 1: carve_jpeg("main.py") = []
    Example 2: carve_jpeg("samples/sample1.jpg") = 
    # [b'\xff\xd8\xff\xe0...\xff\xd9', b'\xff\xd8\xff...\xff\xd9']
    """
    data = None
    with open(inputFile, "rb") as o:
        data = o.read()
    theList = []
    startIndex = -1 
    # for i in range(0,len(data)-1):
    for i in range(0,len(data)-1):
        im = data[i:i+2]
        im = struct.unpack(">H", im)[0]

        
        if im==65496 and startIndex == -1: #remove startIndex== -1 if we ARE supposed to restart every time we encounter a begining of a JPG
            if i+2 < len(data):
                if data[i+2] == 255:
                    startIndex = i
                    # print('here1')
        elif startIndex > -1 and im==65497:
            theList.append(data[startIndex:i+2])
            startIndex = -1
            # print('here2')
    return theList

def parse_exif(inputBytes):
    """
    Description: Given a sequence of bytes inputBytes that is
    # interpreted as a JPEG file, parse through the bytes to find
    # ANY/ALL EXIF segments. For each EXIF segment:
    # 1. Determine its endianness and handle data accordingly.
    # 2. For each IFD, determine the number of entries. Then,
    # for each entry in each IFD:
    #
    # 2.a. Extract the tag and value IF the tag is in tags.TAGS, AND
    ## IF the tag's format is in [1, 2, 3, 4, 5, 7].
    # 2.b. The tag and value should be stored in a tuple (TagName, Value),
    ## noting that if the value has multiple components then store them
    ## in a list (otherwise just as a single variable),
    ## where the value type corresponds for the following formats:
    ## Formats 1, 3, 4: int
    ## Formats 2, 5: str (for Format 5, use "x/y"; for Format 2, strip
    ## the trailing NULL byte)
    ## Format 7: bytes
    ## The tag names can be obtained from tags.TAGS.
    # 2.c. Add the tuple to a list that corresponds to the IFD.
    #
    # 3. Each list of extracted tuples should be stored as a value
    # in a dictionary, where the key is the offset of the IFD starting byte
    # (i.e. the first byte in the two bytes that specify the number of
    # entries that the IFD has) as an integer.
    # 4. Return this dictionary. If there are no entries in a given
    # IFD to extract, use an empty list in the dictionary. If there
    # are no IFDs, then return an empty dictionary.
    Input: bytes object
    Output: dictionary
    Example: parse_exif(carve_jpeg("samples/exif1.jpg")[0]) =
    # { 0x14: [ ("ImageDescription", " " * 31), ("Make", "NIKON"), ... ],
    # 0x1172: [ ("Compression", 6), ("XResolution", "72/1"), ("YResolution", "72/1"), ...],
    # ... }
    """
    # print(inputBytes[1])
    dataFormat = {1:1,2:1,3:2,4:4,5:8,7:1}
    dic = {}
    for i in range(0, len(inputBytes)-6):

        exif = inputBytes[i:i+4]
        exif = struct.unpack(">I", exif)[0]
        pad0 = inputBytes[i+4:i+6]
        pad0 = struct.unpack("H", pad0)[0]
        bigEnd = -1
        begining = -1
        if exif==1165519206 and pad0 == 0:

            hMark = None
            iMark = None

            endianness = inputBytes[i+6:i+8]
            endianness = struct.unpack("H",endianness)[0]
            if endianness == 18761 and struct.unpack(">H", inputBytes[i+8:i+10])[0] == 10752:
                bigEnd = 0
                begining = i+6
                hMark = "<H"
                iMark = "<I"
            elif endianness == 19789 and struct.unpack(">H", inputBytes[i+8:i+10])[0] == 42:
                bigEnd = 1
                begining = i+6
                hMark = ">H"
                iMark = ">I"

            exifStart = inputBytes[i+10:i+14]
            exifStart = struct.unpack(iMark, exifStart)[0] + begining
            offset = exifStart
            curIndex = i+14
            nextSet = 1
            
            while(nextSet != 0):
            # for i in range(0,4):
                curList = []
                toDo = inputBytes[curIndex:curIndex+2]
                toDo = struct.unpack(hMark, toDo)[0]
                curIndex = curIndex+2
                # print(toDo)
                for j in range(0,toDo):
                    curTag = inputBytes[0+curIndex:2+curIndex]
                    curTag = struct.unpack(hMark, curTag)[0]
                    if curTag not in tags.TAGS:
                        # print('here')
                        curIndex += 12
                        continue
                    else:
                        disc = tags.TAGS[curTag]
                    theType = inputBytes[2+curIndex:4+curIndex]
                    theType = struct.unpack(hMark, theType)[0]
                    # print(theType)
                    theCount = inputBytes[4+curIndex:8+curIndex]
                    theCount = struct.unpack(iMark, theCount)[0]
                    blockSize = dataFormat[theType]*theCount
                    if blockSize <= 4:
                        curOff = 8+curIndex
                    else:
                        curOff = inputBytes[8+curIndex:12+curIndex]
                        curOff = struct.unpack(iMark, curOff)[0]
                        curOff = begining+curOff
                    theData = inputBytes[curOff:curOff+blockSize]
                    if theType == 1:
                        theData = struct.unpack("c", theData)[0]
                    elif theType == 3:
                        theData = struct.unpack(hMark, theData)[0]
                        # print(theData,disc)
                    elif theType == 4:
                        theData = struct.unpack(iMark, theData)[0]
                        # print(theData,disc)
                    elif theType == 2:
                        theData = theData.decode("ascii")
                        theData = theData[0:len(theData)-1]
                    elif theType == 5:
                        theData1 = struct.unpack(iMark, theData[0:4])[0]
                        theData2 = struct.unpack(iMark, theData[4:8])[0]
                        theData = (str(theData1) + "/" + str(theData2))
                    curList.append((disc,theData)) #need to trim
                    curIndex += 12
                # print(curIndex)
                nextSet = inputBytes[curIndex:curIndex+4]
                nextSet = struct.unpack(iMark, nextSet)[0]
                # print(nextSet)
                # dic[hex(offset)] = curList
                dic[offset] = curList
                offset = nextSet + begining
                curIndex = nextSet + begining
                # print(dic)


                    

                    

            # print(bigEnd)
    # print(dic)
    return dic
# print(len(carve_jpeg("samples/sample1.jpg")))
# print(carve_jpeg("samples/IMG_6159 2.jpg"))
# print(parse_exif(carve_jpeg("samples/exif1.jpg")[0]))
