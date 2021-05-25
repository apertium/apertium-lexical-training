# removes lines above and below the empty lines including the empty lines in each corpus
# removes lines containing only ° and *
# stripping trailing and leading spaces


import sys


def main(argc, argv):
    if argc != 3:
        print('usage: clean_corpus.py <corpus 1> <corpus 2>')
        exit(-1)

    lines1 = []
    lines2 = []
    lines_to_remove = set()

    with open(argv[1], 'r+') as l1, open(argv[2], 'r+') as l2:
        lines1 = l1.readlines()
        lines2 = l2.readlines()
        assert len(lines1) == len(lines2)
        # print(lines1, lines2)
        i = 0
        for i in range(len(lines1)):
            # if not(lines1[i].strip()) and not(lines2[i].strip()):
            #     continue
                # if i > 0:
                #     if i < len(lines1)-1:
                #         del lines1[i-1], lines2[i-1]
                #         del lines1[i-1], lines2[i-1]
                #         del lines1[i-1], lines2[i-1]
                #     else:
                #         del lines1[i-1], lines2[i-1]
                #         del lines1[i-1], lines2[i-1]
                # else:
                #     if i < len(lines1)-1:
                #         del lines1[i], lines2[i]
                #         del lines1[i], lines2[i]
                #     else:
                #         del lines1[i], lines2[i]
            if (not lines1[i].strip()) or (not lines2[i].strip()):
                lines_to_remove.update([i-1, i, i+1])
                continue
            
            # removing lines only with '°' and '*'
            if (not lines1[i].replace('°', ' ').replace('*', ' ').strip()) and (not lines2[i].replace('°', ' ').replace('*', ' ').strip()):
                lines_to_remove.add(i)
            # print(lines1, lines2)

        # assert len(lines1) == len(lines2)

        # if len(lines1) == 0:
        #     l1.seek(0)
        #     l1.write('\n')
        #     l1.truncate()

        #     l2.seek(0)
        #     l2.write('\n')
        #     l2.truncate()

        #     l1.close()
        #     l2.close()
        #     return

        # if '\n' not in lines1[len(lines1)-1]:
        #     lines1[len(lines1)-1] = lines1[len(lines1)-1] + '\n'
        # if '\n' not in lines2[len(lines2)-1]:
        #     lines2[len(lines2)-1] = lines2[len(lines2)-1] + '\n'

        print(lines_to_remove)

        l1.seek(0)
        # l1.write(''.join(lines1))
        l1.write('')
        l1.truncate()

        l2.seek(0)
        l2.write('')
        l2.truncate()

    with open(argv[1], 'a') as l1, open(argv[2], 'a') as l2:
        lines_to_keep = set()
        lines_to_keep.update([i for i in range(len(lines1))])
        lines_to_keep = lines_to_keep - lines_to_remove
        
        for i in sorted(lines_to_keep):
            # also removing leading and trailing spaces
            l1.write(lines1[i].strip() + '\n')
            l2.write(lines2[i].strip() + '\n')
        
        l1.truncate()
        l2.truncate()

if __name__ == '__main__':
    main(len(sys.argv), sys.argv)