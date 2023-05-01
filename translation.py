import openai
from PrivateKey import key
import json
import os


openai.api_key = key

dataList = []

for dataName in os.listdir("Models/"):
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

   
    prompt = user_input.format(**namespace)
    print(f"Sending quest: {i}")
    i += 1
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=[
            {"role": "system", "content": "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible."},
            {"role": "user", "content": "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible."},
            {"role": "user", "content": f'{prompt}'},
        ]
    )    
    
    responses.append(response['choices'][0]['message']['content'])

print("Writing result")
with open('result.txt', 'w') as w:
    for response in responses:
         w.write(response)
         w.write("\n\n----------------------------------------------------------------------------------------------------------------------------------\n\n")
    w.close()   
print("Result in <result.txt>")
    