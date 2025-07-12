from flask import Flask, request, jsonify, render_template
from transformers import pipeline

app = Flask(__name__)

# Load the model
translator = pipeline("text2text-generation", model="t5-small")

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
        result = translator(prompt, max_length=128, num_beams=5, early_stopping=True)
        bash_command = result[0]['generated_text']
        return jsonify({'bash_command': bash_command})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
