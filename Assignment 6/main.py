import sys
from os import path
import dd

if __name__ == "__main__": # don't remove this line

	args = sys.argv
	inFile = None
	outFile = None
	blockSize = None
	countNum = None
	seek = None
	skip = None
	conv = None
	for arg in args:
		if arg.startswith("if="):
			inFile = arg[3:]
		if arg.startswith("of="):
			outFile = arg[3:]
		if arg.startswith("bs="):
			blockSize = arg[3:]
		if arg.startswith("count="):
			countNum = arg[6:]
		if arg.startswith("seek="):
			seek = arg[5:]
		if arg.startswith("skip="):
			skip = arg[5:]
		if arg.startswith("conv="):
			conv = arg[5:]

	### YOUR LOGIC BELOW ###
	try:
		dd.runDD([inFile,outFile,blockSize,countNum,seek,skip,conv])
	except Exception:
		raise Exception("Problem with a file or input value") from None

	# if path.exists(inFile):
	# 	if not path.isfile(inFile):
	# 		raise Exception("Given path is not a file!")
	# else:
	# 	raise Exception("Given path does not exist!")


	# if args.x:
	# 	print("Extract option specified.")
	# 	if args.n:
	# 		print("n specified; n = %s" % args.n)
	# 	else:
	# 		print("n not specified.")
