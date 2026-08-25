from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def home():
    # สั่งให้ Flask ดึงไฟล์ index.html จากโฟลเดอร์ templates มาแสดง
    return render_template('index.html')

if __name__ == '__main__':
    # Render จะกำหนด PORT มาให้ทาง Environment Variable
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)