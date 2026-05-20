from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    features = [
        {"title": "Lightning Fast", "desc": "Optimized performance for zero-latency interactions.", "icon": "🚀"},
        {"title": "Premium Design", "desc": "Aesthetics that captivate and engage your audience.", "icon": "💎"},
        {"title": "Secure Core", "desc": "Enterprise-grade security built into every layer.", "icon": "🛡️"}
    ]
    return render_template('index.html', features=features)

if __name__ == '__main__':
    app.run(debug=True)
