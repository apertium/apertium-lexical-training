# tests check_config.py
from check_config import check_config
from tomlkit import parse, dumps
import os
import shutil
import sys
sys.path.append('../')


def main(argc, argv):
    tamper_string = 'abc'

    # Test 1
    config_file = open('config_test.toml', 'r')
    config_toml = config_file.read()
    config = parse(config_toml)
    config_file.close()

    print("Test 1 : No installations")
    print("---------------------")

    for key in config:
        if key == 'TRAINING_LINES':
            continue
        config[key] += "abc"

    # if os.fork() == 0:
    #     with open('check_config_test.toml', 'w') as test_file:
    #         test_file.write(dumps(config))
    #     check_config('check_config_test.toml')
    #     exit(0)

    # _, _ = os.wait()

    # # Test 2
    # config_file = open('config_test.toml', 'r')
    # config_toml = config_file.read()
    # config = parse(config_toml)
    # config_file.close()

    # print("Test 2 : partial/no installations")
    # print("----------------------------------")

    # config['SL'] += "abc"

    lex_tools = '/usr/share/apertium-lex-tools'
    if os.path.isdir(lex_tools):
        scripts = ['extract-sentences.py', 'extract-freq-lexicon.py',
                   'ngram-count-patterns-maxent2.py', 'merge-ngrams-lambdas.py', 'lambdas-to-rules.py',
                   'ngrams-to-rules-me.py']

        for script in scripts:
            if os.path.isfile(os.path.join(lex_tools, script)):
                shutil.move(os.path.join(lex_tools, script),
                            os.path.join(lex_tools, script+tamper_string))

    for path in os.environ["PATH"].split(os.pathsep):
        if os.path.isfile(os.path.join(path, 'apertium')):
            shutil.move(os.path.join(path, 'apertium'),
                        os.path.join(path, 'apertium'+tamper_string))
            break

    for path in os.environ["PATH"].split(os.pathsep):
        if os.path.isfile(os.path.join(path, 'yasmet')):
            shutil.move(os.path.join(path, 'yasmet'),
                        os.path.join(path, 'yasmet'+tamper_string))
            break

    for path in os.environ["PATH"].split(os.pathsep):
        if os.path.isfile(os.path.join(path, 'process-tagger-output')):
            shutil.move(os.path.join(path, 'process-tagger-output'),
                        os.path.join(path, 'process-tagger-output'+tamper_string))
            break

    if os.path.isdir(lex_tools):
        scripts = ['extract-sentences.py', 'extract-freq-lexicon.py',
                   'ngram-count-patterns-maxent2.py', 'merge-ngrams-lambdas.py', 'lambdas-to-rules.py',
                   'ngrams-to-rules-me.py']

        for script in scripts:
            if os.path.isfile(os.path.join(lex_tools, script+tamper_string)):
                shutil.move(os.path.join(lex_tools, script+tamper_string),
                            os.path.join(lex_tools, script))
    # if os.path.isfile(os.path.join(config['LEX_TOOLS'], 'process-tagger-output')):
    #     shutil.move(os.path.join(config['LEX_TOOLS'], 'process-tagger-output'),
    #                 os.path.join(config['LEX_TOOLS'], 'process-tagger-output'+tamper_string))

    # if os.path.isfile(os.path.join(config['FAST_ALIGN'], 'fast_align')):
    #     shutil.move(os.path.join(config['FAST_ALIGN'], 'fast_align'), os.path.join(config['FAST_ALIGN'], 'fast_align'+tamper_string))

    if os.fork() == 0:
        with open('check_config_test.toml', 'w') as test_file:
            test_file.write(dumps(config))
        check_config('check_config_test.toml')
        exit(0)

    _, _ = os.wait()

    # shutil.move(os.path.join(config['LEX_TOOLS'], 'process-tagger-output'+tamper_string),
    #             os.path.join(config['LEX_TOOLS'], 'process-tagger-output'))

    # shutil.move(os.path.join(config['FAST_ALIGN'], 'fast_align'+tamper_string), os.path.join(config['FAST_ALIGN'], 'fast_align'))

    for path in os.environ["PATH"].split(os.pathsep):
        if os.path.isfile(os.path.join(path, 'apertium'+tamper_string)):
            shutil.move(os.path.join(path, 'apertium'+tamper_string),
                        os.path.join(path, 'apertium'))
            break

    for path in os.environ["PATH"].split(os.pathsep):
        if os.path.isfile(os.path.join(path, 'yasmet'+tamper_string)):
            shutil.move(os.path.join(path, 'yasmet'+tamper_string),
                        os.path.join(path, 'yasmet'))
            break

    for path in os.environ["PATH"].split(os.pathsep):
        if os.path.isfile(os.path.join(path, 'process-tagger-output'+tamper_string)):
            shutil.move(os.path.join(path, 'process-tagger-output'+tamper_string),
                        os.path.join(path, 'process-tagger-output'))
            break

    # Test 3
    config_file = open('config_test.toml', 'r')
    config_toml = config_file.read()
    config = parse(config_toml)
    config_file.close()

    print("Test 2 : wrong TRAINING_LINES")
    print("---------------------")

    for value in [tamper_string, 1.00, 1e237892]:
        config['TRAINING_LINES'] = value
        if os.fork() == 0:
            with open('check_config_test.toml', 'w') as test_file:
                test_file.write(dumps(config))
            check_config('check_config_test.toml')
            exit(0)

        _, _ = os.wait()

    # Test 4
    config_file = open('config_test.toml', 'r')
    config_toml = config_file.read()
    config = parse(config_toml)
    config_file.close()

    print("Test 3 : correct installations")
    print("-------------------------------")

    if os.fork() == 0:
        with open('check_config_test.toml', 'w') as test_file:
            test_file.write(dumps(config))
        check_config('check_config_test.toml')
        exit(0)

    _, _ = os.wait()

    os.remove('check_config_test.toml')


if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
