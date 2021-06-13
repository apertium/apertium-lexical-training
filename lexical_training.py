# lexical training script
import os
from subprocess import Popen, PIPE, call
from typing import List
from check_config import check_config
from clean_corpus import clean_corpus

def query(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n]"
    elif default == "no":
        prompt = " [y/N]"
    else:
        prompt = " [Y/n]"
        default= "yes"

    while True:
        print(question + prompt+"(default='"+default+"')?")
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            print("Please respond with 'yes', 'no', 'y' or 'n'")
            exit(1)

def main():
    print("validating configuration....")
    config = check_config()

    # cleaning the parallel corpus i.e. removing empty sentences, sentences only with '*', '.', or '°'
    print("cleaning corpus....")
    # clean_corpus(config['CORPUS_SL'], config['CORPUS_TL'])

    # file names
    cache_dir = "cache-"+config['SL']+"-"+config['TL']
    training_log_name = cache_dir+'/'+'training.log'
    sl_tagged = cache_dir+'/'+config['CORPUS']+'.tagged.'+config['SL']
    tl_tagged = cache_dir+'/'+config['CORPUS']+'.tagged.'+config['TL']
    lines = cache_dir+'/'+config['CORPUS']+'.lines'
    tagged_merged = cache_dir+'/'+config['CORPUS']+'.tagged-merged.'+config['SL']+'-'+config['TL']
    alignment = cache_dir+'/'+config['CORPUS']+'.align.'+config['SL']+'-'+config['TL']

    with open(config['CORPUS_SL'], 'r') as corpus_sl:
        training_lines = min(config['TRAINING_LINES'], len(corpus_sl.readlines()))
    
    print('loading', training_lines, 'lines from the corpora')

    # the directory where all the intermediary outputs are stored
    if not os.path.isdir(cache_dir):
        os.mkdir(cache_dir)
    else:
        if not query("Do you want to overwrite the files in "+"'"+cache_dir+"'"):
            print("remove", cache_dir, "and re-run lexical_training.py")
            exit(1)

    if os.path.isfile(training_log_name):
        os.remove(training_log_name)

    training_log = open(training_log_name, 'a')

    # tagging the source side corpus
    c1 = ['head', '-n', str(config['TRAINING_LINES'])]
    with open(config['CORPUS_SL']) as f:
        p1 = Popen(c1, stdin=f, stdout=PIPE, stderr=training_log)

    # c2 = ['apertium-destxt']
    # p2 = Popen(c2, stdin=p1.stdout, stdout=PIPE, stderr=training_log)

    c3 = ['apertium', '-d', config['LANG_DATA'], config['SL']+'-'+config['TL']+'-tagger']
    p3 = Popen(c3, stdin=p1.stdout, stdout=PIPE, stderr=training_log)

    c4 = ['sed', 's/ \+/ /g']
    p4 = Popen(c4, stdin=p3.stdout, stdout=PIPE, stderr=training_log)

    c5 = ['apertium-pretransfer']
    with open(sl_tagged, 'w') as f:
        Popen(c5, stdin=p4.stdout, stdout=f, stderr=training_log)

    # tagging the target side corpus
    c1 = ['head', '-n', str(config['TRAINING_LINES'])]
    with open(config['CORPUS_TL']) as f:
        p1 = Popen(c1, stdin=f, stdout=PIPE, stderr=training_log)

    # c2 = ['apertium-destxt']
    # p2 = Popen(c2, stdin=p1.stdout, stdout=PIPE, stderr=training_log)

    c3 = ['apertium', '-d', config['LANG_DATA'], config['TL']+'-'+config['SL']+'-tagger']
    p3 = Popen(c3, stdin=p1.stdout, stdout=PIPE, stderr=training_log)

    c4 = ['sed', 's/ \+/ /g']
    p4 = Popen(c4, stdin=p3.stdout, stdout=PIPE, stderr=training_log)

    c5 = ['apertium-pretransfer']
    with open(tl_tagged, 'w') as f:
        Popen(c5, stdin=p4.stdout, stdout=f, stderr=training_log).wait()

    # removing lines with no analyses
    with open(lines, 'w+') as f0:
        call(['seq', '1', str(config['TRAINING_LINES'])], stdout=f0, stderr=training_log)
        clean_tagged = cache_dir+'/'+config['CORPUS']+'.clean_tagged'
        with open(clean_tagged, 'w+') as f1:
            p1 = Popen(['paste', lines, sl_tagged, tl_tagged], stdout=PIPE, stderr=training_log)
            Popen(['grep', '<*\t*<'], stdin=p1.stdout, stdout=f1, stderr=training_log).wait()

            call(['cut', '-f', '1'], stdin=f1, stdout=f0, stderr=training_log)

            f1.seek(0)
            with open(sl_tagged, 'w') as f2:
                p1 = Popen(['cut', '-f', '2'], stdin=f1, stdout=PIPE, stderr=training_log)
                p2 = Popen(['sed', 's/ /~/g'], stdin=p1.stdout, stdout=PIPE, stderr=training_log)
                Popen(['sed', 's/\$[^\^]*/$ /g'], stdin=p2.stdout, stdout=f2, stderr=training_log)

            f1.seek(0)
            with open(tl_tagged, 'w') as f2:
                p1 = Popen(['cut', '-f', '3'], stdin=f1, stdout=PIPE, stderr=training_log)
                p2 = Popen(['sed', 's/ /~/g'], stdin=p1.stdout, stdout=PIPE, stderr=training_log)
                Popen(['sed', 's/\$[^\^]*/$ /g'], stdin=p2.stdout, stdout=f2, stderr=training_log).wait()

    os.remove(clean_tagged)

    # aligning the parallel corpus
    with open(tagged_merged, 'w+') as f:
        with open(os.devnull, 'r') as f1:
            call(['paste', '-d', '||| ', tl_tagged, '-', '-', '-', sl_tagged], stdin=f1, stdout=f, stderr=training_log)
        with open(alignment, 'w') as f2:
            call([config['FAST_ALIGN'], '-i', tagged_merged, '-d', '-o', '-v'], stdout=f2, stderr=training_log)

    training_log.close()

if __name__ == '__main__':
    main()


def pipe(cmds, firstin, lastout, stderr):
    """Open a list of commands as a simple shell pipe, using the same stderr
    for all commands.
    Returns None if the command list is empty.
    Example usage:
    >>> cmds = [['yes', 'olleh'], ['head', '-2'], ['rev']]
    >>> with open('/tmp/foo', 'w') as outf:
        p = pipe(cmds, None, outf, sys.stderr)
        retcode = p.wait()
    >>> print(open('/tmp/foo', 'r').read())
    hello
    hello
    """
    if cmds == []:
        return
    procs = []                  # type: List[Popen]
    for i in range(len(cmds)):
        cmd = cmds[i]
        inp = procs[i-1].stdout if i > 0 else firstin
        outp = PIPE if i+1 < len(cmds) else lastout
        procs.append(Popen(cmd, stdin=inp, stdout=outp, stderr=stderr))
    return procs[-1]
