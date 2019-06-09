#Boa:MDIChild:dlgKeywordsSearchReport

#-----------------------------------------------------------------------------
# Name:        dlgEmailKeyExtract.py
# Purpose:     
#
# Author:      Ram B. Basnet
#
# Created:     2008/04/17
# RCS-ID:      $Id: dlgEmailKeyExtract.py $
# Copyright:   (c) 2008
# Licence:     All Rights Reserved.

#-----------------------------------------------------------------------------

import wx
import wx.lib.buttons
import time
import os.path, sys
import shutil

from wx.lib.anchors import LayoutAnchors
import images

def create(parent):
    return dlgKeywordsSearchReport(parent)

[wxID_DLGKEYWORDSSEARCHREPORT, 
 wxID_DLGKEYWORDSSEARCHREPORTBTNBROWSEKEYWORDSFILE, 
 wxID_DLGKEYWORDSSEARCHREPORTBTNBROWSERESULTPATH, 
 wxID_DLGKEYWORDSSEARCHREPORTBTNCANCEL, wxID_DLGKEYWORDSSEARCHREPORTBTNOK, 
 wxID_DLGKEYWORDSSEARCHREPORTPANSETTINGS, 
 wxID_DLGKEYWORDSSEARCHREPORTSTATICTEXT1, 
 wxID_DLGKEYWORDSSEARCHREPORTSTATICTEXT3, 
 wxID_DLGKEYWORDSSEARCHREPORTTXTKEYWORDSFILE, 
 wxID_DLGKEYWORDSSEARCHREPORTTXTRESULTFOLDERPATH, 
] = [wx.NewId() for _init_ctrls in range(10)]

