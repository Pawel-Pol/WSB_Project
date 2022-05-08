# tylko po to aby stworzyc przykladowe dane

import pandas as pd
import random
import datetime
import glob

def create_df():
    a = pd.DataFrame([])
    for i in range(43782):
        id = 'A'+str(random.randint(1, 5000))
        wplata = random.randint(0, 2000)
        start_date = datetime.date(2021, 1, 1)
        end_date = datetime.date(2022, 1, 31)
        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        random_date = start_date + datetime.timedelta(days=random_number_of_days)
        temp = pd.DataFrame({'id':id,'kwota':wplata,'data':random_date}, index = [0])
        a = pd.concat([a,temp])

    a.to_excel(f'Data/wplaty_klientow.xlsx', index = False)

if __name__=='__main__':
    a = pd.read_excel('../Data/wplaty_klientow.xlsx').copy()
    a['kwota']

