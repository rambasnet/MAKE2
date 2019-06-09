#-----------------------------------------------------------------------------
# Name:        PDFToText.py
# Purpose:     
#
# Author:      Ram B Basnet
#
# Created:     2008/07/01
# RCS-ID:      $Id: PDFToText.py $
# Copyright:   (c) 2008
# Licence:     All Rights Reserved
# New field:   Whatever
#-----------------------------------------------------------------------------


#from pdftools.pdffile import PDFDocument
#from pdftools.pdftext import Text
import time
import pyPdf
import PlatformMethods

def GetText(path):
    content = u""
    # Load PDF into pyPDF
    pdf = pyPdf.PdfFileReader(file(path, "rb"))
    # Iterate pages
    for i in range(0, pdf.getNumPages()):
        # Extract text from page and add to content
        content += pdf.getPage(i).extractText() + "\n"
    # Collapse whitespace
    content = " ".join(content.replace(u"\xa0", " ").strip().split())
    return PlatformMethods.Decode(content)

"""
#print getPDFContent("test.pdf").encode("ascii", "ignore")

def ContentsToText(contents, startTime):
    for item in contents:
        if time.time() - startTime > 600:
            return
            
        if isinstance(item, type([])):
            for i in ContentsToText(item, startTime):
                if time.time() - startTime > 600:
                    return
                yield i
                #print 'i ', i
        elif isinstance(item, Text):
            yield item.text
            #print 'text ', item.text


def GetText(fileName):
    doc = PDFDocument(fileName)
    pageCount = doc.count_pages()
    text = []
    startTime=time.time()
    for pageNum in range(1, (pageCount+1)):
        if time.time() - startTime > 600:
            return ""
        
        #print 'for'
        page = doc.read_page(pageNum)
        contents = page.read_contents().contents
        text.extend(ContentsToText(contents, startTime))
        #print ContentsToText(contents)
    return "".join(text)
    
""" 
if __name__ == "__main__":
    import os.path
    import re
    import CommonFunctions
    stTime = time.time()
    splitter = re.compile(r'\W*')
    #docFileName = r'C:\Documents and Settings\Ram\Desktop\SummitVsIBMBadFiles\SU8003444^OnsiteEcommerceReviewwithResume.pdf'
    pdfFile = r'D:\\Make2Scan\\1.pdf'
    data = GetText(pdfFile)
    
    for word in splitter.split(data):
        try:
            print word
        except:
            print 'error'
            
    endTime = time.time()
    print endTime - stTime
    CommonFunctions.ConvertSecondsToDayHourMinSec(endTime-stTime)
    


