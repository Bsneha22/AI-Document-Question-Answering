
from flask import Flask, render_template, request
import fitz
import re

# Create Flask application
app = Flask(
    __name__,
    static_folder="templates/static"
)

app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

# Knowledge Base
knowledge_base = []
document_name = ""


# 1. Extract text from PDF or TXT
def extract_text(file):

    filename = file.filename.lower()

    if filename.endswith(".pdf"):

        pdf = fitz.open(
            stream=file.read(),
            filetype="pdf"
        )

        text = ""

        for page in pdf:
            text += page.get_text() + " "

        pdf.close()

        return text

    elif filename.endswith(".txt"):

        return file.read().decode(
            "utf-8",
            errors="ignore"
        )

    return ""


# 2. Construct Knowledge Base
def create_knowledge_base(text):

    sentences = re.split(r"[.!?]+", text)

    facts = []

    for sentence in sentences:

        sentence = sentence.strip()

        if len(sentence) > 2:
            facts.append(sentence)

    return facts


# 3. Process user question
def get_keywords(question):

    stop_words = {
        "what", "is", "are", "the",
        "a", "an", "of", "in", "to",
        "and", "how", "why", "does",
        "do", "can", "explain", "tell",
        "me", "about", "for", "with",
        "which", "who", "where", "when"
    }

    words = re.findall(
        r"\b[a-z0-9]+\b",
        question.lower()
    )

    return set(words) - stop_words


# 4. Generate answer using Knowledge Base
def generate_answer(question):

    keywords = get_keywords(question)

    if not keywords:
        return "Please enter a meaningful question."

    best_answer = ""
    best_score = 0

    for fact in knowledge_base:

        fact_words = set(
            re.findall(
                r"\b[a-z0-9]+\b",
                fact.lower()
            )
        )

        score = len(keywords.intersection(fact_words))

        if score > best_score:

            best_score = score
            best_answer = fact

    if best_score > 0:

        return best_answer

    return "Sorry! The answer was not found in the uploaded document."


# 5. Display homepage
@app.route("/")
def home():

    return render_template(
        "index.html",
        document_name=document_name,
        fact_count=len(knowledge_base)
    )


# 6. Upload document
@app.route("/upload", methods=["POST"])
def upload():

    global knowledge_base, document_name

    file = request.files.get("document")

    if not file or not file.filename:

        return render_template(
            "index.html",
            message="Please select a document."
        )

    try:

        text = extract_text(file)

        if not text.strip():

            return render_template(
                "index.html",
                message="No readable text found."
            )

        knowledge_base = create_knowledge_base(text)

        document_name = file.filename

        return render_template(
            "index.html",
            message="Document uploaded successfully!",
            document_name=document_name,
            fact_count=len(knowledge_base)
        )

    except Exception:

        return render_template(
            "index.html",
            message="Error processing document."
        )


# 7. Ask question
@app.route("/ask", methods=["POST"])
def ask():

    question = request.form.get(
        "question", ""
    ).strip()

    if not knowledge_base:

        answer = "Please upload a document first."

    elif not question:

        answer = "Please enter a question."

    else:

        answer = generate_answer(question)

    return render_template(
        "index.html",
        answer=answer,
        question=question,
        document_name=document_name,
        fact_count=len(knowledge_base)
    )


# 8. Run website
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)