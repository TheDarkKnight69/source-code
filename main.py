from meta_ai_api import MetaAI
meta = MetaAI()
user_input = input("Input: ")
output = meta.prompt(user_input)
print(output['message'])
while True:

    user_input = input("Input: ")
    output = meta.prompt(user_input)
    print(output['message'])
