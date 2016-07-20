import sys
import string
import os
import re

path_to_input = sys.argv[1]
path_to_negative_deceptive = path_to_input + "/negative_polarity/deceptive_from_MTurk/"
path_to_negative_truthful = path_to_input + "/negative_polarity/truthful_from_Web/"
path_to_positive_deceptive = path_to_input + "/positive_polarity/deceptive_from_MTurk/"
path_to_positive_truthful = path_to_input + "/positive_polarity/truthful_from_TripAdvisor/"

positive_words_map = {}
negative_words_map = {}
truthful_words_map = {}
deceptive_words_map = {}
vocabulary = []
output_file = open('nbmodel.txt','w')
##

filter_keywords = {'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', "arent", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', "cant", 'cannot', 'could', "couldnt", 'did', "didnt", 'do', 'does', "doesnt", 'doing', "dont", 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', "hadnt", 'has', "hasnt", 'have', "havent", 'having', 'he', "hed", "hes", 'her', 'here', "heres", 'hers', 'herself', 'him', 'himself', 'his', 'how', "hows", 'i', "id", "im", "ive", 'if', 'in', 'into', 'is', "isnt", 'it', "its", 'its', 'itself', "lets", 'me', 'more', 'most', "mustnt", 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', "shant", 'she', "shed", "shes", 'should', "shouldnt", 'so', 'some', 'such', 'than', 'that', "thats", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', "theres", 'these', 'they', "theyd", "theyll", "theyre", "theyve", 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', "wasnt", 'we', "we'd", "well", "were", "weve", 'were', "werent", 'what', "whats", 'when', "whens", 'where', "wheres", 'which', 'while', 'who', "whos", 'whom', 'why', "whys", 'with', "wont", 'would', "wouldnt", 'you', "youd", "youll", "youre", "youve", 'your', 'yours', 'yourself', 'yourselves'}

def get_dir_listing(file_list ,dir):
    dir_list = os.listdir(dir)
    for i in xrange(0,len(dir_list)):
        if "fold" in dir_list[i]:
            for dir_entry in os.listdir(dir + dir_list[i]):
                file_list.append(dir + dir_list[i] + '/' + dir_entry)

def populate_positive_map():
    file_path_list = []
    get_dir_listing(file_path_list, path_to_positive_deceptive)
    get_dir_listing(file_path_list , path_to_positive_truthful)
    for i in xrange(0,len(file_path_list)):
        count_words_in_file(file_path_list[i],positive_words_map)
    write_map_to_file(positive_words_map,"##POSITIVE##")

def populate_negative_map():
    file_path_list = []
    get_dir_listing(file_path_list, path_to_negative_deceptive)
    get_dir_listing(file_path_list , path_to_negative_truthful)
    for i in xrange(0,len(file_path_list)):
        count_words_in_file(file_path_list[i],negative_words_map)
    write_map_to_file(negative_words_map,"##NEGATIVE##")

def populate_deceptive_map():
    file_path_list = []
    get_dir_listing(file_path_list , path_to_positive_deceptive)
    get_dir_listing(file_path_list, path_to_negative_deceptive)
    for i in xrange(0,len(file_path_list)):
        count_words_in_file(file_path_list[i],deceptive_words_map)
    write_map_to_file(deceptive_words_map,"##DECEPTIVE##")

def populate_truthful_map():
    file_path_list = []
    get_dir_listing(file_path_list, path_to_positive_truthful)
    get_dir_listing(file_path_list , path_to_negative_truthful)
    for i in xrange(0,len(file_path_list)):
        count_words_in_file(file_path_list[i],truthful_words_map)
    write_map_to_file(truthful_words_map,"##TRUTHFUL##")

def count_words_in_file(file_name,word_count_map):
    with open(file_name, 'r') as f:
        for line in f:
            line = parse_each_line(line)
            count_words_in_line(line,word_count_map)

def parse_each_line(line):
    parsed_line = re.sub(r'\w*\d\w*', '', line).strip().lower()
    for punct in string.punctuation:
        parsed_line=parsed_line.replace(punct,' ')
    return parsed_line

def count_words_in_line(line,word_count_map):
   for word in line.split():
        if (len(word)>2 and word not in filter_keywords):
            if(word==''):
                continue
            else:
                if word not in word_count_map:
                    word_count_map[word] = 1
                else:
                    word_count_map[word] += 1
                if word not in vocabulary:
                    vocabulary.append(word)


def write_map_to_file(word_count_map , map_class_name):
    output_file.write(map_class_name+":"+str(len(word_count_map))+'\n')
    for word,count in word_count_map.items():
        output_file.write(""+word+""+':'+str(count)+'\n')


populate_positive_map()
populate_negative_map()
populate_truthful_map()
populate_deceptive_map()

output_file.write("UniqueWords:" + str(len(vocabulary)))
output_file.close()




