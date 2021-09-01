#!/usr/bin/env python3

# parses the config, check if the tools are present

from tomlkit import parse, dumps
import os
import sys
import re
import xml.etree.ElementTree as ET


# urls of the required tools and data
corpora_url = "https://wiki.apertium.org/wiki/Corpora"
# lex_tools_url = "https://wiki.apertium.org/wiki/Install_Apertium_core_by_compiling"
fast_align_url = "https://github.com/clab/fast_align"
langs_url = "https://wiki.apertium.org/wiki/List_of_language_pairs"
apertium_url = "https://wiki.apertium.org/wiki/Installation"
yasmet_url = "https://wiki.apertium.org/wiki/Using_weights_for_ambiguous_rules"
irstlm_url = "https://wiki.apertium.org/wiki/IRSTLM"


def irstlm_path():
    """Fallback to default Debian installation path if not in environ"""
    if 'IRSTLM' in os.environ:
        return os.environ['IRSTLM']
    else:
        return '/usr/lib/irstlm'


def get_modes(lang_data):
    modesfile = os.path.join(lang_data, 'modes.xml')
    if not os.path.isfile(modesfile):
        print(f"'{modesfile}' doesn't exist, check that LANG_DATA points to an apertium language pair checkout.")
        return None
    return ET.parse(modesfile)


def get_autobil(modes, lang_data, pair):
    found = [n for x in modes.findall(f'.//mode[@name="{pair}"]//file')
             for n in [x.attrib['name']]
             if re.search('autobil[.]bin$', n)]
    if found:
        return os.path.join(lang_data, found[0])
    else:
        print(f"Couldn't find mode with name='{pair}' in modes.xml of '{lang_data}' (LANG_DATA), "
              + f"provide a valid directory or to install, follow {langs_url}")


