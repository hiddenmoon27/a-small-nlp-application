import re
from filepro import add_punctuation,generate_candidates,generate_edit_two
import numpy as np
import json
def convert(str):
    with open('channel_prob.json', 'r') as f:
        channel_prob = json.load(f)
    with open('word_dic.json', 'r') as f:
        word_dic = json.load(f)
    with open('bigram_count.json', 'r') as f:
        bigram_count= json.load(f)
    with open('term_count.json', 'r') as f:
        term_count = json.load(f)
    sentence = str
    word_dic = set(word_dic)
    V = len(term_count)
    sentence = sentence[:-1]  # 去掉句子最后的那个点
    # 去除末尾句号和逗号，并以空格分割句子
    sentence_without_comma = re.sub(r',\s', ' ', sentence)
    words = sentence_without_comma.split()
    corrected_line = []  # 存储纠正后的句子
    stag=0
    ttag=0
    # 遍历句子中的每个单词
    for word in words:
        # 去除单词前后的句号和逗号
        if word.endswith("'s"):
            word = word.rstrip("'s")
            stag = 1
        else:
            stag = 0
        if word.endswith("n't"):
            word = word.rstrip("n't")
            ttag = 1
        else:
            ttag = 0

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
                sentence = str
                idx = sentence_without_comma.split().index(word + "'s" * stag + "n't" * ttag)
                bigram_1 = ' '.join([str.split()[idx - 1], candi])
                if bigram_1 in bigram_count and str.split()[idx - 1] in term_count:
                    prob += np.log((bigram_count[bigram_1] + 1.0) / (
                            term_count[str.split()[idx - 1]] + V))
                else:
                    prob += np.log(1.0 / V)
                if idx + 1 < len(str.split()):
                    bigram_2 = ' '.join([candi, str.split()[idx + 1]])
                    if bigram_2 in bigram_count and candi in term_count:
                        prob += np.log((bigram_count[bigram_2] + 1.0) / (
                                term_count[candi] + V))
                    else:
                        prob += np.log(1.0 / V)
                probs.append(prob)
            if probs:
                max_idx = probs.index(max(probs))
                corrected_line.append(candidates[max_idx] + "'s" * stag + "n't" * ttag)
                stag = 0
                ttag = 0
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
    return final_sentence
if __name__=='__main__':
    str='thiis is a worng, distf.'
    print(convert(str))