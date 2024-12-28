import random
import time
import subprocess
import os


admin_username = "admin"
admin_password = "1234"
leaderboard = []
users_scores = {}
registered_users = {}


USER_DATA_FILE = "users.txt"
LEADERBOARD_FILE = "leaderboard.txt"
FEEDBACK_FILE = "feedback.txt"


categories = {
    "Books": [
        "Moby Dick", "Hamlet", "Pride and Prejudice", "1984", "To Kill a Mockingbird",
        "The Catcher in the Rye", "The Great Gatsby", "War and Peace", "The Odyssey", "Brave New World",
        "Jane Eyre", "Wuthering Heights", "The Hobbit", "Fahrenheit 451", "The Lord of the Rings"
    ],
    "Movies": [
        "Inception", "Titanic", "Avatar", "Gladiator", "The Godfather", "The Dark Knight", "Forrest Gump",
        "The Shawshank Redemption", "Pulp Fiction", "Schindler's List", "Fight Club", "The Matrix",
        "Star Wars", "Jurassic Park", "The Lion King"
    ],
    "Famous People": [
        "Einstein", "Newton", "Darwin", "Galileo", "Tesla", "Curie", "Edison", "Shakespeare",
        "Beethoven", "Cleopatra", "Alexander the Great", "Catherine the Great", "Abraham Lincoln",
        "Mahatma Gandhi", "Winston Churchill"
    ],
}


modes = {"Easy": 60, "Medium": 45, "Hard": 30}


def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            for line in file:
                username, password = line.strip().split(",")
                registered_users[username] = password


def save_user_data():
    with open(USER_DATA_FILE, "w") as file:
        for username, password in registered_users.items():
            file.write(f"{username},{password}\n")


def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as file:
            for line in file:
                data = line.strip().split(",")
                username = data[0]
                scores = list(map(int, data[1:]))
                users_scores[username] = scores


def save_leaderboard():
    with open(LEADERBOARD_FILE, "w") as file:
        for username, scores in users_scores.items():
            scores_str = ",".join(map(str, scores))
            file.write(f"{username},{scores_str}\n")


def load_feedback():
    feedback_list = []
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "r") as file:
            for line in file:
                username, feedback = line.strip().split(",", 1)
                feedback_list.append((username, feedback))
    return feedback_list


def save_feedback(feedback_list):
    with open(FEEDBACK_FILE, "w") as file:
        for username, feedback in feedback_list:
            file.write(f"{username},{feedback}\n")


def clear_terminal():
    try:
        if os.name == "nt":  # For Windows
            subprocess.run("cls", shell=True)
        else:  # For Unix/Linux/Mac
            subprocess.run("clear", shell=True)
    except Exception:
        print("Error clearing the terminal.")


def view_all_users():
    print("\nRegistered Users and Details:")
    if not registered_users:
        print("No registered users yet.")
    else:
        feedback_list = load_feedback()
        for username, password in registered_users.items():
            print(f"Username: {username}")
            print(f"Password: {password}")

            if username in users_scores:
                scores = users_scores[username]
            else:
                scores = []
            if scores:
                print(f"Scores: {', '.join(map(str, scores))}")
                print(f"Total Score: {sum(scores)}")
            else:
                print("Scores: None")

            user_feedback = []
            for item in feedback_list:
                user, feedback = item
                if user == username:
                    user_feedback.append(feedback)

            if user_feedback:
                feedback_li = ','.join(user_feedback)
                print(f"Feedback: {feedback_li}")
            else:
                print("Feedback: None")

            print("-" * 20)
    print()


def search_user():
    print("\nSearch User:")
    search_query = input("Enter username to search: ").strip()
    if search_query in registered_users:
        print(f"Username: {search_query}")
        print(f"Password: {registered_users[search_query]}")
        if search_query in users_scores:
            scores = users_scores[search_query]
        else:
            scores = []
        if scores:
            print(f"Scores: {', '.join(map(str, scores))}")
            print(f"Total Score: {sum(scores)}")
        else:
            print("Scores: None")

        feedback_list = load_feedback()
        user_feedback = []
        for item in feedback_list:
            user, feedback = item
            if user == search_query:
                user_feedback.append(feedback)

        if user_feedback:
            feedback_li = ','.join(user_feedback)
            print(f"Feedback: {feedback_li}")
        else:
            print("Feedback: None")
    else:
        print(f"No user found with username '{search_query}'.")
    print()


def view_leaderboard():
    print("\nLeaderboard:")

    scores_with_totals = []
    for user, scores in users_scores.items():
        total_score = sum(scores)
        scores_with_totals.append((user, total_score))

    def get_total_score(item):
        return item[1]

    scores_with_totals.sort(key=get_total_score, reverse=True)

    rank = 1
    for user, total_score in scores_with_totals:
        print(f"{rank}. {user} - Total: {total_score} points")
        rank = rank+1

    print()


def delete_user():
    print("\nDelete User:")
    if not registered_users:
        print("No registered users to delete.")
        return
    username = input("Enter the username to delete: ").strip()
    if username in registered_users:
        del registered_users[username]
        if username in users_scores:
            del users_scores[username]
        save_user_data()
        save_leaderboard()
        print(f"User '{username}' deleted successfully!")
    else:
        print("User not found!")


