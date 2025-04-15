import pandas as pd
import numpy as np
import get_state
import datetime
import json


class Combination:
    def __init__(self, series: pd.Series, num_bins: int = 4):
        # key = {np.linspace(-100, 100, num=num_bins)[i]: i for i in range(num_bins)}
        thresholds = pd.Series(np.linspace(-100, 100, num=num_bins))
        self.combination = np.digitize(series, thresholds, right=False)

    def __str__(self):
        return str(self.combination)


def transition_fn_by_prob(year_horizon: int = 2015,
                          path: str = './data/inflation_adjusted_berkshire_stocks.csv',
                          col: str = 'Open_adjusted',
                          days: int = 3
                          ) -> []:
    year_horizon = datetime.datetime(year_horizon, 1, 1)
    df = pd.read_csv(path)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df[df['Date'] > year_horizon]
    result_dict = {}
    combos = []
    for i in range(len(df)-days):
        data_series = pd.Series(df[col][i:i+days])
        # print(data_series)
        state = get_state.get_state_by_percentile(data_series=data_series, state_width=1, min=data_series.min(),
                                                  max=data_series.max())
        combination = Combination(state)
        combos.append(str(combination))
        if str(combination) not in result_dict:
            result_dict[str(combination)] = 1
        else:
            result_dict[str(combination)] += 1
        # print(state)
    # result_dict[combination] is the total number of occurrences of combination
    # row of probabilities that you enter each other probability
    result = {}
    for k, v in result_dict.items():  # row
        intermed = {}   # of transitions to each other state
        row_props = {}
        for m, n in result_dict.items():  # column
            for index in range(len(combos) - 1):
                if combos[index] == str(k) and combos[index + 1] == str(m):
                    if m not in intermed:
                        intermed[m] = 1
                    else:
                        intermed[m] += 1
        for key, val in intermed.items():
            proportion = float(val / v)
            row_props[str(key)] = proportion

        result[str(k)] = row_props  # double dict
    print(result)

    with open('transition_table.json', 'w') as f:
        json.dump(result, f, indent=4)


transition_fn_by_prob()