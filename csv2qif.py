#!/usr/bin/python

import sys
import json
import csv
import codecs

# Error handling
if len(sys.argv)!=4:
    print("[ERROR] Need exactly three input arguments.")
    print ("Usage example: python csv2qif.py <BANK_TEMPLATE> <INPUT_CSV> <OUTPUT_QIF>")

# "Parse" input arguments
bank_template_name = str(sys.argv[1])
input_csv_name = str(sys.argv[2])
output_qif_name = str(sys.argv[3])

print("Bank template:", bank_template_name)
print("Input CSV file:", input_csv_name)
print("Output QIF file:", output_qif_name)

# Read bank template file
with open(bank_template_name) as bank_template_file:
    bank_template_data = json.load(bank_template_file)

# Read CSV input file
with codecs.open(input_csv_name, 'r', encoding='utf-8', errors='ignore') as input_csv_file:
    reader = csv.reader(input_csv_file, delimiter=bank_template_data["file_delimiter"])
    line_nums = len(input_csv_file.readlines())

input_csv_data = [[],[],[],[]] # date, memo, amount, payee
counter = 0
with codecs.open(input_csv_name, 'r', encoding='utf-8', errors='ignore') as input_csv_file:
    reader = csv.reader(input_csv_file, delimiter=bank_template_data["file_delimiter"])
    for num, row in enumerate(reader):
        if num < bank_template_data['first_column']+1:
            continue
        if num == bank_template_data['last_column']-1+line_nums:
            break
        input_csv_data[0].append(row[bank_template_data['row_date']-1]); # date
        input_csv_data[1].append(row[bank_template_data['row_memo']-1]); # memo
        input_csv_data[2].append(float(row[bank_template_data['row_amount']-1].replace(bank_template_data['decimal_delimiter'],"."))); # account
        input_csv_data[3].append(row[bank_template_data['row_payee']-1]); # payee
        counter = counter + 1

# Write QIF output file
header = "!Account\nN%s\nT%s\n^\n"
item = "!Type:%s\nD%s\nT%f\nC\nP%s\nM%s\nL\n^\n"
with open(output_qif_name, 'w') as output_qif_file:
    output_qif_file.write(header%(bank_template_data['account_name'],bank_template_data['account_type']))
    for k in range(len(input_csv_data[0])):
        output_qif_file.write(item%(bank_template_data['account_type'],input_csv_data[0][k],input_csv_data[2][k],input_csv_data[3][k],input_csv_data[1][k]))

print(counter, "items written to output file.")
