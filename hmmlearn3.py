import sys
import math
import time
import json
start_time = time.time()


word_tag_dict={}  # word to tag dictionary
tag_tag_dict={}   # tag to tag dictionary
tags_dict={}       # Dictionary to count number of times each tag is occuring
words_dict={}     # Dictionary to count number of times each word is occuring


def main(word_tag_dict, tag_tag_dict, tags_dict, words_dict):
    start = "<s>"  # start state given a s
    end= "<e>"
    tag_tag_dict[end]={}
    file = open("en_train_tagged.txt",encoding="UTF-8").read().strip().splitlines()

    for line in file:
        #reading each line in training file
        line = start + '/' + start + ' ' + line + ' ' + end + '/' + end
        symbols=line.split(" ")   # splitting each word by space and symbol is the token (word/tag) in each line read in the corpus
        prevtag = start
        #prevword = start

        for symbol in symbols:
            # print (symbol)
            word= symbol.rsplit('/',1)[0]
            #print (word)
            tag= symbol.rsplit ('/',1)[1]
            #print (tag)

            if word in words_dict:
                words_dict[word] += 1        # Incrementing count of corresponding word in word dictionary
            else:
                words_dict[word] = 1     # Putting that word in word dictionary
            # print (words_dict[word])

            if tag in tags_dict:
                tags_dict[tag] += 1      # Incrementing count of corresponding tag in tag dictionary
            else:
                tags_dict[tag] = 1    # Putting that tag in tag dictionary
            # print(tags_dict[tag])



            if word in word_tag_dict:
                if tag in word_tag_dict[word]:
                    word_tag_dict[word][tag] += 1
                else:
                    word_tag_dict[word][tag]=1
            else:
                word_tag_dict[word]={}
                word_tag_dict[word][tag]=1
            # print(word_tag_dict[word])


            nexttag=tag
            if prevtag in tag_tag_dict:
                if nexttag in tag_tag_dict[prevtag]:
                    tag_tag_dict[prevtag][nexttag] += 1  # next tag is the nested tag in tag to tag dictionary
                else:
                    tag_tag_dict[prevtag][nexttag]=1
            else:
                tag_tag_dict[prevtag]={}
                tag_tag_dict[prevtag][nexttag]=1

            prevtag=nexttag




    return word_tag_dict, tag_tag_dict, tags_dict, words_dict

def output():
    output = open('hmmmodel.txt', 'w')   # Writing all contents to file
    result = dict()
    result['TranistionProb'] = tag_tag_dict
    result['EmmissionProb'] = word_tag_dict
    result['TagCounts'] = tags_dict
    json.dump(result,output)
    output.close()
    # try:
    #     output.write(str(word_tag_dict))
    #     output.write("\n \n")
    #     output.write(str(tag_tag_dict))
    #     output.write("\n \n")
    #     output.write(str(tags_dict))
    #     output.write("\n \n")
    #     # output.write(str(words_dict))
    #     # output.write("\n \n")
    #
    # finally:
    #     output.close()

if __name__=="__main__":
    word_tag_dict, tag_tag_dict, tags_dict, words_dict = main(word_tag_dict, tag_tag_dict, tags_dict, words_dict)
    # print(tags_dict)
    nooftags = len(tags_dict)  # counting number of tags in corpus
    # print(nooftags)
    noofwords = len(words_dict)  # counting number of words in corpus
    output()

