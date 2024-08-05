import os
import fitz
import re
import random
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
import spacy

# Load the spaCy English language model
nlp = spacy.load("en_core_web_sm")


class PDFQuestionGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Question Generator")

        self.file_path = tk.StringVar()
        self.num_questions = tk.IntVar()
        self.num_questions.set(5)  # Default value
        self.create_widgets()

    def extract_text_from_pdf(self, pdf_file):
        pdf_document = fitz.open(pdf_file)
        text = ""

        for page in pdf_document:
            text += page.get_text()

        pdf_document.close()
        return text

    def preprocess_text(self, text):
        return text

    def generate_basic_question(self, sentence):
        # Form a basic question
        return f"What is the main idea of the following sentence?\n\n{sentence.strip()}"

    def generate_reasoning_question(self, sentence):
        # Form a reasoning question
        return f"Why do you think the author mentioned the following?\n\n{sentence.strip()}"

    def generate_inference_question(self, sentence):
        # Form an inference question
        return f"What can you infer from the given information in the following sentence?\n\n{sentence.strip()}"

    def generate_multiple_choice(self, sentence):
        options = re.split(r'[,;]\s?', sentence.strip())
        correct_answer = random.choice(options)
        random.shuffle(options)
        options.insert(random.randint(0, len(options)), correct_answer)
        options_text = "\n".join(f"{chr(65 + i)}. {option}" for i, option in enumerate(options))
        # Form a multiple-choice question
        return f"Choose the correct option for the following:\n\n{sentence.strip()}\n\n{options_text}"

    def generate_questions(self, text):
        doc = nlp(text)
        sentences = [sent.text for sent in doc.sents if len(sent) > 10]
        questions = []

        num_to_generate = self.num_questions.get()
        selected_sentences = random.sample(sentences, num_to_generate)

        for idx, sentence in enumerate(selected_sentences, start=1):
            basic_question = self.generate_basic_question(sentence)
            reasoning_question = self.generate_reasoning_question(sentence)
            inference_question = self.generate_inference_question(sentence)
            multiple_choice_question = self.generate_multiple_choice(sentence)
            questions.extend([f"{idx}. {basic_question}\n", f"{idx + 0.33:.2f}. {reasoning_question}\n",
                              f"{idx + 0.67:.2f}. {inference_question}\n",
                              f"{idx + 1:.2f}. {multiple_choice_question}\n"])

        return questions

    def open_file_dialog(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            self.file_path.set(file_path)

    def set_num_questions(self):
        num = simpledialog.askinteger("Number of Questions", "Enter the number of questions to generate:", minvalue=1)
        if num is not None:
            self.num_questions.set(num)

    def generate_button_click(self):
        pdf_path = self.file_path.get()
        if pdf_path:
            text = self.extract_text_from_pdf(pdf_path)
            preprocessed_text = self.preprocess_text(text)
            questions = self.generate_questions(preprocessed_text)
            self.display_questions(questions)
        else:
            messagebox.showwarning("Warning", "Please select a PDF file.")

    def display_questions(self, questions):
        self.questions_text.delete("1.0", tk.END)  # Clear the previous content
        for question in questions:
            self.questions_text.insert(tk.END, f"{question}\n")

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(padx=20, pady=20)

        tk.Label(frame, text="PDF File:").grid(row=0, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.file_path, width=40, state="readonly").grid(row=0, column=1)
        tk.Button(frame, text="Browse", command=self.open_file_dialog).grid(row=0, column=2)

        tk.Label(frame, text="Number of Questions:").grid(row=1, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.num_questions, width=10).grid(row=1, column=1)
        tk.Button(frame, text="Set", command=self.set_num_questions).grid(row=1, column=2)

        tk.Button(frame, text="Generate Questions", command=self.generate_button_click).grid(row=2, columnspan=3)

        tk.Label(frame, text="Generated Questions:").grid(row=3, column=0, sticky="w")
        self.questions_text = tk.Text(frame, height=15, width=100, wrap="word")
        self.questions_text.grid(row=4, columnspan=3)


if __name__ == "__main__":
    root = tk.Tk()
    app = PDFQuestionGeneratorApp(root)
    root.mainloop()
