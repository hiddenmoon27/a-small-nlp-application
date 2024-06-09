from nltk.corpus import brown
import random
import string

# 提取 Brown 语料库中的词汇表
brown_words = set(brown.words())
word_dict = {word.lower() for word in brown_words}


# 拼写错误生成函数
def generate_typo(word, word_dict):
    """生成一个拼写错误，并确保它是一个非单词"""
    typo = word
    while typo in word_dict or typo == word:
        typo_types = ['insert', 'delete', 'replace', 'transpose']
        typo_type = random.choice(typo_types)

        if typo_type == 'insert':
            pos = random.randint(0, len(word))
            char = random.choice(string.ascii_lowercase)
            typo = word[:pos] + char + word[pos:]

        elif typo_type == 'delete':
            if len(word) == 1:
                continue  # 无法删除唯一的字符
            pos = random.randint(0, len(word) - 1)
            typo = word[:pos] + word[pos + 1:]

        elif typo_type == 'replace':
            pos = random.randint(0, len(word) - 1)
            char = random.choice(string.ascii_lowercase)
            typo = word[:pos] + char + word[pos + 1:]

        elif typo_type == 'transpose':
            if len(word) == 1:
                continue  # 无法交换唯一的字符
            pos = random.randint(0, len(word) - 2)
            typo = word[:pos] + word[pos + 1] + word[pos] + word[pos + 2:]

    return typo


# 构建拼写错误集
typo_data = {}

for word in word_dict:
    typo = generate_typo(word, word_dict)
    if typo != word:
        if word not in typo_data:
            typo_data[word] = []
        typo_data[word].append(typo)

# 保存拼写错误集到文件
with open("spell-errors.txt", "w", encoding="utf-8") as f:
    for correct, typos in typo_data.items():
        f.write(f"{correct}: {', '.join(typos)}\n")


