#CSV munge

#input CSV from bank and remove unwanted characters from transaction descriptions

#import os
import pandas as pd

inpfile = 'raw_bank_xacts.csv'
outfile = 'cleaned_'+inpfile

try:
    df = pd.read_csv(inpfile)
except Exception as e:
    print("Error in reading", inpfile)
    print(e)
    df = pd.DataFrame()
