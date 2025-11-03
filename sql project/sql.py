import sqlite3
import tkinter as tk
from tkinter import messagebox

# --- Database Setup ---
conn = sqlite3.connect("questions.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    option1 TEXT NOT NULL,
    option2 TEXT NOT NULL,
    option3 TEXT NOT NULL,
    option4 TEXT NOT NULL,
    answer TEXT NOT NULL
)
""")
conn.commit()

# Pre-fill SQL questions if table is empty
sql_questions = [
    ("Which SQL statement is used to extract data from a database?", "GET", "SELECT", "EXTRACT", "OPEN", "SELECT"),
    ("Which SQL statement is used to delete data from a table?", "REMOVE", "DELETE", "DROP", "ERASE", "DELETE"),
    ("Which keyword is used to sort the result-set in ascending order?", "SORT", "ORDER BY", "GROUP BY", "ASCENDING", "ORDER BY"),
    ("Which statement is used to add a new record to a table?", "INSERT INTO", "ADD RECORD", "UPDATE", "NEW ROW", "INSERT INTO"),
    ("Which SQL clause is used to filter the results?", "WHERE", "HAVING", "FILTER", "GROUP BY", "WHERE")
]
cursor.execute("SELECT COUNT(*) FROM questions")
if cursor.fetchone()[0] == 0:
    cursor.executemany("INSERT INTO questions (question, option1, option2, option3, option4, answer) VALUES (?, ?, ?, ?, ?, ?)", sql_questions)
    conn.commit()

# --- Main Window ---
def open_admin_window():
    admin_window = tk.Toplevel()
    admin_window.title("Admin Panel")
    admin_window.geometry("500x400")

    tk.Label(admin_window, text="Admin Panel", font=("Helvetica", 16, "bold")).pack(pady=10)

    def add_question():
        q_win = tk.Toplevel(admin_window)
        q_win.title("Add Question")
        q_win.geometry("400x400")
        tk.Label(q_win, text="Enter Question:").pack()
        question_entry = tk.Entry(q_win, width=50)
        question_entry.pack(pady=5)

        options = []
        for i in range(1, 5):
            tk.Label(q_win, text=f"Option {i}:").pack()
            opt = tk.Entry(q_win, width=40)
            opt.pack(pady=3)
            options.append(opt)

        tk.Label(q_win, text="Correct Answer:").pack()
        answer_entry = tk.Entry(q_win, width=40)
        answer_entry.pack(pady=5)

        def save_question():
            question = question_entry.get()
            opts = [o.get() for o in options]
            answer = answer_entry.get()
            if not question or "" in opts or not answer:
                messagebox.showerror("Error", "All fields are required")
                return
            cursor.execute("INSERT INTO questions (question, option1, option2, option3, option4, answer) VALUES (?, ?, ?, ?, ?, ?)",
                           (question, opts[0], opts[1], opts[2], opts[3], answer))
            conn.commit()
            messagebox.showinfo("Success", "Question added!")
            q_win.destroy()

        tk.Button(q_win, text="Save Question", command=save_question, bg="green", fg="white").pack(pady=10)

    def view_questions():
        view_win = tk.Toplevel(admin_window)
        view_win.title("All Questions")
        view_win.geometry("600x400")
        cursor.execute("SELECT * FROM questions")
        records = cursor.fetchall()
        text = tk.Text(view_win, width=80, height=25)
        text.pack()
        for r in records:
            text.insert(tk.END, f"ID:{r[0]} Q:{r[1]} Options: {r[2]}, {r[3]}, {r[4]}, {r[5]} Answer:{r[6]}\n\n")

    tk.Button(admin_window, text="Add Question", command=add_question, width=20, bg="blue", fg="white").pack(pady=5)
    tk.Button(admin_window, text="View Questions", command=view_questions, width=20, bg="purple", fg="white").pack(pady=5)

# --- Quiz Window ---
def start_quiz():
    cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()
    if not questions:
        messagebox.showinfo("Info", "No questions available!")
        return

    quiz_window = tk.Toplevel()
    quiz_window.title("SQL Quiz")
    quiz_window.geometry("700x400")

    score = tk.IntVar(value=0)
    q_index = tk.IntVar(value=0)
    selected_answer = tk.StringVar()

    def show_question():
        idx = q_index.get()
        if idx >= len(questions):
            messagebox.showinfo("Quiz Completed", f"You scored {score.get()} out of {len(questions)}")
            quiz_window.destroy()
            return

        q = questions[idx]
        question_label.config(text=f"Q{idx+1}: {q[1]}")
        selected_answer.set(None)
        for i, opt in enumerate([q[2], q[3], q[4], q[5]]):
            radio_buttons[i].config(text=opt, value=opt)

    def next_question():
        idx = q_index.get()
        q = questions[idx]
        if selected_answer.get() == q[6]:
            score.set(score.get() + 1)
        q_index.set(idx + 1)
        show_question()

    question_label = tk.Label(quiz_window, text="", font=("Helvetica", 14), wraplength=600)
    question_label.pack(pady=20)

    radio_buttons = []
    for i in range(4):
        rb = tk.Radiobutton(quiz_window, text="", variable=selected_answer, value="", font=("Helvetica", 12))
        rb.pack(anchor='w', padx=50, pady=5)
        radio_buttons.append(rb)

    tk.Button(quiz_window, text="Next", command=next_question, bg="green", fg="white").pack(pady=20)

    show_question()

# --- Main GUI ---
root = tk.Tk()
root.title("📚 SQL Question Bank System")
root.geometry("400x300")

tk.Label(root, text="SQL Question Bank", font=("Helvetica", 18, "bold")).pack(pady=20)
tk.Button(root, text="Start Quiz", command=start_quiz, width=20, bg="orange", fg="white").pack(pady=10)
tk.Button(root, text="Admin Panel", command=open_admin_window, width=20, bg="blue", fg="white").pack(pady=10)

root.mainloop()
