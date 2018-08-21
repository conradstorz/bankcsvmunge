#CSV munge

#input CSV from bank and remove unwanted characters from transaction descriptions

import re
import sys
import csv
import pandas as pd

inpfile = 'raw_bank_xacts.csv'
outfile = 'cleaned_'+inpfile

try:
    df = pd.read_csv(inpfile)
except Exception as e:
    print("Error in reading", inpfile)
    print(e)
    df = pd.DataFrame()
    sys.exit(1)

print('Original...')
print(df)

#df['Description'] = df['Description'].replace(to_replace='/d/d\/d/d ', value='', regex=True)

#map(lambda x: str.replace(x, "AC-", ""), df['Description'])
#for i in df['Description'] .replace('AC-', '')

df['Description'] = df['Description'].str.replace(r'\d\d/\d\d ', '').astype('str')
#df['Description'] = re.sub('\d\d/\d\d ', '', df['Description'].str) #remove dates from description

df['Description'] = df['Description'].str.replace('CKCD DEBIT ', '')

df['Description'] = df['Description'].str.replace('POS DB ', '')

df['Description'] = df['Description'].str.replace('AC-', '')

df['Description'] = df['Description'].str.replace('POS DEBIT', '')

#df['Description'] = df['Description']

print()
print('Altered...')
print(df)

df.to_csv(outfile, encoding='utf-8', index=False) #, quoting=csv.QUOTE_NONNUMERIC