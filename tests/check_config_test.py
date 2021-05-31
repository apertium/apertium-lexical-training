# tests check_config.py
import sys
from tomlkit import parse, dumps
import os
import shutil

sys.path.append('../')

from check_config import check_config

def main(argc, argv):
    
    # Test 1
    config_file = open('config_test.toml', 'r')
    config_toml = config_file.read()
    config = parse(config_toml)
    config_file.close()

    print("Test 1 : wrong paths")
    print("---------------------")

    for key in config:
        config[key]+="abc"

    if os.fork() == 0:
        with open('check_config_test.toml', 'w') as test_file:
            test_file.write(dumps(config))
        check_config('check_config_test.toml')
        exit(0)

    _, _ = os.wait()

    # Test 2
    config_file = open('config_test.toml', 'r')
    config_toml = config_file.read()
    config = parse(config_toml)
    config_file.close()

    print("Test 2 : partial/no installations")
    print("----------------------------------")

    config['SL']+="abc"

    for path in os.environ["PATH"].split(os.pathsep):
        if os.path.isfile(os.path.join(path, 'apertium')):
            shutil.move(os.path.join(path, 'apertium'), os.path.join(path, 'apertium'+'abc'))
            break
    
    for path in os.environ["PATH"].split(os.pathsep):
        if os.path.isfile(os.path.join(path, 'yasmet')):
            shutil.move(os.path.join(path, 'yasmet'), os.path.join(path, 'yasmet'+'abc'))
            break

    if os.path.isfile(os.path.join(config['LEX_TOOLS'], 'process-tagger-output')):
        shutil.move(os.path.join(config['LEX_TOOLS'], 'process-tagger-output'), os.path.join(config['LEX_TOOLS'], 'process-tagger-output'+'abc'))

    if os.path.isfile(os.path.join(config['FAST_ALIGN'], 'fast_align')):
        shutil.move(os.path.join(config['FAST_ALIGN'], 'fast_align'), os.path.join(config['FAST_ALIGN'], 'fast_align'+'abc'))

    if os.fork() == 0:
        with open('check_config_test.toml', 'w') as test_file:
            test_file.write(dumps(config))
        check_config('check_config_test.toml')
        exit(0)

    _, _ = os.wait()

    shutil.move(os.path.join(config['LEX_TOOLS'], 'process-tagger-output'+'abc'), os.path.join(config['LEX_TOOLS'], 'process-tagger-output'))

    shutil.move(os.path.join(config['FAST_ALIGN'], 'fast_align'+'abc'), os.path.join(config['FAST_ALIGN'], 'fast_align'))

    for path in os.environ["PATH"].split(os.pathsep):
        if os.path.isfile(os.path.join(path, 'apertium'+'abc')):
            shutil.move(os.path.join(path, 'apertium'+'abc'), os.path.join(path, 'apertium'))
            break
    
    for path in os.environ["PATH"].split(os.pathsep):
        if os.path.isfile(os.path.join(path, 'yasmet'+'abc')):
            shutil.move(os.path.join(path, 'yasmet'+'abc'), os.path.join(path, 'yasmet'))
            break
    
    # Test 3
    config_file = open('config_test.toml', 'r')
    config_toml = config_file.read()
    config = parse(config_toml)
    config_file.close()

    print("Test 3 : correct installations")
    print("-------------------------------")

    with open('check_config_test.toml', 'w') as test_file:
        test_file.write(dumps(config))
    check_config('check_config_test.toml')

    os.remove('check_config_test.toml')

if __name__ == '__main__':
    main(len(sys.argv), sys.argv)