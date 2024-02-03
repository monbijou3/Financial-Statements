import dart_fss as dart
import pandas as pd
import visualize, classify

# Open DART API KEY 설정
api_key='Your api key'
dart.set_api_key(api_key=api_key)
corporations = dart.get_corp_list()

# 회사명 추출을 위해 extract액셀 파일 불러오기
company_name = pd.read_excel('./dart/company_name.xlsx')
codes = []
names = []

#company_name 액셀파일에서 code, 이름 분리
for i in company_name['회사명']:
    codes.append(i[1:7])
    names.append(i[8:])

#시각화할 회사 리스트
print(names)

#main
for code, name in zip(codes, names):
        """ 1번case : 0,4 index에 각각 매출액/영업이익 대응 -> dart.py의 doDart function 쓰면됨
            2번case : 0,4 index는 아닌데 매출액/영업이익이 있음 -> doDart 살짝 변형하면됨
            3번case:  1, 2번 둘다 아님(return안 할 거임)
            return은 multiple 리스트 -> return [[삼성전자,,...],[POSCO홀딩스....]]
        """
        try:
            # 연결재무제표부터 불러오기, #report_tp = 'quarter'로 분기도 가능
            print(name + " 연결재무제표 불러오는 중")
            fs = dart.fs.extract(corp_code=code, bgn_de='20200101', fs_tp=('bs','is','cis'), skip_error= False, progressbar=True)
            
            #원본확인용도 아니면 필요없음
            fs.save(filename = name + '.xlsx')
            
            result = classify.classify(name, fs)
            
            #case 확인용(디버깅용)
            #print(str(result) + "번")

            if (result == 1):
                    visualize.visualize1(name, fs)
            
            elif(result == 2):
                    visualize.visualize2(name, fs)

            elif(result == 3):
                    pass
    
        except:
             print(name + " 작업 중 오류 발생")
        
            
        
            
        
