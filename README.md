This repository is a Hidden Markov Model part-of-speech tagger for English and Chinese. The training data is tokenized and tagged; the test data is tokenized, and this tagger will add the tags.

## **Data Description**

Two files (one English, one Chinese) with tagged training data in the word/TAG format, with words separated by spaces and each sentence on a new line. "en_train_tagged.txt" is English tagged training data and "zh_train_tagged.txt" is Chinese tagged training data. 

Two files (one English, one Chinese) with untagged development data, with words separated by spaces and each sentence on a new line. "en_dev_raw.txt" is English untagged development data and "zh_dev_raw.txt" is Chinese untagged development data. 

Two files (one English, one Chinese) with tagged development data in the word/TAG format, with words separated by spaces and each sentence on a new line, to determine the accuracy of the Part-of-Speech Tagger. "en_dev_tagged.txt" is English tagged development data and "zh_dev_tagged.txt" is Chinese tagged development data. 

## **Code Description**

hmmlearn3.py is learning a hidden Markov model from the training data, and hmmdecode3.py is using the model to tag new data.

hmmlearn3.py - This program learns a hidden Markov model, and write the model parameters to a file called hmmmodel.txt.

hmmdecode3.py - This program reads the parameters of a hidden Markov model from the file hmmmodel.txt, tag each word in the test data, and write the results to a text file called hmmoutput.txt.
