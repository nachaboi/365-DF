# COMPSCI 365
# Spring 2020
# NATHAN NG
# Assignment 3: WAV Manipulation

# Complete the relevant functions.
# Make sure to test your implementations.
# You can import any standard library.
# You can define any new function you want.

# WARNING: As you work through parsing
# the WAV standard, keep the endianness
# of each field in the file header in mind.

import struct

def carve_wav(inputFile):
    """
    Description: Read the input file and extract ANY/ALL valid
    # sequences of bytes that conform to the WAV standard. Assume
    # that all WAV file headers will only have three chunks: the
    # RIFF chunk, the fmt chunk (the basic style, not a variant),
    # and the data chunk. That is, the WAV file will be a
    # 44-byte header followed by the audio data. Also assume that
    # all WAV files will follow the WAVE PCM format category (0x0001).
    # The function should return a list of bytes objects, where each
    # bytes object is the extracted sequence of bytes corresponding
    # to one WAV file. The ordering of the list does not matter. For
    # example, if l_1 = b'\x52\x49\x46\x46\x71\xaf\x00\x00...', then
    # the list returned would be [l_1, l_2, ...]. If there is
    # just one valid WAV file, then it would be [l_1]. If there are
    # no valid WAV files, return an empty list.
    Input: string inputFile
    Output: list of bytes objects
    Example 1: carve_wav("main.py") = []
    Example 2: carve_wav("samples/sample1.jpg") = 
    # [bytes([82, 73, 70, 70, 240, 4, 2, 0, 87, 65, 86, ...])]
    """
    # struct.pack()
    # struct.unpack(">", subdata[0:4])
    # struct.calcsize()
    data = None
    with open(inputFile, "rb") as o:
        data = o.read()
    theList = []
    startIndex = -1 
    for i in range(0,len(data)-43):
        chunkID = data[i:i+4]
        chunkID = struct.unpack(">I", chunkID)[0]
        if chunkID==1380533830:
            if startIndex > -1:
                theList.append(data[startIndex:i])
            forMat = data[i+8:i+12]
            forMat = struct.unpack(">I", forMat)[0]
            subChunkID = data[i+12:i+16]
            subChunkID = struct.unpack(">I", subChunkID)[0]
            subChunk2ID = data[i+36:i+40]
            subChunk2ID = struct.unpack(">I", subChunk2ID)[0]
            if forMat==1463899717 and subChunkID==1718449184 and subChunk2ID==1684108385:
                startIndex = i
    theList.append(data[startIndex:len(data)])
    return theList


def parse_wav_header(inputBytes):
    """
    Description: Given a sequence of bytes inputBytes that is
    # interpreted as a WAV file, parse the header and return
    # the extracted fields. These fields should be returned
    # in a dictionary, where each key is the field name, and
    # the corresponding value is the value found in the WAV
    # header. The values should be parsed according to the
    # WAV standard, and then stored in the dictionary
    # according to the format specified in wav_format.txt. If
    # a field is not included in wav_format.txt, then do not
    # include it in your returned dictionary.
    # If a field cannot be parsed properly, set the corresponding
    # dictionary value to None. If all fields cannot be parsed,
    # such as due to the bytes not being a valid sequence of
    # WAV bytes, or empty bytes object, return None.
    Input: bytes object
    Output: dictionary or None
    Example: parse_wav_header(carve_wav("samples/sample1.jpg")[0]) =
    # {'nChannels': 1, 'samplesPerSecond': 22050, ...}
    """

    # 'nChannels' : int,
    # 'samplesPerSecond' : int,
    # 'averageBytesPerSecond' : int,
    # 'blockAlignment' : int,
    # 'bitsPerSample' : int,
    # 'dataSizeBytes' : int
    dic = {}
    dic['nChannels'] = None
    dic['samplesPerSecond'] = None
    dic['averageBytesPerSecond'] = None
    dic['blockAlignment'] = None
    dic['bitsPerSample'] = None
    dic['dataSizeBytes'] = None

    nChannels = inputBytes[22:24]
    nChannels = struct.unpack("<h", nChannels)[0]
    samplesPerSecond = inputBytes[24:28]
    samplesPerSecond = struct.unpack("<I", samplesPerSecond)[0]
    averageBytesPerSecond = inputBytes[28:32]
    averageBytesPerSecond = struct.unpack("<I", averageBytesPerSecond)[0]
    blockAlignment = inputBytes[32:34]
    blockAlignment = struct.unpack("<h", blockAlignment)[0]
    bitsPerSample = inputBytes[34:36]
    bitsPerSample = struct.unpack("<h", bitsPerSample)[0]
    dataSizeBytes = inputBytes[40:44]
    dataSizeBytes = struct.unpack("<I", dataSizeBytes)[0]
    one = 0
    if nChannels != 0:
        dic['nChannels'] = nChannels
        one += 1
    if samplesPerSecond != 0:
        dic['samplesPerSecond'] = samplesPerSecond
        one += 1
    if averageBytesPerSecond != 0:
        dic['averageBytesPerSecond'] = averageBytesPerSecond
        one += 1
    if blockAlignment != 0:
        dic['blockAlignment'] = blockAlignment
        one += 1
    if bitsPerSample != 0:
        dic['bitsPerSample'] = bitsPerSample
        one += 1
    if dataSizeBytes == len(inputBytes[44:len(inputBytes)]):
        dic['dataSizeBytes'] = dataSizeBytes
        one += 1
    if one > 0:
        return dic
    else:
        return None

def pack_wav(audioBytes, fields):
	toReturn = bytearray()
	chunkID = 1380533830
	chunkID = struct.pack(">I", chunkID)
	toReturn += chunkID

	chunkSize = 36 + len(audioBytes)
	chunkSize = struct.pack("<I", chunkSize)
	toReturn += chunkSize

	theFormat = 1463899717
	theFormat = struct.pack(">I", theFormat)
	toReturn += theFormat

	subChunk1ID = 1718449184
	subChunk1ID = struct.pack(">I", subChunk1ID)
	toReturn += subChunk1ID

	subChunk1Size = 16
	subChunk1Size = struct.pack("<I", subChunk1Size)
	toReturn += subChunk1Size

	audioFormat = 1
	audioFormat = struct.pack("<H", audioFormat)
	toReturn += audioFormat

	numChannels = fields[0]
	numChannels = struct.pack("<H", numChannels)
	toReturn += numChannels

	sampleRate = fields[1]
	sampleRate = struct.pack("<I", sampleRate)
	toReturn += sampleRate

	byteRate = fields[1] * fields[0] * fields[4] / 8
	byteRate = int(byteRate)
	byteRate = struct.pack("<I", byteRate)
	toReturn += byteRate

	blockAlign = fields[3]
	blockAlign = struct.pack("<H", blockAlign)
	toReturn += blockAlign

	bitsPerSample = fields[4]
	bitsPerSample = struct.pack("<H", bitsPerSample)
	toReturn += bitsPerSample

	subChunk2ID = 1684108385
	subChunk2ID = struct.pack(">I", subChunk2ID)
	toReturn += subChunk2ID

	subChunk2Size = len(audioBytes)
	subChunk2Size = struct.pack("<I", subChunk2Size)
	toReturn += subChunk2Size

	toReturn += audioBytes
	toReturn = bytes(toReturn)
	return toReturn

# print(pack_wav(carve_wav("samples/sample1.jpg")[0], (2,2,2,2,2)))


# carve_wav("samples/sample1.jpg")
# print(parse_wav_header(carve_wav("samples/cantina.wav")[0]))
