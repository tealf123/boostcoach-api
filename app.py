from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from coaching_engine import generate_coaching_report, generate_qa_response
from uuid import uuid4

app = Flask(__name__)
CORS(app)

app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
os.makedirs('/tmp/boostcoach', exist_ok=True)

analyses_store = {}

@app.route('/', methods=['GET'])
def index():
    return '''<!DOCTYPE html>
<html>
<head><title>BoostCoach</title>
<script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-900 text-white">
<div class="max-w-2xl mx-auto p-8">
<h1 class="text-3xl font-bold mb-4">BoostCoach</h1>
<p class="text-gray-300 mb-6">Upload your Rocket League replay for AI coaching</p>
<form id="form" class="bg-gray-800 p-6 rounded">
<input type="file" id="file" accept=".replay" class="mb-4 block w-full">
<button type="submit" class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded w-full">Analyze</button>
</form>
<div id="result" class="mt-8 hidden">
<h2 class="text-2xl font-bold mb-4">Coaching Report</h2>
<div id="report" class="bg-gray-800 p-6 rounded whitespace-pre-wrap mb-6"></div>
<input type="text" id="question" placeholder="Ask a question..." class="w-full bg-gray-800 text-white rounded px-4 py-2 mb-2">
<button onclick="askQuestion()" class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Ask</button>
<div id="qa" class="mt-4"></div>
</div>
</div>
<script>
let aid = null;
document.getElementById('form').onsubmit = async (e) => {
  e.preventDefault();
  const file = document.getElementById('file').files[0];
  const fd = new FormData();
  fd.append('file', file);
  const r = await fetch('/api/replays/upload', {method:'POST', body:fd});
  const data = await r.json();
  if (data.status === 'success') {
    aid = data.analysis_id;
    document.getElementById('report').textContent = data.coaching_report;
    document.getElementById('result').classList.remove('hidden');
  } else {
    alert(data.error);
  }
};
async function askQuestion() {
  const q = document.getElementById('question').value;
  const r = await fetch(`/api/analyses/${aid}/ask`, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({question:q})});
  const data = await r.json();
  document.getElementById('qa').innerHTML += `<p class="mb-2"><strong>Q:</strong> ${q}</p><p class="mb-4"><strong>A:</strong> ${data.response}</p>`;
  document.getElementById('question').value = '';
}
</script>
</body>
</html>''', 200, {'Content-Type': 'text/html'}

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200

@app.route('/api/replays/upload', methods=['POST'])
def upload():
    try:
        file = request.files['file']
        replay_bytes = file.read()
        result = generate_coaching_report(replay_bytes, file.filename)
        if result['status'] != 'success':
            print(f"Coaching error: {result['error']}")
            return jsonify({'error': f"Coaching failed: {result['error']}"}), 500
        aid = str(uuid4())
        analyses_store[aid] = {'report': result['report']}
        return jsonify({'status': 'success', 'analysis_id': aid, 'coaching_report': result['report']}), 201
    except Exception as e:
        print(f"Upload error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyses/<aid>/ask', methods=['POST'])
def ask(aid):
    try:
        if aid not in analyses_store:
            return jsonify({'error': 'Not found'}), 404
        q = request.json.get('question', '')
        result = generate_qa_response(analyses_store[aid]['report'], q)
        if result['status'] != 'success':
            return jsonify({'error': 'Failed'}), 500
        return jsonify({'response': result['response']}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
