from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


"""
Chatbot client
Author: Justin Hammel
Description: Script instantiates chatbot using chatterbot and training with corpus database in the trainer.py file.
"""

chatbot = ChatBot('2d')

trainer = ChatterBotCorpusTrainer(chatbot)

trainer.train(
    "chatterbot.corpus.english"
)


# while True:
#     userInput = input("\n>> ")
#     print(userInput)
#     if userInput == "exitnow":
#         break
#     response = chatbot.get_response(userInput)
#     print(response)
