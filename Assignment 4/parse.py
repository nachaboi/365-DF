# COMPSCI 365
# Spring 2020
# NATHAN NG
# Assignment 4: Extraction from Network Traffic

# Complete the relevant functions.
# Make sure to test your implementations.
# You can import any standard library.
# You can define any new function you want.

import struct

def extract_passwords(inputFile, N=6):
    """
    Description: Read the given input file and extract valid
    ASCII strings that are at least N characters in length and
    contain no spaces (0x20) from any TCP data segments in the
    packet capture.

    Resources:
    - https://wiki.wireshark.org/Development/LibpcapFileFormat#Packet_Data
    - http://www.deic.uab.es/material/25977-ethernet.pdf
    - https://en.wikipedia.org/wiki/EtherType
    - https://en.wikipedia.org/wiki/IPv4#Header
    - https://en.wikipedia.org/wiki/IPv6_packet#Fixed_header
    - https://en.wikipedia.org/wiki/List_of_IP_protocol_numbers
    - https://www.freesoft.org/CIE/Course/Section4/8.htm

    1. The input file will be a packet capture in the libpcap format.
    2. The first 24 bytes will correspond to the PCAP Global Header.
    3.a. The remainder of the bytes will contain packets, segmented
    into packet headers and packet data.
    3.b. Each of these packets will be of the structure:

    PCAP Packet Header (16 bytes)
    OSI Layer 2 - Ethernet Header (14 bytes)
    OSI Layer 3 - IPv4 Header (20 to 60 bytes) OR IPv6 Header (40 bytes)
    OSI Layer 4 - Protocol Header and Data (variable length)

    4. If the protocol extracted from the IP Header is the TCP
    protocol, then read the data offset from the TCP header. If
    the data offset does not go out of bounds of the packet, then
    the TCP packet has data. Extract this data and keep it in a
    running ByteArray object that contains all data you extract. NOTE
    that the data offset is from the start of the TCP header.

    5. After you've extracted all TCP data from the packet capture,
    parse the bytes to extract any and all ASCII-printable strings
    that are >= N characters in length and contain no spaces (0x20).
    Keep these strings in an "extracted passwords" list. Note that
    these strings can be split across multiple TCP packets.

    6. Return this list, or an empty list if you could extract
    no strings.

    It is guaranteed that the Data Link Type (in Global Header) will
    always be Ethernet (0x1) (i.e. Layer 2 will always be Ethernet)
    and the Layer 3 protocol will always be IPv4 or IPv6 (i.e. the
    EtherType in the Ethernet header always 0x0800 or 0x86DD). There
    are no other guarantees.

    Input: string inputFile, int N
    Output: list of strings

    Example 1: extract_passwords("samples/capture1.pcap", N=6) returns:
    Extracted Passwords: ['&&4gk+K`&6', 'RP3jf_', ']B7<nb', 'etcfoS', 'N`t|x!', 'joanclarke', 'p)TE~o', '*a_`(yOh']

    Example 2: extract_passwords("samples/capture2.pcap", N=6) returns:
    Extracted Passwords: ['>ukSo1', '07.N&R', 'y,;!,{}N', "Nw>4<]'", 'A9ka]{', "27*Cru'", 'gracehopper']
    """
    if N == 0:
        N == 1

    data = None
    with open(inputFile, "rb") as o:
        data = o.read()
    im = data[37:41]
    # print(data[40:41])
    i=24
    im = data[i+12:i+14]
    im = struct.unpack(">H", im)[0]
    # print(im)
    # print(data[52:54])

    # print(im)

    # print(data[54:56])
    #assume we have a valid packet found
    collected = bytearray()
    first = 0
    for i in range(0, len(data)-2):

        if struct.unpack(">H", data[i:i+2])[0] == 2048:
            if struct.unpack("B", data[i+11:i+12])[0] == 6:
                ihl = (struct.unpack("B", data[i+2:i+3])[0] -64) * 4
                # print(ihl)
                # print(struct.unpack("B", data[i+34:i+35])[0]/16 + 70)
                # print("crycry")
                # print(struct.unpack("<I", data[i-16:i-12])[0])
                # print(struct.unpack("B", data[i+34:i+35])[0])
                offsetFromBegining = int(struct.unpack("B", data[i+34:i+35])[0]/16) * 4 +30 + ihl
                lengthOfPacket = struct.unpack("<I", data[i-20:i-16])[0]
                # print(int(struct.unpack("B", data[i+34:i+35])[0]/16) * 4)
                # print(lengthOfPacket)
                # print(i+46)
                # print(offsetFromBegining < lengthOfPacket)
                # return
                # if first == 0:
                #     first += 1
                #     print(data[i+42:i+lengthOfPacket-12])
                # elif first == 1:
                #     first += 1
                #     print(data[i+42:i+lengthOfPacket-12])
                # elif first == 2:
                #     first += 1
                #     print(data[i+42:i+lengthOfPacket-12])
                #     return
                # print('beg')
                # print(offsetFromBegining + (i))
                # print(i+42)
                # print(offsetFromBegining)
                # print(lengthOfPacket)
                if offsetFromBegining < lengthOfPacket:
                    # collected += (data[i+46:lengthOfPacket-24+i])
                    # print('here')
                    # collected += data[i+42:i+lengthOfPacket-12]
                    beginingIndex = i - 12 - 16
                    collected += data[beginingIndex + offsetFromBegining:beginingIndex + lengthOfPacket + 16]
        elif struct.unpack(">H", data[i:i+2])[0] == 34525:
            if struct.unpack("B", data[i+8:i+9])[0] == 6:
                # print(data[i+54:i+55])
                offsetFromBegining = int(struct.unpack("B", data[i+54:i+55])[0]/16) * 4 + 70
                # offsetFromBegining = int(struct.unpack("B", data[i+54:i+55])[0]/16 + 70)
                lengthOfPacket = struct.unpack("<I", data[i-16:i-12])[0]
                # print(int(struct.unpack("B", data[i+54:i+55])[0]/16))
                # print(lengthOfPacket)
                # print(offsetFromBegining)
                # print(lengthOfPacket)
                if offsetFromBegining < lengthOfPacket:
                    # print('here')
                    # print(data[i+74:i+lengthOfPacket-13])
                    # collected += (data[i+46:lengthOfPacket-24+i])
                    beginingIndex = i - 12 - 16
                    # collected += data[i+74:i+lengthOfPacket-13]
                    collected += data[beginingIndex + offsetFromBegining:beginingIndex + lengthOfPacket + 16]
                # print(data[i+54:i+55])
                # struct.unpack("B", )
    # print(collected[0:4])
    # print(collected)
    theStrings = []
    curString = ""
    # print(collected)
    for i in collected:
        if i > 32 and i < 128:
            curString += chr(i)
        elif len(curString) > 0:
            if len(curString) >= N:
                theStrings.append(curString)
            curString = ""
    # print(theStrings)
    # print(theStrings)
    # print(theStrings)
    return theStrings

                    
            # print('ah')
    # print(data[54:55])

# extract_passwords("samples/capture2.pcap", N=0)

















