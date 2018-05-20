import os
import sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from mlp_base import *
from manipulation import get_master_df

def train_year_range(df, num_years):
    results = []
    for day in test_dates:
        X, y = create_X_y(df=df, columns=columns, target='DNI_T_plus15', date=day, num_units=num_years, units='years')
        train_rmse = train_mlp(X.values, y.values)
        print("\nMLP Training RMSE | {:.4f}\n".format(train_rmse))
        results.append((day, train_rmse))
    return results


if __name__ == "__main__":
    df = get_master_df("../../data/ivanpah_measurements.csv")
    df['Direct Normal [W/m^2]'] = np.where(df['Direct Normal [W/m^2]'] < 0, 0, df['Direct Normal [W/m^2]'])
    df = create_lagged_DNI_features(15, df)

    one_year_results = train_year_range(df, 1)
    two_year_results = train_year_range(df, 2)
