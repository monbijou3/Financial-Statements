import boto3
import pandas as pd

def s3_connection():
    try:
        # s3 클라이언트 생성
        s3 = boto3.client(
            service_name="s3",
            region_name="ap-northeast-2",
            aws_access_key_id="AKIAZFEQRMP37KHVN3PM",
            aws_secret_access_key="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",
        )
    except Exception as e:
        print(e)
    else:
        return s3

def upload_file(name):
        full_name = name + " 시각화 이미지.png"
        try:
            s3 = s3_connection()  
            s3.upload_file(full_name, "jmjp-bucket",full_name)
            #디버깅 체크용
            #print("S3에 " + name+ " 시각화 이미지 업로드 완료")
        except Exception as e:
            print(e)

def upload_csv_file(name):
        try:
            s3 = s3_connection()  
            for format in ['_포괄손익계산서.csv', '_재무상태표.csv']:
                full_name = name + format
                s3.upload_file(full_name, "jmjp-bucket", full_name)
                #디버깅 체크용
                #print("S3에 " + full_name + " 업로드 완료")
        except Exception as e:
            print(e)

def upload_json():
    try:
            s3 = s3_connection()  
            full_name = "삼성전자_naver_news.json"
            s3.upload_file(full_name, "jmjp-bucket", full_name)
            #디버깅 체크용
            #print("S3에 " + full_name + " 업로드 완료")
            print("dd")
    except:
         pass
