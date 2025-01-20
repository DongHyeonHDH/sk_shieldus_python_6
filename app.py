from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        recipient_email = request.form['email']
        file = request.files['file']
        
        if recipient_email and file:
            send_email(recipient_email, file)
            return redirect(url_for('index')) 
    return render_template('index.html')

def send_email(recipient_email, file):
    sender_email = 'SECRET_ID' 
    password = 'SECRET_PASS'              
    
    try:
        server = smtplib.SMTP('smtp.naver.com', 587)
        server.starttls()
        server.login(sender_email, password)
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = "이것은 날씨를 알 수 있는 파일입니다."
        
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={file.filename}')
        msg.attach(part)
        
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(f'이메일 전송 실패: {str(e)}')

if __name__ == '__main__':
    app.run(debug=True)

