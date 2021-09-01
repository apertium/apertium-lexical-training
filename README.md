# apertium-lexical-training

This is a script for training *lexical selection rules* based on parallel or non-parallel corpora, for use in Apertium machine translation pairs.

The procedure for lexical selection training has historically been a bit messy, with various scripts involved that require lots of manual tweaking, and many third party tools to be installed. The goal of this project is to make the training procedure as streamlined and user-friendly as possible.

## Requirements

**Training on parallel corpora:**

If you have a parallel corpus, you should use that.

- [parallel corpus](https://wiki.apertium.org/wiki/Corpora)
- [apertium-core](https://wiki.apertium.org/wiki/Installation) (install apertium-lex-tools with yasmet)
- [fast_align](https://github.com/clab/fast_align)
- [language pair](https://wiki.apertium.org/wiki/List_of_language_pairs) (install locally)
- python dependencies in [requirements.txt](requirements.txt)

**Training on non-parallel corpora:**

If you have don't have a parallel corpus, you can still get useful rules out of a monolingual corpus.

- [non-parallel corpus](https://wiki.apertium.org/wiki/Corpora)
- [apertium-core](https://wiki.apertium.org/wiki/Installation)
- [language pair](https://wiki.apertium.org/wiki/List_of_language_pairs) (install locally)
- [IRSTLM](https://wiki.apertium.org/wiki/IRSTLM)
- python dependencies in [requirements.txt](requirements.txt)


### Installing requirements on Ubuntu

We assume you've already got Tino's nightly repo set up, since you're
developing a language pair – if not, see
[http://wiki.apertium.org/wiki/Ubuntu](http://wiki.apertium.org/wiki/Ubuntu).

```
sudo apt install -y irstlm
```

The python dependencies aren't currently packaged for Ubuntu
etc., so to install them, you should use
a VirtualEnv to not clutter your regular Python path:
```
sudo apt install python3-virtualenv
virtualenv .venv
source .venv/bin/activate  # you have to do this every time you want the dependencies to be available
.venv/bin/pip3 install -r requirements.txt
```

For parallel training, you'll also need fast_align; following
`config.toml.example` we'll check it out in the parent directory (so
it's "next to" this project):

```
sudo apt install -y libgoogle-perftools-dev libsparsehash-dev

git clone https://github.com/clab/fast_align
mkdir -p fast_align/build
cd fast_align/build
cmake ..
make -j
```

# Finding corpora

## Parallel corpora

If you don't have a corpus, the first place you should go looking is
[Opus](https://opus.nlpl.eu/). Pick a source and target language, then
download the file `moses` column if there is one. The `moses` column
gives you a parallel, sentence-aligned corpus. You'll get a zip file
containing a pair of files with aligned lines, these are the files you
use in training.

Say you downloaded the `WikiMatrix` Moses file for Norwegian and
Swedish, you'll get a zip file called `no-svn.txt.zip`. Unzip that,
and you'll see files

    LICENSE
    README
    WikiMatrix.no-sv.no
    WikiMatrix.no-sv.sv
    WikiMatrix.no-sv.xml

The files ending in the language codes contain the actual
sentences. We can verify that they're aligned sentences with

    paste WikiMatrix.no-sv.no WikiMatrix.no-sv.sv |less -S

If you found nothing on Opus, you may want to check
[Corpora](https://wiki.apertium.org/wiki/Corpora) on the Apertium
wiki, or try using a non-parallel corpus.

## Non-parallel corpora

Any text in a .txt file will do, as long as it's in your target
language. See [Corpora](https://wiki.apertium.org/wiki/Corpora) on the
Apertium wiki for possible sources.

You can also use a precompiled (target) language model if you have
that, instead of a corpus.

## How to train

- Install the requirements
- Clone this repo<br>
  ```
  git clone https://github.com/apertium/apertium-lexical-training.git
  ```
- Create `config.toml` (for reference, see [config.toml.example](config.toml.example))
  ```
  cp config.toml.example config.toml
  ```
  - Now edit `config.toml` and give the rigth paths to tools and your corpus
  - Enter `IS_PARALLEL = true` for parallel corpora, `false` for non-parallel corpora
- Run `lexical_training.py`<br>
  ```
  python3 lexical_training.py [CONFIG_FILE]

  args:
    CONFIG_FILE : optional, default='config.toml'
  ```

## Tests

This folder contains scripts and data for automated testing of the training scripts. It is run as a Github workflow with the little test corpus included in the repo.

## References

This project was started as part of Google Summer of Code 2021 (complete work submission: https://apertium.projectjj.com/gsoc2021/vivekvardhanadepu/vivekvardhanadepu.html ,
original GsoC Idea https://wiki.apertium.org/wiki/Ideas_for_Google_Summer_of_Code/User-friendly_lexical_selection_training ).

<a id="1">[1]</a>
Philipp Koehn.
*Europarl: A Parallel Corpus for Statistical Machine Translation.*
MT Summit 2005.

<a id="2">[2]</a>
https://www-i6.informatik.rwth-aachen.de/web/Software/YASMET.html
