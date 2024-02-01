import pandas as pd

def classify(name, fs):
        """ 1번case : 0,4 index에 각각 매출액/영업이익 대응 -> visualize1 함수 사용해서 시각화
            2번case : 0,4 index는 아닌데 매출액/영업이익이 있음 -> visualize2 함수 사용해서 시각화
            3번case:  1, 2번 둘다 아님(시각화 보류) 주로 증권사, 보험사, 게임회사 등 서비스 그 자체를 제공하는 회사들이 해당
        """
        # case분류를 위한 bool
        having_revenue = False
        having_profit = False
        right_index_profit = False

        print(str(name) +"의 case : " , end ="")
        
            
        if type(fs['is']) == pd.core.frame.DataFrame:
            check = fs['is']

        else: 

            check = fs['cis']

        #bs ,cis indexing
        keys = check.keys()
        label= keys[0][0]
        index = check[label]['label_ko']
        
        #classify
        if ('매출액' in index[0] or '매출' == index[0] or '영업수익' in index[0]):
                having_revenue = True
               
        for i in range(len(index)):
            if ('영업이익' in index[i]):
                having_profit = True 
                if (i == 4):
                    right_index_profit = True
            
        right_category = having_profit and having_revenue 
        

        if (right_category and right_index_profit):
            return 1

        elif (right_category and not right_index_profit):
            return 2
            
        else: 
            return 3
        

    
        
