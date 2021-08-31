from Load_And_Visualize_Time_Data import Load_and_Visualize_Time_Data
import pandas as pd
import numpy as np
import sys
from sktime.forecasting.model_selection import temporal_train_test_split
from sktime.utils.plotting import plot_series
from sktime.performance_metrics.forecasting import smape_loss
from sktime.forecasting.arima import AutoARIMA


class Auto_Arima_Univariate_Forecasting:
    def __init__(self, path, time_freq, trend=None, seasonal=None, time_column=0, day_to_month=False,
                 month_to_year=False, sp=12, test_size=0.2, model="additive"):
        preload = Load_and_Visualize_Time_Data(path, time_column, model)
        self.data, self.columns = preload.return_data()
        preload.visualize_data()
        preload.decompose_time_series()
        if day_to_month and time_freq == 'M':
            self.day_to_month()
        elif month_to_year and time_freq == 'Y':
            self.day_to_month()
            self.month_to_year()
        else:
            sys.exit("time frequency and converted frequency does not match")
        self.time_freq = time_freq
        self.trend = trend
        self.seasonal = seasonal
        self.sp = sp
        self.test_size = test_size

    def train_test_split(self):
        self.data.index = pd.PeriodIndex(self.data.index, freq=self.time_freq)
        self.y_train, self.y_test = temporal_train_test_split(self.data, test_size=self.test_size)

    def day_to_month(self):
        self.data = self.data.resample('M').sum()

    def month_to_year(self):
        self.data = self.data.resample('Y').sum()

    def forecast_and_visualize(self, task_id):
        self.train_test_split()
        forecaster = AutoARIMA(sp=self.sp, suppress_warnings=True)
        forecaster.fit(self.y_train)
        fh = np.arange(1, len(self.y_test) + 1)
        y_pred = forecaster.predict(fh)
        plot = plot_series(self.y_train, self.y_test, y_pred, labels=["y_train", "y_test", "y_pred"])
        plot.savefig("files/autoArimaUnivariateForecasting_" + str(task_id) + ".png", dpi=100)
        return {'smape_loss': smape_loss(self.y_test, y_pred),
                'figure': "autoArimaUnivariateForecasting_" + str(task_id) + ".png"}
