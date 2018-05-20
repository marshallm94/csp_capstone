import pandas as pd
import numpy as np
from modeling_base import get_random_test_dates, test_model
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split
from keras.callbacks import EarlyStopping
from keras.objectives import MSE, MAE
from keras.models import Sequential
from keras import metrics as met
from keras.layers.core import Activation, Dense


def build_neural_network(n_predictors, hidden_layer_neurons, loss='mean_squared_error'):
    '''
    Builds a Multi-Layer-Perceptron utilizing Keras.

    Parameters:
    ----------
    n_predictors : (int)
        The number of attributes that will be used as input for the model
        (i.e. the number of columns in a dataframe or array)
    hidden_layer_neurons : (list)
        List (length 2) of ints for the number of neurons in each hidden layer.
    loss : (str)
        The loss function for which the network will be optimized. Options
        are 'mean_squared_error' or 'mean_absolute_error'

    Returns:
    ----------
    model : (keras model object)
        A Multi-Layer Perceptron with 2 hidden layers
    '''
    model = Sequential()
    input_layer_neurons = n_predictors

    model.add(Dense(units=hidden_layer_neurons[0],
                    input_dim=input_layer_neurons,
                    kernel_initializer='uniform',
                    activation='relu'))

    model.add(Dense(units=hidden_layer_neurons[1],
                    kernel_initializer='uniform',
                    activation='relu'))

    model.add(Dense(units=1))

    model.compile(optimizer='rmsprop',
                  loss=loss,
                  metrics=['mse','mae'])

    return model

# stop_criteria = EarlyStopping(monitor='val_loss', min_delta=0.00001)

hidden_layer_neurons = [10, 40]

NN_dict = {'epochs': 38,
           'batch_size': 17,
           'shuffle': True,
           'validation_split': 0.2,
           # 'callback': stop_criteria
}

# mlp = build_neural_network(len(columns), hidden_layer_neurons)

# test_dates = get_random_test_dates(5, 2017, (4, 20), 2)

def test_nn_model(model, X, y, fit_params=NN_dict):
    '''
    Evaluates the model specified using 5-fold cross validation and tests model
    on unseen data.

    Parameters:
    ----------
    model : (object)
        Machine Learning object that implements both .fit() and .predict()
    X : (Pandas DataFrame)
        Contains attributes on which the model will be trained
    y : (Pandas Series)
        Target variable
    fit_params : (dictionary)
        Parameters to pass to the fit method

    Returns:
    ----------
    mae : (float)
        Testing Mean Absolute Error
    rmse : (float)
        Testing Root Mean Squared Error
    pm_mae : (float)
        Persistence model Mean Absolute Error
    pm_rmse : (float)
        Persistence model Root Mean Squared Error
    '''
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.15)

    history = model.fit(x_train.values,
              y_train.values,
              epochs=fit_params['epochs'],
              batch_size=fit_params['batch_size'],
              shuffle=fit_params['shuffle'],
              validation_split=fit_params['validation_split'],
              # callbacks=[fit_params['callback']],
              verbose=1)


    # evaluation = model.evaluate(x_test.values, y_test.values, verbose=1)

    y_hat = model.predict(x_test)
    mae = mean_absolute_error(y_test, y_hat)
    rmse = np.sqrt(mean_squared_error(y_test, y_hat))

    pm_rmse = np.sqrt(mean_squared_error(y_test, x_test['DNI'].values))
    pm_mae = mean_absolute_error(y_test, x_test['DNI'].values)

    return mae, rmse, pm_mae, pm_rmse