import itertools
import pprint
f2=open("hmmoutput.txt","r")
f3=open("F:\workspace\python\NLP\Assignment5\hw6-dev-train\catalan_corpus_dev_tagged.txt","r")
err_count=0
err_list = []
for i in range(3983):
    line2 = f2.readline()
    line3 = f3.readline()
    my_words=line2.split()
    op_words=line3.split()
    for my_word,op_word in itertools.izip(my_words,op_words):
        my_word_tag = my_word[-2:]
        op_word_tag = op_word[-2:]
        if(my_word_tag!=op_word_tag):
            err_count += 1
            err_str = "my tag: "+my_word+ " " + "correct tag: " + op_word
            err_list.append(err_str)
print err_count
#pprint.pprint(err_list)
f2.close()
f3.close()