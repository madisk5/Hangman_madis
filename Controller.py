
from GameTime import GameTime
from Model import Model
from View import View, draw_scoreboard, show_message
from tkinter import simpledialog


class Controller:
    def __init__(self, db_name=None):
        self.__model = Model()
        self.__view = View(self, self.__model)
        if db_name is not None:
            self.__model.database = db_name
        self.__game_time = GameTime(self.__view.lbl_time)

    def main(self):
        self.__view.main()

    def btn_scoreboard_click(self):
        window = self.__view.create_scoreboard_window()
        data = self.__model.read_scores_data()
        draw_scoreboard(window, data)

    def buttons_to_game(self):
        self.__view.btn_new['state'] = 'disabled'
        self.__view.btn_cancel['state'] = 'normal'
        self.__view.btn_send['state'] = 'normal'
        self.__view.char_input['state'] = 'normal'
        self.__view.char_input.focus()

    def btn_new_click(self):
        self.buttons_to_game()
        self.__view.change_image(0)
        self.__model.setup_new_game()
        self.__view.lbl_result.config(text=self.__model.hidden_word)
        self.__view.lbl_error.config(text='Vigased tähed:', fg='blue')
        self.__game_time.reset()
        self.__game_time.start()

    def btn_cancel_click(self):
        self.__game_time.stop()
        self.__view.change_image(-1)
        self.buttons_no_game()
        self.__view.lbl_result.config(text='MÄNGIME?')
    def buttons_no_game(self):
        self.__view.btn_new['state'] = 'normal'
        self.__view.btn_cancel['state'] = 'disabled'
        self.__view.btn_send['state'] = 'disabled'
        self.__view.char_input.delete(0, 'end')
        self.__view.char_input['state'] = 'disabled'

    def btn_send_click(self):

        print(self.__model.wrong_guesses)
        if self.__model.wrong_guesses >= 10:
            print('Kaotasid!')
            self.btn_cancel_click()
            show_message('lose')
            return

        print(self.__view.char_input.get())

        self.__model.process_user_input(self.__view.char_input.get())
        print(self.__model.hidden_word)
        self.__view.lbl_result.config(text=self.__model.hidden_word)
        vigased = "Vigased tähed: " + self.__model.get_wrong_guesses_as_string()
        self.__view.lbl_error.config(text=vigased, fg="blue")
        self.__view.char_input.delete(0, 'end')
        self.__view.change_image(self.__model.wrong_guesses)

        if self.__model.hidden_word == self.__model.random_word:
            print('Võitsid!')
            self.btn_cancel_click()
            show_message('won')
            player_name = simpledialog.askstring("Sisesta nimi:", "Sisesta oma nimi:")
            if player_name:
                self.__model.add_player_score(player_name, self.__game_time.counter)
                return
