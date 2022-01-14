from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
# Uncomment the following lines to enable verbose logging
# import logging
# logging.basicConfig(level=logging.INFO)

"""
Chatbot client
Author: Justin Hammel
Description: Script instantiates chatbot using chatterbot and training with corpus database in the trainer.py file.
"""

chatbot = ChatBot(
    '2d',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.sqlite3',
)

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
