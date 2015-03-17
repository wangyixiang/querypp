#!/usr/bin/env python
#coding:utf-8

import urllib
import os
import logging

PPURLDATA=r"../PPURLALL"
ED2K_URL_ENDING_MARK = "|/"
ED2K_SPILTER = "|"

class BadFormedED2K(Exception):
    pass

def is_ed2k_wellformed(ed2k_url):
    if ed2k_url[-2:] != ED2K_URL_ENDING_MARK:
        return False
    return True

def guess_fileformat(filename):
    finished = False
    fileformat = "unknown"
    while (not finished):
        filebase, fileformat = os.path.splitext(filename)
        fileformat = fileformat.strip()
        if fileformat.isdigit():
            logging.info(filename)
            logging.info("the fileformat are all digits")
            filename = filebase
            continue
        finished = True
    if (len(fileformat) > 7):
        logging.warn(filename)
        logging.warn("The fileformart %s is larger than 7" % fileformat)
    return fileformat

def decode_filename(filename):
    return urllib.unquote(filename).decode("utf-8")

#column list
#BookName, BookFileFormat, BookRawED2k, BookDecodedName, isValid(True), isDownloadable(True), 
COLUMN_BookName = "BN"
COLUMN_BookFileFormat = "BFF"
COLUMN_BookRawED2K = "BRED2K"
COLUMN_BookDecodeName = "BDN"
COLUMN_ED2KIsValid = "EIV"
COLUMN_BookIsDownloadable = "BID"

#return the dict which repesent a row will be inserted into the database
#the filename is the 3rd field
def get_rowdata(ed2k_url):
    field_list = ed2k_url.split(ED2K_SPILTER)
    if ( (not is_ed2k_wellformed(ed2k_url)) or (len(field_list) != 7) ):
        raise BadFormedED2K()
    result_dict = dict()
    result_dict[COLUMN_BookName] = field_list[2]
    result_dict[COLUMN_BookFileFormat] = guess_fileformat(field_list[2])
    result_dict[COLUMN_BookRawED2K] = ed2k_url
    result_dict[COLUMN_BookDecodeName] = decode_filename(field_list[2])
    result_dict[COLUMN_ED2KIsValid] = True
    result_dict[COLUMN_BookIsDownloadable] = True
    
    return result_dict
    
def insert_rowdata(row_dict):
    #print row_dict
    pass

def feed_data_from_datafile(filename):
    if(not os.path.exists(filename)):
        raise IOError("file %s can't be found!" & filename)
    datalinenum = 0
    datafile = open(filename)
    badEd2k = 0
    badcoding = 0
    for dataline in datafile:
        try:
            datalinenum += 1
            dataline = dataline.strip()
            if dataline == "":
                continue
            datarow = get_rowdata(dataline.strip())
            insert_rowdata(datarow)
        except BadFormedED2K as e:
            #print str(datalinenum) + " : "
            try:
                #print decode_filename(dataline).encode("gb18030")
                pass
            except:
                badcoding += 1
                pass
            badEd2k += 1
    print str(badEd2k)
    print str(badcoding)
    datafile.close()


def main():
    feed_data_from_datafile(PPURLDATA)


if __name__ == "__main__":
    main()