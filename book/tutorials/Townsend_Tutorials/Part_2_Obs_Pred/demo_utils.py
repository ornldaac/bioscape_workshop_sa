from typing import List, Tuple, Dict
import numpy as np 
import pandas as pd
from sklearn.cross_decomposition import PLSRegression
from sklearn.metrics import r2_score #root_mean_squared_error,

DEFAULT_BAD_BAND_RANGES = [(300, 400), (1320, 1430), (1800, 1960), (2450, 2600)]

def read_data(data_csv, 
              trait_col) -> Tuple[np.ndarray, np.ndarray, List[float]]:
    '''
    Returns X, y, wavelengths.
    '''
    df = pd.read_csv(data_csv)
    refl_cols = [c for c in df.columns if 'X_' in c]
    wavelengths = [float(c.split('_')[-1]) for c in df.columns if 'X_' in c]
    return (df[refl_cols].values, df[trait_col].values, wavelengths)


def split_samples(indices: np.ndarray,
                  n_eval: int,
                  rng: np.random.Generator) -> Tuple[np.ndarray, np.ndarray]:
    '''
    Splits indices contents into two random pieces with lengths:
    (len(indices) - n_eval) and n_eval.
    '''
    permutation = rng.permutation(np.arange(indices.size))
    n_other = indices.size - n_eval
    return (indices[permutation[:n_other]], indices[permutation[n_other:]])


def unit_vector_normalization(X: np.ndarray) -> np.ndarray:
    '''
    Normalizes each row to be a unit vector.
    '''
    return X/np.linalg.norm(X, axis=1, keepdims=True) 


def bad_bands_removal(X: np.ndarray,
                      column_wavelengths: List[float],
                      remove_ranges: List[Tuple[float, float]] = DEFAULT_BAD_BAND_RANGES) -> Tuple[np.ndarray, np.ndarray]:
    '''
    Removes columns whose wavelengths lie in the specified ranges.
    '''
    wanted_cols, wanted_waves = [], []
    for (i, w) in enumerate(column_wavelengths):
        remove = False
        for r in remove_ranges:
            if (r[0] <= w <= r[1]):
                remove = True
        if not remove:
            wanted_cols.append(i)
            wanted_waves.append(w)
    return (X[:, np.array(wanted_cols, dtype=np.int32)], np.array(wanted_waves)) 


#def get_rmses_for_one_inner_loop_step(X_train: np.ndarray, 
#                                      y_train: np.ndarray, 
#                                      n_components: int,
#                                      X_valid: np.ndarray,
#                                      y_valid: np.ndarray) -> np.ndarray:
#    '''
#    Returns vector of rmses of length n_components.
#    '''
#    rmses = []
#    for nc in (np.arange(n_components) + 1):
#        m = PLSRegression(n_components=nc, scale=False)
#        m = m.fit(X_train, y_train)
#        y_pred = m.predict(X_valid)
#        rmses.append(root_mean_squared_error(y_valid, y_pred, multioutput='uniform_average'))
#    return np.array(rmses)


def get_hyperparameter_details_for_one_inner_loop(X_full: np.array,
                                                  y_full: np.array,
                                                  calib_indices: np.ndarray,
                                                  n_valid: int,
                                                  n_steps: int,
                                                  n_components: int,
                                                  rng: np.random.Generator) -> [np.ndarray, np.ndarray, int]:
    '''
    Returns:
    all rmses in a matrix, shape (n_steps, n_components)
    mean_rmses in a matrix, shape (1, n_components)
    n_components that corresponds to minimum of mean_rmses
    '''
    rmse_arrs = []
    for i in range(n_steps):
        train_idxs, valid_idxs = split_samples(indices=calib_indices,
                                               n_eval=n_valid,
                                               rng=rng) 
        rmse_arr = get_rmses_for_one_inner_loop_step(X_train=X_full[train_idxs, :],
                                                     y_train=y_full[train_idxs],
                                                     n_components=n_components,
                                                     X_valid=X_full[valid_idxs, :],
                                                     y_valid=y_full[valid_idxs])
        rmse_arrs.append(rmse_arr.reshape(1, -1))
    rmse_arrs = np.vstack(rmse_arrs)
    mean_rmses = np.mean(rmse_arrs, axis=0, keepdims=True) 
    opt_ncomps = np.argmin(mean_rmses) + 1
    return (rmse_arrs, mean_rmses, opt_ncomps)


def get_raw_std_model(X: np.ndarray,
                      y: np.ndarray,
                      n_components: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    '''
    Returns: raw coefficients, intercepts, std coefficients
    '''
    raw = PLSRegression(n_components=n_components, scale=False)
    raw = raw.fit(X, y) 
    std = PLSRegression(n_components=n_components, scale=True)
    std = std.fit(X, y)
    return (raw.coef_, (raw.intercept_ - raw.coef_@raw._x_mean).reshape(-1, 1), std.coef_) 

def get_predictions(W: np.ndarray,
                    b: np.ndarray,
                    X: np.ndarray,
                    y: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    y_pred = X@W.T + b
    rmse = root_mean_squared_error(y, y_pred)
    if not isinstance(rmse, np.ndarray):
        rmse = np.array([[rmse]])
    r2 = r2_score(y, y_pred)
    if not isinstance(r2, np.ndarray):
        r2 = np.array([[r2]])
    return (y_pred, rmse, r2)
