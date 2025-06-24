from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import logging

app = Flask(__name__)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('index.html')  # 暂时重定向到首页

@app.route('/register')
def register():
    return render_template('index.html')  # 暂时重定向到首页

@app.route('/fetch_tracking', methods=['POST'])
def fetch_tracking():
    try:
        data = request.get_json()
        tba_number = data.get('tba_number')
        
        if not tba_number:
            logger.warning('No TBA number provided')
            return jsonify({'success': False, 'error': '请输入TBA单号'})

        # 检查track目录是否存在
        if not os.path.exists('track'):
            os.makedirs('track')
            logger.info('Created track directory')

        # 检查track目录是否存在对应的HTML文件
        track_file = os.path.join('track', f'{tba_number}.html')
        if os.path.exists(track_file):
            logger.info(f'Found tracking file for {tba_number}')
            return jsonify({
                'success': True,
                'url': f'/track/{tba_number}.html'
            })
        
        logger.warning(f'No tracking file found for {tba_number}')
        return jsonify({
            'success': False,
            'error': '未找到该单号的轨迹信息'
        })

    except Exception as e:
        logger.error(f'Error in fetch_tracking: {str(e)}')
        return jsonify({
            'success': False,
            'error': '服务器内部错误，请稍后重试'
        })

@app.route('/track/<path:filename>')
def serve_track_file(filename):
    try:
        return send_from_directory('track', filename)
    except Exception as e:
        logger.error(f'Error serving track file {filename}: {str(e)}')
        return jsonify({
            'success': False,
            'error': '文件访问错误'
        })

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'success': False, 'error': '页面未找到'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'error': '服务器内部错误'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True) 