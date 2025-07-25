import tkinter as tk
from tkinter import filedialog, messagebox
from ui_components import create_ui, create_pdf_manager_ui
from api_client import upload_pdf, ask_question
from tkinter import Listbox, Scrollbar, END
import requests
import platform
import subprocess
import os

def main():
    print("starting main")
    root = tk.Tk()
    root.title("PDF Query Agent")
    root.geometry("600x600")
    

    def handle_upload():
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            success = upload_pdf(file_path)
            if success:
                messagebox.showinfo("Success", "PDF uploaded successfully!")
            else:
                messagebox.showerror("Error", "Failed to upload PDF.")

     # Create a parent frame with a grid layout
    parent_frame = tk.Frame(root)
    parent_frame.grid(row=0, column=0, sticky="NSEW")
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    # Make two subframes: one for PDF manager, one for Q&A
    left_frame = tk.Frame(parent_frame, padx=10, pady=10)
    left_frame.grid(row=0, column=0, sticky="NS")
    right_frame = tk.Frame(parent_frame, padx=10, pady=10)
    right_frame.grid(row=0, column=1, sticky="NSEW")

    parent_frame.columnconfigure(1, weight=1)
    parent_frame.rowconfigure(0, weight=1)

    # Create UI components in their respective frames
    question_entry, answer_box, upload_btn, ask_btn = create_ui(right_frame, handle_upload, None)
    pdf_listbox, refresh_btn, view_btn, delete_btn = create_pdf_manager_ui(left_frame)


    # Now define the query handler that uses the widgets captured here
    def handle_query():
        question = question_entry.get()
        if question.strip() == "":
            messagebox.showwarning("Input Required", "Please enter a question.")
            return
        answer = ask_question(question)
        answer_box.delete("1.0", tk.END)
        answer_box.insert(tk.END, answer)
    
    BACKEND_URL = "http://127.0.0.1:8000"

    def refresh_pdf_list():
        try:
            response = requests.get(f"{BACKEND_URL}/pdfs")
            response.raise_for_status()
            pdfs = response.json()["files"]
            pdf_listbox.delete(0, END)
            for pdf in pdfs:
                pdf_listbox.insert(END, pdf)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch PDFs: {e}")

    def view_pdf():
        selection = pdf_listbox.curselection()
        if not selection:
            messagebox.showwarning("Select a PDF", "Please select a PDF to view.")
            return

        filename = pdf_listbox.get(selection[0])
        url = f"{BACKEND_URL}/pdfs/{filename}"

        try:
            if platform.system() == 'Windows':
                os.startfile(url)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.run(["open", url])
            else:  # Linux
                subprocess.run(["xdg-open", url])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open PDF: {e}")

    def delete_pdf():
        selection = pdf_listbox.curselection()
        if not selection:
            messagebox.showwarning("Select a PDF", "Please select a PDF to delete.")
            return

        filename = pdf_listbox.get(selection[0])
        confirm = messagebox.askyesno("Confirm Delete", f"Delete '{filename}'?")
        if not confirm:
            return

        try:
            response = requests.delete(f"{BACKEND_URL}/pdfs/{filename}")
            if response.status_code == 200:
                messagebox.showinfo("Deleted", f"{filename} deleted.")
                refresh_pdf_list()
            else:
                messagebox.showerror("Error", response.json().get("error", "Failed to delete file."))
        except Exception as e:
            messagebox.showerror("Error", f"Delete failed: {e}")
        
    # Bind buttons
    refresh_btn.config(command=refresh_pdf_list)
    view_btn.config(command=view_pdf)
    delete_btn.config(command=delete_pdf)
    
    # Assign the ask button command now that handle_query has no params
    ask_btn.config(command=handle_query)
    refresh_pdf_list()
    root.mainloop()
if __name__ == "__main__":
    main()