import random # თამაშის შემთხვევითი ელემენტების შესაქმნელად
import os # ფაილური ოპერაციების სამართავად
import json  # JSON ფაილებით სამუშაოდ

# ჰენგმენის კლასის განსაზღვრა (სადაც თამაშის ლოგიკას აღვწერ)
class Hangman:
    def __init__(self, word_list, max_attempts=5): #არჩეული სიტყვა მოდის word_list-დან შემთხვევითობის პრინციპით, განვსაზღვრე მაქსიმალური ცდები
        self.word = random.choice(word_list).lower()  # ვირჩევ შემთხვევით სიტყვას გადმოცემული სიტყვების სიიდან და ვაქცევ პატარა ასოებად
        self.max_attempts = max_attempts  # ვადგენ ცდების მაქსიმალურ რაოდენობას, რაც მოთამაშეს ექნება
        self.attempts_left = max_attempts  # ვაყენებ დარჩენილი ცდების საწყის რაოდენობას მაქსიმალურ ცდებზე
        self.guessed_letters = []  # ვქმნი ცარიელ სიას, რომელშიც მოთამაშის მიერ გამოცნობილი ასოები მექნება შენახული
        self.hidden_word = ["_" for _ in self.word]  # ვქმნი ჩაფიქრებულ სიტყვას ქვედა ტირეების სახით

    def display_word(self):
        # აჩვენებს მოთამაშეს მიმდინარე მდგომარეობას სიტყვას, სადაც თითოეული ასო გამოყოფილია სფეისებით (.join მეთოდი იღებს self.hidden_word სიის ყველა ელემენტს და აერთიანებს მათ ერთ ლაინზე, თითოეულ ელემენტს შორის სფეისით)
        return " ".join(self.hidden_word)

    def guess_letter(self, letter):
        # ამოწმებს მოთამაშის მიერ არჩეულ ასოს: ასო სწორია თუ არა,ანახლებს დარჩენილი ცდების რაოდენობას და ანახლებს სიტყვას
        if letter in self.guessed_letters:
            # თუ მოთამაშე მეორედ აირჩევს არჩეულ ასოს, ასე შევატყობინებ
            print("You already guessed that letter!")
            return
        self.guessed_letters.append(letter)  # გამოცნობილი ასოს დამატება, გამოცნობილი ასოების სიაში

        if letter in self.word:
            # თუ ასო სიტყვაშია, განსაზღვრავს ასოს მდებარეობას
            print(f"Good guess! {letter} is in the word.")
            for i, l in enumerate(self.word):
                if l == letter:
                    self.hidden_word[i] = letter
        else:
            # თუ მითითებული ასო არ არის სიტყვაში, შეამცირებს მცდელობებს და შეატყობინებს ამას მოთამაშეს
            self.attempts_left -= 1
            print(f"Wrong guess! {letter} is not in the word.")
            print(f"Attempts left: {self.attempts_left}")

    def is_word_guessed(self):
        # ამოწმებს დარჩა თუ არა ქვედა ტირე სიტყვაში (ანუ გამოცნობილია სრულად თუ არა)
        return "_" not in self.hidden_word

    def save_game(self, filename="hangman_save.json"):
        # შევინახავ თამაშის მიმდინარე მდგომარეობას ფაილში, შემდგომი გაგრძელებისთვის
        game_data = {
            "word": self.word,
            "attempts_left": self.attempts_left,
            "guessed_letters": self.guessed_letters,
            "hidden_word": self.hidden_word
        }
        with open(filename, "w") as file:
            json.dump(game_data, file, indent=4)  # თამაშის მონაცემების JSON ფაილში შენახვა
        print("Game saved!")  # შეტყობინება მოთამაშეს რომ თამაში შენახულია

    def load_game(self, filename="hangman_save.json"):
        # შენახული თამაშის ჩატვირთვა, რათა მოთამაშემ გააგრძელოს თამაში
        if not os.path.exists(filename):
            # თუ ფაილი წაშლილია/არ არსებობს, შეატყობინებს მოთამაშეს
            print("No saved game found.")
            return
        with open(filename, "r") as file:
            game_data = json.load(file)  # JSON ფაილიდან თამაშის მონაცემების წაკითხვა
            self.word = game_data["word"]
            self.attempts_left = game_data["attempts_left"]
            self.guessed_letters = game_data["guessed_letters"]
            self.hidden_word = game_data["hidden_word"]
        print("Game loaded!")  # მოთამაშეს მიაწვდის ინფორმაციას რომ თამაში ჩაიტვირთა

def main():
    # მთავარი ფუნქცია , რომელიც მართავს მთელ თამაშის პროცესს
    words = ["khachapuri","lobiani","khinkali","mtsvadi","elarji"] # სიტყვების სია, საიდანაც შემთხვევითობის პრონციპით მოხდება სიტყვის არჩევა
    hangman = Hangman(words)  # ახალი hangman ობიექტის შექმნა

    # მისასალმებელი სიტყვა და ზოგადი ინსტრუქცია
    print("\nWelcome to Georgian Hangman!")
    print(f"You have {hangman.max_attempts} attempts to guess GEORGIAN FOOD <3")

    # მთავარი ციკლი, რომელიც თამაშოს ბოლომდე გაგრძელდება
    while hangman.attempts_left > 0 and not hangman.is_word_guessed():
        # დაუპრინტავს სიტყვის მიმდინარე მდგომარეობას, დარჩენილ ცდებს და გამოცნობილ ასოებს
        print(f"\n Word: {hangman.display_word()}\n")
        print(f"Attempts left: {hangman.attempts_left}")
        print(f"Guessed letters: {', '.join(hangman.guessed_letters)}")

        # სთხოვს მოთამაშეს ასოს გამოცნობას
        guess = input("Guess a letter: ").lower()
        if len(guess) != 1 or not guess.isalpha():
            # ვამოწმებთ რომ მოთამაშემ შეიყვანოს მხოლოდ ასო, და ისიც ერთი
            print("Invalid input! Please enter a letter (just one)")
            continue

        hangman.guess_letter(guess)  # მიმართავს Hangman ობიექტს, რომ შეამოწმოს მოთამაშის მითითებული ასო

    # თამაშის დასასრულის ტექსტი მოთამაშისთვის მოგების ან/და წაგების შემთხვევაში
    if hangman.is_word_guessed():
        print(f"\nCongratulations! You guessed the word: {hangman.word}")
    else:
        print(f"\nGame over! The word was: {hangman.word}")


# თამაშის გაშვება (თუ სკრიპტი სწორადაა დაწერილი)
if __name__ == "__main__":
    main()
