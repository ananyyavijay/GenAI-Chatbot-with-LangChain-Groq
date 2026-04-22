from dotenv import load_dotenv

load_dotenv()

from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

model = init_chat_model("groq:llama-3.1-8b-instant")

print("choose your AI mode!")
print("press 1 for Angry mode")
print("press 2 for Happy mode")
print("press 3 for Sad mode")

choice = int(input("tell me your response:- "))
if choice == 1:
    mode = "You are an angry AI agent. You must respond in very aggresive and irritated manner."
elif choice == 2:
    mode = "You are a funny AI agent. You must respond like you are one of the happiest person alive on this planet, and you should respond everthing with humor and jokes."
elif choice == 3:
    mode = "You are a sad AI agent. You must respond like you are a failure and the most annoyed thing that is ever existing."

messages = [
    SystemMessage(content=mode)
]

while True:

    prompt = input("You : ")
    messages.append(HumanMessage(content=prompt))
    if prompt == "0":
        break

    response = model.invoke(messages)

    messages.append(response.content)
    print("Bot: ", AIMessage(content=response.content))

print(messages)