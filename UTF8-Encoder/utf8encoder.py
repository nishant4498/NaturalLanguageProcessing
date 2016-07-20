import sys
import math
#filename = 'F:\workspace\python\NLP\Assignment1\english_in.txt' #sys.argv[1]
filename = sys.argv[1]

def convert_byte_string_to_binary(byte_string):
     binary_format=''.join((bin(ord(c))[2:].zfill(8) for c in byte_string))
     return binary_format

def convert_byte_string_to_decimal(byte_string):
    decimal_number = int("".join(map(lambda x: '%02x' % ord(x), byte_string)),16)
    return decimal_number

def get_utf8_representation_from_utf16_binary_string(my_binary_list):
    num = convert_byte_string_to_decimal(utf_16_byte)
    if num >= 0 and num <= 127:
        utf8_binary_list = [0,-1,-1,-1,-1,-1,-1,-1]
    elif num >= 128 and num <= 2047:
        utf8_binary_list = [1,1,0,-1,-1,-1,-1,-1,1,0,-1,-1,-1,-1,-1,-1]
    else:
        utf8_binary_list = [1,1,1,0,-1,-1,-1,-1,1,0,-1,-1,-1,-1,-1,-1,1,0,-1,-1,-1,-1,-1,-1]

    length = len(my_binary_list)-1
    len_utf8 = len(utf8_binary_list)
    for i in range(len_utf8 -1, -1 , -1):
        if utf8_binary_list[i] == -1:
            utf8_binary_list[i] = my_binary_list[length]
            length -= 1

    for i in range(0,len(utf8_binary_list)-1):
        if utf8_binary_list[i] == -1:
            utf8_binary_list[i] = 0

    return utf8_binary_list

def convert_binary_list_to_string(binary_list):
    binary_string =''.join(str(s) for s in binary_list)
    return binary_string

input_file = open(filename,'rb')
output_file = open("utf8encoder_out.txt","w")


while 1:
        utf_16_byte = input_file.read(2)
        if not utf_16_byte:
            break
        binary_value = convert_byte_string_to_binary(utf_16_byte)
        utf8_binary = get_utf8_representation_from_utf16_binary_string(binary_value)
        utf8_length = len(utf8_binary)
        utf8_byte1 =[]
        utf8_byte2 =[]
        utf8_byte3 =[]

        if(utf8_length==8):
            output_file.write(chr(int(convert_binary_list_to_string(utf8_binary),2)))
        elif(utf8_length==16):
            for i in range(0,8):
                utf8_byte1.append(utf8_binary[i])
                utf8_byte2.append(utf8_binary[i+8])
            output_file.write(chr(int(convert_binary_list_to_string(utf8_byte1),2))+chr(int(convert_binary_list_to_string(utf8_byte2),2)))

        elif(utf8_length==24):
            for i in range(0,8):
                utf8_byte1.append(utf8_binary[i])
                utf8_byte2.append(utf8_binary[i+8])
                utf8_byte3.append(utf8_binary[i+16])
            output_file.write(chr(int(convert_binary_list_to_string(utf8_byte1),2))+chr(int(convert_binary_list_to_string(utf8_byte2),2))+chr(int(convert_binary_list_to_string(utf8_byte3),2)))