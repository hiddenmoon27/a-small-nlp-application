import numpy as np
import re
import string
from nltk.corpus import reuters
from collections import defaultdict
import json
def add_punctuation(original_sentence, corrected_sentence):
    # 初始化纠正后的句子，用于存储最终结果
    result_sentence = ""
    # 初始化索引变量，用于跟踪已添加到纠正后句子的字符数
    original_sentence=original_sentence[:-1]
    # 遍历原始句子的每个字符
    douhaoindex=0
    douhao=[]
    owords=original_sentence.split()
    for word in owords:
        #要识别出真正逗号的位置，什么456,789中间这种逗号是没必要的
        if ',' == word[-1]:
            douhao.append(douhaoindex)
        douhaoindex = douhaoindex + 1
    cwords=corrected_sentence.split()
    clen=len(cwords)
    ctag=0
    for word in cwords:
        if ctag in douhao:
            result_sentence=result_sentence+word+','+' '
        elif ctag<clen-1:
            result_sentence=result_sentence+word+' '
        else:
            result_sentence=result_sentence+word
        ctag=ctag+1
    # 返回带有标点符号的纠正后的句子
    return result_sentence+'.'
def generate_candidates(word=''):
    """
    word: 给定的错误输入
    返回的是所有的候选集合
    生成编辑距离为1的单词
    1、insert
    2、delete
    3、replace
    """
    # string.ascii_lowercase: 所有的小写字母
    letters = ''.join([word for word in string.ascii_lowercase])
    # 将单词分割成一个元组，把所有的可能性添加到一个列表中去。
    # [('', 'abcd'), ('a', 'bcd'), ('ab', 'cd'), ('abc', 'd'), ('abcd', '')]
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    # 遍历字母，遍历所有的分割，把他们组合起来
    # 插入到所有可能的位置
    inserts = [L + i + R for L, R in splits for i in letters]
    # delete
    # 每次都是删除R的第一个元素（如果R存在的话）
    deletes = [L + R[1:] for L, R in splits if R]
    # replace
    # 替换嘛。就是插入和删除的合体。
    replaces = [L + i + R[1:] for L, R in splits if R for i in letters]
    return set(inserts + deletes + replaces+[word])

def generate_edit_two(word=''):
    """
    给定一个字符串，生成编辑距离不大于2的字符串。
    """
    return set([j for i in generate_candidates(word) for j in generate_candidates(i)])

# 读取 Birkbeck Spelling Error Corpus
def load_birkbeck_corpus(file_path):
    channel_prob = defaultdict(dict)
    current_correct = None

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()  # 去掉每行两端的空白字符
            if line.startswith('$'):
                current_correct = line[1:]  # 以 $ 开头的行为正确拼写单词，去掉 $ 符号
            else:
                if current_correct:
                    if line in channel_prob[current_correct]:
                        channel_prob[current_correct][line] += 1
                    else:
                        channel_prob[current_correct][line] = 1

    # 计算错误拼写的概率
    for correct, errors in channel_prob.items():
        total_errors = sum(errors.values())
        for error in errors:
            channel_prob[correct][error] /= total_errors

    return channel_prob
def setgram():
    categories = reuters.categories()
    corpus = reuters.sents(categories=categories)
    term_count = {}
    # bigram_count：双字符字典
    bigram_count = {}
    for doc in corpus:
        # 每一个句子都加上起始符
        doc = ['<s>'] + doc
        # 遍历每一个句子的每一个字符，并将其个数记载入term_count字典里。
        for i in range(len(doc)-1):
            # term: 当前字符
            term = doc[i]
            # bigram:当前字符以及后一个字符组成的列表
            bigram = doc[i:i + 2]
            if term in term_count:
                term_count[term] += 1
            else:
                term_count[term] = 1
            # 把bigram变换成一个字符串。
            bigram = ' '.join(bigram)
            if bigram in bigram_count:
                bigram_count[bigram] += 1
            else:
                bigram_count[bigram] = 1
    return bigram_count,term_count
