import csv
import random
import os


# ლექსიკონის წაკითხვა CSV ფაილიდან
def read_dictionary_from_csv(filename):
    dictionary = {}
    try:
        with open(filename, mode="r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                dictionary[row["word"]] = row["translation"]
    except FileNotFoundError:
        print(f"ფაილი {filename} ვერ მოიძებნა.")
    return dictionary


# აქტიური ფაილის წაკითხვა
def get_active_dictionary():
    if os.path.exists("active_dictionary.txt"):
        with open("active_dictionary.txt", "r", encoding="utf-8") as file:
            return file.read().strip()
    return None


# აქტიური ფაილის შენახვა
def set_active_dictionary(dictionary_name):
    with open("active_dictionary.txt", "w", encoding="utf-8") as file:
        file.write(dictionary_name)


# დასრულებული ფაილების წაკითხვა
def read_completed_dictionaries():
    completed = []
    if os.path.exists("completed_dictionaries.csv"):
        with open("completed_dictionaries.csv", "r", encoding="utf-8") as file:
            completed = [line.strip() for line in file.readlines()]
    return completed


# აქტიური ფაილის არჩევა იმ ფაილებიდან, რომელიც არ არის დასრულებული
def choose_random_dictionary():
    all_files = [f for f in os.listdir("./dict") if f.endswith(".csv")]
    completed = read_completed_dictionaries()

    # არჩევა იმ ფაილებიდან, რომელიც არ არის დასრულებული
    remaining_files = [f for f in all_files if f not in completed]

    if remaining_files:
        return random.choice(remaining_files)
    else:
        print("ყველა ფაილი უკვე დასრულებულია.")
        return None


# ტესტის ჩატარება
def quiz_user(dictionary):
    score = 0
    words = list(dictionary.keys())
    random.shuffle(words)

    # 5 სიტყვის კითხვა ტესტში
    for word in words[:5]:
        answer = input(f"რა არის '{word}' ქართულად? ")
        if answer.lower() == dictionary[word].lower():
            print("სწორია!")
            score += 1
        else:
            print(f"არასწორია. სწორი პასუხია: {dictionary[word]}")

    print(f"\nთქვენ მიიღეთ {score}/5 ქულა.")
    return score


# ტესტირების შედეგების შემოწმება
def check_completion_status(dictionary_name, score):
    results_file = f"{dictionary_name}_results.txt"

    if score == 5:  # თუ ყველა პასუხი სწორია
        current_streak = read_results_from_file(results_file)
        current_streak += 1
        save_results_to_file(results_file, current_streak)

        if current_streak >= 3:
            print(f"ლექსიკონი '{dictionary_name}' წარმატებით დასრულებულია!")
            mark_as_completed(dictionary_name)
    else:
        print(f"თქვენი მიმდინარე წარმატების სერია განულებულია.")
        save_results_to_file(results_file, 0)


# ლექსიკონის დასრულება
def mark_as_completed(dictionary_name):
    completed_file = "completed_dictionaries.csv"
    with open(completed_file, "a", encoding="utf-8") as file:
        file.write(f"{dictionary_name}\n")
    os.remove("active_dictionary.txt")  # აქტიური ფაილის გაუქმება


# შედეგების წაკითხვა და შენახვა
def read_results_from_file(results_file):
    if os.path.exists(results_file):
        with open(results_file, "r", encoding="utf-8") as file:
            return int(file.read().strip())
    return 0


def save_results_to_file(results_file, score):
    with open(results_file, "w", encoding="utf-8") as file:
        file.write(str(score))


# მთავარი ფუნქცია
def main():
    active_dict = get_active_dictionary()

    if not active_dict:  # თუ აქტიური ფაილი არ არსებობს
        active_dict = choose_random_dictionary()
        if active_dict:
            set_active_dictionary(active_dict)
            print(f"\nლექსიკონი '{active_dict}' გახდა აქტიური.")
        else:
            print("მეტი ხელმისაწვდომი ფაილი არ არსებობს.")
            return

    # ლექსიკონის წაკითხვა
    dictionary = read_dictionary_from_csv(f"./dict/{active_dict}")

    if dictionary:
        score = quiz_user(dictionary)
        check_completion_status(active_dict, score)
    else:
        print(f"ლექსიკონი '{active_dict}' ცარიელია ან ფაილში შეცდომაა.")


if __name__ == "__main__":
    main()
