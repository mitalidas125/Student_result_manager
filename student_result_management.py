import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os

# Constants
CSV_FILE = 'student_data.csv'
COLUMNS = ["Roll", "Name", "Math", "Science", "English", "Total", "Average", "Grade"]

# Create file if not exists
if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=COLUMNS).to_csv(CSV_FILE, index=False)

# Grade calculator
def get_grade(avg):
    if avg >= 90: return "A+"
    elif avg >= 80: return "A"
    elif avg >= 70: return "B"
    elif avg >= 60: return "C"
    else: return "F"

# Submit data
def submit():
    try:
        roll = roll_entry.get().strip()
        name = name_entry.get().strip()
        math = float(math_entry.get())
        science = float(science_entry.get())
        english = float(english_entry.get())

        if not roll or not name:
            raise ValueError("Roll and Name cannot be empty!")

        if not (0 <= math <= 100 and 0 <= science <= 100 and 0 <= english <= 100):
            raise ValueError("Marks must be between 0 and 100.")

        df_existing = pd.read_csv(CSV_FILE)
        if roll in df_existing['Roll'].astype(str).values:
            messagebox.showerror("Error", "This Roll Number already exists!")
            return

        total = math + science + english
        average = round(total / 3, 2)
        grade = get_grade(average)

        df_new = pd.DataFrame([[roll, name, math, science, english, total, average, grade]], columns=COLUMNS)
        df_new.to_csv(CSV_FILE, mode='a', header=False, index=False)

        messagebox.showinfo("Success", f"Student data saved!\nGrade: {grade}")
        clear_entries()

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Clear fields
def clear_entries():
    for entry in [roll_entry, name_entry, math_entry, science_entry, english_entry]:
        entry.delete(0, tk.END)

# Show all records
def show_students():
    try:
        df = pd.read_csv(CSV_FILE)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, df.to_string(index=False))
    except Exception as e:
        output_text.insert(tk.END, f"Error loading file:\n{e}")

# Search by roll no
def search_student():
    roll = search_entry.get().strip()
    if not roll:
        messagebox.showerror("Error", "Please enter a Roll Number.")
        return

    try:
        df = pd.read_csv(CSV_FILE)
        df['Roll'] = df['Roll'].astype(str)  # Important fix
        result = df[df['Roll'] == roll]
        output_text.delete(1.0, tk.END)
        if not result.empty:
            output_text.insert(tk.END, result.to_string(index=False))
        else:
            output_text.insert(tk.END, f"No student found with Roll No: {roll}")
    except Exception as e:
        output_text.insert(tk.END, f"Error:\n{e}")

# GUI setup
root = tk.Tk()
root.title("📘 Student Result Manager")
root.geometry("750x600")
root.resizable(False, False)

# Input fields
labels = ["Roll No", "Name", "Math Marks", "Science Marks", "English Marks"]
entry_list = []

for i, label in enumerate(labels):
    tk.Label(root, text=label, font=('Arial', 12)).grid(row=i, column=0, padx=10, pady=5, sticky='w')

roll_entry = tk.Entry(root, width=30)
name_entry = tk.Entry(root, width=30)
math_entry = tk.Entry(root, width=30)
science_entry = tk.Entry(root, width=30)
english_entry = tk.Entry(root, width=30)

entry_list = [roll_entry, name_entry, math_entry, science_entry, english_entry]
for i, entry in enumerate(entry_list):
    entry.grid(row=i, column=1, padx=10, pady=5)

# Buttons
tk.Button(root, text="Submit", width=15, command=submit, bg="#4CAF50", fg="white").grid(row=5, column=1, pady=10)
tk.Button(root, text="Clear", width=15, command=clear_entries).grid(row=5, column=0, pady=10)
tk.Button(root, text="Show All Students", width=30, command=show_students, bg="#2196F3", fg="white").grid(row=6, column=0, columnspan=2, pady=10)

# Search section
tk.Label(root, text="Search by Roll No:", font=('Arial', 11)).grid(row=7, column=0, pady=5, padx=10, sticky='w')
search_entry = tk.Entry(root, width=30)
search_entry.grid(row=7, column=1, pady=5)
tk.Button(root, text="Search", command=search_student).grid(row=7, column=2, padx=5)

# Output area with scrollbar
output_text = tk.Text(root, width=85, height=15, wrap=tk.WORD)
output_text.grid(row=8, column=0, columnspan=3, padx=10, pady=10)

scrollbar = tk.Scrollbar(root, command=output_text.yview)
scrollbar.grid(row=8, column=3, sticky='ns', pady=10)
output_text.config(yscrollcommand=scrollbar.set)

# Start GUI
root.mainloop()
