
import pandas as pd
from constants import *




index_names = ['engine', 'cycle']
# Operational conditions: altitude, mach_number and throttle_resolver_angle
operational_condition_names = ['altitude',  'mach_nr', 'TRA']
sensor_names = ['T2', # total temperature at fan inlet
                'T24',# total temperature at LPC outlet
                'T30', # total temperature at HPC outlet
                'T50', # total temperature at LPT outlet
                'P2', # Pressure at fan inlet
                'P15', #Total pressure in bypass-duct
                'P30', #Total pressure at HPC outlet
                'Nf', #Physical fan speed rpm
                'Nc', #Physical core speed rpm
                'epr', #Engine pressure ratio (P50/P2)
                'Ps30', #Static pressure at HPC outlet
                'phi', #Ratio offuel flow to Ps30
                'NRf', #Corrected fan speed
                'NRc', #Corrected core speed
                'BPR', #Bypass Ratio
                'farB', #Burner fuel-air ratio
                'htBleed', #Bleed Enthalpy
                'Nf_dmd', # Demanded fan speed rpm
                'PCNfR_dmd', #Demanded corrected fan speed rpm
                'W31', #HPT coolant bleed lbm/s
                'W32', #LPT coolant bleed
                ]
# options to visualize the datadrame
col_names =  index_names + operational_condition_names + sensor_names

df_train = pd.read_csv(fr'Data\train_{DATASET_NAME}.txt' ,  sep = ' ' , names=col_names, index_col = False,  usecols=range(len(col_names))) 


df_test = pd.read_csv(fr'Data\test_{DATASET_NAME}.txt' , sep=' ' , names= col_names, index_col = False,  usecols=range(len(col_names)))


# Prepare the data
test_labels = pd.read_csv(fr"Data\RUL_{DATASET_NAME}.txt", header=None)
df_train_grouped = df_train.groupby('engine')
df_train_last_cycle = df_train_grouped.max()['cycle']
df_train_with_labels = df_train.copy()
df_train_with_labels['RUL'] = df_train_with_labels.apply(lambda row: df_train_last_cycle[row['engine']] - row['cycle'], axis=1)

sensor_columns = df_train_with_labels.columns[5:-1]  # Exclude 'engine', 'cycle', and 'RUL'
uncorrelated_sensors = ["T2","P2", "P15", "epr", "farB", "Nf_dmd", "PCNfR_dmd"]
sensors_of_interest = [sens for sens in sensor_columns if sens not in uncorrelated_sensors]

# Cap RUL to 125
df_train_with_labels['RUL'] = df_train_with_labels['RUL'].clip(upper=125)
test_labels = test_labels.clip(upper=125)


df_test_grouped = df_test.groupby('engine')
df_test_last = df_test_grouped.last() # last cycle of each engine in the test set


# helper function
def fig_size(x_ratio=1.0, y_ratio=1.0):
    """
    Assuming an A4 paper size, this function returns a tuple
    representing the figure size in inches.
    parameters:
    x_ratio: float, ratio of the width relative to A4 width
    y_ratio: float, ratio of the height relative to A4 height
    """
    A4_WIDTH = 6.202  # A4 paper text width in inches
    A4_HEIGHT = 9.3562  # A4 paper text height in inches
    if x_ratio <= 0 or y_ratio <= 0:
        raise ValueError("Ratios must be positive numbers.")
    return (A4_WIDTH * x_ratio, A4_HEIGHT * y_ratio)