import sys

anagram_list = []
def swap_character(char_list,left,right):
    temp = char_list[left]
    char_list[left] = char_list[right]
    char_list[right] = temp
    return char_list

def convert_list_to_string(char_list):
    return ''.join(char_list)

def find_anagram(char_list, left, right):
    if left==right:
        anagram_list.append(convert_list_to_string(char_list))
    else:
        for index in range(left,right+1):
            char_list = swap_character(char_list,left,index)
            find_anagram(char_list, left+1, right)
            char_list = swap_character(char_list,left,index)

input_string = sys.argv[1]
find_anagram(list(input_string) , 0 , len(input_string)-1)
output_file = open("anagram_out.txt",'w')
sorted_list = sorted(anagram_list)
for i in range(0,len(sorted_list)):
    output_file.write(convert_list_to_string(sorted_list[i]))
    output_file.write('\n')