if __name__=='__main__':
    # 构建词库
    word_dic = []
    # 通过迭代器访问: for word in f
    # 用列表生成式直接将数据加入到一个空的列表中去
    with open('./vocab.txt', 'r') as f:
        word_dic = [word.rstrip() for word in f]
    with open('word_dic.json', 'w') as f:
        json.dump(word_dic, f)
    word_dic=set(word_dic)

    # 示例用法
    file_path = 'missp.dat'  # 替换为实际的文件路径
    channel_prob = load_birkbeck_corpus(file_path)
    with open('channel_prob.json', 'w') as f:
        json.dump(channel_prob, f)


    bigram_count,term_count=setgram()
    V = len(term_count)
    with open('bigram_count.json', 'w') as f:
        json.dump(bigram_count, f)
    with open('term_count.json', 'w') as f:
        json.dump(term_count, f)
    stag=0
    tag=0
    ttag=0
    # 打开测试数据
    with open("./testdata.txt", 'r', encoding='utf8') as f:
        with open("result.txt", 'w', encoding='utf8') as result_file:
            # 遍历每一行
            for line in f:
                tag = tag + 1
                print(tag)
                items = line.rstrip().split('\t')
                sentence = items[2]
                sentence=sentence[:-1]  #去掉句子最后的那个点
                # 去除末尾句号和逗号，并以空格分割句子
                sentence_without_comma =re.sub(r',\s', ' ', sentence)
                words = sentence_without_comma.split()
                corrected_line = []  # 存储纠正后的句子
                # 遍历句子中的每个单词
                for word in words:
                    # 去除单词前后的句号和逗号
                    if word.endswith("'s"):
                        word=word.rstrip("'s")
                        stag=1
                    else:
                        stag=0
                    if word.endswith("n't"):
                        word=word.rstrip("n't")
                        ttag=1
                    else:
                        ttag=0

                    # 如果单词不在词库中，进行纠正
                    if word not in word_dic:
                        candidates_one = generate_candidates(word)
                        candidates = [word for word in candidates_one if word in word_dic]
                        if len(candidates) < 1:
                            candidates_two = generate_edit_two(word)
                            candidates = [word for word in candidates_two if word in word_dic]
                            if len(candidates) < 1:
                                corrected_line.append(word + "'s" * stag + "n't" * ttag)
                                stag = 0
                                ttag = 0
                                continue
                        probs = []
                        for candi in candidates:
                            prob = 0
                            if candi in channel_prob and word in channel_prob[candi]:
                                prob += np.log(channel_prob[candi][word])
                            else:
                                prob += np.log(0.00001)
                            sentence = items[2]
                            idx = sentence_without_comma.split().index(word+"'s"*stag+"n't"*ttag)
                            bigram_1 = ' '.join([items[2].split()[idx - 1], candi])
                            if bigram_1 in bigram_count and items[2].split()[idx - 1] in term_count:
                                prob += np.log((bigram_count[bigram_1] + 1.0) / (
                                        term_count[items[2].split()[idx - 1]] + V))
                            else:
                                prob += np.log(1.0 / V)
                            if idx + 1 < len(items[2].split()):
                                bigram_2 = ' '.join([candi, items[2].split()[idx + 1]])
                                if bigram_2 in bigram_count and candi in term_count:
                                    prob += np.log((bigram_count[bigram_2] + 1.0) / (
                                            term_count[candi] + V))
                                else:
                                    prob += np.log(1.0 / V)
                            probs.append(prob)
                        if probs:
                            max_idx = probs.index(max(probs))
                            corrected_line.append(candidates[max_idx]+"'s"*stag+"n't"*ttag)
                            stag=0
                            ttag=0
                        else:
                            corrected_line.append(word + "'s" * stag + "n't" * ttag)
                            stag = 0
                            ttag = 0
                    else:
                        corrected_line.append(word + "'s" * stag + "n't" * ttag)
                        stag = 0
                        ttag = 0

                corrected_sentence = ' '.join(corrected_line)
                final_sentence = add_punctuation(sentence, corrected_sentence)
                result_file.write(str(tag) + '\t' + final_sentence + '\n')

