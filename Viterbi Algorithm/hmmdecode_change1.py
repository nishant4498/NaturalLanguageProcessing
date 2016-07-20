from __future__ import division
from collections import defaultdict
import math
import sys
import os
import operator
import json

train_file_path = str(sys.argv[1])
dev_file_name='catalan_corpus_dev_raw_copy.txt'
path=os.path.join(train_file_path,dev_file_name)

word_tag_emission_count_map = defaultdict(dict)
q0_start_transition_probablity_map = {}
transition_probability_map = {}
total_tag_list=[]

def read_model_data_from_file(file_name):
    with open(file_name,'r') as input_model_data:
        model_dictionary = eval(input_model_data.read())
        global q0_start_transition_probablity_map
        q0_start_transition_probablity_map = model_dictionary.get('start_tag_transition_probability')
        global transition_probability_map
        transition_probability_map = model_dictionary.get('transition_probability_map')
        global word_tag_emission_count_map
        word_tag_emission_count_map = model_dictionary.get('emmision_probability')
        global total_tag_list
        total_tag_list = model_dictionary.get("tags_count_map").keys()

def write_map_to_file(map_name , file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
    with open(file_name,'a+') as fopen:
        json.dump(map_name,fopen,ensure_ascii=False)

read_model_data_from_file('hmmmodel.txt')
last_transition_map={}
with open(train_file_path,'r') as fopen:
    for line in fopen:
        viterbi_map=defaultdict(dict)
        last_transition_map={}
        previous_word_tags=[]
        tagged_sentence_output = []
        word_list=line.strip().split()
        for i in range(0,len(word_list)):
            if word_list[i] in word_tag_emission_count_map:
                tag_cnt_map={}
                tag_cnt_map=word_tag_emission_count_map.get(word_list[i])
                if i == 0:
                    for tag, prob in tag_cnt_map.iteritems():
                        tag_transition_key = 'q->'+tag
                        previous_word_tags.append(tag)
                        transition_probability = q0_start_transition_probablity_map.get(tag_transition_key)
                        emission_probability = prob
                        viterbi_map[i+ 1][tag_transition_key] = math.log(transition_probability) + math.log(emission_probability)
                else:
                    tag_appended_string=''
                    for tag, prob in tag_cnt_map.iteritems():
                        for previous_tag in previous_word_tags:
                            tag_transition_key = previous_tag +'->'+ tag
                            if tag not in tag_appended_string:
                                tag_appended_string = tag_appended_string + tag + ' '
                            last_transition_map = viterbi_map.get(i)
                            max_prob = -10000000
                            max_prob_transition_key = ""
                            for tag_tran_key, prob1 in last_transition_map.iteritems():
                                if previous_tag == tag_tran_key.split('->')[1]:
                                    transition_probability = transition_probability_map.get(tag_transition_key)
                                    emission_probability = prob
                                    total_prob = math.log(transition_probability) + math.log(emission_probability) + prob1
                                    if(max_prob < total_prob):
                                        max_prob = total_prob
                                        max_prob_transition_key = previous_tag + "->" + tag
                            viterbi_map[i+1][max_prob_transition_key] = max_prob
                    previous_word_tags = []
                    tag_appended_string = tag_appended_string.strip()
                    previous_word_tags = tag_appended_string.split(' ')
            else:
                max_prob = -10000000
                max_prob_transition_key = ""
                if i==0:
                    prev_tag = "q"
                    for tag in total_tag_list:
                        next_trans_key = prev_tag + "->" + tag
                        previous_word_tags.append(tag)
                        next_trans_prob = math.log(q0_start_transition_probablity_map[next_trans_key])
                        viterbi_map[i+ 1][next_trans_key] = next_trans_prob#math.log(transition_probability) + math.log(emission_probability)
                        #if(max_prob < next_trans_prob):
                        #    max_prob = next_trans_prob
                        #    max_prob_transition_key = next_trans_key
                else:
                    last_transition_map = viterbi_map.get(i)
                    for tag_tran_key, prob1 in last_transition_map.iteritems():
                        prev_tag = tag_tran_key.split('->')[1]
                        for tag in total_tag_list:
                            next_trans_key = prev_tag + "->" + tag
                            next_trans_prob = math.log(transition_probability_map[next_trans_key]) + prob1
                            if(max_prob < next_trans_prob):
                                max_prob = next_trans_prob
                                max_prob_transition_key = next_trans_key

                    viterbi_map[i+1][max_prob_transition_key] = max_prob
                    previous_word_tags = []
                    previous_word_tags.append(max_prob_transition_key.split("->")[1])

        for i in range(len(word_list),0,-1):
            tag_transitions_for_word = viterbi_map.get(i)
            if i == len(word_list):
                max_tag_path = max(tag_transitions_for_word.iteritems(), key=operator.itemgetter(1))[0]
                current_tag = max_tag_path.split('->')[1]
                previous_tag = max_tag_path.split('->')[0]
                last_word_tag = word_list[i-1]+'/' + current_tag
                tagged_sentence_output.append(last_word_tag)
            else:
                max_prob = -10000000
                output_tag = ''
                for tag_transtn_key, prob in tag_transitions_for_word.iteritems():
                    if previous_tag in tag_transtn_key.split('->')[1]:
                        if( max_prob < prob ):
                            max_prob = prob
                            output_tag = tag_transtn_key
                current_word_tag = word_list[i-1]+'/'+ output_tag.split('->')[1]
                tagged_sentence_output.append(current_word_tag)
                previous_tag = output_tag.split('->')[0]


        with open("hmmoutput.txt",'a+') as fileopen:
            for i in range(0,len(tagged_sentence_output)):
                word_tagged=tagged_sentence_output[len(tagged_sentence_output)-i-1]
                fileopen.write(word_tagged+' ')
            fileopen.seek(-1, os.SEEK_END)
            fileopen.truncate()
            fileopen.write('\n')