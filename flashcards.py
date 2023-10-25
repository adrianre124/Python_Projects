import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import tempfile
import jellyfish

# Tworzenie pliku tymczasowego
tmp = tempfile.NamedTemporaryFile(mode = "w+t")
tmp.tempdir = "/temp"
tmp.write("Wrong Answers:\n\n")
print(tmp.name)

def main():
    # Wyświetlać instrukcję obsługi po uruchomieniu
    print_start()
    user_input = input("> ")

    # Start pytań
    if (user_input == ':start'):
        start_game(user_input)

    # Wyświetla informacje o udzielanych odpowiedziach w formie wykresu
    if (user_input == ':results'):
        make_chart()

    # Umożliwiać wyjście z programu
    if (user_input == ':quit'):
        exit_game()


def start_game(user_input):
    os.system('cls')
    # Wyświetlać instrukcję obsługi po uruchomieniu
    print_help()
    correctAnswer = 0
    wrongAnswer = 0

    # Wczytywać bazę pytań i odpowiedzi z pliku .json
    with open('questions.json') as f:
        questions = json.load(f)

    # W pętli wyświetlać kolejno pytania i słuchać odpowiedzi użytkownika.
    for question in questions:
        # Wyświetlać obecny wynik użytkownika
        user_input = print_question(question, correctAnswer)

        while True:
            match user_input:
                # Wyświetlać instrukcję obsługi na żądanie użytownika
                case ":help":
                    os.system('cls')
                    print_help()
                    user_input = print_question(question, correctAnswer)
                case ":results":
                    os.system('cls')
                    make_chart()
                    user_input = print_question(question, correctAnswer)
                # Umożliwiać załadowanie pliku tymczasowego
                case ":load":
                    os.system('cls')
                    tmp.seek(0)
                    temp = tmp.read()
                    print(temp)
                    user_input = print_question(question, correctAnswer)
                # Umożliwiać wyjście z programu
                case ":quit":
                    exit_game()
                case _:
                    break
        
        # Wyświetlać poprawność odpowiedzi
        # Uznawać za poprawne odpowiedzi, które są odpowiednio podobne do wzorca
        if (jellyfish.jaro_distance(user_input, question['answer']) >= 0.80):
            # Zliczać poprawne odpowiedzi
            correctAnswer += 1
            print("Correct!")
        else:
            # Zapisywać błędne odpowiedzi w pliku tymczasowym
            write_wrong_answer_to_file(question['question'], user_input)
            # Zliczać błędne odpowiedzi
            wrongAnswer += 1
            print("Wrong!")

        print("Press any key to continue...")
        input()
        # Czyśćić ekran po każdym pytaniu
        os.system('cls')

    write_json({"correctAnswers": [correctAnswer], "wrongAnswers": [wrongAnswer]})
    print("You got", correctAnswer, "points")
    exit(1)

# Wyświetlanie pytania
def print_question(question, correctAnswer):
    print("Wynik: ", correctAnswer)
    print(question['question'])
    return input("> ")

# Zapisywać błędne odpowiedzi w pliku tymczasowym
def write_wrong_answer_to_file(question, answer):
    tmp.write(question + "\n")
    tmp.write("Wrong answer: " + answer + "\n\n")

def write_json(new_data, filename='data.json'):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            file_data = json.load(file)
        file_data['correctAnswers'].append(new_data['correctAnswers'][0])
        file_data['wrongAnswers'].append(new_data['wrongAnswers'][0])
    else:
        file_data = new_data

    with open(filename, "w") as file:
        json.dump(file_data, file)

# Wyświetlać zebrane informacje w formie wykresu
def make_chart(filename='data.json'):
    if os.path.exists('data.json'):
        data = pd.read_json(filename)
        df = pd.DataFrame(data)
        df.plot.line()
        plt.show()
    else:
        print("There's not enough data. Complete Quiz first")

# Wyświetla instukcje po uruchomieniu
def print_start():
    print("************************************")
    print("To start quiz enter ':start'")
    print("To quit quiz enter ':quit'")
    print("To view results history enter ':results'")
    print("************************************")

# Wyświetla instrukcje po wpisaniu :start lub :help
def print_help():
    print("************************************")
    print("To view help enter ':help'")
    print("To view results history enter ':results'")
    print("To view wrong answers you answered enter ':load'")
    print("To quit quiz enter ':quit'")
    print("************************************")

# Wyjście z programu
def exit_game():
    tmp.close()
    exit(1)

if __name__ == "__main__":
    main()


#  Napisz program "Fiszki", który zadaje użytkownikowi pytania, przyjmuje odpowiedź, a następnie sprawdza poprawność podanej odpowiedzi.

# Must:
    # 1. Wyświetlać instrukcję obsługi po uruchomieniu a także na żądanie użytownika (np. po wpisaniu :help)
    # 2. Umożliwiać wyjście z programu (np. po wpisaniu :quit)
    # 3. W pętli wyświetlać kolejno pytania i słuchać odpowiedzi użytkownika.
    # 4. Wyświetlać poprawność odpowiedzi
    # 5. Wczytywać bazę pytań i odpowiedzi z pliku .json

# Should:
    # 1. Czyśćić ekran po każdym pytaniu
    # 2. Zliczać poprawne i błędne odpowiedzi
    # 3. Wyświetlać obecny wynik użytkownika

# Could:
    # 1. Zapisywać błędne odpowiedzi w pliku tymczasowym i umożliwiać jego załadowanie
    # 2. Umożliwiać wyświetlenie możliwych do załadowania plików
    # 3. Umożliwiać wczytanie pliku bez modyfikowania kodu (np. po wpisaniu komendy :load)
    # 4. Uznawać za poprawne odpowiedzi, które są odpowiednio podobne do wzorca (np. z użyciem biblioteki jellyfish i funkcji jaro_distance)
    # 5. Zapisywać informacje o dynamice uczenia się użytkownika przy każdym uruchomieniu
    # 6. Wyświetlać zebrane informacje w formie wykresu
    # 7. Używać ramek danych
