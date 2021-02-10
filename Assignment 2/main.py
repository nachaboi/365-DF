import argparse
import dumper
import carver
from os import path

if __name__ == "__main__":

    p = argparse.ArgumentParser()
    p.add_argument("file", type=str, help="name/path of the input file")
    p.add_argument("-c", action="store_true", help="carve file for UTF-8 characters")
    p.add_argument("-d", action="store_true", help="dump hex view of file")
    p.add_argument("-s", help="search for first occurrence of code point")
    args = p.parse_args()

    if path.exists(args.file):
        if not path.isfile(args.file):
            raise Exception("Given path is not a file!")
    else:
        raise Exception("Given path does not exist!")

    if args.d:
        print(dumper.hex_dump(args.file))

    if args.s and args.s.startswith("U+") and len(args.s) <= 8:
        print(carver.utf8_search(args.file, args.s))

    if args.c:
        print(carver.utf8_carve(args.file))
