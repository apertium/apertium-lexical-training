# parses the config, check if the tools are present

from tomlkit import parse, dumps
import os

# urls of the required tools and data
corpora_url = "https://wiki.apertium.org/wiki/Corpora"
# lex_tools_url = "https://wiki.apertium.org/wiki/Install_Apertium_core_by_compiling"
fast_align_url = "https://github.com/clab/fast_align"
langs_url = "https://wiki.apertium.org/wiki/List_of_language_pairs"
apertium_url = "https://wiki.apertium.org/wiki/Installation"
yasmet_url = "https://wiki.apertium.org/wiki/Using_weights_for_ambiguous_rules"


def check_config(filename='config.toml'):
    misconfigured = False
    lex_tools_paths = ['/opt/local/share/apertium-lex-tools',
                       '/usr/local/share/apertium-lex-tools', '/usr/share/apertium-lex-tools']
    with open(filename) as config_file:
        config_toml = config_file.read()
        config = parse(config_toml)

    # gives error if not parsed well
    assert config_toml == dumps(config)

    # changing the paths to absolute
    for key in ['CORPUS_SL', 'CORPUS_TL', 'FAST_ALIGN', 'LANG_DATA']:
        if not os.path.isabs(config[key]):
            config[key] = os.path.join(os.path.abspath('.'), config[key])

    if not os.path.isfile(config['CORPUS_SL']):
        print(
            f"'{config['CORPUS_SL']}'(CORPUS_SL) is not a file, provide a valid file or \nto download, look {corpora_url}\n")
        misconfigured = True

    if not os.path.isfile(config['CORPUS_TL']):
        print(
            f"'{config['CORPUS_TL']}'(CORPUS_TL) is not a file, provide a valid file or \nto download, look {corpora_url}\n")
        misconfigured = True

    is_lex_tools_present = False
    for lex_tools in lex_tools_paths:
        if os.path.isdir(lex_tools):
            scripts = ['extract-sentences.py', 'extract-freq-lexicon.py',
                       'ngram-count-patterns-maxent2.py', 'merge-ngrams-lambdas.py', 'lambdas-to-rules.py',
                       'ngrams-to-rules-me.py', 'common.py']

            for script in scripts:
                if not os.path.isfile(os.path.join(lex_tools, script)):
                    print(
                        f"'{script}' is not present in '{lex_tools}', re-install apertium-lex-tools {apertium_url}\n")
                    misconfigured = True
            is_lex_tools_present = True

    if not is_lex_tools_present:
        print(
            f"'apertium_lex_tools'is not installed, to install apertium-lex-tools follow {apertium_url}\n")
        misconfigured = True

        # assuming scripts are intact
        # if 'process-tagger-output' not in os.listdir(config['LEX_TOOLS']):
        #     print("'process-tagger-output' is not in", "'"+config['LEX_TOOLS']+"'(LEX_TOOLS),",
        #           "provide a valid directory or \nto install, follow", lex_tools_url, '\n')
        #     misconfigured = True

    if not os.path.isfile(config['FAST_ALIGN']):
        print(
            f"'{config['FAST_ALIGN']}'(FAST_ALIGN) is not a file, provide a valid executable or \nto install, follow {fast_align_url}\n")
        misconfigured = True
    # else:
    #     if 'fast_align' not in os.listdir(config['FAST_ALIGN']):
    #         print("fast_align is not present in", "'"+config['FAST_ALIGN']+"'(FAST_ALIGN),", \
    #                         "provide a valid directory or \nto install, follow", fast_align_url, '\n')
    #         misconfigured = True

    if not os.path.isdir(config['LANG_DATA']):
        print(
            f"'{config['LANG_DATA']}'(LANG_DATA) is not a directory, provide a valid directory or \nto install, follow {langs_url}\n")
        misconfigured = True
    else:
        sl_tl_autobil = f"{config['SL']}-{config['TL']}.autobil.bin"
        tl_sl_autobil = f"{config['TL']}-{config['SL']}.autobil.bin"
        if sl_tl_autobil not in os.listdir(config['LANG_DATA']):
            print(f"'{sl_tl_autobil}' is not in '{config['LANG_DATA']}'(LANG_DATA), \
                  provide a valid directory or \nto install, follow {langs_url}\n")
            misconfigured = True
        if tl_sl_autobil not in os.listdir(config['LANG_DATA']):
            print(f"'{tl_sl_autobil}' is not in '{config['LANG_DATA']}'(LANG_DATA), \
                  provide a valid directory or \nto install, follow {langs_url}\n")
            misconfigured = True

    apertium_present = False
    for path in os.environ["PATH"].split(os.pathsep):
        if os.path.isfile(os.path.join(path, 'apertium')):
            apertium_present = True
            break

    if not apertium_present:
        print(
            f"apertium is either not installed or not added to path, see {apertium_url}\n")
        misconfigured = True

    yasmet_present = False
    for path in os.environ["PATH"].split(os.pathsep):
        if os.path.isfile(os.path.join(path, 'yasmet')):
            yasmet_present = True
            break

    if not yasmet_present:
        print(
            f"yasmet is either not installed or not added to path, install yasmet and add to the path, \
                {yasmet_url} or re-install apertium-lex-tools with yasmet, {apertium_url}\n")
        misconfigured = True

    process_tagger_output_present = False
    for path in os.environ["PATH"].split(os.pathsep):
        if os.path.isfile(os.path.join(path, 'process-tagger-output')):
            process_tagger_output_present = True
            break

    if not process_tagger_output_present:
        print(
            f"process-tagger-output is either not installed or not added to path, re-install apertium-lex-tools {apertium_url}\n")
        misconfigured = True

    if not isinstance(config['TRAINING_LINES'], int):
        print(
            f"'{config['TRAINING_LINES']}'(TRAINING_LINES) is not an integer \n")
        misconfigured = True

    if misconfigured:
        exit(1)

    return config


if __name__ == '__main__':
    check_config()
