# pvpc_to_telegram
Bot that will send energy prices for the following day according to the PVPC webpage

![Screenshot](media/telegrambot.PNG)

# Telegram package
This package allows you to use a Telegram bot as handler for the standard logging library. In order to use this you will 
need to carry out some configurations outside the scope of this repository.

## How to create a Telegram Bot
The process is very well documented online. I found this link (https://dev.to/rizkyrajitha/get-notifications-with-telegram-bot-537l)
very easy to follow.

1) Copy the Bot's token in tokens.json under the 'bot_token' object.
2) Copy the Chat's token in tokens.json under the 'chats_token' list. More than a single chat can be used seamlessly

## How to create a logging handler for a Telegram Bot
This section of the project is actually forked from https://github.com/dmitryikh/loggingbot with some fixes that I 
found required for my setup.

Clone my forked repo at least until PR is accepted
1) git clone https://github.com/Guillelerial/loggingbot.git


# Roadmap

1) Pending to add color to graph.
2) Pending to decide how to make the code run automatically every midnight
