from chatbot import chatbot
from chatterbot.trainers import ChatterBotCorpusTrainer

"""
Chatbot trainer
Author: Justin Hammel
Description: Script uses corpus data to train chatbot with responses.
"""

trainer = ChatterBotCorpusTrainer(chatbot)

trainer.train(
    "chatterbot.corpus.english"
)
