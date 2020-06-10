import re

trivials = ['the','be','to','of','and','a','in','that']
sentence = '(?<!etc|e\.g|i\.e)\. ' # count occurences, + 1.
