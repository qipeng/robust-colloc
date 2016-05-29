import sys

if len(sys.argv) < 3:
    print "Usage: %s <input_gz_file> <output_txt_file>" % (sys.argv[1])
    sys.exit(0)

import nltk
import nltk.data
from nltk.tokenize.punkt import PunktLanguageVars
import gzip

sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
punktlv = PunktLanguageVars()

input_file = sys.argv[1]
output_file = open(sys.argv[2], 'w')

def process_sent(s):
    s = " ".join(punktlv.word_tokenize(s))
    idx = len(s)-1
    while idx > 0 and s[idx] in ['.', ' ', '"']:
        idx -= 1

    s = s[:(idx+1)] + " " + s[(idx+1):]
    return s

counter = 0
with gzip.open(input_file, 'r') as f:
    in_paragraph = False
    for line in f:
        line = line.strip()
        if line == "<P>":
            in_paragraph = True
            current_paragraph = []
        elif line == "</P>":
            in_paragraph = False
            current_paragraph = " ".join(current_paragraph).decode('utf-8')
            current_paragraph = [s for s in sent_detector.tokenize(current_paragraph)]
            current_paragraph = [process_sent(s) for s in current_paragraph]
            output_file.write("%s " % ((" ".join(current_paragraph)).encode('utf-8')))
            counter += 1
            if counter % 1000 == 0:
                print "%d paragraphs processed" % (counter)
        elif in_paragraph:
            current_paragraph += [line]

print "Done. %d paragraphs processed in total" % (counter)
