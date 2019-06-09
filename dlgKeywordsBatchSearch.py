#-----------------------------------------------------------------------------
# Name:        dlgEmailMapping.py
# Purpose:     
#
# Author:      Ram Basnet
#
# Created:     2008/04/17
# RCS-ID:      $Id: dlgEmailMapping.py $
# Copyright:   (c) 2008
# Licence:     All Rights Reserved.
#-----------------------------------------------------------------------------
#Boa:MDIChild:dlgKeywordsBatchSearch

import wx
import wx.lib.buttons
import time
import os.path, sys
import os, shutil

from wx.lib.anchors import LayoutAnchors

import CommonFunctions
from Search import *
import Globals
import images

def create(parent, StopwordsList=[]):
    return dlgKeywordsBatchSearch(parent, StopwordsList)

[wxID_DLGKEYWORDSBATCHSEARCH, 
 wxID_DLGKEYWORDSBATCHSEARCHBTNBROWSEKEYWORDSFILE, 
 wxID_DLGKEYWORDSBATCHSEARCHBTNBROWSEOUTPUTPATH, 
 wxID_DLGKEYWORDSBATCHSEARCHBTNCANCEL, wxID_DLGKEYWORDSBATCHSEARCHBTNOK, 
 wxID_DLGKEYWORDSBATCHSEARCHPANSETTINGS, 
 wxID_DLGKEYWORDSBATCHSEARCHSTATICTEXT1, 
 wxID_DLGKEYWORDSBATCHSEARCHSTATICTEXT2, 
 wxID_DLGKEYWORDSBATCHSEARCHTXTKEYWORDSFILE, 
 wxID_DLGKEYWORDSBATCHSEARCHTXTOUTPUTPATH, 
] = [wx.NewId() for _init_ctrls in range(10)]

