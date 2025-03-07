from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, NumericProperty
from kivy.animation import Animation
import random

class MainMenu(Screen):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        layout.add_widget(Label(text="Nano Games", font_size='40sp', bold=True))
        layout.add_widget(Button(text="Number Guessing Game", on_press=self.start_number_guessing, font_size='20sp', background_color=(0.2, 0.6, 0.8, 1)))
        layout.add_widget(Button(text="Stone-Paper-Scissor", on_press=self.start_stone_paper_scissor, font_size='20sp', background_color=(0.2, 0.6, 0.8, 1)))
        layout.add_widget(Button(text="Quit", on_press=self.quit_app, font_size='20sp', background_color=(0.8, 0.2, 0.2, 1)))
        self.add_widget(layout)

    def start_number_guessing(self, instance):
        self.manager.current = 'number_guessing'

    def start_stone_paper_scissor(self, instance):
        self.manager.current = 'stone_paper_scissor'

    def quit_app(self, instance):
        App.get_running_app().stop()

class NumberGuessingGame(Screen):
    result_text = StringProperty("")
    attempts = NumericProperty(0)

    def __init__(self, **kwargs):
        super(NumberGuessingGame, self).__init__(**kwargs)
        self.g_number = random.randint(1, 100)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        self.layout.add_widget(Label(text="Number Guessing Game", font_size='30sp', bold=True))
        self.info_label = Label(text="Type your guess below, then press Submit to confirm, or press Back to quit.")
        self.layout.add_widget(self.info_label)
        self.input = TextInput(multiline=False, font_size='20sp')
        self.layout.add_widget(self.input)
        self.submit_button = Button(text="Submit", on_press=self.check_guess, font_size='20sp', background_color=(0.2, 0.8, 0.2, 1))
        self.layout.add_widget(self.submit_button)
        self.back_button = Button(text="Back", on_press=self.go_back, font_size='20sp', background_color=(0.8, 0.2, 0.2, 1))
        self.layout.add_widget(self.back_button)
        self.result_label = Label(text="", font_size='20sp')
        self.layout.add_widget(self.result_label)
        self.add_widget(self.layout)

        # Bind the result_text property to the result_label text
        self.result_label.bind(text=self.update_result_label)

    def check_guess(self, instance):
        try:
            guess = int(self.input.text)
            self.attempts += 1
            if guess == self.g_number:
                self.result_text = f"Correct! Attempts: {self.attempts}"
                self.result_label.color = (0, 1, 0, 1)
            elif guess > self.g_number:
                self.result_text = "Too high!"
                self.result_label.color = (1, 0, 0, 1)
            else:
                self.result_text = "Too low!"
                self.result_label.color = (1, 0, 0, 1)
            self.input.text = ""
        except ValueError:
            self.result_text = "Please enter a valid number!"
            self.result_label.color = (1, 0, 0, 1)
            self.input.text = ""

        # Update the result_label text
        self.result_label.text = self.result_text

    def update_result_label(self, instance, value):
        self.result_label.text = value

    def go_back(self, instance):
        self.manager.current = 'main_menu'

class StonePaperScissor(Screen):
    result_text = StringProperty("")
    choice_text = StringProperty("")
    wins = NumericProperty(0)
    losses = NumericProperty(0)

    def __init__(self, **kwargs):
        super(StonePaperScissor, self).__init__(**kwargs)
        self.items = ['stone', 'paper', 'scissor']
        self.player_choice = 0
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        self.layout.add_widget(Label(text="Stone-Paper-Scissor", font_size='30sp', bold=True))
        self.info_label = Label(text="Press the buttons below to choose option, Enter to play, or Back to quit.")
        self.layout.add_widget(self.info_label)
        self.choice_label = Label(text=f"Your choice: {self.items[self.player_choice]}", font_size='20sp')
        self.layout.add_widget(self.choice_label)
        self.result_label = Label(text="", font_size='20sp')
        self.layout.add_widget(self.result_label)
        
        # Add buttons for selection
        self.button_layout = BoxLayout(orientation='horizontal', spacing=10)
        self.button_layout.add_widget(Button(text="Stone", on_press=self.select_stone, font_size='20sp', background_color=(0.6, 0.6, 0.6, 1)))
        self.button_layout.add_widget(Button(text="Paper", on_press=self.select_paper, font_size='20sp', background_color=(0.6, 0.6, 0.6, 1)))
        self.button_layout.add_widget(Button(text="Scissor", on_press=self.select_scissor, font_size='20sp', background_color=(0.6, 0.6, 0.6, 1)))
        self.layout.add_widget(self.button_layout)
        
        self.play_button = Button(text="Play", on_press=self.play_game, font_size='20sp', background_color=(0.2, 0.8, 0.2, 1))
        self.layout.add_widget(self.play_button)
        self.back_button = Button(text="Back", on_press=self.go_back, font_size='20sp', background_color=(0.8, 0.2, 0.2, 1))
        self.layout.add_widget(self.back_button)
        self.add_widget(self.layout)

        # Bind the wins and losses properties to the respective labels
        self.wins_label = Label(text=f"Wins: {self.wins}", font_size='20sp')
        self.losses_label = Label(text=f"Losses: {self.losses}", font_size='20sp')
        self.layout.add_widget(self.wins_label)
        self.layout.add_widget(self.losses_label)
        self.bind(wins=self.update_wins_label)
        self.bind(losses=self.update_losses_label)

    def select_stone(self, instance):
        self.player_choice = 0
        self.choice_label.text = f"Your choice: {self.items[self.player_choice]}"

    def select_paper(self, instance):
        self.player_choice = 1
        self.choice_label.text = f"Your choice: {self.items[self.player_choice]}"

    def select_scissor(self, instance):
        self.player_choice = 2
        self.choice_label.text = f"Your choice: {self.items[self.player_choice]}"

    def play_game(self, instance):
        opponent = random.choice(self.items)
        if opponent == self.items[self.player_choice]:
            result = "Draw!"
            self.result_label.color = (1, 1, 0, 1)
        elif (opponent == 'stone' and self.items[self.player_choice] == 'paper') or \
             (opponent == 'paper' and self.items[self.player_choice] == 'scissor') or \
             (opponent == 'scissor' and self.items[self.player_choice] == 'stone'):
            result = f"You won! Opponent chose {opponent}"
            self.wins += 1
            self.result_label.color = (0, 1, 0, 1)
        else:
            result = f"You lost! Opponent chose {opponent}"
            self.losses += 1
            self.result_label.color = (1, 0, 0, 1)
        self.result_label.text = result
        self.choice_label.text = f"Your choice: {self.items[self.player_choice]}"

    def update_wins_label(self, instance, value):
        self.wins_label.text = f"Wins: {value}"

    def update_losses_label(self, instance, value):
        self.losses_label.text = f"Losses: {value}"

    def go_back(self, instance):
        self.manager.current = 'main_menu'

class NanoGamesApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenu(name='main_menu'))
        sm.add_widget(NumberGuessingGame(name='number_guessing'))
        sm.add_widget(StonePaperScissor(name='stone_paper_scissor'))
        return sm

if __name__ == "__main__":
    NanoGamesApp().run()