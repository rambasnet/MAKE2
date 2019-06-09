#-----------------------------------------------------------------------------
# Name:        OfficeToText.py
# Purpose:     
#
# Author:      Ram B. Basnet
#
# Created:     2008/07/01
# RCS-ID:      $Id: OfficeToText.py $
# Copyright:   (c) 2008
# Licence:     All Rights Reserved.
#-----------------------------------------------------------------------------

import win32com.client

import CommonFunctions

def Excel(excelfile, psfile, printer):
    pythoncom.CoInitializeEx(pythoncom.COINIT_APARTMENTTHREADED)
    myExcel = win32com.client.DispatchEx('Excel.Application')
    myExcel.Application.AskToUpdateLinks = 0
    Excel = myExcel.Workbooks.Open(excelfile, 0, False, 2)
    Excel.Saved = 1
    Excel.PrintOut(1, 5000, 1, False, printer, True, False, psfile)
    Excel.Close()
    myExcel.Quit()
    del myExcel
    del Excel
    pythoncom.CoUninitialize()
    
def WordToText(wordFileName):
    app = win32com.client.Dispatch('Word.Application')
    doc = app.Documents.Open(wordFileName)
    text = doc.Content.Text
    doc.Close()
    app.Quit()
    return text

def ExcelToText(excelFile):
    excel = win32com.client.Dispatch('Excel.Application')
    Excel = excel.Workbooks.Open(excelFile, 0, False, 2)
    print Excel.Content.Text
    excel.Visible = 1
    #Excel.Close()
    #excel.Quit()



def PowerpointToText(fileName):
    ppt = win32com.client.Dispatch('Powerpoint.Application')
    Powerpoint = ppt.Presentations.Open(fileName, False, False, False)
    #print Excel.Content.Text
    ppt.Visible = 1
    #Excel.Close()
    #excel.Quit()


if __name__ == "__main__":
    import os.path
    import time
    import re
    stTime = time.time()
    splitter = re.compile(r'\W*')
    docFileName = r'c:\test.doc'
    data = WordToText(docFileName)
    
    for word in splitter.split(data):
        try:
            print word
        except:
            print 'error'
            
    endTime = time.time()
    print endTime - stTime
    CommonFunctions.ConvertSecondsToDayHourMinSec(endTime-stTime)
    #print os.path.exists(r'Data\NSRL.db')
    #docFileName = r"C:\NMT\Research\ForensicsTool\EmailTest1\Attachments\2006-12-01 14.30.25 - Director's Secretary - Lawson Consultant Team - Lawson Consultant Team-cell and email.doc"
    #import os.path
    #print os.path.isfile(docFileName)
    
    #excelFile = r'C:\Documents and Settings\Ram\Desktop\Test\TomSavageKeywords.xls'
    #ExcelToText(excelFile)
    #pptFile = r'C:\Documents and Settings\Ram\Desktop\Test\BasnetCACTUSTextCat.ppt'
    #PowerpointToText(pptFile)
    
    
