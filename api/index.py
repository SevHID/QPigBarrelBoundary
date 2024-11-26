from flask import Flask, request, jsonify, render_template, send_from_directory
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/static/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('static/images', filename)

def load_serial_numbers():
    file_path = os.path.join("dist", "serial_numbers.txt")
    serial_numbers = {}
    if not os.path.exists(file_path):
        print(f"Error: {file_path} 文件不存在")
        return serial_numbers

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue  # 跳过空行
            parts = line.split(',')
            if len(parts) != 3:
                print(f"Warning: 跳过格式错误的行: {line}")
                continue
            serial_number, image_url, description = parts
            serial_numbers[serial_number] = {'image_url': image_url, 'description': description}
    return serial_numbers

valid_serial_numbers = load_serial_numbers()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def verify_serial_number():
    data = request.get_json()
    serial_number = data.get('serialNumber')
    serial_info = valid_serial_numbers.get(serial_number, {'image_url': 'static/images/default.png', 'description': '默认描述'})
    if serial_number in valid_serial_numbers:
        return jsonify({'message': '此鞋子为 WY正品 以下为产品信息', 'imageUrl': serial_info['image_url'], 'description': serial_info['description']})
    else:
        return jsonify({'message': '编号无效'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)