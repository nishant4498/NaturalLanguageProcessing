from __future__ import division
import os
import sys
import json
from collections import defaultdict


train_file_path = str(sys.argv[1])
count=0
sentence_count_in_file=0

## This map gives all the initial state to first tag transition probabilities.
start_tag_count_map={}
## This contains the count of transition bw one tag to another.
tags_transition_count_map={}
## This contains all tags and their count
tags_count_map={}
word_tag_emission_count_map= defaultdict(dict)
q0_start_transition_probablity_map={}
transition_probability_map={}
hmm_model_map = {}
total_tag_list = []
last_tag_count_map = {}

filename='catalan_corpus_train_tagged.txt'
path=os.path.join(train_file_path + filename)


def write_map_to_file(map_name , file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
    with open(file_name,'a+') as fopen:
        json.dump(map_name,fopen,ensure_ascii=False)


with open(path,'r') as fopen:
    for line in fopen:
        word_tag_list=line.split()
        start_word_tag=word_tag_list[0]
        start_tag=start_word_tag[-2:]
        sentence_count_in_file +=1
        for i in range(0,len(word_tag_list)):
            word_tag=word_tag_list[i]
            tag=word_tag[-2:]
            if i == len(word_tag_list)-1:
                if tag not in last_tag_count_map:
                    last_tag_count_map[tag] = 1
                else:
                    last_tag_count_map[tag] += 1
            else:
                if tag not in tags_count_map:
                    tags_count_map[tag] = 1
                else:
                    tags_count_map[tag] += 1
        if start_tag not in start_tag_count_map:
            start_tag_count_map[start_tag] = 1
        else:
            start_tag_count_map[start_tag] += 1

        for i in range(0,len(word_tag_list)-1):
            current_word_tag= word_tag_list[i]
            next_word_tag= word_tag_list[i+1]
            current_word=current_word_tag[0:len(current_word_tag)-3]
            current_tag = current_word_tag[-2:]
            next_tag = next_word_tag[-2:]
            tag_transition_key= current_tag.strip()+'->'+ next_tag.strip()

            if tag_transition_key not in tags_transition_count_map:
                tags_transition_count_map[tag_transition_key] = 1
            else:
                tags_transition_count_map[tag_transition_key] += 1

            if current_word not in word_tag_emission_count_map:
                word_tag_emission_count_map[current_word]={}
                word_tag_emission_count_map[current_word][current_tag]=1
            else:
                temp = word_tag_emission_count_map.get(current_word)
                if current_tag not in temp:
                    word_tag_emission_count_map[current_word][current_tag] = 1
                else:
                    word_tag_emission_count_map[current_word][current_tag]+=1

total_tag_list = tags_count_map.keys()

for tag in total_tag_list:
    for i in range(0,len(total_tag_list)):
        tag_key = tag + "->" + total_tag_list[i]
        if tag_key not in tags_transition_count_map:
            tags_transition_count_map[tag_key] = 0
            #tags_count_map[tag] += 1
        #else:
        #    tags_transition_count_map[tag_key] += 1
        #tags_count_map[tag] += 1

for i in range(0,len(total_tag_list)):
    start_tag_key = total_tag_list[i]
    if start_tag_key not in start_tag_count_map:
        start_tag_count_map[start_tag_key] = 0
    #    tags_count_map[start_tag_key] += 1
    #else:
    #    start_tag_count_map[start_tag_key] += 1

for tag, count in start_tag_count_map.iteritems():
    start_transition_tag ="q->"+ tag
    q0_start_transition_probablity_map[start_transition_tag]=((count + 1)*1.0)/(sentence_count_in_file + len(tags_count_map.keys()))

for tag, count in tags_transition_count_map.iteritems():
    first_tag= tag.split('->')[0]
    transition_probability_map[tag]=((count +1) * 1.0)/(tags_count_map.get(first_tag) + len(tags_count_map.keys()))

for word, tag_count_map in word_tag_emission_count_map.iteritems():
    for tag, tag_count in tag_count_map.iteritems():
        if tag not in last_tag_count_map.keys():
            word_tag_emission_count_map[word][tag]=(tag_count * 1.0)/tags_count_map.get(tag)
        else:
            word_tag_emission_count_map[word][tag]=(tag_count * 1.0)/((tags_count_map.get(tag))+ last_tag_count_map.get(tag))


hmm_model_map['emmision_probability']=word_tag_emission_count_map
hmm_model_map['start_tag_transition_probability']=q0_start_transition_probablity_map
hmm_model_map['transition_probability_map']=transition_probability_map
hmm_model_map['tags_count_map'] = tags_count_map

write_map_to_file(hmm_model_map , "hmmmodel.txt")
