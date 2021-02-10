def runDD(theVars):
	inFile = theVars[0]
	outFile = theVars[1]
	blockSize = theVars[2]
	countNum = theVars[3]
	seek = theVars[4]
	skip = theVars[5]
	conv = theVars[6]

	suffixFull = {"c":1,"w":2,"b":512,"kB":1000,"K":1024,"MB":1000*1000,"M":1024*1024,"xM":1024*1024,"GB":1000**3,
	"G":1024**3,"TB":1000**4,"T":1024**4,"PB":1000**5,"P":1024**5,"EB":1000**6,"E":1024**6,"ZB":1000**7,"Z":1024**7,"YB":1000**8,"Y":1024**8}
	suffix1 = {"c":1,"w":2,"b":512,"K":1024,"M":1024*1024,"G":1024**3,"T":1024**4,"P":1024**5,"E":1024**6,"Z":1024**7,"Y":1024**8}
	suffix2 = {"kB":1000,"MB":1000*1000,"xM":1024*1024,"GB":1000**3,"TB":1000**4,"PB":1000**5,"EB":1000**6,"ZB":1000**7,"YB":1000**8}

	countBlocks = None
	seekBlocks = None
	skipBlocks = None

	if blockSize == None:
		blockSize = 512
	elif str(blockSize)[-2:] in suffix2:
		blockSize = float(str(blockSize)[:-2]) * suffix2[str(blockSize)[-2:]]
	elif str(blockSize)[-1:] in suffix1:
		blockSize = float(str(blockSize)[:-1]) * suffix1[str(blockSize)[-1:]]
	blockSize = int(blockSize)
	if countNum != None:
		if str(countNum)[-2:] in suffix2:
			countNum = float(str(countNum)[:-2]) * suffix2[str(countNum)[-2:]]
		elif str(countNum)[-1:] in suffix1:
			countNum = float(str(countNum)[:-1]) * suffix1[str(countNum)[-1:]]
		countNum = int(countNum)
		countBlocks = countNum * blockSize
	if seek != None:
		if str(seek)[-2:] in suffix2:
			seek = float(str(seek)[:-2]) * suffix2[str(seek)[-2:]]
		elif str(seek)[-1:] in suffix1:
			seek = float(str(seek)[:-1]) * suffix1[str(seek)[-1:]]
		seek = int(seek)
		seekBlocks = seek * blockSize
	else:
		seek = 0
		seekBlocks = 0
	if skip != None:
		if str(skip)[-2:] in suffix2:
			skip = float(str(skip)[:-2]) * suffix2[str(skip)[-2:]]
		elif str(skip)[-1:] in suffix1:
			skip = float(str(skip)[:-1]) * suffix1[str(skip)[-1:]]
		skip = int(skip)
		skipBlocks = skip * blockSize
	else:
		skip = 0
		skipBlocks = 0

	lookAt = None
	if countBlocks == None:
		lookAt = open(inFile, "rb").read()[skipBlocks:]
	else:
		lookAt = open(inFile, "rb").read()[skipBlocks:countBlocks+skipBlocks]

	toWrite = lookAt
	
	lcArr = bytearray()
	ucArr = bytearray()
	spArr = b''

	if conv == "lcase":
		for i in lookAt:
			cur = i
			if cur >= 65 and cur <= 90:
				temp = chr(cur)
				lowered = temp.lower()
				cur = ord(lowered)
			lcArr.append(cur)
		toWrite = lcArr

	
	elif conv == "ucase":
		for i in lookAt:
			cur = i
			if cur >= 97 and cur <= 122:
				temp = chr(cur)
				uppered = temp.upper()
				cur = ord(uppered)
			ucArr.append(cur)
		toWrite = ucArr


	elif conv == "sparse":
		endRange = int((len(lookAt)/blockSize) + 1)

		perf = (len(lookAt) % blockSize)

		for i in range(0,endRange):
			for j in range(0,blockSize):
				try:
					if lookAt[(i*blockSize)+j] != 0:
						spArr += (lookAt[i*blockSize:(i*blockSize)+blockSize])
						break
				except:
					break
		toWrite = spArr

	toOutput = None
	endFile = bytearray()
	written = 0
	try:
		toOutput = open(outFile, "rb").read()
		for i in range(0,seekBlocks):
			endFile.append(toOutput[i])
			written += 1
	except:
		pass


	f = open(outFile,"wb+")
	f.write(endFile)
	f.write(bytearray(seekBlocks-written))
	f.write(toWrite)
	f.close()



