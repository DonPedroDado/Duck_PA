import requests
from flask import (Flask, jsonify, redirect, render_template_string, request,
                   url_for)
from requests.exceptions import RequestException

app = Flask(__name__)
app.secret_key = "replace-with-a-secure-random-key"

# In-memory data store: conversation history by user name
conversations = []


##############################################################################
# Mock Ollama function calls
##############################################################################
def ollama_start_profile_creation(name):
    """
    Call external API /create_profile, passing the name as a query parameter.
    Assumes the API returns JSON containing a "question" key.
    """
    url = f"http://192.168.178.41:8000/create_profile/{name}"
    try:
        print(f"Requesting URL {url}")
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if status != 200
        data = response.json()
        # e.g. data might look like: {"question": "Hello John, what is your favorite color?"}
        question = data.get("text", "No question returned from API.")
        conversations.append(question)
        return question
    except requests.exceptions.RequestException as e:
        # If there's a network or status code error, handle it here
        print(f"Error contacting external API: {e}")
        return "Error retrieving question from external API."


def ollama_continue_profile_creation(name, history):
    print(history)
    url = "http://192.168.178.41:8000/continue_profile_creation"
    payload = {"name": name, "messages": history}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an exception if the status is 4xx/5xx
        data = response.json()
        # "question" might be <EOP> or an actual question string
        return data.get("question", "<EOP>")
    except RequestException as e:
        print(f"[ERROR] Unable to contact external API: {e}")
        return "<EOP>"  # Fallback, treat as if conversation ended or error occurred""


##############################################################################
# Views / Endpoints
##############################################################################


@app.route("/")
def index():
    """
    (1) Student ->> ChatUI: open address in the browser
    Display a simple form that asks the student’s name.
    (2) ChatUI ->> Student: asks Name
    """
    html = """
    <h1>Welcome to the Profile Creation</h1>
    <form action="/create_profile" method="get">
      <label for="name">Enter your name:</label>
      <input type="text" id="name" name="name" required>
      <button type="submit">Start</button>
    </form>
    """
    return render_template_string(html)


@app.route("/create_profile")
def create_profile():
    """
    (3) Student ->> ChatUI: name
    (4) ChatUI ->> Server: GET /create_profile/{name}
    (5) Server ->> Ollama: message to tell Ollama to start profile creation
    (6) Ollama ->> Server: first response asking first question
    (7) Server ->> ChatUI: forward just the message
    (8) ChatUI ->> Student: Display the message with the question
    """
    name = request.args.get("name")
    if not name:
        return redirect(url_for("index"))

    # “Call” Ollama to get the first question
    first_question = ollama_start_profile_creation(name)

    # Show the question to the student
    return render_template_string(
        """
        <h1>Profile Creation</h1>
        <p>{{ question }}</p>
        <form action="{{ url_for('continue_profile_creation', name=name) }}" method="post">
          <label for="answer">Your answer:</label>
          <input type="text" id="answer" name="answer" required>
          <button type="submit">Continue</button>
        </form>
    """,
        name=name,
        question=first_question,
    )


@app.route("/continue_profile_creation/<name>", methods=["POST"])
def continue_profile_creation(name):
    answer = request.form.get("answer", "")

    conversations.append(answer)
    # Call Ollama with the entire conversation
    next_question = ollama_continue_profile_creation(name, conversations)
    if next_question.startswith("<EOP>") and next_question.endswith("<EOP>"):
        # Strip off the <EOP> from both ends:
        final_text = next_question[5:-5].strip()  # remove <EOP> + trailing spaces
        conversations.clear()
        conversations.append(final_text)
        return render_template_string(
            """
            <h1>Profile Creation Completed</h1>
            <p>{{ message }}</p>
            <a href="/">Go back to start</a>
        """,
            message=final_text,
        )
    else:
        # Append Ollama's question to the conversation
        conversations.append(next_question)
        # Forward the new question to the student
        return render_template_string(
            """
            <h1>Profile Creation</h1>
            <p>{{ question }}</p>
            <form action="{{ url_for('continue_profile_creation', name=name) }}" method="post">
              <label for="answer">Your answer:</label>
              <input type="text" id="answer" name="answer" required>
              <button type="submit">Continue</button>
            </form>
        """,
            name=name,
            question=next_question,
        )


##############################################################################
# Entry point
##############################################################################
if __name__ == "__main__":
    app.run(debug=True)
