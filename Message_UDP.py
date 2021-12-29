import struct 

Magic_Cookie = 0xabcddcba
Message_Type = 0x2
Encoding_Format = 'IBH'


def pack_message(port):
    return struct.pack(Encoding_Format,Magic_Cookie,Message_Type,port)


def unpack_message(message):
    try:
        unpacked_message = struct.unpack(Encoding_Format,message)
        if unpacked_message[0] == Magic_Cookie and unpacked_message[1] == Message_Type: return unpacked_message[2]
        return None
    except struct.error as error: 
        print("error occured in Message_UDP: "+str(error))
        return None


