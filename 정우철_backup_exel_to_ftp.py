import os
from dotenv import load_dotenv
import ftplib

def backup_exel_to_ftp(filename): # 정우철: FTP서버로 엑셀파일 백업하는 함수, 데코레이터로 라우팅 되는 함수가 아닌 특정 함수에서 호출하는 함수
    
    load_dotenv()

    DIR = os.getcwd()
    file_path = os.path.join(DIR, filename)

    host_ip = os.getenv("FTP_HOST_IP")
    host_id = os.getenv("FTP_LOGIN_ID")
    host_pw = os.getenv("FTP_LOGIN_PWD")

    with ftplib.FTP(host_ip) as ftp:
        ftp.login(host_id, host_pw)
        with open(file_path, "rb") as file:
            ftp.storbinary("STOR " + filename, file)
            ftp.retrlines("LIST")

    print(f"{filename} 파일이 FTP 서버로 백업되었습니다.")