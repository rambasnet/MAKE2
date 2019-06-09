import os, sys
import zipfile
import xml.dom.minidom

class ODFReader:
    def __init__(self,filename):
        """
        Open an ODF file.
        """
        self.filename = filename
        self.m_odf = zipfile.ZipFile(filename)
        self.filelist = self.m_odf.infolist()

    def showManifest(self):
        """
        Just tell me what files exist in the ODF file.
        """
        for s in self.filelist:
            #print s.orig_filename, s.date_time,
            print s.orig_filename, s.file_size, s.compress_size, s.date_time, s.filename, s.create_system, s.CRC
            #print s.orig_filename

    def getContents(self):
        """
        Just read the paragraphs from an XML file.
        """
        ostr = self.m_odf.read('content.xml')
        doc = xml.dom.minidom.parseString(ostr)
        paras = doc.getElementsByTagName('text:p')
        print "I have ", len(paras), " paragraphs "
        self.text_in_paras = []
        for p in paras:
            for ch in p.childNodes:
                if ch.nodeType == ch.TEXT_NODE:
                    self.text_in_paras.append(ch.data)

    def findIt(self,name):
        for s in self.text_in_paras:
            if name in s:
               print s.encode('utf-8')

if __name__ == '__main__':
    """
    Pass in the name of the incoming file and the
    phrase as command line arguments. Use sys.argv[]
    """
    #filename = sys.argv(0)
    filename = r'c:\documents and settings\ram\desktop\Bratabandha.rar'
    #phrase = sys.argv(1)
    if zipfile.is_zipfile(filename):
        myodf = ODFReader(filename) # Create object.
        myodf.showManifest()        # Tell me what files
                                    # we have here
        #myodf.getContents()         # Get the raw
                                    # paragraph text.
        #myodf.findIt(phrase)        # find the phrase ...