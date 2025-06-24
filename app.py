from flask import Flask, request, jsonify, render_template, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_tracking', methods=['POST'])
def fetch_tracking():
    try:
        data = request.get_json()
        tba_number = data.get('tba_number')
        
        if not tba_number:
            return jsonify({'success': False, 'error': '请输入TBA单号'})

        # 检查track目录是否存在对应的HTML文件
        track_file = os.path.join('track', f'{tba_number}.html')
        if os.path.exists(track_file):
            return jsonify({
                'success': True,
                'url': f'/track/{tba_number}.html'
            })
        
        return jsonify({
            'success': False,
            'error': '未找到该单号的轨迹信息'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/track/<path:filename>')
def serve_track_file(filename):
    return send_from_directory('track', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True) 