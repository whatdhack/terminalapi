import os
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

app = Flask(__name__)

# Configure the Gemini API
try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
except KeyError:
    print("Please set the GEMINI_API_KEY environment variable.")
    exit(1)


# Create the model
model = genai.GenerativeModel('gemini-1.0-pro')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    query = data.get('query')
    if not query:
        return jsonify({'error': 'Query not provided'}), 400

    try:
        # Perform the translation with few-shot prompting
        prompt = f"""\
Translate the following natural language queries to bash commands.

Query: list all files in the current directory
Bash: ls -a

Query: count the number of files in the current directory
Bash: ls -l | wc -l

Query: find all files with the .py extension in the current directory
Bash: find . -name "*.py"

Query: {query}
Bash:"""
        response = model.generate_content(prompt)
        bash_command = response.text
        return jsonify({'bash_command': bash_command})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