def play_game(username):
    guessed_words = set()
    score = 0

    print("\nChoose Game Mode:")
    for mode in modes:
        print(f"- {mode}")
    mode = input("Enter mode: ").capitalize()
    if mode not in modes:
        print("Invalid mode selected. Exiting game.")
        return

    time_limit = modes[mode]
    start_time = time.time()

    print("\nMemorize these words:")
    for category, words in categories.items():
        print(f"{category}: {', '.join(words)}")

    memorization_time = 10
    for i in range(memorization_time, 0, -1):
        print(f"\rTime remaining to memorize: {i} seconds", end="")
        time.sleep(1)

    clear_terminal()
    print("The list has been hidden. Time to start the game!")

    while True:
        elapsed_time = time.time() - start_time
        remaining_time = time_limit - elapsed_time
        if remaining_time <= 0:
            print("\nTime's up! Game Over!")
            break

        category = random.choice(list(categories.keys()))
        print(f"\nCategory: {category}")
        print(
            f"Guess the word (Time Remaining: {int(remaining_time)} seconds):")

        user_input = input("Your guess: ").strip().lower()

        found = False
        for word in categories[category]:
            if user_input == word.lower():
                found = True
                break

        if found:
            if user_input not in guessed_words:
                guessed_words.add(user_input)
                score += 5
                time_limit += 5
                print("Correct! Time and Score updated.")
            else:
                print("You already guessed that word!")
        else:
            time_limit -= 5
            print("Incorrect! Time reduced.")

    print(f"\nGame Over! Your final score: {score}")
    if username not in users_scores:
        users_scores[username] = []
    users_scores[username].append(score)
    save_leaderboard()


def send_feedback(username, feedback_list):
    feedback = input("\nEnter your feedback: ")
    feedback_list.append((username, feedback))
    save_feedback(feedback_list)
    print("Thank you for your feedback!")


def update_password(username):
    current_password = input("\nEnter your current password: ").strip()
    if registered_users.get(username) == current_password:
        new_password = input("Enter your new password: ").strip()
        confirm_password = input("Confirm your new password: ").strip()
        if new_password == confirm_password:
            registered_users[username] = new_password
            save_user_data()
            print("Password updated successfully!")
        else:
            print("Passwords do not match. Try again.")
    else:
        print("Incorrect current password!")


def admin_login():
    print("\nAdmin Login:")
    username = input("Enter admin username: ").strip()
    password = input("Enter admin password: ").strip()
    if username == admin_username and password == admin_password:
        print("Admin login successful!")
        return True
    else:
        print("Incorrect admin credentials! Access denied.")
        return False


def register_user():
    print("\nUser Registration:")
    username = input("Enter a username: ").strip()
    if username in registered_users:
        print("Username already taken! Please try a different username.")
    else:
        password = input("Enter a password: ").strip()
        registered_users[username] = password
        save_user_data()
        print(f"User {username} registered successfully!")


def login_user():
    print("\nUser Login:")
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()
    if username in registered_users and registered_users[username] == password:
        print("Login successful!")
        return username
    else:
        print("Incorrect username or password!")
        return None


def main():
    load_user_data()
    load_leaderboard()
    feedback_list = load_feedback()

    print("Welcome to the Word Memorization Game!")
    while True:
        print("\nMain Menu:")
        print("1. Admin Login\n2. User Login\n3. Register\n4. View Leaderboard\n5. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            if admin_login():
                while True:
                    print("\nAdmin Menu:")
                    print(
                        "1. View All Users\n2. Search User\n3. View Feedback\n4. Delete User\n5. Logout")
                    admin_choice = input("Enter choice: ").strip()
                    if admin_choice == "1":
                        view_all_users()
                    elif admin_choice == "2":
                        search_user()
                    elif admin_choice == "3":
                        for user, feedback in feedback_list:
                            print(f"User: {user}, Feedback: {feedback}")
                    elif admin_choice == "4":
                        delete_user()
                    elif admin_choice == "5":
                        print("Admin logged out.")
                        break
                    else:
                        print("Invalid choice! Please try again.")

        elif choice == "2":
            user = login_user()
            if user:
                while True:
                    print("\nUser Menu:")
                    print(
                        "1. Play Game\n2. View Scores\n3. Send Feedback\n4. Update Password\n5. Logout")
                    user_choice = input("Enter choice: ").strip()
                    if user_choice == "1":
                        play_game(user)
                    elif user_choice == "2":
                        if user in users_scores:
                            scores = users_scores[user]
                            print(
                                f"\nYour Scores: {', '.join(map(str, scores))}")
                        else:
                            print("No scores yet.")

                    elif user_choice == "3":
                        send_feedback(user, feedback_list)
                    elif user_choice == "4":
                        update_password(user)
                    elif user_choice == "5":
                        print("User logged out.")
                        break
                    else:
                        print("Invalid choice! Please try again.")

        elif choice == "3":
            register_user()

        elif choice == "4":
            view_leaderboard()

        elif choice == "5":
            print("Thank you for playing! Goodbye!")
            break

        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()
