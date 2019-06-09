#-----------------------------------------------------------------------------
# Name:        HTMLParser.py
# Purpose:     
#
# Author:      Ram B. Basnet
#
# Created:     2008/06/30
# RCS-ID:      $Id: HTMLParser.py $
# Copyright:   (c) 2008
# Licence:     All Rights Reserved.
#-----------------------------------------------------------------------------


from BeautifulSoup import *
import re
from urlparse import urlparse, urljoin

def getText(fileName):
    fin = open(fileName, 'rb')
    soup = BeautifulSoup(fin.read())
    fin.close()
    g = soup.recursiveChildGenerator()
    text = unicode("")
    while True:
        try:
            item = g.next()
            if isinstance(item, unicode):
                #print 'navigable string ', item.contents
                if not isinstance(item, Comment) and not isinstance(item, Declaration):
                    itemText = item.strip()
                    #print 'itemText ', itemText
                    if itemText:
                        if not itemText.startswith("<!") and not itemText.startswith("&") and not itemText.startswith("doctype html "):
                            text += " " + itemText
                            #self.TextList.append(itemText)
            else:
                pass
        except StopIteration:
            break
    #self.Text = text
    return text
    
    

if __name__== "__main__":
    print getText("copyright.doc")
    

    
