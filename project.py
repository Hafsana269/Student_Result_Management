import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

# 🗃️ Store student records
students = []

# 📊 Grade calculation
def get_grade(avg):
    if avg >= 90: return 'A'
    elif avg >= 80: return 'B'
    elif avg >= 70: return 'C'
    elif avg >= 60: return 'D'
    else: return 'F'

# ➕ Add student record
def add_student():
    name = entry_name.get().strip()
    try:
        m1 = float(entry_math.get())
        m2 = float(entry_sci.get())
        m3 = float(entry_eng.get())
    except ValueError:
        messagebox.showerror("❌ Invalid Input", "Please enter numeric marks.")
        return

    if not name:
        messagebox.showwarning("⚠️ Missing Info", "Please enter student name.")
        return

    students.append({"name": name, "marks": [m1, m2, m3]})
    entry_name.delete(0, tk.END)
    entry_math.delete(0, tk.END)
    entry_sci.delete(0, tk.END)
    entry_eng.delete(0, tk.END)
    update_table()

# 🔄 Refresh table and stats
def update_table():
    for row in table.get_children():
        table.delete(row)

    if not students:
        label_total.config(text="👥 Total Students: 0")
        label_avg.config(text="📊 Class Average: --")
        label_top.config(text="🏆 Top Performer: --")
        label_toppers.config(text="⭐ Subject Toppers: --")
        label_grades.config(text="📦 Grade Summary: --")
        return

    all_marks = np.array([s['marks'] for s in students])
    totals = np.sum(all_marks, axis=1)
    avgs = np.mean(all_marks, axis=1)

    for i, student in enumerate(students):
        m1, m2, m3 = student["marks"]
        total = totals[i]
        avg = avgs[i]
        grade = get_grade(avg)
        table.insert("", "end", values=(student["name"], m1, m2, m3, total, f"{avg:.2f}", grade))

    class_avg = np.mean(avgs)
    label_total.config(text=f"👥 Total Students: {len(students)}")
    label_avg.config(text=f"📊 Class Average: {class_avg:.2f}")
    top_idx = np.argmax(totals)
    label_top.config(text=f"🏆 Top Performer: {students[top_idx]['name']} ({totals[top_idx]} marks)")

    # Subject-wise toppers
    subjects = ["Math", "Science", "English"]
    toppers = []
    for i in range(3):
        top_sub = np.argmax(all_marks[:, i])
        toppers.append(f"{subjects[i]} → {students[top_sub]['name']} ({all_marks[top_sub][i]})")
    label_toppers.config(text="⭐ Subject Toppers:\n" + "\n".join(toppers))

    # Grade summary
    all_grades = [get_grade(avg) for avg in avgs]
    summary = ""
    for g in sorted(set(all_grades)):
        summary += f"{g}: {all_grades.count(g)}   "
    label_grades.config(text=f"📦 Grade Summary: {summary}")

# 🗑️ Delete selected student
def delete_selected():
    selected = table.selection()
    if not selected:
        messagebox.showwarning("No selection", "Please select a student to delete.")
        return
    name = table.item(selected[0])['values'][0]
    students[:] = [s for s in students if s["name"] != name]
    update_table()

# ❌ Clear all records
def clear_all():
    if messagebox.askyesno("Confirm", "Are you sure you want to delete all records?"):
        students.clear()
        update_table()

# 🖼️ GUI setup
root = tk.Tk()
root.title("🎓 Student Result Management System")
root.geometry("1000x700")
root.config(bg="#e8f0fe")

tk.Label(root, text="Add Student Marks", font=("Arial", 18, "bold"), bg="#e8f0fe", fg="#333").pack(pady=10)

form = tk.Frame(root, bg="#e8f0fe")
form.pack()

tk.Label(form, text="Name:", bg="#e8f0fe").grid(row=0, column=0, padx=5)
entry_name = tk.Entry(form)
entry_name.grid(row=0, column=1, padx=5)

tk.Label(form, text="Math:", bg="#e8f0fe").grid(row=0, column=2)
entry_math = tk.Entry(form)
entry_math.grid(row=0, column=3, padx=5)

tk.Label(form, text="Science:", bg="#e8f0fe").grid(row=0, column=4)
entry_sci = tk.Entry(form)
entry_sci.grid(row=0, column=5, padx=5)

tk.Label(form, text="English:", bg="#e8f0fe").grid(row=0, column=6)
entry_eng = tk.Entry(form)
entry_eng.grid(row=0, column=7, padx=5)

tk.Button(root, text="➕ Add Student", command=add_student, bg="#4CAF50", fg="white", padx=20).pack(pady=10)

btns = tk.Frame(root, bg="#e8f0fe")
btns.pack()
tk.Button(btns, text="🗑️ Delete Selected", command=delete_selected, bg="#f44336", fg="white", padx=15).grid(row=0, column=0, padx=10)
tk.Button(btns, text="❌ Clear All", command=clear_all, bg="#9C27B0", fg="white", padx=15).grid(row=0, column=1, padx=10)

# 📋 Table
table_frame = tk.Frame(root)
table_frame.pack()

cols = ("Name", "Math", "Science", "English", "Total", "Average", "Grade")
table = ttk.Treeview(table_frame, columns=cols, show="headings", height=10)

for col in cols:
    table.heading(col, text=col)
    table.column(col, anchor="center", width=100)

scroll = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
table.config(yscrollcommand=scroll.set)
scroll.pack(side="right", fill="y")
table.pack(side="left")

# 📊 Stats Section
summary = tk.Frame(root, bg="#e8f0fe")
summary.pack(pady=20)

label_total = tk.Label(summary, text="👥 Total Students: 0", font=("Arial", 12), bg="#e8f0fe")
label_total.pack()

label_avg = tk.Label(summary, text="📊 Class Average: --", font=("Arial", 12), bg="#e8f0fe")
label_avg.pack()

label_top = tk.Label(summary, text="🏆 Top Performer: --", font=("Arial", 12), bg="#e8f0fe")
label_top.pack()

label_toppers = tk.Label(summary, text="⭐ Subject Toppers: --", font=("Arial", 12), bg="#e8f0fe", justify="left")
label_toppers.pack()

label_grades = tk.Label(summary, text="📦 Grade Summary: --", font=("Arial", 12), bg="#e8f0fe")
label_grades.pack()

root.mainloop()
