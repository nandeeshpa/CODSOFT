import datetime

def chatbot_response(user_input):
    user_input = user_input.lower().strip()

    if "hello" in user_input or "hi" in user_input:
        return "Hello! How can I help you today?"

    elif "how are you" in user_input:
        return "I'm just a bot, but I'm doing great! Thanks for asking."

    elif "your name" in user_input:
        return "I'm Friday a rule-based chatbot created by Nandeesh."

    elif "bye" in user_input:
        return "Goodbye! Have a great day!"

    elif "time" in user_input:
        now = datetime.datetime.now()
        return f"The current time is {now.strftime('%I:%M %p')}."

    elif "date" in user_input:
        today = datetime.date.today()
        return f"Today's date is {today.strftime('%B %d, %Y')}."

    elif "day" in user_input:
        today = datetime.date.today()
        return f"Today is {today.strftime('%A')}."

    elif "help" in user_input or "commands" in user_input:
        return (
            "Here are some things you can ask me:\n"
            "- Say 'hello' or 'hi'\n"
            "- Ask 'how are you'\n"
            "- Ask 'what is your name'\n"
            "- Ask 'what is the time'\n"
            "- Ask 'what is the date'\n"
            "- Ask 'what day is today'\n"
            "- Say 'bye' to exit"
        )

    else:
        return "I'm sorry, I didn't understand that. Type 'help' to see what I can do."


# Start the chat
print("Chatbot: Hello! Type 'bye' to exit.")

while True:
    user_input = input("You: ")
    response = chatbot_response(user_input)
    print("Chatbot:", response)

    if "bye" in user_input.lower():
        break
