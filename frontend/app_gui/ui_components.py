import tkinter as tk
from tkinter import ttk

def create_ui(root, upload_callback, query_callback):
    container = ttk.Frame(root, padding=10)
    container.grid(row=0, column=0, sticky="NSEW")
    
    # Make root expandable
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    
    # Upload button
    upload_btn = ttk.Button(container, text="Upload PDF", command=upload_callback)
    upload_btn.grid(row=0, column=0, pady=(0, 10), sticky="W")
    
    # Question label and entry
    ttk.Label(container, text="Ask a question:").grid(row=1, column=0, sticky="W")
    question_entry = ttk.Entry(container, width=60)
    question_entry.grid(row=2, column=0, pady=5, sticky="EW")
    
    # Answer box label
    ttk.Label(container, text="Answer:").grid(row=4, column=0, sticky="W", pady=(10,0))
    
    # Answer box with scrollbar
    answer_box = tk.Text(container, height=10, width=70, wrap="word", background="#f0f0f0", relief="sunken", borderwidth=1)
    answer_box.grid(row=5, column=0, sticky="NSEW", pady=5)
    
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=answer_box.yview)
    scrollbar.grid(row=5, column=1, sticky="NS", pady=5)
    answer_box.config(yscrollcommand=scrollbar.set)
    
    # Ask button
    ask_btn = ttk.Button(container, text="Submit", command=lambda: query_callback(question_entry, answer_box))
    ask_btn.grid(row=3, column=0, sticky="E", pady=5)
    
    # Make answer box expandable
    container.rowconfigure(5, weight=1)
    container.columnconfigure(0, weight=1)
    
    return question_entry, answer_box, upload_btn, ask_btn

def create_pdf_manager_ui(root):
    container = ttk.Frame(root, padding=10)
    container.grid(row=1, column=0, sticky="NSEW", pady=(10,0))  # Below existing container

    # Make container expandable
    root.rowconfigure(1, weight=1)
    root.columnconfigure(0, weight=1)
    container.rowconfigure(1, weight=1)
    container.columnconfigure(0, weight=1)

    ttk.Label(container, text="Stored PDFs:").grid(row=0, column=0, sticky="W")

    # Listbox with scrollbar inside a frame
    list_frame = ttk.Frame(container)
    list_frame.grid(row=1, column=0, sticky="NSEW")

    scrollbar = ttk.Scrollbar(list_frame, orient="vertical")
    scrollbar.pack(side="right", fill="y")

    pdf_listbox = tk.Listbox(list_frame, height=10, yscrollcommand=scrollbar.set)
    pdf_listbox.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=pdf_listbox.yview)

    # Buttons
    btn_frame = ttk.Frame(container)
    btn_frame.grid(row=2, column=0, pady=5, sticky="EW")

    refresh_btn = ttk.Button(btn_frame, text="Refresh List")
    view_btn = ttk.Button(btn_frame, text="View PDF")
    delete_btn = ttk.Button(btn_frame, text="Delete PDF")

    refresh_btn.pack(side="left", padx=5)
    view_btn.pack(side="left", padx=5)
    delete_btn.pack(side="left", padx=5)

    return pdf_listbox, refresh_btn, view_btn, delete_btn