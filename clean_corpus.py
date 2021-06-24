# removes lines above and below the empty lines including the empty lines in each corpus
# removes lines containing only '°', '*' or '.'
# stripping trailing and leading spaces


import sys
import re


def clean_corpus(corpus1, corpus2):

    lines1 = []
    lines2 = []
    lines_to_remove = set()

    with open(corpus1, 'r+') as l1, open(corpus2, 'r+') as l2:
        lines1 = l1.readlines()
        lines2 = l2.readlines()
        assert len(lines1) == len(lines2)
        # print(lines1, lines2)
        for i in range(len(lines1)):
            removal_map = "".maketrans('', '', '°.*')
            if (not lines1[i].translate(removal_map).strip()) != (not lines2[i].translate(removal_map).strip()):
                lines_to_remove.update([i-1, i, i+1])
                continue

            # removing lines only with '°', '*' and '.'
            # if (not lines1[i].replace('°', '').replace('*', '').replace('.', '').strip()) and \
            #         (not lines2[i].replace('°', '').replace('*', '').replace('.', '').strip()):
            #     lines_to_remove.add(i)
            # print(lines1, lines2)
            if (not lines1[i].translate(removal_map).strip()) and \
                    (not lines2[i].translate(removal_map).strip()):
                lines_to_remove.add(i)

        # print(lines_to_remove)

        # l1.seek(0)
        # # l1.write(''.join(lines1))
        # l1.write('')
        l1.truncate(0)

        # l2.seek(0)
        # l2.write('')
        l2.truncate(0)

    with open(corpus1, 'w') as l1, open(corpus2, 'w') as l2:
        lines_to_keep = set()
        lines_to_keep.update([i for i in range(len(lines1))])
        lines_to_keep = lines_to_keep - lines_to_remove

        # also removing leading and trailing spaces
        l1.writelines(
            re.sub(' +', ' ', lines1[i]).strip()+'\n' for i in sorted(lines_to_keep))
        l2.writelines(
            re.sub(' +', ' ', lines2[i]).strip()+'\n' for i in sorted(lines_to_keep))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('usage: clean_corpus.py <corpus 1> <corpus 2>')
        exit(1)
    clean_corpus(sys.argv[1], sys.argv[2])
