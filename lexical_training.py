# lexical training script
import os
from subprocess import Popen, PIPE, call
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
        default = "yes"

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


def training(config, cache_dir, log):
    # file names
    sl_tagged = cache_dir+'/'+config['CORPUS']+'.tagged.'+config['SL']
    tl_tagged = cache_dir+'/'+config['CORPUS']+'.tagged.'+config['TL']
    lines = cache_dir+'/'+config['CORPUS']+'.lines'
    tagged_merged = cache_dir+'/' + \
        config['CORPUS']+'.tagged-merged.'+config['SL']+'-'+config['TL']
    alignment = cache_dir+'/'+config['CORPUS'] + \
        '.align.'+config['SL']+'-'+config['TL']

    with open(config['CORPUS_SL'], 'r') as corpus_sl:
        training_lines = min(config['TRAINING_LINES'],
                             len(corpus_sl.readlines()))

    print('loading', training_lines, 'lines from the corpora')

    # tagging the source side corpus
    cmds = [['head', '-n', str(training_lines)],
            ['apertium', '-d', config['LANG_DATA'],
             config['SL']+'-'+config['TL']+'-tagger'],
            ['sed', 's/ \+/ /g'], ['apertium-pretransfer']]
    with open(config['CORPUS_SL']) as inp, open(sl_tagged, 'w') as outp:
        pipe(cmds, inp, outp, log)

    # c2 = ['apertium-destxt']
    # p2 = Popen(c2, stdin=p1.stdout, stdout=PIPE, stderr=training_log)

    # tagging the target side corpus
    cmds = [['head', '-n', str(training_lines)],
            ['apertium', '-d', config['LANG_DATA'],
             config['TL']+'-'+config['SL']+'-tagger'],
            ['sed', 's/ \+/ /g'], ['apertium-pretransfer']]
    with open(config['CORPUS_TL']) as inp, open(tl_tagged, 'w') as outp:
        pipe(cmds, inp, outp, log).wait()

    # c2 = ['apertium-destxt']
    # p2 = Popen(c2, stdin=p1.stdout, stdout=PIPE, stderr=training_log)

    # removing lines with no analyses
    with open(lines, 'w+') as f0:
        call(['seq', '1', str(training_lines)],
             stdout=f0, stderr=log)
        clean_tagged = cache_dir+'/'+config['CORPUS']+'.clean_tagged'
        with open(clean_tagged, 'w+') as f1:
            cmds = [['paste', lines, sl_tagged, tl_tagged],
                    ['grep', '<*\t*<']]
            pipe(cmds, None, f1, log)

            call(['cut', '-f', '1'], stdin=f1, stdout=f0, stderr=log)

            f1.seek(0)
            with open(sl_tagged, 'w') as f2:
                cmds = [['cut', '-f', '2'], ['sed', 's/ /~/g'],
                        ['sed', 's/\$[^\^]*/$ /g']]
                pipe(cmds, f1, f2, log)

            f1.seek(0)
            with open(tl_tagged, 'w') as f2:
                cmds = [['cut', '-f', '3'], ['sed', 's/ /~/g'],
                        ['sed', 's/\$[^\^]*/$ /g']]
                pipe(cmds, f1, f2, log).wait()

    os.remove(clean_tagged)

    # aligning the parallel corpus
    with open(tagged_merged, 'w+') as f:
        with open(os.devnull, 'r') as f1:
            call(['paste', '-d', '||| ', tl_tagged, '-', '-', '-',
                  sl_tagged], stdin=f1, stdout=f, stderr=log)
        with open(alignment, 'w') as f2:
            call([config['FAST_ALIGN'], '-i', tagged_merged, '-d',
                  '-o', '-v'], stdout=f2, stderr=log)


def main():
    print("validating configuration....")
    config = check_config()

    # cleaning the parallel corpus i.e. removing empty sentences, sentences only with '*', '.', or '°'
    print("cleaning corpus....")
    # clean_corpus(config['CORPUS_SL'], config['CORPUS_TL'])

    cache_dir = "cache-"+config['SL']+"-"+config['TL']
    log = cache_dir+'/'+'training.log'

    # the directory where all the intermediary outputs are stored
    if not os.path.isdir(cache_dir):
        os.mkdir(cache_dir)
    else:
        if not query("Do you want to overwrite the files in "+"'"+cache_dir+"'"):
            print("remove", cache_dir, "and re-run lexical_training.py")
            exit(1)

    if os.path.isfile(log):
        os.remove(log)

    with open(log, 'a') as log_file:
        training(config, cache_dir, log_file)


if __name__ == '__main__':
    main()
