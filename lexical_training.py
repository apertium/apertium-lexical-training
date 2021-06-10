# lexical training script
import os
from subprocess import Popen, PIPE
from check_config import check_config
from clean_corpus import clean_corpus

def main():
    print("validating configuration....")
    config = check_config()

    # cleaning the parallel corpus i.e. removing empty sentences, sentences only with '*', '.', or '°'
    print("cleaning corpus....")
    # clean_corpus(config['CORPUS_SL'], config['CORPUS_TL'])

    with open(config['CORPUS_SL'], 'r') as corpus_sl:
        training_lines = min(config['TRAINING_LINES'], len(corpus_sl.readlines()))
    
    print('loading', training_lines, 'lines from the corpora')

    # the directory where all the intermediary outputs are stored
    cache_dir = "cache-"+config['SL']+"-"+config['TL']
    if not os.path.isdir(cache_dir):
        os.mkdir(cache_dir)

    training_log_name = cache_dir+'/'+'training.log'
    if os.path.isdir(training_log_name):
        os.remove(training_log_name)

    training_log = open(training_log_name, 'a')

    # tagging the source side corpus
    c1 = ['head', '-n', str(config['TRAINING_LINES'])]
    with open(config['CORPUS_SL']) as f:
        p1 = Popen(c1, stdin=f, stdout=PIPE, stderr=training_log)

    c2 = ['apertium-destxt']
    p2 = Popen(c2, stdin=p1.stdout, stdout=PIPE, stderr=training_log)

    c3 = ['apertium', '-d', config['LANG_DATA'], config['SL']+'-'+config['TL']+'-tagger']
    p3 = Popen(c3, stdin=p2.stdout, stdout=PIPE, stderr=training_log)

    c4 = ['apertium-pretransfer']
    sl_tagged = cache_dir+'/'+config['CORPUS']+'.tagged.'+config['SL']
    with open(sl_tagged, 'w') as f:
        Popen(c4, stdin=p3.stdout, stdout=f, stderr=training_log)

    # tagging the target side corpus
    c1 = ['head', '-n', str(config['TRAINING_LINES'])]
    with open(config['CORPUS_TL']) as f:
        p1 = Popen(c1, stdin=f, stdout=PIPE, stderr=training_log)

    c2 = ['apertium-destxt']
    p2 = Popen(c2, stdin=p1.stdout, stdout=PIPE, stderr=training_log)

    c3 = ['apertium', '-d', config['LANG_DATA'], config['TL']+'-'+config['SL']+'-tagger']
    p3 = Popen(c3, stdin=p2.stdout, stdout=PIPE, stderr=training_log)

    c4 = ['apertium-pretransfer']
    tl_tagged = cache_dir+'/'+config['CORPUS']+'.tagged.'+config['TL']
    with open(tl_tagged, 'w') as f:
        Popen(c4, stdin=p3.stdout, stdout=f, stderr=training_log).wait()

    training_log.close()

if __name__ == '__main__':
    main()