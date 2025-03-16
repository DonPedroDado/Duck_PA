from flask import render_template
from Duck_PA import app

@app.route("/", methods=["GET"])
def homepage():
    """
    Returns the main page which is divided into:
      a) Teacher selection (info + radio button or some control to choose).
      b) A text area to specify the test topic.
      c) A selection for the type of test.
    """
    return render_template('index.html')