import sys

if len(sys.argv) < 4:
    print "Usage: %s <txt_file> <ind_file> <mapping_file>" % sys.argv[0]
    sys.exit(0)

ind = 0
mapping = dict()
invmapping = []

outfile = open(sys.argv[2], 'w')
with open(sys.argv[1], 'r') as f:
    for line in f:
        line = line.strip().split()
        line_out = []
        for w in line:
            if w in mapping:
                line_out += [mapping[w]]
            else:
                ind += 1
                mapping[w] = ind
                invmapping += [w]
                line_out += [ind]

        outfile.write('%s\n' % ('\n'.join([str(x) for x in line_out])))

outfile.close()

with open(sys.argv[3], 'w') as f:
    for i, w in enumerate(invmapping):
        f.write('%d %s\n' % (i + 1, w))
