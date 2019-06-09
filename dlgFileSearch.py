#Boa:MDIChild:dlgFileSearch

#-----------------------------------------------------------------------------
# Name:        dlgEmailKeyExtract.py
# Purpose:     
#
# Author:      Ram B. Basnet
#
# Created:     2008/11/17
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
    return dlgFileSearch(parent)

[wxID_DLGFILESEARCH, wxID_DLGFILESEARCHBTNCANCEL, wxID_DLGFILESEARCHBTNSEARCH, 
 wxID_DLGFILESEARCHPANSETTINGS, wxID_DLGFILESEARCHSTATICTEXT3, 
] = [wx.NewId() for _init_ctrls in range(5)]

class dlgFileSearch(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DLGFILESEARCH, name='dlgFileSearch',
              parent=prnt, pos=wx.Point(813, 468), size=wx.Size(484, 194),
              style=wx.DEFAULT_DIALOG_STYLE, title='Search Files')
        self.SetClientSize(wx.Size(476, 163))
        self.SetAutoLayout(True)
        self.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.SetCursor(wx.STANDARD_CURSOR)
        self.SetMinSize(wx.Size(-1, -1))
        self.Center(wx.BOTH)

        self.btnCancel = wx.Button(id=wxID_DLGFILESEARCHBTNCANCEL,
              label=u'&Cancel', name=u'btnCancel', parent=self,
              pos=wx.Point(208, 128), size=wx.Size(75, 23), style=0)
        self.btnCancel.Bind(wx.EVT_BUTTON, self.OnBtnCancelButton,
              id=wxID_DLGFILESEARCHBTNCANCEL)

        self.panSettings = wx.Panel(id=wxID_DLGFILESEARCHPANSETTINGS,
              name='panSettings', parent=self, pos=wx.Point(16, 16),
              size=wx.Size(448, 96), style=wx.TAB_TRAVERSAL)
        self.panSettings.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.panSettings.SetAutoLayout(True)

        self.btnSearch = wx.Button(id=wxID_DLGFILESEARCHBTNSEARCH,
              label='Search', name='btnSearch', parent=self.panSettings,
              pos=wx.Point(360, 48), size=wx.Size(72, 24), style=0)
        self.btnSearch.Bind(wx.EVT_BUTTON, self.OnBtnSearchButton,
              id=wxID_DLGFILESEARCHBTNBROWSERESULTPATH)

        self.staticText3 = wx.StaticText(id=wxID_DLGFILESEARCHSTATICTEXT3,
              label='All or part of the file name:', name='staticText3',
              parent=self.panSettings, pos=wx.Point(16, 32), size=wx.Size(129,
              13), style=0)

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.SetIcon(images.getMAKE2Icon())
        self.AddSearchControl()
        
        
    def AddSearchControl(self):
        """
        self.txtResultFolderPath = wx.TextCtrl(id=wxID_DLGFILESEARCHTXTRESULTFOLDERPATH,
              name='txtResultFolderPath', parent=self.panSettings,
              pos=wx.Point(16, 48), size=wx.Size(328, 21), style=0, value='')
        self.txtResultFolderPath.Enable(True)
        """
        self.search = wx.SearchCtrl(self.panSettings, pos=wx.Point(16, 48), size=(328, -1), style=wx.TE_PROCESS_ENTER)
        self.search.ShowSearchButton(True)
        self.search.ShowCancelButton(True)
        
        self.SearchMenu = wx.Menu()
        item = self.SearchMenu.Append(-1, "Recent Searches")
        item.Enable(False)
        
        self.search.SetMenu(self.SearchMenu)
        
        self.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.OnSearch, self.search)
        self.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.OnSearchCancel, self.search)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnDoSearch, self.search)
        
        
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

    def OnBtnSearchButton(self, event):
        event.Skip()
        

