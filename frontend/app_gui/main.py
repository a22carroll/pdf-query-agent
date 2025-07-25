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

    def handle_query(question_entry, answer_textbox):
        question = question_entry.get()
        if question.strip() == "":
            messagebox.showwarning("Input Required", "Please enter a question.")
            return
        answer = ask_question(question)
        answer_textbox.delete("1.0", tk.END)
        answer_textbox.insert(tk.END, answer)

    create_ui(root, handle_upload, handle_query)
    root.mainloop()

if __name__ == "__main__":
    main()
