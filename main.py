import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox


class HangmanGUI(QWidget):
    def __init__(self, words):
        super().__init__()
        self.words = words
        self.word = ''
        self.max_attempts = 6
        self.attempts_left = self.max_attempts
        self.guessed_letters = set()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.word_label = QLabel()
        layout.addWidget(self.word_label)

        self.guess_label = QLabel("Guess a letter:")
        layout.addWidget(self.guess_label)

        self.guess_input = QLineEdit()
        layout.addWidget(self.guess_input)

        self.guess_button = QPushButton("Guess")
        self.guess_button.clicked.connect(self.make_guess)
        layout.addWidget(self.guess_button)

        self.info_label = QLabel()
        layout.addWidget(self.info_label)

        self.new_game_button = QPushButton("New Game")
        self.new_game_button.clicked.connect(self.new_game)
        layout.addWidget(self.new_game_button)

        self.setLayout(layout)

        self.new_game()

    def new_game(self):
        self.word = random.choice(self.words).lower()
        self.attempts_left = self.max_attempts
        self.guessed_letters = set()

        self.update_word_label()
        self.info_label.setText('')
        self.guess_input.setText('')

    def update_word_label(self):
        display = ''
        for letter in self.word:
            if letter in self.guessed_letters:
                display += letter
            else:
                display += '_'
        self.word_label.setText(display)

    def make_guess(self):
        guess = self.guess_input.text().lower()
        if len(guess) != 1 or not guess.isalpha():
            QMessageBox.warning(self, "Invalid Input", "Please enter a single letter.")
            return

        if guess in self.guessed_letters:
            QMessageBox.warning(self, "Already Guessed", "You've already guessed this letter.")
            return

        self.guessed_letters.add(guess)
        if guess not in self.word:
            self.attempts_left -= 1
            self.info_label.setText(f"Incorrect guess! Attempts left: {self.attempts_left}")
        else:
            self.info_label.setText("Correct guess!")

        self.update_word_label()

        if self.attempts_left <= 0:
            QMessageBox.information(self, "Game Over", f"You ran out of attempts. The word was: {self.word}")
            self.new_game()
        elif self.word == self.word_label.text():
            QMessageBox.information(self, "Congratulations!", f"You guessed the word: {self.word}")
            self.new_game()


if __name__ == '__main__':
    words = ["hangman", "python", "programming", "computer", "code", "game", "player"]

    app = QApplication(sys.argv)
    hangman_game = HangmanGUI(words)
    hangman_game.setWindowTitle("Hangman Game")
    hangman_game.show()
    sys.exit(app.exec_())
