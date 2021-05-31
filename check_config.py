# parses the config, check if the tools are present

from tomlkit import parse, dumps
import os

# urls of the required tools and data
corpora_url = "https://wiki.apertium.org/wiki/Corpora"
lex_tools_url = "https://wiki.apertium.org/wiki/Install_Apertium_core_by_compiling"
fast_align_url = "https://github.com/clab/fast_align"
langs_url = "https://wiki.apertium.org/wiki/List_of_language_pairs"
apertium_url = "https://wiki.apertium.org/wiki/Installation"
yasmet_url = "https://wiki.apertium.org/wiki/Using_weights_for_ambiguous_rules"

def check_config(filename='config.toml'):
    misconfigured = False
    with open(filename) as config_file:
        config_toml = config_file.read()
        config = parse(config_toml)

    # gives error if not parsed well
    assert config_toml == dumps(config)

    # changing the paths to absolute
    for key in ['CORPUS_SL', 'CORPUS_TL', 'LEX_TOOLS', 'FAST_ALIGN', 'LANG_DATA']:
        if not os.path.isabs(config[key]):
            config[key] = os.path.join(os.path.abspath('.'), config[key])

    if not os.path.isfile(config['CORPUS_SL']):
        print("'"+config['CORPUS_SL']+"'(CORPUS_SL)","is not a file, provide a valid"+ \
                    " file or \nto download, look", corpora_url, '\n')
        misconfigured = True

    if not os.path.isfile(config['CORPUS_TL']):
        print("'"+config['CORPUS_TL']+"'(CORPUS_TL)", "is not a file, provide a valid "+ \
                    "file or \nto download, look", corpora_url, '\n')
        misconfigured = True

    if not os.path.isdir(config['LEX_TOOLS']):
        print("'"+config['LEX_TOOLS']+"'(LEX_TOOLS)", "is not a directory, provide a valid "+ \
                    "directory or \nto install, follow", lex_tools_url, '\n')
        misconfigured = True
    else:
        # scripts = ['process-tagger-output', 'extract-sentences.py', 'extract-freq-lexicon.py', \
        #                 'ngram-count-patterns-maxent2.py', 'merge-ngrams-lambdas.py', 'lambdas-to-rules.py', \
        #                     'ngrams-to-rules-me.py']

        # for script in scripts:

        # assuming scripts are intact
        if 'process-tagger-output' not in os.listdir(config['LEX_TOOLS']):
            print("'process-tagger-output' is not in", "'"+config['LEX_TOOLS']+"'(LEX_TOOLS),", \
                        "provide a valid directory or \nto install, follow", lex_tools_url, '\n')
            misconfigured = True

    if not os.path.isdir(config['FAST_ALIGN']):
        print("'"+config['FAST_ALIGN']+"'(FAST_ALIGN)", "is not a directory, provide"+ \
                    " a valid directory or \nto install, follow", fast_align_url, '\n')
        misconfigured = True
    else:
        if 'fast_align' not in os.listdir(config['FAST_ALIGN']):
            print("fast_align is not present in", "'"+config['FAST_ALIGN']+"'(FAST_ALIGN),", \
                            "provide a valid directory or \nto install, follow", fast_align_url, '\n')
            misconfigured = True
    
    if not os.path.isdir(config['LANG_DATA']):
        print("'"+config['LANG_DATA']+"'(LANG_DATA)", "is not a directory, provide a valid "+ \
                    "directory or \nto install, follow", langs_url, '\n')
        misconfigured = True
    else:
        sl_tl_autobil = config['SL'] + '-' + config['TL'] + '.autobil.bin'
        tl_sl_autobil = config['TL'] + '-' + config['SL'] + '.autobil.bin'
        if sl_tl_autobil not in os.listdir(config['LANG_DATA']):
            print("'"+sl_tl_autobil+"'", "is not in", "'"+config['LANG_DATA']+ "'(LANG_DATA),", \
                        "provide a valid directory or \nto install, follow", langs_url, '\n')
            misconfigured = True
        if tl_sl_autobil not in os.listdir(config['LANG_DATA']):
            print("'"+tl_sl_autobil+"'", "is not in", "'"+config['LANG_DATA']+ "'(LANG_DATA),", \
                        "provide a valid directory or \nto install, follow", langs_url, '\n')
            misconfigured = True

    apertium_present = False
    for path in os.environ["PATH"].split(os.pathsep):
        if os.path.isfile(os.path.join(path, 'apertium')):
            apertium_present = True
            break

    if not apertium_present:
        print("apertium is either not installed or not added to path, see", apertium_url, '\n')
        misconfigured = True

    yasmet_present = False
    for path in os.environ["PATH"].split(os.pathsep):
        if os.path.isfile(os.path.join(path, 'yasmet')):
            yasmet_present = True
            break
        
    if not yasmet_present:
        print("yasmet is either not installed or not added to path, see", yasmet_url, '\n')
        misconfigured = True

    if misconfigured:
        exit(1)

    return config

if __name__ == '__main__':
    check_config()