def check_config(config_filename):
    misconfigured = False
    lex_tools_paths = ['/opt/local/share/apertium-lex-tools',
                       '/usr/local/share/apertium-lex-tools', '/usr/share/apertium-lex-tools']
    with open(config_filename) as config_file:
        config_toml = config_file.read()
        config = parse(config_toml)

    # gives error if not parsed well
    assert config_toml == dumps(config)

    # changing the paths to absolute
    for key in ['CORPUS_SL', 'CORPUS_TL', 'LANG_DATA']:
        if not os.path.isabs(config[key]):
            config[key] = os.path.join(os.path.abspath('.'), config[key])

    if not os.path.isfile(config['CORPUS_SL']):
        print(
            f"'{config['CORPUS_SL']}'(CORPUS_SL) is not a file, provide a valid file or \nto download, look {corpora_url}\n")
        misconfigured = True
    if 'TL_MODEL' not in config:
        if not os.path.isfile(config['CORPUS_TL']):
            print(
                f"'{config['CORPUS_TL']}'(CORPUS_TL) is not a file, provide a valid file or \nto download, look {corpora_url}\n")
            misconfigured = True

    modes = None
    if not os.path.isdir(config['LANG_DATA']):
        print(
            f"'{config['LANG_DATA']}'(LANG_DATA) is not a directory, provide a valid directory or \nto install, follow {langs_url}\n")
        misconfigured = True
    else:
        modes = get_modes(config['LANG_DATA'])
        if not modes:
            misconfigured = True
        else:
            sl_tl_autobil = get_autobil(modes, config['LANG_DATA'], config['PAIR'])
            if not sl_tl_autobil:
                misconfigured = True
            if sl_tl_autobil and not os.path.exists(sl_tl_autobil):
                print(f"'{sl_tl_autobil}' is not in '{config['LANG_DATA']}' (LANG_DATA), "
                    + f"provide a valid directory or to install, follow {langs_url}")
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

    if not isinstance(config['TRAINING_LINES'], int):
        print(
            f"'{config['TRAINING_LINES']}'(TRAINING_LINES) is not an integer. pass an integer \n")
        misconfigured = True

    if not isinstance(config['MAX_RULES'], int):
        print(
            f"'{config['MAX_RULES']}'(MAX_RULES) is not an integer. pass an integer \n")
        misconfigured = True
    
    if not (isinstance(config['CRISPHOLD'], int) or isinstance(config['CRISPHOLD'], float)):
        print(
            f"'{config['CRISPHOLD']}'(CRISPHOLD) is not an integer. pass an integer \n")
        misconfigured = True

    if not isinstance(config['IS_PARALLEL'], bool):
        print(
            f"'{config['IS_PARALLEL']}'(IS_PARALLEL) is not an boolean. pass true or false \n")
        misconfigured = True
    else:
        if config['IS_PARALLEL']:
            if not os.path.isabs(config['FAST_ALIGN']):
                config['FAST_ALIGN'] = os.path.join(
                    os.path.abspath('.'), config['FAST_ALIGN'])
            if not os.path.isfile(config['FAST_ALIGN']):
                print(
                    f"'{config['FAST_ALIGN']}'(FAST_ALIGN) is not a file, provide a valid executable or \nto install, follow {fast_align_url}\n")
                misconfigured = True

            if modes:
                tl_sl_autobil = get_autobil(get_modes(config['LANG_DATA']), config['LANG_DATA'], config['REVERSE_PAIR'])
                if not tl_sl_autobil:
                    misconfigured = True
                if tl_sl_autobil and not os.path.exists(tl_sl_autobil):
                    print(f"'{tl_sl_autobil}' is not in '{config['LANG_DATA']}' (LANG_DATA), "
                          + f"provide a valid directory or to install, follow {langs_url}")
                    misconfigured = True

            yasmet_present = False
            for path in os.environ["PATH"].split(os.pathsep):
                if os.path.isfile(os.path.join(path, 'yasmet')):
                    yasmet_present = True
                    break

            if not yasmet_present:
                print(
                    f"yasmet is either not installed or not added to path, install yasmet and add to the path, \
                        {yasmet_url} or \nre-install apertium-lex-tools with yasmet, {apertium_url}\n")
                misconfigured = True

            process_tagger_output_present = False
            for path in os.environ["PATH"].split(os.pathsep):
                if os.path.isfile(os.path.join(path, 'process-tagger-output')):
                    process_tagger_output_present = True
                    break

            if not process_tagger_output_present:
                print(
                    f"process-tagger-output is not installed, re-install apertium-lex-tools {apertium_url}\n")
                misconfigured = True
            # else:
            #     if 'fast_align' not in os.listdir(config['FAST_ALIGN']):
            #         print("fast_align is not present in", "'"+config['FAST_ALIGN']+"'(FAST_ALIGN),", \
            #                         "provide a valid directory or \nto install, follow", fast_align_url, '\n')
            #         misconfigured = True

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
                    f"apertium_lex_tools scripts are not installed, re-install apertium-lex-tools {apertium_url}\n")
                misconfigured = True

        else:
            if os.path.isdir(config['LANG_DATA']):
                modules = []
                modules.append(
                    f"apertium-{config['PAIR']}.{config['SL']}-{config['TL']}.t1x")
                modules.append(f"{config['SL']}-{config['TL']}.t1x.bin")
                modules.append(
                    f"apertium-{config['PAIR']}.{config['SL']}-{config['TL']}.t2x")
                modules.append(f"{config['SL']}-{config['TL']}.t2x.bin")
                modules.append(
                    f"apertium-{config['PAIR']}.{config['SL']}-{config['TL']}.t3x")
                modules.append(f"{config['SL']}-{config['TL']}.t3x.bin")
                modules.append(f"{config['SL']}-{config['TL']}.autogen.bin")
                modules.append(f"{config['SL']}-{config['TL']}.autopgen.bin")
                for module in modules:
                    if module not in os.listdir(config['LANG_DATA']):
                        print(f"'{module}' is not in '{config['LANG_DATA']}'(LANG_DATA), \
                            provide a valid directory or \nto install, follow {langs_url}\n")
                        misconfigured = True

            if not os.path.isfile(os.path.join(irstlm_path(), 'bin/build-lm.sh')):
                if 'IRSTLM' not in os.environ:
                    print(
                        "IRSTLM doesn't seem to be installed to /usr/lib/irstlm,"
                        + " couldn't find /usr/lib/bin/build-lm.sh (if you installed"
                        + f" it elsewhere, set the environment variable IRSTLM), see {irstlm_url}\n")
                    misconfigured = True
                else:
                    print(
                        f"'bin/build-lm.sh' is not present in $IRSTLM ('{os.environ['IRSTLM']}'), see {irstlm_url}\n")
                    misconfigured = True

            multitrans_present = False
            for path in os.environ["PATH"].split(os.pathsep):
                if os.path.isfile(os.path.join(path, 'multitrans')):
                    multitrans_present = True
                    break

            if not multitrans_present:
                print(
                    f"multitrans is not installed, re-install apertium-lex-tools {apertium_url}\n")
                misconfigured = True

            ranker_present = False
            for path in os.environ["PATH"].split(os.pathsep):
                if os.path.isfile(os.path.join(path, 'irstlm-ranker')):
                    ranker_present = True
                    break

            if not ranker_present:
                print(
                    f"irstlm-ranker is not installed, re-install apertium-lex-tools with irstlm {apertium_url}\n")
                misconfigured = True

            is_lex_tools_present = False
            for lex_tools in lex_tools_paths:
                if os.path.isdir(lex_tools):
                    scripts = ['biltrans-extract-frac-freq.py', 'extract-alig-lrx.py',
                               'biltrans-count-patterns-ngrams.py', 'ngram-pruning-frac.py', 'ngrams-to-rules.py',
                               'biltrans_count_common.py', 'common.py']

                    for script in scripts:
                        if not os.path.isfile(os.path.join(lex_tools, script)):
                            print(
                                f"'{script}' is not present in '{lex_tools}', re-install apertium-lex-tools {apertium_url}\n")
                            misconfigured = True
                    is_lex_tools_present = True

            if not is_lex_tools_present:
                print(
                    f"apertium_lex_tools scripts are not installed, re-install apertium-lex-tools {apertium_url}\n")
                misconfigured = True

            if 'TL_MODEL' in config:
                if not os.path.isfile(config['TL_MODEL']):
                    print(
                        f"'{config['TL_MODEL']}'(TL_MODEL) is not a file, provide a valid file or \nto build, see {irstlm_url}\n")
                    misconfigured = True

    if misconfigured:
        exit(1)
    else:
        print("prerequisites are properly installed")

    return config


if __name__ == '__main__':
    config_file = 'config.toml'
    if(len(sys.argv) == 2):
        config_file = sys.argv[1]
    check_config(config_file)
