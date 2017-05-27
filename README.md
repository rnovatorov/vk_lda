Description
===========

This program's purpose is to download VK posts, process them (i.e. normalize) and make LDA out of processed docs.


Components
==========

It consists of three components:
  1. get_vk_posts.py - responsible for getting posts
  2. process_vk_posts.py - responsible for normalizing docs
  3. make_lda.py - responsible for making sense of this shit


Usage
=====

Usage details of each component may be obtained by using `--help` option while calling them.


Casual workflow
===============

Supposing target VK group has id 42:

1. Downloading VK posts:

  `python get_vk_posts.py -42 -o 42_posts.json`

2. Processing posts:

  `python process_vk_posts.py 42_posts.json -o 42_prepared.json`

  ### Hint:
    It is also good idea to pass -n parameter to leave only nouns

3. Making LDA:

  `python make_lda.py -t 7 -p 30 -o 42_lda.json`
