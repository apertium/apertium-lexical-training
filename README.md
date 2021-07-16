# apertium-lexical-training

The procedure for lexical selection training is a bit messy, with various scripts involved that require lots of manual tweaking, and many third party tools to be installed, e.g. fast_align, yasmet, etc. The goal of this task is to make the training procedure as streamlined and user-friendly as possible

for more, read https://wiki.apertium.org/wiki/Ideas_for_Google_Summer_of_Code/User-friendly_lexical_selection_training

## Requirements

- [parallel corpus](https://wiki.apertium.org/wiki/Corpora)
- [apertium-core](https://wiki.apertium.org/wiki/Installation) (install apertium-lex-tools with yasmet)
- [fast_align](https://github.com/clab/fast_align)
- [language pair](https://wiki.apertium.org/wiki/List_of_language_pairs) (install locally)
- python dependencies in requirements.txt

## Installation steps

- install the requirements and download or clone this repo (`git clone https://github.com/vivekvardhanadepu/apertium-lexical-training.git`)
- create config.toml and provide tools' and corpus' paths in it (for ref, see [config.toml.example](config.toml.example"))
- run lexical_training.py

## tests

This folder contains scripts for automated testing of the helper scripts
