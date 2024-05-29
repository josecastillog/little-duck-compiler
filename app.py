from flask import Flask, render_template, request, jsonify
import lex
import importlib

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_code', methods=['POST'])
def run_code():
    try:
        code = request.json.get('code')
        importlib.reload(lex)
        output = lex.run(code)

        def list_to_string_with_line_breaks(lst):
            return "\n".join(str(element) for element in lst)

        output_str = list_to_string_with_line_breaks(output)
        return jsonify({"output": output_str})

    except Exception as e:
        error_message = str(e)
        return jsonify({"output": error_message.strip('"')})


if __name__ == '__main__':
    app.run(debug=True)
