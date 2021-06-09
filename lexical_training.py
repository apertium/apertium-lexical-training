# lexical training script
import os
from check_config import check_config
from clean_corpus import clean_corpus

def main():
    print("validating configuration....")
    config = check_config()

    # cleaning the parallel corpus i.e. removing empty sentences, sentences only with '*', '.', or '°'
    print("cleaning corpus....")
    clean_corpus(config['CORPUS_SL'], config['CORPUS_TL'])

    with open(config['CORPUS_SL'], 'r') as corpus_sl:
        training_lines = min(config['TRAINING_LINES'], len(corpus_sl.readlines()))
    
    print('loading', training_lines, 'lines from the corpora')

    # the directory where all the intermediary outputs are stored
    cache_dir = "cache-"+config['SL']+"-"+config['TL']
    os.mkdir(cache_dir)

if __name__ == '__main__':
    main()