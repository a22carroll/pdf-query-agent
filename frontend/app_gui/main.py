import tkinter as tk
from tkinter import filedialog, messagebox
from ui_components import create_ui
from api_client import upload_pdf, ask_question

def main():
    root = tk.Tk()
    root.title("PDF Query Agent")
    root.geometry("600x400")

    def handle_upload():
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            success = upload_pdf(file_path)
            if success:
                messagebox.showinfo("Success", "PDF uploaded successfully!")
            else:
                messagebox.showerror("Error", "Failed to upload PDF.")

    # Get the UI widgets from create_ui
    question_entry, answer_box, upload_btn, ask_btn = create_ui(root, handle_upload, None)

    # Now define the query handler that uses the widgets captured here
    def handle_query():
        question = question_entry.get()
        if question.strip() == "":
            messagebox.showwarning("Input Required", "Please enter a question.")
            return
        answer = ask_question(question)
        answer_box.delete("1.0", tk.END)
        answer_box.insert(tk.END, answer)

    # Assign the ask button command now that handle_query has no params
    ask_btn.config(command=handle_query)

    root.mainloop()
if __name__ == "__main__":
    main()