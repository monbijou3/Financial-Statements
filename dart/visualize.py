import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from matplotlib import style
import matplotlib

def preprogressing(name, fs): 
        """필요 데이터만 뽑는 함수(전처리)"""
        bs = fs['bs']
        #is or cis 추출
        if type(fs['is']) == pd.core.frame.DataFrame:
                income = fs['is']
        else: 
                income = fs['cis']

        #bs ,(c)is indexing 
        keys1 = bs.keys()
        keys2 = income.keys()
        bs_str1 = keys1[0][0]
        cis_str2 = keys2[0][0]

        index1 = bs[bs_str1]['label_ko']
        index2 = income[cis_str2]['label_ko']

        # pandas로 옮기기
        df_index1 = pd.DataFrame(index1)
        df_index2 = pd.DataFrame(index2)


        # dataframe column 만들고 합치기; 연도를 직접 설정한 하드코딩이라 나중에 바꿀 예정
        df_contents = bs[['20221231','20211231','20201231','20191231']].droplevel(1, axis=1)
        df_contents2 = income[['20220101-20221231','20210101-20211231','20200101-20201231',
                                '20190101-20191231']].droplevel(1, axis=1)

        bs_statement = pd.merge(df_index1, df_contents, left_index=True, right_index=True)
        cis_statement = pd.merge(df_index2, df_contents2,left_index=True, right_index=True)

        bs_statement.columns = ['Label', '2022년','2021년','2020년','2019년']
        cis_statement.columns = ['Label', '2022년','2021년','2020년','2019년']

        bs_statement.set_index('Label', inplace=True)
        cis_statement.set_index('Label', inplace=True)
                
        # dataframe을 csv로 저장
        bs_statement.to_csv( name + '_재무상태표'+'.csv')
        cis_statement.to_csv( name + '_포괄손익계산서'+'.csv')
        
        #bs_statment도 return 하려면 list로 담아서 bs,cis리턴하기
        return cis_statement

def draw(name, cis_statement, index_profit = 4):
        """visualize 함수에서 쓰일 그래프 그리는 함수"""
        extract = pd.DataFrame(cis_statement.iloc[[0,index_profit],[0,1,2,3]]).transpose().sort_index(ascending=True)
        extract['영업이익률'] = extract.iloc[:, 1] / extract.iloc[:, 0]
        extract.columns = ['매출액', '영업이익', '영업이익률']
        extract[['전기매출액', '전기영업이익', '전기영업이익률']] = extract[['매출액','영업이익','영업이익률']].shift(1)
        extract['매출액 변화'] = ( extract['매출액'] - extract['전기매출액'] ) / extract['전기매출액']
        extract['영업이익 변화'] = ( extract['영업이익'] - extract['전기영업이익'] ) / extract['전기영업이익']
        extract['영업이익률 변화'] = ( extract['영업이익률'] - extract['전기영업이익률'] )
        final = extract.iloc[1:].drop(['전기매출액','전기영업이익','전기영업이익률'], axis=1)

        matplotlib.rcParams['axes.unicode_minus'] = False
        plt.rcParams["figure.figsize"] = (12,8)
        font_name = font_manager.FontProperties(fname ="c:/Windows/Fonts/malgun.ttf").get_name()
        rc('font', family=font_name)
        style.use('ggplot')
        plt.plot(final[['매출액 변화', '영업이익 변화', '영업이익률 변화']])
        ax = plt.subplot()
        ax.legend(['매출액 증가율', '영업이익 증가율', '영업이익률 증가율'])
        current_values = plt.gca().get_yticks()
        ax.yaxis.set_ticks(current_values)
        plt.gca().set_yticklabels(['{:.0%}'.format(x) for x in current_values]) 
        plt.title(name + " 매출액/영업이익 추이")
        plt.savefig(name + " 시각화 이미지")
        plt.clf()
        print(name + " 시각화 완료")

def visualize1(name,fs):
        """표준을 잘 따른 bs, cis를 시각화 해주는 함수"""
        cis_statement = preprogressing(name, fs)
        
        draw(name,cis_statement)

def visualize2(name, fs):
        """매출, 매출액, 매출(~~), 영업이익, 영업이익(손실) 등등 항목이 이름이 달라도 시각화 해주는 함수"""

        # index_profit 구하기
        if type(fs['is']) == pd.core.frame.DataFrame:
                check = fs['is']
        else: 
                check = fs['cis']

        keys = check.keys()
        label= keys[0][0]
        index = check[label]['label_ko']
        
        for i in range(len(index)):
                if "영업이익" in index[i]:
                        index_profit = i
                        break

        cis_statement = preprogressing(name, fs)  
        draw(name, cis_statement, index_profit= index_profit)

        

  
