import json
import random
from datetime import datetime
from collections import Counter

# -------- Core Data --------
flashcards = []

# -------- File Operations --------
def save_cards(cards, filename='flashcards.json'):
    with open(filename, 'w') as file:
        json.dump(cards, file, indent=4)

def load_cards(filename='flashcards.json'):
    try:
        with open(filename, 'r') as file:
            cards = json.load(file)
            print(f"{len(cards)} cards loaded.\n")
            return cards
    except FileNotFoundError:
        print("No file found. Starting fresh.\n")
        return []

# -------- Input Handling --------
def safe_input(prompt):
    value = input(prompt).strip()
    if value.lower() in ['q', 'quit']:
        print("Exiting to menu.\n")
        return None
    return value

# -------- Add Card --------
def add_card_interactive():
    question = safe_input("Enter question: ")
    if question is None: return

    answer = safe_input("Enter answer: ")
    if answer is None: return

    entry = {
        "question": question,
        "answer": answer,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    if entry not in flashcards:
        flashcards.append(entry)
        save_cards(flashcards)
        print("Card saved.\n")
    else:
        print("Duplicate skipped.\n")

# -------- Display --------
def show_cards(cards):
    if not cards:
        print("No cards.\n")
        return
    print(f"Total cards: {len(cards)}\n")
    for entry in cards:
        print("-" * 30)
        print(f"Time: {entry['timestamp']}")
        print(f"Q: {entry['question']}")
        print(f"A: {entry['answer']}")
        print("-" * 30)

# -------- Search --------
def search_cards(cards, keyword):
    keyword = keyword.lower()
    found = False
    for entry in cards:
        if keyword in entry['question'].lower() or keyword in entry['answer'].lower():
            print("-" * 30)
            print(f"Q: {entry['question']}")
            print(f"A: {entry['answer']}")
            print("-" * 30)
            found = True
    if not found:
        print("No matches.\n")

# -------- Edit/Delete --------
def list_cards(cards):
    for i, entry in enumerate(cards):
        print(f"{i}: {entry['question']}")

def edit_card(cards):
    list_cards(cards)
    try:
        idx = int(input("Select card #: "))
        field = input("Edit (question/answer): ").lower()
        if field in cards[idx]:
            new_val = safe_input("New value: ")
            if new_val:
                cards[idx][field] = new_val
                save_cards(cards)
                print("Updated.\n")
    except:
        print("Invalid selection.\n")

def delete_card(cards):
    list_cards(cards)
    try:
        idx = int(input("Delete #: "))
        removed = cards.pop(idx)
        save_cards(cards)
        print(f"Deleted: {removed['question']}\n")
    except:
        print("Invalid.\n")

# -------- Sorting --------
def sort_by_time(cards):
    show_cards(sorted(cards, key=lambda x: x['timestamp'], reverse=True))

def sort_by_question(cards):
    show_cards(sorted(cards, key=lambda x: x['question'].lower()))

# -------- Stats --------
def show_stats(cards):
    print(f"\nTotal cards: {len(cards)}\n")

# -------- Export --------
def export_cards(cards, keyword=None, filename='export.json'):
    if keyword:
        keyword = keyword.lower()
        filtered = [c for c in cards if keyword in c['question'].lower() or keyword in c['answer'].lower()]
    else:
        filtered = cards

    if not filtered:
        print("No data to export.\n")
        return

    with open(filename, 'w') as file:
        json.dump(filtered, file, indent=4)

    print(f"{len(filtered)} cards exported.\n")

# -------- Quiz Mode --------
def save_score(entry, filename='scores.json'):
    try:
        with open(filename, 'r') as file:
            scores = json.load(file)
    except:
        scores = []

    scores.append(entry)

    with open(filename, 'w') as file:
        json.dump(scores, file, indent=4)

def quiz_mode(cards):
    if not cards:
        print("No cards.\n")
        return

    try:
        num = int(input("How many questions? "))
    except:
        print("Invalid.\n")
        return

    score = 0

    for i in range(num):
        print(f"\nQuestion {i+1}/{num} (q to quit)")
        card = random.choice(cards)

        print(f"Q: {card['question']}")
        ans = input("Your answer: ").lower()

        if ans == 'q':
            break

        if ans in card['answer'].lower():
            print("Correct")
            score += 1
        else:
            print(f"Wrong. A: {card['answer']}")

    print(f"\nScore: {score}/{num}")

    save_score({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "score": score,
        "total": num
    })

# -------- Analytics --------
def show_history():
    try:
        with open('scores.json') as f:
            scores = json.load(f)
    except:
        print("No history.\n")
        return

    for s in scores:
        print(f"{s['timestamp']} - {s['score']}/{s['total']}")

def show_average():
    try:
        scores = json.load(open('scores.json'))
    except:
        print("No data.\n")
        return

    total = sum(s['score'] for s in scores)
    count = sum(s['total'] for s in scores)

    print(f"Average: {total/count:.2%}\n")

# -------- Main --------
flashcards = load_cards()

while True:
    banner = """⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀⠀⠀⠀⠀⠀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡿⠇⠀⠀⠀⠀⢻⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡇⠀⠀⠀⠀⡸⣞⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠃⠀⠀⠀⢀⣧⢿⣽⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢴⣿⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⣼⣞⡿⣞⡅⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠓⢤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⠀⠀⠀⣰⣟⢾⣽⢫⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣠⢤⣶⡻⣞⣿⣺⢯⣽⣳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⢠⣄⡀⠀⠀⠀⠀⠙⢦⡀⠀⠀⠀⠀⣀⣠⣤⣿⣽⣻⢾⣽⣷⣾⣽⣻⣞⣷⣳⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⣶⣄⡀⠀⠀⠀⣉⣲⣴⢶⣞⡿⣽⣞⡷⣯⢿⡽⣞⣿⠟⠋⠁⠉⠈⠳⣟⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⢶⣾⣿⡽⣯⣟⡾⣽⡷⣯⣟⡽⡾⣽⡯⠁⠀⠀⠀⠀⠀⠀⢮⣭⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⢞⣿⣿⢯⡿⣿⣯⣟⣷⣯⢿⣳⣟⡷⣽⣼⣻⣽⠀⠀⠀⠀⠀⠀⠀⢀⣼⡯⡗⠋⠤⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢾⣿⣿⣯⣽⣾⣿⣾⣗⡿⣯⡷⣯⣟⡷⣞⣼⣿⣀⠀⠀⠀⠀⢀⣠⡿⣏⡗⠈⠐⠈⠅⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⠛⠏⠉⠉⠽⢟⢿⣿⣿⣿⣿⣷⣻⢾⡽⣞⡷⠄⡹⣶⢿⣻⢿⣻⡽⢯⣼⢦⠶⠁⠈⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣯⠇⠀⠀⠀⠀⠀⠁⣽⣿⣿⣿⣷⣯⣿⣽⣛⡦⠀⠀⢩⣿⣹⢯⣷⢻⣟⠺⢣⡖⣘⠤⠓⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢈⣿⡃⠁⠀⠀⠀⢀⣤⣾⣟⢿⣻⣿⣿⣟⡾⣽⡳⠄⠎⢳⣯⢯⣟⡾⢯⣞⣯⣓⠉⢀⠀⠀⡄⢢⡀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣷⣷⣶⣳⣶⣺⣿⣿⣳⢯⣟⣿⣿⣳⢯⠛⠅⠃⠀⠀⣴⣿⡿⣬⢶⠾⠙⣊⣥⠾⡒⠊⢁⢠⠣⣌⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢺⡽⣾⡽⣯⣟⣿⡿⣯⣿⣿⣾⢿⣿⠳⢏⣈⢠⠀⠀⣰⢿⡿⣽⣉⡶⠌⠋⠉⣀⡀⠁⠀⠀⠀⣘⡐⣂⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣽⣳⣟⣳⣟⣾⣽⣿⣿⣿⣿⣿⣦⣜⡻⡽⠆⠧⣴⡟⣯⢟⡳⣭⠲⠄⠐⠀⠀⠀⠈⠁⠉⠑⢊⡕⢃⠄⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣾⣿⣯⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣾⢧⠀⠹⠾⡵⡞⡽⢢⣃⠐⠀⠀⠄⡐⠀⠀⠀⡘⢦⠘⣌⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠹⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢯⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠒⡈⠀⡀⠄⡑⠢⣉⠴⣈⣆
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢯⣏⡴⣶⣵⣢⢤⢠⡀⡄⢠⠐⡰⢌⡱⠀⡁⡀⠆⡥⠆⡥⣛⡽⣾
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠔⠉⠀⠀⢽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣼⣻⢷⣯⡽⣞⣷⣻⡼⣡⢋⡔⠣⠜⡐⢐⠠⡓⣤⣙⣲⣽⣻⢷
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡿⣽⣞⣷⣻⡴⣣⢜⡱⣊⡕⣊⠠⡙⡰⣭⢷⣯⣿⢿"""

    print(banner)
    print("\n=== Flashcards ===")
    print("[1:add] [2:edit] [3:delete] [4:show] [5:search]")
    print("[6:time] [7:question] [8:stats] [9:export]")
    print("[10:quiz] [11:history] [12:avg] [13:quit]")

    choice = input("Select: ")

    if choice == '1': add_card_interactive(), input("\nPress Enter to return to menu…")
    elif choice == '2': edit_card(flashcards), input("\nPress Enter to return to menu…")
    elif choice == '3': delete_card(flashcards), input("\nPress Enter to return to menu…")
    elif choice == '4': show_cards(flashcards), input("\nPress Enter to return to menu…")
    elif choice == '5': search_cards(flashcards, input("Keyword: ")), input("\nPress Enter to return to menu…")
    elif choice == '6': sort_by_time(flashcards), input("\nPress Enter to return to menu…")
    elif choice == '7': sort_by_question(flashcards), input("\nPress Enter to return to menu…")
    elif choice == '8': show_stats(flashcards), input("\nPress Enter to return to menu…")
    elif choice == '9': export_cards(flashcards, input("Keyword (optional): ")), input("\nPress Enter to return to menu…")
    elif choice == '10': quiz_mode(flashcards), input("\nPress Enter to return to menu…")
    elif choice == '11': show_history(), input("\nPress Enter to return to menu…")
    elif choice == '12': show_average(), input("\nPress Enter to return to menu…")
    elif choice == '13':
        save_cards(flashcards)
        print("Saved. Exiting.")
        break
    else:
        print("Invalid option.")