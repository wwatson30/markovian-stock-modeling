import pandas as pd
import numpy as np
import get_state
import datetime
import json


def get_target(t_table: str = 'transition_table.json',
               cur_state: str = '[3 2 1]', days_into_future: int = 1):

    df = pd.read_json(t_table)
    matrix = df.T.fillna(0)
    power_matrix = matrix ** days_into_future
    prob_list = power_matrix[cur_state]
    prob_list.sort_values()

    print(prob_list)


get_target()
