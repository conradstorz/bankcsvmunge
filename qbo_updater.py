#qbo_updater

#files to be updated
filename = 'download.qbo'
cleanfile = 'clean.qbo'

#text to remove from transaction descriptions
bad_text = ['CKCD DEBIT ', 'AC-', 'POS DEBIT ', 'POS DB ']

import os
import re
import sys
import logging

#establish logging state
FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
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
            sys.exit(1)

        logging.debug(file_contents)
        logging.info('File contents read successfully.', extra=d)

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
        logging.debug(line, extra=d)
        line = re.sub(r' +', ' ', line) #remove duplicate spaces from within line
        line = re.sub(r' \d\d\d\d ', ' ', line) #remove 4 digit date from within line
        if line.startswith(memotag):
            line = line.replace(memotag, '').lstrip() #remove memotag
            for t in text: #remove each occurance from line
                line = line.replace(t, '').lstrip() #strip leading and trailing whitespace
                logging.debug(line, extra=d)

            line = memotag + line #replace memotag
            name_line = line.replace(memotag, nametag)

        if line.startswith(nametag):
            line = name_line #replace nameline with memoline

        logging.debug(line, extra=d)
        clean.append(line)

    return clean[::-1] #return lines in same order as submitted

if __name__ == "__main__":
    fc = read_base_file('./', filename)

    result = clean_qbo_file(fc, bad_text)

    #Attempt to write results to cleanfile
    try:
        with open(cleanfile, 'w') as f:
            f.writelines(result)
    except Exception as e:
        logging.exception("Error in writing %s", cleanfile, extra=d)
        logging.warning(str(e), extra=d)
        sys.exit(1)

    logging.info('File contents written successfully.', extra=d)

    logging.info('Attempting to remove old file...', extra=d)

    if os.path.exists(filename):
        try:
            os.remove(filename)
        except OSError as e:
            logging.warning("Error: %s - %s." % (e.filename, e.strerror), extra=d)
            sys.exit(1)
        logging.info("Success removing %s" % filename, extra=d)

    else:
        logging.info("Sorry, I can not find %s file." % filename, extra=d)

    #declare program end
    logging.info('Program End: %s', 'nominal', extra=d)
    sys.exit(0)