class dlgKeywordsBatchSearch(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DLGKEYWORDSBATCHSEARCH,
              name='dlgKeywordsBatchSearch', parent=prnt, pos=wx.Point(580,
              280), size=wx.Size(433, 244), style=wx.DEFAULT_DIALOG_STYLE,
              title='Search Keywords in Batch and Create HTML Reports')
        self.SetClientSize(wx.Size(425, 210))
        self.SetAutoLayout(True)
        self.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.SetCursor(wx.STANDARD_CURSOR)
        self.SetMinSize(wx.Size(-1, -1))
        self.Center(wx.BOTH)

        self.btnOK = wx.Button(id=wxID_DLGKEYWORDSBATCHSEARCHBTNOK,
              label='&Start', name=u'btnOK', parent=self, pos=wx.Point(232,
              168), size=wx.Size(91, 23), style=0)
        self.btnOK.Bind(wx.EVT_BUTTON, self.OnBtnOKButton,
              id=wxID_DLGKEYWORDSBATCHSEARCHBTNOK)

        self.btnCancel = wx.Button(id=wxID_DLGKEYWORDSBATCHSEARCHBTNCANCEL,
              label=u'&Cancel', name=u'btnCancel', parent=self,
              pos=wx.Point(336, 168), size=wx.Size(75, 23), style=0)
        self.btnCancel.Bind(wx.EVT_BUTTON, self.OnBtnCancelButton,
              id=wxID_DLGKEYWORDSBATCHSEARCHBTNCANCEL)

        self.panSettings = wx.Panel(id=wxID_DLGKEYWORDSBATCHSEARCHPANSETTINGS,
              name='panSettings', parent=self, pos=wx.Point(16, 24),
              size=wx.Size(392, 128), style=wx.TAB_TRAVERSAL)
        self.panSettings.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.panSettings.SetAutoLayout(True)

        self.txtOutputPath = wx.TextCtrl(id=wxID_DLGKEYWORDSBATCHSEARCHTXTOUTPUTPATH,
              name='txtOutputPath', parent=self.panSettings, pos=wx.Point(16,
              80), size=wx.Size(312, 21), style=0, value='')
        self.txtOutputPath.Enable(True)

        self.staticText2 = wx.StaticText(id=wxID_DLGKEYWORDSBATCHSEARCHSTATICTEXT2,
              label='Keywords Text File:', name='staticText2',
              parent=self.panSettings, pos=wx.Point(16, 16), size=wx.Size(95,
              13), style=0)

        self.staticText1 = wx.StaticText(id=wxID_DLGKEYWORDSBATCHSEARCHSTATICTEXT1,
              label='Output Report Path:', name='staticText1',
              parent=self.panSettings, pos=wx.Point(16, 64), size=wx.Size(99,
              13), style=0)

        self.txtKeywordsFile = wx.TextCtrl(id=wxID_DLGKEYWORDSBATCHSEARCHTXTKEYWORDSFILE,
              name='txtKeywordsFile', parent=self.panSettings, pos=wx.Point(16,
              32), size=wx.Size(312, 21), style=0, value='')

        self.btnBrowseKeywordsFile = wx.Button(id=wxID_DLGKEYWORDSBATCHSEARCHBTNBROWSEKEYWORDSFILE,
              label='...', name='btnBrowseKeywordsFile',
              parent=self.panSettings, pos=wx.Point(336, 32), size=wx.Size(40,
              23), style=0)
        self.btnBrowseKeywordsFile.Bind(wx.EVT_BUTTON,
              self.OnBtnBrowseKeywordsFileButton,
              id=wxID_DLGKEYWORDSBATCHSEARCHBTNBROWSEKEYWORDSFILE)

        self.btnBrowseOutputPath = wx.Button(id=wxID_DLGKEYWORDSBATCHSEARCHBTNBROWSEOUTPUTPATH,
              label='...', name='btnBrowseOutputPath', parent=self.panSettings,
              pos=wx.Point(336, 80), size=wx.Size(40, 24), style=0)
        self.btnBrowseOutputPath.Bind(wx.EVT_BUTTON,
              self.OnBtnBrowseOutputPathButton,
              id=wxID_DLGKEYWORDSBATCHSEARCHBTNBROWSEOUTPUTPATH)

    def __init__(self, parent, StopwordsList=[]):
        self._init_ctrls(parent)
        self.SetIcon(images.getMAKE2Icon())
        
        self.StopwordsList = StopwordsList
        self.search = Search(Globals.TextCatFileName, self.StopwordsList)
    
    def CheckInputError(self):
        errMsg = ""
        
        if not self.txtKeywordsFile.GetValue():
            errMsg = "Please Enter or Browse to Keywords File Path!"
            
        elif not self.txtOutputPath.GetValue():
            errMsg = "Please Enter or Browse Path to Output Report!"
            
        
        if errMsg:
            CommonFunctions.ShowErrorMessage(self, errMsg)
            return True
        else:
            return False
        
    def OnBtnOKButton(self, event):
        if self.CheckInputError():
            return
        
        busy = wx.BusyInfo("Generating Keywords Search Report...It might take some time; just relax!")
        wx.Yield()
        
        self.OutputPath = self.txtOutputPath.GetValue().strip()
        if not os.path.exists(self.OutputPath):
            try:
                os.makedirs(self.OutputPath)
            except Exception, value:
                print 'Error ::', value
                return
        
        
        self.ReadKeywords()
        self.CreateHTMLFrames()
        self.CreateDocListFiles()
        self.Close()
        event.Skip()
        
        
    def OnBtnCancelButton(self, event):
        self.Close()



    def OnBtnBrowseKeywordsFileButton(self, event):
        dlg = wx.FileDialog(self, "Open Keywords Text File", ".", "", "*.txt", wx.OPEN)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                self.txtKeywordsFile.SetValue(dlg.GetPath())
        finally:
            dlg.Destroy()
            
        event.Skip()

    def OnBtnBrowseOutputPathButton(self, event):
        dlg = wx.DirDialog(self, message="Choose Empty Folder to Save Search Results")
        try:
            if dlg.ShowModal() == wx.ID_OK:
                self.txtOutputPath.SetValue(dlg.GetPath())
            
        finally:
            dlg.Destroy()
        event.Skip()

    
    def CreateHTMLFrames(self):
        indexPath = os.path.join(self.OutputPath, 'index.html')
        
        fout = open(indexPath, 'w')
        html = """
        <html>
            <head>
                <title>EmailSearch</title>
            </head>
            
            <frameset rows="*" cols="15%,30%,*" framespacing="0" frameborder="yes" border="3">
                <frame src=".\Keywords.html" name="keywordsFrame" scrolling="yes" id="keywordsFrame" title="Keywords Frame" />
                <frame src=".\DocList.html" name="docListFrame" scrolling="yes" id="docListFrame" title="Documents List" />
                <frame src=".\DocView.html" name="docViewFrame" scrolling="yes" id="docViewFrame" title="Document View Frame" />
            </frameset>
        <noframes>
        <body>
        </body></noframes>
        </html>
        """
        fout.write(html)
        fout.close()

        docListPath = os.path.join(self.OutputPath, 'DocList.html')
        html = """
        <html>
            <head>
                <title>Dcouments List</title>
            </head>
            <body>
            <p><B><I> Contains Document List for Each Keyword </I></B></P>
            </body>
        </html>
        """
        fout = open(docListPath, 'w')
        fout.write(html)
        fout.close()
        
        
        docViewPath = os.path.join(self.OutputPath, 'DocView.html')
        fout = open(docViewPath, 'w')
        html = """
        <html>
            <head>
                <title>Document Viewer</title>
            </head>
            <body>
            <p><B><I> Opens Each Document when Clicked on Document List </I></B></P>
            </body>
        </html>
        """
        fout.write(html)
        fout.close()
        
        
        
    def ReadKeywords(self):
        fin = open(self.txtKeywordsFile.GetValue(), 'r')
        lines = fin.readlines()
        self.Keywords = []
        for line in lines:
            self.Keywords.append(line.lower().strip())
            
        fin.close()


    def CreateDocListFiles(self):
        filePath = os.path.join(self.OutputPath, 'Keywords')
        docPath = os.path.join(self.OutputPath, 'Docs')
        if not os.path.exists(filePath):
            os.mkdir(filePath)
            
        if not os.path.exists(docPath):
            os.mkdir(docPath)
        
        keywordsPath = os.path.join(self.OutputPath, 'Keywords.html')
        fout = open(keywordsPath, 'w')
            
        html = """
        <html>
            <head>
                <title>Keywords List</title>
            </head>
            <body>
            <h1><b>Keywords List</b></h1>\n
        """
        fout.write(html)
        
        for word in self.Keywords:
            DocPaths, totalResults = self.search.GetRankedDocuments(word)
            keywordFile = word + ".html"
            fout.write('<a href=".\\Keywords\\%s" target="docListFrame">%s (%d) </a><br />'%(keywordFile, word, totalResults))
            docListPath = os.path.join(filePath, keywordFile)
            fout1 = open(docListPath, 'w')
            fout1.write("<html><head><title>Docs List</title></head><body>\n")
            fout1.write("<h1><b>Documents List for <u>%s</u> =></b></h1>\n"%word)
            for result in DocPaths:
                href = result[result.find(os.sep)+1:].replace(os.sep, '-')
                destPath = os.path.join(docPath, href)
                fout1.write('<a href="..\\Docs\\%s" target="docViewFrame">%s</a><br />'%(href, result))
                if not os.path.exists(destPath):
                    shutil.copy2(result, destPath)
            fout1.write('</body></html>\n')
            fout1.close()
            
        fout.write('</body></html>\n')
        fout.close()
                
                
            
            
            
            
