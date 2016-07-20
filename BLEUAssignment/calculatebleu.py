import sys
import math
import os

candidate_sentences = [] ## This contains all the sentences in the file
reference_translation_list = [] ## This is the list of all the reference translations for the candidate file
N = 4 ## n-gram baseline size

candidate_path = sys.argv[1]
reference_path =  sys.argv[2]

### These variables determine the length on n-grams in the whole set of candidates
candidate_one_grams = 0
candidate_two_grams = 0
candidate_three_grams = 0
candidate_four_grams = 0

unigram_clipped_count = 0
two_gram_clipped_count = 0
three_gram_clipped_count = 0
four_gram_clipped_count = 0
c = 0
r = 0

def is_dir(path):
    return os.path.isdir(path)

def populate_candidate_sentences():
    global candidate_sentences
    with open(candidate_path , "r") as candidate_file:
        candidate_sentences = candidate_file.read().splitlines()

def populate_reference_translation_list():
    global reference_translation_list
    if(is_dir(reference_path)):
        ref_files = [os.path.join(reference_path,file_name) for file_name in next(os.walk(reference_path))[2]]
        for file_path in ref_files:
            with open(file_path , "r") as ref_file:
                ref_lines = ref_file.read().splitlines()
                reference_translation_list.append(ref_lines)
    else:
        with open(reference_path , "r") as reference_file:
            ref_lines = reference_file.read().splitlines()
            reference_translation_list.append(ref_lines)

def get_max_refrence_count(feature,refrence_map,refrence_list):
    max_count = 0
    for sentence in refrence_list:
        if feature in refrence_map[sentence].keys():
            if (refrence_map[sentence][feature] > max_count):
                max_count = refrence_map[sentence][feature]
    return max_count

def compute_unigram_clipped_count(candidate , refrence_list):
    clipped_count = 0
    cand_grams = candidate.strip().split()
    global candidate_one_grams
    candidate_one_grams += len(cand_grams)
    cand_grams_map = {}
    for feature in cand_grams:
        if feature in cand_grams_map:
            cand_grams_map[feature] = cand_grams_map[feature] + 1
        else:
            cand_grams_map[feature] = 1
    rfrnc_grams_map = {}
    for sntnc in refrence_list:
        rfrnc_grams = sntnc.strip().split()
        rfrnc_grams_map[sntnc] = {}
        for feature in rfrnc_grams:
            if feature in rfrnc_grams_map[sntnc]:
                rfrnc_grams_map[sntnc][feature] = rfrnc_grams_map[sntnc][feature] + 1
            else:
                rfrnc_grams_map[sntnc][feature] = 1
    #print cand_grams_map
    for feature,count in cand_grams_map.iteritems():
        clipped_count += min(count,get_max_refrence_count(feature , rfrnc_grams_map , refrence_list))
    return clipped_count


def compute_bigram_clipped_count(candidate , refrence_list):
    clipped_count = 0
    cand_grams = candidate.strip().split()
    if (len(cand_grams) < 2):
        return clipped_count
    global candidate_two_grams
    candidate_two_grams += len(cand_grams) - 1
    cand_grams_map = {}
    for i in range(0,len(cand_grams)-1):
        feature = str(cand_grams[i:i+2])
        if feature in cand_grams_map:
            cand_grams_map[feature] = cand_grams_map[feature] + 1
        else:
            cand_grams_map[feature] = 1

    rfrnc_grams_map = {}
    for sntnc in refrence_list:
        rfrnc_grams = sntnc.strip().split()
        rfrnc_grams_map[sntnc] = {}
        for i in range(0,len(rfrnc_grams)-1):
            feature = str(rfrnc_grams[i:i+2])
            if feature in rfrnc_grams_map[sntnc]:
                rfrnc_grams_map[sntnc][feature] = rfrnc_grams_map[sntnc][feature] + 1
            else:
                rfrnc_grams_map[sntnc][feature] = 1
    for feature,count in cand_grams_map.iteritems():
        clipped_count += min(count,get_max_refrence_count(feature , rfrnc_grams_map , refrence_list))
    return clipped_count

def compute_trigram_clipped_count(candidate , refrence_list):
    clipped_count = 0
    cand_grams = candidate.strip().split()
    if (len(cand_grams) < 3):
        return clipped_count
    global candidate_three_grams
    candidate_three_grams += len(cand_grams) - 2
    cand_grams_map = {}
    for i in range(0,len(cand_grams)-2):
        feature = str(cand_grams[i:i+3])
        if feature in cand_grams_map:
            cand_grams_map[feature] = cand_grams_map[feature] + 1
        else:
            cand_grams_map[feature] = 1

    rfrnc_grams_map = {}
    for sntnc in refrence_list:
        rfrnc_grams = sntnc.strip().split()
        rfrnc_grams_map[sntnc] = {}
        for i in range(0,len(rfrnc_grams)-2):
            feature = str(rfrnc_grams[i:i+3])
            if feature in rfrnc_grams_map[sntnc]:
                rfrnc_grams_map[sntnc][feature] = rfrnc_grams_map[sntnc][feature] + 1
            else:
                rfrnc_grams_map[sntnc][feature] = 1
    for feature,count in cand_grams_map.iteritems():
        clipped_count += min(count,get_max_refrence_count(feature , rfrnc_grams_map , refrence_list))
    return clipped_count

