import os
import shutil
import zipfile, os.path
import string

from xml.dom import minidom, Node

infile = 'Cramer.docx'
#infilePath = 'testfile'
fileData = ''

def docxParser(infile, extractMedia = False, MediaPath=""):
    unzip = zipfile.ZipFile(infile)
    dataFile = ''

    for name in unzip.namelist():
        if extractMedia:
            if name.find('media') != -1:
                imgName = name.split('/')
                imgFile = open(os.path.join(MediaPath, imgName[2]), 'wb')
                imgFile.write(unzip.read(name))
                imgFile.close()

        if name == '[Content_Types].xml':
            flag = 'header'
            dataDom = minidom.parseString(unzip.read(name))
            dataFile = DFS(dataDom.documentElement,flag).strip('/')

    buf = unzip.read(dataFile)
    flag = 'data'
    dataDom = minidom.parseString(buf)
    data = DFS(dataDom.documentElement, flag)

    #return data
    """
    # Main Data is written 
    tmpFile = open('tmp.txt','w')
    for ch in data:
        try:
            tmpFile.write(ch)
        except UnicodeEncodeError:
            print ch
    tmpFile.close()
    
    """
    
def DFS(rootNode, flag):
    global fileData

    if flag == 'header':
        for childNodes in rootNode.childNodes:
            if childNodes.nodeName == 'Override':
                if childNodes.attributes.get('PartName').value.endswith('document.xml'):
                    return childNodes.attributes.get('PartName').value

            DFS(childNodes,flag)

    if flag == 'data':
        for childNodes in rootNode.childNodes:
            if childNodes.nodeType  == 3:
                fileData = fileData +'\n'+ childNodes.nodeValue
            DFS(childNodes, flag)

    #return fileData



if __name__ == "__main__":
    import re
    splitter = re.compile(r'\W*')
    docxParser(infile)
    for word in splitter.split(fileData):
        try:
            print word
        except:
            print 'error'