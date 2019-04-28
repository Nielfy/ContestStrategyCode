import Data_processing
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
class KnnMarketMaker(Data_processing.Strategies):
    def __init__(self,data_freq=15,Run_freq=90,gap=0.1,n=3,lookback=10,window=50):
        self.Model=KNeighborsClassifier(n_neighbors=n)
        self.data_freq = data_freq
        self.gap = gap
        self.Run_freq = Run_freq
        self.look_back=lookback
        self.window=window

    def run(self):
        if len(self.PriceList)<self.window+self.look_back+1:
            return 0
        Xtrain=[self.PriceList[-self.window-self.look_back+i-1:-self.look_back+i-1] for i in range(self.look_back)]
        Ytrain=[np.sign(self.PriceList[-self.look_back+i]-self.PriceList[-self.look_back+i-1]) for i in range(self.look_back)]
        self.Model.fit(Xtrain,Ytrain)
        return self.Model.predict(self.PriceList[-1])

