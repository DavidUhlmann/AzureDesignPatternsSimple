import json
import os
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Global variable in DesignPatternsGame.py to store progress
progress = {"current": 0, "total": 0, "percentage": 0}

def fetch_page_content(url):
    optionstring = "test"
    options = Options()
    options.add_argument("--headless")
    with webdriver.Chrome(options=options) as driver:
        driver.get(url)
        return driver.page_source


def load_design_patterns():
    with open('DesignPatternsJSON.json', 'r', encoding='utf-8') as file:
        patterns = json.load(file)
    return patterns

def quiz_user(patterns_details):
    total_patterns = len(patterns_details)
    print(f"There are a total of {total_patterns} design patterns loaded.")

    while True:
        num_questions = input(f"How many design patterns do you want to be quizzed on? (1-{total_patterns}): ")
        try:
            num_questions = int(num_questions)
            if 1 <= num_questions <= total_patterns:
                break
            else:
                print(f"Please enter a number between 1 and {total_patterns}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    random_patterns = random.sample(patterns_details, num_questions)
    correct_answers = 0
    patterns_to_review = []

    for index, pattern in enumerate(random_patterns, start=1):
        print(f"\nDesign pattern {index}/{num_questions}: What is this design pattern about: {pattern['DesignPattern']}?")

        for i in range(5, 0, -1):
            print(f"Time remaining: {i} seconds")
            time.sleep(1)
        print("Time's up!\n")

        print(f"Description: {pattern['Description']}")
        user_answer = input("Did you get it right? (yes/no): ")

        if user_answer.lower() == 'yes':
            correct_answers += 1
        else:
            patterns_to_review.append(pattern)

        print("\n")

    # Show the final score and feedback
    print(f"You got {correct_answers} out of {num_questions} correct!\n")
    
    percentage_correct = (correct_answers / num_questions) * 100
    if percentage_correct == 100:
        print("Stunning, what a pro!")
    elif percentage_correct >= 80:
        print("Very nice, you know design patterns very well.")
    elif percentage_correct < 50:
        print("You clearly need to study more.")

    # Show the patterns to review
    if patterns_to_review:
        print("\nHere are the design patterns you might want to review:\n")
        for pattern in patterns_to_review:
            print(f"Design Pattern: {pattern['DesignPattern']}")
            print(f"Description: {pattern['Description']}")
            print(f"Link: {pattern['Link']}\n")


def main():

    patterns_details = load_design_patterns()

    # Confirm with the user to start the quiz
    start_quiz = input("Start the design patterns quiz? (yes/no): ")
    if start_quiz.lower() == 'yes':
        quiz_user(patterns_details)
    else:
        print("Quiz skipped. Exiting program.")