import sys
import math
import time
import json
start_time = time.time()

model_file = open('hmmmodel.txt', 'r')
modelResult = json.load(model_file)
word_tag_dict= modelResult['EmmissionProb']
tag_tag_dict=modelResult['TranistionProb']
tags_dict= modelResult['TagCounts']
start='<s>'
end='<e>'
target = open('hmmoutput.txt', 'w',encoding="UTF-8")

def decode():
    for sent in open("en_dev_raw.txt", encoding="UTF-8"):
        sent = start + ' ' + sent + ' ' + end  # Adding start and end tags to each sentence in the file
        sentence = sent.split()
        sentlen = len(sentence)
        viterbi = []      # viterbi is list of dictionaries in which alpha value is stored for each word's every tag (including start for which it is assigned as 1)
        backpointer = []  # backpointer is list of dictionaries in which backpointer is stored for each word's every tag (except start)

        viterbi.append({start:0})   #appending a dictionary with start tag and probability value as 1
        backpointer.append({start : None})      #appending a dictionary to the backpointer already created as a list

        for i in range(1,sentlen):
            viterbi.append({})  # creating a dictionary in corresponding list (the list contains the words)
            if sentence[i] in word_tag_dict.keys():  # checking if word is present in word_tag_dictionary
                backpointer.append({})
                for curr_tag in word_tag_dict[sentence[i]].keys(): #iterating over all the tags of corresponding word in word_tag_dictionary


                    best_prev_key= None #initializing best previous key as viterbi's list (i-1)st element's(dictionary) containing first tag in it as best_prev_key
                    max_alpha= -99999  # initializing max alpha value as 0
                    for prev_key in viterbi[i-1].keys():  #iterating over possible tags of previous (i-1)st element of viterbi list

                        alpha= (viterbi[i-1][prev_key]) + math.log((tag_tag_dict[prev_key].get(curr_tag, 0)+1)) - math.log((tags_dict[prev_key] + len(tags_dict.keys()))) + math.log((word_tag_dict[sentence[i]][curr_tag]/tags_dict[curr_tag]))

                        # Above line ((i-1)st element every previous_key's value is taken  * transition probability of prev_key to curr_tag * emission probability of sentence[i](word) to curr_tag)

                        if alpha>= max_alpha:
                            max_alpha = alpha # updating alpha value if there is an increment in alpha in subsequent tags in max_alpha
                            best_prev_key = prev_key #updating best_prev_key value if there is an increment in alpha in subsequent keys in list's (i-1)st element

                        viterbi[i][curr_tag]=alpha # Assigning alpha to value of word's tag of viterbi list
                        backpointer[i][curr_tag]=best_prev_key

            else:
                backpointer.append({})
                for curr_tag in tags_dict.keys(): #iterating over all tags in tag_dictionary keys so that all can be put in that particular word's dictionary
                    best_prev_key = None  # initializing best previous key as viterbi's list (i-1)st element's(dictionary) containing first tag in it as best_prev_key
                    max_alpha = -99999  # initializing max alpha value as 0
                    for prev_key in viterbi[i-1].keys():  #iterating over possible tags of previous (i-1)st element of viterbi list
                        alpha= ((viterbi[i-1][prev_key])) + math.log(((tag_tag_dict[prev_key].get(curr_tag, 0) + 1))) - math.log((tags_dict[prev_key] + len(tags_dict.keys()))) + math.log((1))
                        # Above line ((i-1)st element every previous_key's value is taken * transition probability of prev_key to curr_tag * emission probability is 1 for each new inserted tag)
                        if alpha >= max_alpha:
                            max_alpha = alpha  # updating alpha value if there is an increment in alpha in subsequent tags in max_alpha
                            best_prev_key = prev_key #updating best_prev_key value if there is an increment in alpha in subsequent keys in list's (i-1)st element


                        viterbi[i][curr_tag]=alpha # Assigning alpha to value of word's tag of viterbi list
                        backpointer[i][curr_tag]=best_prev_key


        best_tagsequence = []
        backpointer.reverse()
        current_best_key = end
        del backpointer[len(backpointer) - 1]

        for bp in backpointer:
            best_tagsequence.append(bp[current_best_key])
            current_best_key = bp[current_best_key]

        del best_tagsequence[len(best_tagsequence) - 1]


        best_tagsequence.reverse()
        sentence.pop(0)  # popping the start element from the sentence list

        count = 1
        for w, t in zip(sentence, best_tagsequence):
            if count < (len(sentence)-1):   # count is run from position 0 till before end tag
                target.write(w+"/"+t+" ")
                count += 1
            else:
                target.write(w+"/"+t)
        target.write("\n")



if __name__ == "__main__":
    decode()