def compute_quadgram_clipped_count(candidate , refrence_list):
    clipped_count = 0
    cand_grams = candidate.strip().split()
    if (len(cand_grams) < 4):
        return clipped_count
    global candidate_four_grams
    candidate_four_grams += len(cand_grams) - 3
    cand_grams_map = {}
    for i in range(0,len(cand_grams)-3):
        feature = str(cand_grams[i:i+4])
        if feature in cand_grams_map:
            cand_grams_map[feature] = cand_grams_map[feature] + 1
        else:
            cand_grams_map[feature] = 1

    rfrnc_grams_map = {}
    for sntnc in refrence_list:
        rfrnc_grams = sntnc.strip().split()
        rfrnc_grams_map[sntnc] = {}
        for i in range(0,len(rfrnc_grams)-3):
            feature = str(rfrnc_grams[i:i+4])
            if feature in rfrnc_grams_map[sntnc]:
                rfrnc_grams_map[sntnc][feature] = rfrnc_grams_map[sntnc][feature] + 1
            else:
                rfrnc_grams_map[sntnc][feature] = 1
    for feature,count in cand_grams_map.iteritems():
        clipped_count += min(count,get_max_refrence_count(feature , rfrnc_grams_map , refrence_list))
    return clipped_count

def compute_brevity_penalty_parameters(candidate_sentence,sentence_reference_list):
    cand_len = len(candidate_sentence.strip().split())
    min_diff = 1000
    best_match_len = len(sentence_reference_list[0].strip().split(" "))
    for sntnc in sentence_reference_list:
        rfrnc_len = len(sntnc.strip().split())
        diff = abs(cand_len - rfrnc_len)
        if(diff < min_diff):
            min_diff = diff
            best_match_len = rfrnc_len
    global c
    c += cand_len
    global r
    r += best_match_len



def calc_brevity_penalty():
    if c > r:
        return 1
    else:
        return math.pow(math.e , 1 - (r*1.0)/c)

def calc_bleu_score():
    BP = calc_brevity_penalty()
    print unigram_clipped_count
    print two_gram_clipped_count
    print three_gram_clipped_count
    print four_gram_clipped_count
    print ((two_gram_clipped_count*1.0)/(candidate_two_grams)*1.0)
    print ((three_gram_clipped_count*1.0)/(candidate_three_grams)*1.0)
    print ((four_gram_clipped_count*1.0)/(candidate_four_grams)*1.0)
    p1 = 0.25*math.log((unigram_clipped_count*1.0)/(candidate_one_grams)*1.0)
    p2 = 0.25*math.log((two_gram_clipped_count*1.0)/(candidate_two_grams)*1.0)
    p3 = 0.25*math.log((three_gram_clipped_count*1.0)/(candidate_three_grams)*1.0)
    p4 = 0.25*math.log((four_gram_clipped_count*1.0)/(candidate_four_grams)*1.0)
    print p1
    print p2
    print p3
    print p4

    bleu = BP * math.exp( p1 + p2 + p3 + p4)
    return bleu

def write_output_to_file(score):
    file_name = "bleu_out.txt"
    if os.path.exists(file_name):
        os.remove(file_name)
    with open(file_name,'a+') as fileopen:
        fileopen.write(score)

populate_candidate_sentences()
populate_reference_translation_list()


for sentence_num in range(0,len(candidate_sentences)):
    candidate_sentence = candidate_sentences[sentence_num]
    sentence_reference_list = []
    for refr_list in reference_translation_list:
        sentence_reference_list.append(refr_list[sentence_num])
    unigram_clipped_count += compute_unigram_clipped_count(candidate_sentence , sentence_reference_list)
    print unigram_clipped_count
    two_gram_clipped_count += compute_bigram_clipped_count(candidate_sentence , sentence_reference_list)
    three_gram_clipped_count += compute_trigram_clipped_count(candidate_sentence , sentence_reference_list)
    four_gram_clipped_count += compute_quadgram_clipped_count(candidate_sentence , sentence_reference_list)
    compute_brevity_penalty_parameters(candidate_sentence,sentence_reference_list)

bleu_score = calc_bleu_score()
print bleu_score
#write_output_to_file(str(bleu_score))