class dlgKeywordsSearchReport(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DLGKEYWORDSSEARCHREPORT,
              name='dlgKeywordsSearchReport', parent=prnt, pos=wx.Point(855,
              328), size=wx.Size(433, 287), style=wx.DEFAULT_DIALOG_STYLE,
              title='Keywords Search Report')
        self.SetClientSize(wx.Size(425, 256))
        self.SetAutoLayout(True)
        self.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.SetCursor(wx.STANDARD_CURSOR)
        self.SetMinSize(wx.Size(-1, -1))
        self.Center(wx.BOTH)

        self.btnOK = wx.Button(id=wxID_DLGKEYWORDSSEARCHREPORTBTNOK,
              label='&Generate Report', name=u'btnOK', parent=self,
              pos=wx.Point(216, 216), size=wx.Size(107, 23), style=0)
        self.btnOK.Bind(wx.EVT_BUTTON, self.OnBtnOKButton,
              id=wxID_DLGKEYWORDSSEARCHREPORTBTNOK)

        self.btnCancel = wx.Button(id=wxID_DLGKEYWORDSSEARCHREPORTBTNCANCEL,
              label=u'&Cancel', name=u'btnCancel', parent=self,
              pos=wx.Point(336, 216), size=wx.Size(75, 23), style=0)
        self.btnCancel.Bind(wx.EVT_BUTTON, self.OnBtnCancelButton,
              id=wxID_DLGKEYWORDSSEARCHREPORTBTNCANCEL)

        self.panSettings = wx.Panel(id=wxID_DLGKEYWORDSSEARCHREPORTPANSETTINGS,
              name='panSettings', parent=self, pos=wx.Point(16, 24),
              size=wx.Size(392, 176), style=wx.TAB_TRAVERSAL)
        self.panSettings.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.panSettings.SetAutoLayout(True)

        self.txtResultFolderPath = wx.TextCtrl(id=wxID_DLGKEYWORDSSEARCHREPORTTXTRESULTFOLDERPATH,
              name='txtResultFolderPath', parent=self.panSettings,
              pos=wx.Point(16, 48), size=wx.Size(312, 21), style=0, value='')
        self.txtResultFolderPath.Enable(True)

        self.staticText1 = wx.StaticText(id=wxID_DLGKEYWORDSSEARCHREPORTSTATICTEXT1,
              label='Keywords Text File:', name='staticText1',
              parent=self.panSettings, pos=wx.Point(16, 88), size=wx.Size(95,
              13), style=0)

        self.btnBrowseResultPath = wx.Button(id=wxID_DLGKEYWORDSSEARCHREPORTBTNBROWSERESULTPATH,
              label='...', name='btnBrowseResultPath', parent=self.panSettings,
              pos=wx.Point(336, 48), size=wx.Size(40, 24), style=0)
        self.btnBrowseResultPath.Bind(wx.EVT_BUTTON,
              self.OnBtnBrowseResultPathButton,
              id=wxID_DLGKEYWORDSSEARCHREPORTBTNBROWSERESULTPATH)

        self.staticText3 = wx.StaticText(id=wxID_DLGKEYWORDSSEARCHREPORTSTATICTEXT3,
              label='Result Folder Path:', name='staticText3',
              parent=self.panSettings, pos=wx.Point(16, 32), size=wx.Size(92,
              13), style=0)

        self.txtKeywordsFile = wx.TextCtrl(id=wxID_DLGKEYWORDSSEARCHREPORTTXTKEYWORDSFILE,
              name='txtKeywordsFile', parent=self.panSettings, pos=wx.Point(16,
              104), size=wx.Size(312, 21), style=0, value='')
        self.txtKeywordsFile.Enable(True)

        self.btnBrowseKeywordsFile = wx.Button(id=wxID_DLGKEYWORDSSEARCHREPORTBTNBROWSEKEYWORDSFILE,
              label='...', name='btnBrowseKeywordsFile',
              parent=self.panSettings, pos=wx.Point(336, 104), size=wx.Size(40,
              24), style=0)
        self.btnBrowseKeywordsFile.Bind(wx.EVT_BUTTON,
              self.OnBtnBrowseKeywordsFileButton,
              id=wxID_DLGKEYWORDSSEARCHREPORTBTNBROWSEKEYWORDSFILE)

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.SetIcon(images.getMAKE2Icon())
    
    def OnBtnOKButton(self, event):
        self.startTime = time.time()
        busy = wx.BusyInfo("Extracting Emails and Attachments and generating reports...It might take some time; just relax!")
        wx.Yield()
        
        """
        import keyextract
        keyextract.msg_Folder_Path = self.txtMessageFolderPath.GetValue()
        keyextract.result_Dir_Path = self.txtResultFolderPath.GetValue()
        keyextract.file_Name = self.txtKeywordsFile.GetValue()
        keyextract.DoIt()
        """
        
        db = SqliteDatabase(Globals.EmailsFileName)
        if not db.OpenConnection():
            return
        
        keywordsFile = self.txtKeywordsFile.GetValue()
        outPutPath = self.txtResultFolderPath.GetValue()
        if not outPutPath:
            outPutPath = "."
            
        self.MessageOutputPath = os.path.join(outPutPath, "Messages")
        
        if not keywordsFile:
            return
        
        
        keywordsList = self.ReadKeywords(keywordsFile)
            
        
        for keyword in keywordsList:
            self.searchBitMap(db, keyword.strip())
            
        self.elapsedTime = CommonFunctions.ConvertSecondsToYearDayHourMinSec(time.time() - self.startTime)
        self.MessagesHeading = "%d Results for %s (%s)"%(len(self.SearchDocIDList), self.searchWords, self.elapsedTime)
        self.Close()
        #event.Skip()
        
        
    def OnBtnCancelButton(self, event):
        self.Close()


    def OnBtnBrowseMessagePathButton(self, event):
        dlg = wx.DirDialog(self)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                self.txtMessageFolderPath.SetValue(dlg.GetPath())
            
        finally:
            dlg.Destroy()
        event.Skip()
        

    def OnBtnBrowseResultPathButton(self, event):
        dlg = wx.DirDialog(self)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                self.txtResultFolderPath.SetValue(dlg.GetPath())
            
        finally:
            dlg.Destroy()
        event.Skip()
        

    def OnBtnBrowseKeywordsFileButton(self, event):
        dlg = wx.FileDialog(self, "Open Text File", ".", "", "*.*", wx.OPEN)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                self.txtKeywordsFile.SetValue(dlg.GetPath())
        finally:
            dlg.Destroy()

        event.Skip()

    
    def searchBitMap(self, db, keyword, encoded=True):
        
        self.SearchDocIDList = []
        #self.webDocs = {}
        self.searchWords = ''
        self.wordList = []
        self.startTime = 0
        self.elapsedTime = ''
        
        self.encoded = encoded
        word = ''
        totalResult = 0
        
        self.searchWords = keyword
        if not self.searchWords:
            #CommonFunctions.ShowErrorMessage(self, "Failed to Export Phone List. Error: %s"%value)
            return
        
        if self.SearchMenu.FindItem(self.searchWords) < 0:
            id = wx.NewId()
            self.SearchMenu.Append(id, self.searchWords)
            self.Bind(wx.EVT_MENU, self.OnSearchFromSearchMenu, id=id)
        
        if encoded:
            query = "select keyword, compressed from %s where (Keyword = "%Constants.TextCatBitMapIndex
        else:
            query = "select keyword, bitmap from %s where (Keyword = '"%Constants.TextCatBitMapIndex
        
        i = 0    
        for word in string.split(self.searchWords, ' '):
            word = word.strip().lower()
            #word = word.strip('"')
                    
            if word not in Globals.EmailsStopwords:
                i += 1
                self.wordList.append(word)
                if i == 1:
                    query += db.SqlSQuote(word)
                else:
                    query += " or keyword = %s"%(db.SqlSQuote(word))
        
        query += ")"
        if self.wordList < 0:
            return None
        
        #print query
        bitMap = []
        docIndex = 0

        
        #print query
        rows = db.FetchAllRows(query)
        totalResult = len(rows)
        """
        if totalResult < len(self.wordList):
            self.elapsedTime = CommonFunctions.ConvertSecondsToYearDayHourMinSec(time.time() - self.startTime)
            self.MessagesHeading = "%d Results for %s (%s)"%(len(self.SearchDocIDList), self.searchWords, self.elapsedTime)
            return None
        """
        
        if totalResult < 1:
            self.elapsedTime = CommonFunctions.ConvertSecondsToYearDayHourMinSec(time.time() - self.startTime)
            self.MessagesHeading = "%d Results for %s (%s)"%(len(self.SearchDocIDList), self.searchWords, self.elapsedTime)
            return None
        
        if totalResult == 1:
            if self.encoded:
                bitMap = binascii.rledecode_hqx(rows[0][1])
            else:
                bitMap = rows[0][1]
        elif totalResult > 1:
            if self.encoded:
                bits = binascii.rledecode_hqx(rows[0][1])
                for bit in bits:
                    bitMap.append(bit)
            else:
                for bit in rows[0][1]: # get the bitmap of first word/row
                    bitMap.append(bit)
        
        i = 1
        
        while i < totalResult:
            row = rows[i]
            i += 1
            index = 0 # start from the beginning of the bitmap
            if encoded:
                bits = binascii.rledecode_hqx(row[1])
            else:
                bits = row[1]
            
            for bit in bits:
                #if self.searchWords.startswith('"'):
                bitMap[index] = str(int(bitMap[index]) & int(bit))
                """
                else:
                    bitMap[index] = str(int(bitMap[index]) | int(bit))
                """
                index += 1
        
        #print bitMap
        docIndex = 1
        for bit in bitMap:
            if bit == '1':
                #if len(self.docIDString) >= 1:
                #    self.docIDString += ','
                self.SearchDocIDList.append(docIndex)
                #self.docIDString += str(docIndex)
            docIndex += 1
        
        msgOutputPath = os.path.join(self.MessageoutputPath, keyword)
        os.makedirs(msgOutputPath)
        for key in Globals.MessageDict:
            for msg in Globals.MessageDict[key]:
                if msg.DocID in self.SearchDocIDList:
                    destPath = os.path.join(msgOutputPath, os.path.basename(msg.filePath))
                    if os.path.isfile(destPath):
                        shutil.copyfile(msg.filePath, destPath)
                    
        #query = "select ID, Path, FileName from %s left join where docID in (" + self.docIDString + ");"       
        #db.CloseConnection()
        
        
    def ReadKeywords(self, keywordsFile):
        fin = file(keywordsFile, 'r')
        return fin.readlines()
        

