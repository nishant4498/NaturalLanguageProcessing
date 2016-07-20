import sys
import string
import re
import math
import os

path_to_input = sys.argv[1]

positive_words_map = {}
negative_words_map = {}
truthful_words_map = {}
deceptive_words_map = {}
vocabulary_count = 0

positive_count = 0
negative_count = 0
truthful_count = 0
deceptive_count = 0

positive_prob = 0
negative_prob = 0
truthful_prob = 0
deceptive_prob = 0

positive_negative_class = ""
truthful_deceptive_class = ""

filter_keywords = {'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', "arent", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', "cant", 'cannot', 'could', "couldnt", 'did', "didnt", 'do', 'does', "doesnt", 'doing', "dont", 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', "hadnt", 'has', "hasnt", 'have', "havent", 'having', 'he', "hed", "hes", 'her', 'here', "heres", 'hers', 'herself', 'him', 'himself', 'his', 'how', "hows", 'i', "id", "im", "ive", 'if', 'in', 'into', 'is', "isnt", 'it', "its", 'its', 'itself', "lets", 'me', 'more', 'most', "mustnt", 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', "shant", 'she', "shed", "shes", 'should', "shouldnt", 'so', 'some', 'such', 'than', 'that', "thats", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', "theres", 'these', 'they', "theyd", "theyll", "theyre", "theyve", 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', "wasnt", 'we', "we'd", "well", "were", "weve", 'were', "werent", 'what', "whats", 'when', "whens", 'where', "wheres", 'which', 'while', 'who', "whos", 'whom', 'why', "whys", 'with', "wont", 'would', "wouldnt", 'you', "youd", "youll", "youre", "youve", 'your', 'yours', 'yourself', 'yourselves'}

flag = ""
feature_count_map = {}

classification_output_file = open("nboutput.txt" , 'w')

def read_classifier_model_data():
    with open('nbmodel.txt', 'r') as f:
        for line in f:
            if "##POSITIVE##" in line:
                flag = "P"
                continue
            elif "##NEGATIVE##" in line:
                flag = "N"
                continue
            elif "##TRUTHFUL##" in line:
                flag = "T"
                continue
            elif "##DECEPTIVE##" in line:
                flag = "D"
                continue
            elif "UniqueWords:" in line:
                flag = ""
                get_vocabulary_count
            get_word_count(line , flag)



def get_word_count(line , flag):
    count_list = line.strip().split(':')
    word = count_list[0]
    count = int(count_list[1])
    if flag == "P":
        positive_words_map[word] = count
        global positive_count
        positive_count += count
    elif flag == "N":
        negative_words_map[word] = count
        global negative_count
        negative_count += count
    elif flag == "D":
        deceptive_words_map[word] = count
        global deceptive_count
        deceptive_count += count
    elif flag == "T":
        truthful_words_map[word] = count
        global truthful_count
        truthful_count += count

def get_vocabulary_count(line):
    global vocabulary_count
    vocabulary_count = line.strip().split()[1]

def classify_input_files():
    for root, dirs, files in os.walk(path_to_input):
        for file in files:
            if file.endswith(".txt"):
                file_path=os.path.join(root, file)
                classify_file(file_path)
    classification_output_file.close()


def classify_file(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            line = parse_each_line(line)
            classify_each_word_in_line(line)
    global positive_prob
    global negative_prob
    global truthful_prob
    global deceptive_prob
    global positive_negative_class
    global truthful_deceptive_class
    if(positive_prob > negative_prob):
        positive_negative_class = "positive"
    else:
        positive_negative_class = "negative"

    if(truthful_prob > deceptive_prob):
        truthful_deceptive_class = "truthful"
    else:
        truthful_deceptive_class = "deceptive"

    classification_output_file.write(truthful_deceptive_class + " " + positive_negative_class + " " + file_path + "\n")

    positive_prob = 0
    negative_prob = 0
    truthful_prob = 0
    deceptive_prob = 0
    positive_negative_class = ""
    truthful_deceptive_class = ""

def parse_each_line(line):
    parsed_line = re.sub(r'\w*\d\w*', '', line).strip().lower()
    for punct in string.punctuation:
        parsed_line=parsed_line.replace(punct,' ')
    return parsed_line

def classify_each_word_in_line(line):
   for word in line.split():
        if (len(word)>2 and word not in filter_keywords):
            if(word==''):
                continue
            else:
                if positive_words_map.has_key(word):
                    p_count = int(positive_words_map[word]) + 1
                else:
                    p_count = 1
                if negative_words_map.has_key(word):
                    n_count = int(negative_words_map[word]) + 1
                else:
                    n_count = 1
                if truthful_words_map.has_key(word):
                    t_count = int(truthful_words_map[word]) + 1
                else:
                    t_count = 1
                if deceptive_words_map.has_key(word):
                    d_count = int(deceptive_words_map[word]) + 1
                else:
                    d_count = 1

                global positive_prob
                positive_prob += math.log((p_count)/float(positive_count + vocabulary_count))
                global negative_prob
                negative_prob += math.log((n_count)/float(negative_count + vocabulary_count))
                global truthful_prob
                truthful_prob += math.log((t_count)/float(truthful_count + vocabulary_count))
                global deceptive_prob
                deceptive_prob += math.log((d_count)/float(deceptive_count + vocabulary_count))



read_classifier_model_data()
#print str(positive_count) + ":" + str(negative_count) + ":" + str(truthful_count) + ":" + str(deceptive_count)
classify_input_files()