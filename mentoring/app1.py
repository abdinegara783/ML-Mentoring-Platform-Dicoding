from flask import Flask, render_template

app1 = Flask(__name__)

# Route untuk halaman utama
@app.route('/')
def index():
    # Baca file HTML
    with open('C:/Users/Asus/pyton for data science/mentoring/templates/index.html', 'r') as file:
        html_code = file.read()

    return html_code

if __name__ == '__main__':
    app1.run()
