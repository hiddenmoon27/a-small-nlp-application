import re
def find_non_matching_indices(list1, list2):
    # 确保两个列表长度相同以避免索引错误
    if len(list1) != len(list2):
        raise ValueError("两个列表长度不相等")

    non_matching_indices = []
    for index in range(len(list1)):
        if list1[index] != list2[index]:
            non_matching_indices.append(index)

    return non_matching_indices
anspath='./ans.txt'
resultpath='./result.txt'
ansfile=open(anspath,'r')
resultfile=open(resultpath,'r')
count=0
tag=0
for i in range(1000):
    tag=tag+1
    ansline=ansfile.readline().split('\t')[1]
    ansl=re.sub(r',\s', ' ', ansline)
    ansset=ansl.split()
    resultline=resultfile.readline().split('\t')[1]
    resl=re.sub(r',\s', ' ', resultline)
    resultset=resl.split()
    if ansset==resultset:
        count+=1
    # else:
    #     print("序号是{}".format(tag))
    #     dex=find_non_matching_indices(ansset,resultset)
    #     for index in dex:
    #         print(f'正确+{ansset[index]}')
    #         print(f'错误+{resultset[index]}')
print("Accuracy is : %.2f%%" % (count*1.00/10))
