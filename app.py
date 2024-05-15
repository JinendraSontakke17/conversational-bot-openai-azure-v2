from flask import Flask, render_template, request, jsonify
import logging
# import openai
from openai import OpenAI

openai.api_key = ""

app = Flask(__name__)

# def generate_text(prompt, temperature=0.7, max_tokens=100, n=1, stop=None):
#     response = openai.Completion.create(
#         engine="gpt-3.5-turbo-instruct", 
#         prompt=prompt,
#         temperature=temperature,
#         max_tokens=max_tokens,
#         n=n,
#         stop=stop
#     )

#     return [completion.text.strip() for completion in response.choices]

def generate_text(prompt_text, model_name="gpt-4o", api_key="<api_key>"):
    client = OpenAI(api_key=api_key)

    completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "user", "content": prompt_text}
        ]
    )

    return completion.choices[0].message.content

@app.route('/')
def home():
    return render_template('index.html')

logging.basicConfig(filename='app.log', level=logging.ERROR)

@app.route('/receive_text', methods=['POST'])
def receive_text():
    try:
        data = request.json
        recognized_text = data['recognized_text']
        result = recognized_text.upper()
        generate_text_result = generate_text(result)

        
        # Return the result to the client
        return jsonify({'result': generate_text_result[0]})
    except Exception as e:
        # Log the error
        app.logger.error('An error occurred: %s', str(e))
        # If an error occurs, return an error response
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(filename='app.log', level=logging.ERROR)
    app.run(debug=True)
