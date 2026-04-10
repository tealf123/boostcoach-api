from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return '''<!DOCTYPE html>
<html>
<head>
<title>BoostCoach - Coming Soon</title>
<style>
body{font-family:sans-serif;display:flex;align-items:center;justify-content:center;height:100vh;margin:0;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);}
.container{text-align:center;color:white;}
h1{font-size:3em;margin:0;}
p{font-size:1.2em;margin-top:10px;}
</style>
</head>
<body>
<div class="container">
<h1>BoostCoach</h1>
<p>AI-powered Rocket League coaching</p>
<p style="font-size:0.9em;color:#ccc;margin-top:40px;">Coming soon...</p>
</div>
</body>
</html>''', 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200
