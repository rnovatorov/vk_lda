Description:
============

This program's purpose is to download VK posts, process them (i.e. normalize) and make LDA out of processed docs.


Components:
===========

It consists of these components:
  1. get_vk_posts.py - getting posts
  2. process_vk_posts.py - normalizing docs
  3. make_lda.py - using latent Dirichlet allocation to find popular topics
  4. interprete_json.py - interpreting results in human readable form


Usage:
======

Usage details of each component may be obtained by using `--help` option while calling them.


Casual workflow:
================

Supposing target VK group has id 42:

#### 1. Downloading VK posts:

  `python get_vk_posts.py -42 -o 42_posts.json`

#### 2. Processing posts:

  `python process_vk_posts.py 42_posts.json -o 42_prepared.json`

  #### Hint:
    It is also good idea to pass `-n` parameter to leave only nouns
    
  #### Hint:
    You can extend stopwords by providing `-s` parameter and path to stopwords

#### 3. Making LDA:

  `python make_lda.py -t 7 -p 30 -o 42_lda.json`

where:
  - `-t` is amount of topics
  - `-p` amount of passes through text

#### 4. Interpreting result:

  `python interprete_json.py -o 42_interpreted.txt 42_lda.json`
