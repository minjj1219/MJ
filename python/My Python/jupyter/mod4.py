import pandas as pd

class Change_dt_2():

    def __init__(self,input_url):
        self.url = input_url


    def csv_read(self):
        self.dt = pd.read_csv("./csv/Sales Records.csv")
        self.dt.sort_values("Country", inplace=True)
        self.dt.reset_index(drop=True,inplace=True)
        return self.dt
        

    def remove_c(self, input_a):
        self.dt.drop(input_a, axis=1, inplace=True)
        return self.dt