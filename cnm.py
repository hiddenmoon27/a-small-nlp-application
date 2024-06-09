import re

sentence = "Hello, world, how,are, you? 568,500"
sentence_without_comma = re.sub(r',\s', ' ', sentence)
print(sentence_without_comma)

