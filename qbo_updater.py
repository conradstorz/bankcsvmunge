#qbo_updater

#files to be updated
filename = 'download(41).qbo'

#text to remove from transaction descriptions
bad_text = ['CKCD DEBIT ', 'AC-', 'POS DEBIT ', 'POS DB ', r'\d\d/\d\d ']

import os
import logging

#establish logging state
FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
logging.basicConfig(format=FORMAT)
d = {'clientip': 'xxx.xxx.xxx.xxx', 'user': 'qbo_loggs'}
#logging.warning('Protocol problem: %s', 'connection reset', extra=d)

#declare program start
logging.info('Program Start: %s', 'nominal', extra=d)


def read_base_file(data_folder, base_file):
    #files = map(lambda x: os.path.join(data_folder, x), os.listdir(data_folder))
    files = base_file
    logging.debug(files)
    if base_file in files:
        try:
            with open(base_file) as f:
                file_contents = f.readlines()
        except Exception as e:
            logging.exception("Error in reading %s", base_file, extra=d)
            logging.warning(str(e), extra=d)
            file_contents = []
        logging.debug(file_contents)
        logging.info('File contents read successfully', extra=d)

    else:
        logging.warning("File Not Found %s", base_file, extra=d)
        file_contents = []

    return file_contents


def clean_qbo_file(lines, text):
    memotag = '<MEMO>'
    nametag = '<NAME>'
    name_line = '<ERROR>'
    clean = []
    for line in lines[::-1]: #in reverse order [::-1] so we see memo before name lines
        if line.startswith(memotag):
            for t in text: #remove each occurance from line
                line = line.replace(t, '')
                logging.warning(line, extra=d)
            #make a copy of result
            name_line = line.replace(memotag, nametag)
        if line.startswith(nametag):
            line = name_line
        clean.append(line)

    return clean[::-1] #return lines in same order as submitted

if __name__ == "__main__":
    fc = read_base_file('./', filename)
    print(fc)
    result = clean_qbo_file(fc, bad_text)


