from __future__ import division
from lemtag01 import *
import os
import csv
import matplotlib.pyplot as plt
import numpy as np
from sys import stdout

os.chdir("/home/paharov/bursty/sent01/lemma/")

def get_sent_wave(curtext, bagsize):
    blank = ''
    seq = ('/home/paharov/bursty/sent01/waves/', str(curtext),'.csv')

    words = []

    seq2 = (str(curtext), '.csv')
    with open(blank.join(seq2), 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            words.append(', '.join(row))
        
    sents = []

    cursent = []
    for word in words:
        if word == "SENT":
            if cursent != []:
                sents.append(cursent)
                cursent = []
        else:
            if word not in cursent:
                cursent.append(word)

    sent_lens = []

    for sent in sents:
        sent_lens.append(len(sent))

    bags_lens = []

    for i in range(len(sent_lens)//bagsize):
        bag = []
        for j in range(bagsize):
            bag.append(sent_lens[bagsize*i + j])
        bags_lens.append(np.mean(bag))

    return bags_lens

baglist = [1, 2, 4, 8, 16, 32, 64, 128]


files = ['{:03}'.format(x) for x in range(1,101)]

for file in files:
    waves = []

    for i in baglist:
        waves.append(get_sent_wave(file, i))

    # write the output csv        
    with open('/home/paharov/bursty/sent01/waves/' + file +'.csv', "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        for val in waves:
            writer.writerow(val)
    
    plt.figure(figsize=(120,30))

    plt.suptitle('text: ' + file)
    plt.title('Lengths of every 1, 2, 4, 8, 16, 32, 64 and 128 sentences long bags (using means), normalized in the x direction.')

    plt.subplot(8, 1, 1)
    plt.plot(range(len(waves[0])), waves[0])
    plt.ylim()

    for k in [1, 2, 3, 4, 5, 6, 7]:
        plt.subplot(8, 1, k+1)
        plt.plot([i*baglist[k] for i in range(len(waves[k]))], waves[k])

    plt.savefig('/home/paharov/bursty/sent01/waves/' + file + '.png')
    plt.close()

    stdout.write('\r%s done' % file)
    stdout.flush()