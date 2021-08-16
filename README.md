# apertium-lexical-training

The procedure for lexical selection training is a bit messy, with various scripts involved that require lots of manual tweaking, and many third party tools to be installed, e.g. fast_align, yasmet, etc. The goal of this task is to make the training procedure as streamlined and user-friendly as possible

for more, read https://wiki.apertium.org/wiki/Ideas_for_Google_Summer_of_Code/User-friendly_lexical_selection_training

## requirements

**parallel corpora:**

- [parallel corpus](https://wiki.apertium.org/wiki/Corpora)
- [apertium-core](https://wiki.apertium.org/wiki/Installation) (install apertium-lex-tools with yasmet)
- [fast_align](https://github.com/clab/fast_align)
- [language pair](https://wiki.apertium.org/wiki/List_of_language_pairs) (install locally)
- python dependencies in [requirements.txt](requirements.txt)

**non-parallel corpora:**
- [non-parallel corpus](https://wiki.apertium.org/wiki/Corpora)
- [apertium-core](https://wiki.apertium.org/wiki/Installation)
- [language pair](https://wiki.apertium.org/wiki/List_of_language_pairs) (install locally)
- [IRSTLM](https://wiki.apertium.org/wiki/IRSTLM)
- python dependencies in [requirements.txt](requirements.txt)


## how to use

- install the requirements and download or clone this repo (`git clone https://github.com/vivekvardhanadepu/apertium-lexical-training.git`)
- create config.toml and provide tools' and corpus' paths in it (for ref, see [config.toml.example](config.toml.example))
- run lexical_training.py</br>
  ```
  python3 lexical_training.py [CONFIG_FILE]

  args:
    CONFIG_FILE : optional, default='config.toml'
  ```
  Note: Enter `IS_PARALLEL = true` for parallel corpora `false` for non-parallel corpora

## tests

This folder contains scripts and data for automated testing of the training scripts

## references

<a id="1">[1]</a>
Philipp Koehn.
*Europarl: A Parallel Corpus for Statistical Machine Translation.*
MT Summit 2005.

<a id="2">[2]</a>
https://www-i6.informatik.rwth-aachen.de/web/Software/YASMET.html
