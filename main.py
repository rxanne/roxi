import tkinter as ap
from tkinter import messagebox
import requests
from html import unescape

class TRIV:
    def __init__(my, root):
        my.root = root
        my.root.title("TRIV")

        my.setup_gui()

        my.correct_answer = ""
        my.correct_score = 0
        my.asked_count = 0
        my.total_question = 10


        my.load_question()

    def setup_gui(my):
        my.wrapper = ap.Frame(my.root, bg="white", padx=40, pady=30)
        my.wrapper.pack()

        my.title = ap.Label(my.wrapper, text="TRIV", font=("Poppins", 20))
        my.title.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        my.score = ap.Label(my.wrapper, text="0/0", font=("Poppins", 12), fg="#8854C0")
        my.score.grid(row=1, column=1, sticky="e")

        my.question = ap.Label(my.wrapper, text="", font=("Poppins", 14), justify="center")
        my.question.grid(row=2, column=0, columnspan=2, pady=20)

        my.options = ap.Listbox(my.wrapper, selectmode=ap.SINGLE, font=("Poppins", 12), height=4, bd=3, relief="solid")
        my.options.grid(row=3, column=0, columnspan=2, pady=10)

        my.result = ap.Label(my.wrapper, text="", font=("Poppins", 14), fg="#8854C0")
        my.result.grid(row=4, column=0, columnspan=2, pady=10)

        my.check_button = ap.Button(my.wrapper, text="Check Answer", command=my.check_answer)
        my.check_button.grid(row=5, column=0, pady=10)

        my.again = ap.Button(my.wrapper, text="Play Again!", command=my.restart_quiz)
        my.again.grid(row=5, column=1, pady=10)


        my.again.grid_remove()

    def load_question(my):

        api_url = 'https://opentdb.com/api.php?amount=1'
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            question_data = data['results'][0]

            question_text = unescape(question_data['question'])
            options = [unescape(option) for option in question_data['incorrect_answers']] + [unescape(question_data['correct_answer'])]

            my.correct_answer = options[-1]
            my.question.config(text=question_text)
            my.options.delete(0, ap.END)
            for index, option in enumerate(options, start=1):
                my.options.insert(ap.END, f"{index}. {option}")
        else:
            messagebox.showerror("Error", "Failed to fetch question from the API")

    def check_answer(my):
        selected_index = my.options.curselection()
        if not selected_index:
            messagebox.showinfo("TRIV", "Please select an option!")
            return

        selected_answer = my.options.get(selected_index[0])

        if selected_answer[3:] == my.correct_answer:
            my.correct_score += 1
            my.result.config(text="Correct Answer!", fg="green")
        else:
            my.result.config(text=f"Incorrect Answer!\nCorrect Answer: {my.correct_answer}", fg="red")
    
        my.asked_count += 1
        my.score.config(text=f"{my.correct_score}/{my.asked_count}")

        if my.asked_count == my.total_question:
            my.result.config(text=f"Your score is {my.correct_score}.")
            my.check_button.config(state=ap.DISABLED)
            my.again.grid()

        else:
            my.root.after(300, my.load_question)
    def restart_quiz(my):
        my.correct_score = 0
        my.asked_count = 0
        my.check_button.config(state=ap.NORMAL)
        my.again.grid_remove()
        my.update_score()
        my.load_question()

if __name__ == "__main__":
    root = ap.Tk()
    app = TRIV(root)
    root.mainloop()