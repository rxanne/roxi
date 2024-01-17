import tkinter as tk
from tkinter import messagebox
import requests
from html import unescape

class TRIV:
    def __init__(self, root):
        self.root = root
        self.root.title("TRIV")

        self.setup_gui()

        self.correct_answer = ""
        self.correct_score = 0
        self.asked_count = 0
        self.total_question = 10


        self.load_question()

    def setup_gui(self):
        self.wrapper = tk.Frame(self.root, bg="white", padx=40, pady=30)
        self.wrapper.pack()

        self.quiz_title = tk.Label(self.wrapper, text="TRIV", font=("Poppins", 20))
        self.quiz_title.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        self.quiz_score = tk.Label(self.wrapper, text="0/0", font=("Poppins", 12), fg="#8854C0")
        self.quiz_score.grid(row=1, column=1, sticky="e")

        self.quiz_question = tk.Label(self.wrapper, text="", font=("Poppins", 14), justify="center")
        self.quiz_question.grid(row=2, column=0, columnspan=2, pady=20)

        self.quiz_options = tk.Listbox(self.wrapper, selectmode=tk.SINGLE, font=("Poppins", 12), height=4, bd=3, relief="solid")
        self.quiz_options.grid(row=3, column=0, columnspan=2, pady=10)

        self.result_label = tk.Label(self.wrapper, text="", font=("Poppins", 14), fg="#8854C0")
        self.result_label.grid(row=4, column=0, columnspan=2, pady=10)

        self.check_button = tk.Button(self.wrapper, text="Check Answer", command=self.check_answer)
        self.check_button.grid(row=5, column=0, pady=10)

        self.play_again_button = tk.Button(self.wrapper, text="Play Again!", command=self.restart_quiz)
        self.play_again_button.grid(row=5, column=1, pady=10)


        self.play_again_button.grid_remove()

    def load_question(self):

        api_url = 'https://opentdb.com/api.php?amount=1'
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            question_data = data['results'][0]

            question_text = unescape(question_data['question'])
            options = [unescape(option) for option in question_data['incorrect_answers']] + [unescape(question_data['correct_answer'])]

            self.correct_answer = options[-1]
            self.quiz_question.config(text=question_text)
            self.quiz_options.delete(0, tk.END)
            for index, option in enumerate(options, start=1):
                self.quiz_options.insert(tk.END, f"{index}. {option}")
        else:
            messagebox.showerror("Error", "Failed to fetch question from the API")

    def check_answer(self):
        selected_index = self.quiz_options.curselection()
        if not selected_index:
            messagebox.showinfo("TRIV", "Please select an option!")
            return

        selected_answer = self.quiz_options.get(selected_index[0])

        if selected_answer[3:] == self.correct_answer:
            self.correct_score += 1
            self.result_label.config(text="Correct Answer!", fg="green")
        else:
            self.result_label.config(text=f"Incorrect Answer!\nCorrect Answer: {self.correct_answer}", fg="red")
    
        self.asked_count += 1
        self.quiz_score.config(text=f"{self.correct_score}/{self.asked_count}")

        if self.asked_count == self.total_question:
            self.result_label.config(text=f"Your score is {self.correct_score}.")
            self.check_button.config(state=tk.DISABLED)
            self.play_again_button.grid()

        else:
            self.root.after(300, self.load_question)
    def restart_quiz(self):
        self.correct_score = 0
        self.asked_count = 0
        self.check_button.config(state=tk.NORMAL)
        self.play_again_button.grid_remove()
        self.update_score()
        self.load_question()

if __name__ == "__main__":
    root = tk.Tk()
    app = TRIV(root)
    root.mainloop()