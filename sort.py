import openai
from PrivateKey import key
import json
import os
import re

openai.api_key = key

dataList = []


# Human sort 
def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


filelist = os.listdir("Models/")
filelist = sorted(filelist,key=natural_keys)


for dataName in filelist:
    if(not dataName.endswith('.json')):
        continue
    print(dataName)
    fileName = "%s/%s" % ("Models", dataName)
    with open(fileName, 'r') as f:
        data = json.load(f)
        dataList.append(data)
    
print("Reading Prompt from <ExamplePrompt.txt>")
with open('ExamplePrompt.txt', 'r') as f:
    user_input = f.read()


responses = [] 
i = 1
for data in dataList:
    namespace = {'modelName' : data['modelName'], 'modelId' : data['modelId'],\
            'goal' : data['goal'], 'description' : data['description'],\
            'numStakeHolders' : data['stakeHolders']['number'],\
            'namesStakeHolder' : data['stakeHolders']['names'],\
            'treeNodes' : data['treeNodes'],\
            'numEpic' : data['epics']['number'],\
            'namesEpic' : data['epics']['names'],\
            'emotionalGoals' : data['epics']['emotionalGoals']\
            }


file_incre = 1
while os.path.exists("result%s.txt" % file_incre):
    file_incre += 1
    print(file_incre)
