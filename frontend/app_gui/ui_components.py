import tkinter as tk

def create_ui(root, upload_callback, query_callback):
    # Upload button
    upload_btn = tk.Button(root, text="Upload PDF", command=upload_callback)
    upload_btn.pack(pady=10)

    # Question entry
    tk.Label(root, text="Ask a question:").pack()
    question_entry = tk.Entry(root, width=60)
    question_entry.pack(pady=5)

    # Ask button
    ask_btn = tk.Button(root, text="Submit", command=lambda: query_callback(question_entry, answer_box))
    ask_btn.pack(pady=5)

    # Answer box
    tk.Label(root, text="Answer:").pack()
    answer_box = tk.Text(root, height=10, width=70)
    answer_box.pack(pady=10)
