import requests
import html
import random
import threading
import time

# Global flag to track if time is up
time_up = False

# Countdown function
def countdown(seconds):
    global time_up
    for i in range(seconds, 0, -1):
        print(f"Time left: {i}", end="\r")
        time.sleep(1)
    time_up = True
    print("\n⏳ Time's up!")

# Fetch quiz data
url = "https://opentdb.com/api.php?amount=5&type=multiple"
data = requests.get(url).json()

score = 0

# Loop through questions
for q_num, question_data in enumerate(data["results"], start=1):
    # Decode HTML entities in text
    question = html.unescape(question_data["question"])
    correct = html.unescape(question_data["correct_answer"])
    incorrect = [html.unescape(ans) for ans in question_data["incorrect_answers"]]

    # Mix correct + incorrect answers
    options = incorrect + [correct]
    random.shuffle(options)

    print(f"\nQuestion {q_num}: {question}")

    # Display options as A, B, C, D
    for idx, option in enumerate(options):
        print(f"{chr(65 + idx)}. {option}")

    # Reset timer flag
    time_up = False

    # Start timer thread
    threading.Thread(target=countdown, args=(15,), daemon=True).start()

    # Take answer from player
    answer = input("Your answer (A-D): ").strip().upper()

    # Check if time is up
    if time_up:
        print("❌ Too late!")
        continue

    # Check correctness
    if answer in ["A", "B", "C", "D"]:
        chosen_option = options[ord(answer) - 65]
        if chosen_option == correct:
            print("✅ Correct!")
            score += 1
        else:
            print(f"❌ Wrong! Correct answer: {correct}")
    else:
        print("⚠ Invalid choice!")

print(f"\n🎯 Final Score: {score} / {len(data['results'])}")
