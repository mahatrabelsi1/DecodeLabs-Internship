print("🤖 DecodeLabs AI Chatbot")
print("Type 'exit' to quit.\n")

responses = {
    "hello": "Hi there!",
    "hi": "Hello!",
    "how are you": "I am doing great!",
    "what is your name": "I am DecodeBot.",
    "bye": "Goodbye!"
}

while True:
    user_input = input("You: ").lower().strip()

    if user_input == "exit":
        print("Bot: Goodbye!")
        break

    reply = responses.get(
        user_input,
        "Sorry, I don't understand that."
    )

    print("Bot:", reply)