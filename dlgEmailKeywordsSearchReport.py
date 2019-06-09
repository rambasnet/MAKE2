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
import time
import re, string
import os, os.path, sys
import binascii
import shutil


from SqliteDatabase import *
import Globals
import Constants
import CommonFunctions
import images

from wx.lib.anchors import LayoutAnchors


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
              name='dlgKeywordsSearchReport', parent=prnt, pos=wx.Point(594,
              316), size=wx.Size(433, 290), style=wx.DEFAULT_DIALOG_STYLE,
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
            
        self.ReportOutputPath = os.path.join(outPutPath, "KeywordsReport")
        self.MessageOutputPath = os.path.join(self.ReportOutputPath, "Messages")
        #self.HTMLOutputPath = os.path.join(self.ReportOutputPath, "HTML")
        if not keywordsFile:
            return
        
        
        keywordsList = self.ReadKeywords(keywordsFile)
            
        
        for keyword in keywordsList:
            self.searchBitMap(db, keyword.strip())
            
        self.elapsedTime = CommonFunctions.ConvertSecondsToYearDayHourMinSec(time.time() - self.startTime)
        msg = "Done generating report! (%s)"%(self.elapsedTime)
        CommonFunctions.ShowErrorMessage(self, msg, error=False)
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
        
       
        if encoded:
            query = "select keyword, compressed from %s where (Keyword = "%Constants.TextCatBitMapIndex
        else:
            query = "select keyword, bitmap from %s where (Keyword = '"%Constants.TextCatBitMapIndex
        
        i = 0    
        for word in string.split(self.searchWords, ' '):
            word = word.strip().lower()
            word = word.strip('"')
                    
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
                if self.searchWords.startswith('"'):
                    bitMap[index] = str(int(bitMap[index]) & int(bit))
                    
                else:
                    bitMap[index] = str(int(bitMap[index]) | int(bit))
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
        
            
        if len(self.SearchDocIDList) == 0:
            return
        
        if keyword.startswith('"'):
            keyword = keyword.replace('"', "'")
            
        msgOutputPath = os.path.join(self.MessageOutputPath, keyword)
        try:
            os.makedirs(msgOutputPath)
        except:
            pass
            
        for key in Globals.MessageDict:
            for msg in Globals.MessageDict[key]:
                if msg.DocID in self.SearchDocIDList:
                    destPath = os.path.join(msgOutputPath, os.path.basename(msg.filePath))
                    if not os.path.isfile(destPath):
                        shutil.copyfile(msg.filePath, destPath)
                    
        #query = "select ID, Path, FileName from %s left join where docID in (" + self.docIDString + ");"       
        #db.CloseConnection()
        
        
    def ReadKeywords(self, keywordsFile):
        fin = file(keywordsFile, 'r')
        return fin.readlines()
        

    def create_OpenPage(self):
        if not os.path.exists('..\\html'):
            os.makedirs('..\\html\\msg')
            os.makedirs('..\\html\\att')

        page_Title = msg_Folder_Path.strip('\\n').split('\\')

        indexPage_Filename = '..\\html\\verify.html'
        indexPage_File = open(indexPage_Filename,'w')
        indexPage_File.write('<html><head><title>EmailSearch</title></head>'+'\n')
        indexPage_File.write('<frameset rows="*" cols="15%,*" framespacing="0" frameborder="yes" border="3">'+'\n')
        indexPage_File.write('<frame src=".\\msg\\'+page_Title[len(page_Title)-1]+'.html" name="leftFrame" scrolling="yes" noresize="noresize" id="leftFrame" title="messagesFrame" />'+'\n')
        indexPage_File.write('<frameset rows="60%,*" cols="*" framespacing="0" frameborder="yes" border="3">'+'\n')
        indexPage_File.write('<frame src="righttop.html" name="righttopFrame" scrolling="yes" id="righttopFrame" title="righttopFrame" />'+'\n')
        indexPage_File.write('<frame src="rightbot.html" name="rightbotFrame" scrolling="yes" id="rightbotFrame" title="rightbotFrame" />'+'\n')
        #
        #indexPage_File.write('<frameset rows="*" cols="50%,*" framespacing="0" frameborder="yes" border="3">'+'\n')
        #indexPage_File.write('<frame src="rightbotleft.html" name="rightbotleftFrame" scrolling="yes" id="rightbotleftFrame" title="rightbotleftFrame" />'+'\n')
        #indexPage_File.write('<frame src="rightbotright.html" name="rightbotrightFrame" scrolling="yes" id="rightbotrightFrame" title="rightbotrightFrame" />'+'\n')
        #
        indexPage_File.write('</frameset>'+'\n')
        indexPage_File.write('<noframes><body></body></noframes></html>'+'\n')
        indexPage_File.close()

        indexPage_Filename = '..\\html\\righttop.html'
        indexPage_File = open(indexPage_Filename,'w')
        indexPage_File.write('<html><head><title>Emails Information Display Window</title></head><body>'+'\n')
        indexPage_File.write('<p><B><I> Email information display Pane </I></B></P>'+'\n')
        indexPage_File.write('</body></html>'+'\n')
        indexPage_File.close()


        indexPage_Filename = '..\\html\\rightbot.html'
        indexPage_File = open(indexPage_Filename,'w')
        indexPage_File.write('<html><head><title>Emails Information Display Window</title></head><body>'+'\n')
        indexPage_File.write('<p><B><I> Email Listing Display pane </I></B></P>'+'\n')
        indexPage_File.write('</body></html>'+'\n')
        indexPage_File.close()

        #
        #indexPage_Filename = '..\\html\\rightbotright.html'
        #indexPage_File = open(indexPage_Filename,'w')
        #indexPage_File.write('<html><head><title>Emails Attachment Display Window</title></head><body>'+'\n')
        #indexPage_File.write('<p><B><I> Email Attachment Listing Display pane </I></B></P>'+'\n')
        #indexPage_File.write('</body></html>'+'\n')
        #indexPage_File.close()
        #
        

    def create_Interface():
        os.chdir(msg_Folder_Path)
        create_OpenPage()

        count = 0
        file_Count = 0

        for files in os.walk('.\\'):
            temp = files[0].strip('.').strip('\\').split('\\')
            temp_FileName = ''

            if count == 0:
                page_Title = msg_Folder_Path.strip('\\n').split('\\')
                temp_FileName = msg_HTML_Dir+page_Title[len(page_Title)-1]+'.html'
                print temp_FileName
                temp_File = open(temp_FileName,'w')
                temp_File.write('<html><head><title>MessageIndex</title></head><body>'+'\n')
                temp_File.write('<a href="..\\verify.html" target="_parent"> Home </a><br>'+'\n')
                temp_File.write('<B>Click for Contents</B><br><br>')

                for directory in files[1]:
                    temp_File.write('<a href=".\\'+directory+'.html" target="rightbotFrame">'+directory+'<br>\n')
                temp_File.close()
                count = 1
            else:
                for names in temp:        
                    temp_FileName = temp_FileName + names

                temp_FileName = msg_HTML_Dir+temp_FileName+'.html'
                temp_File = open(temp_FileName,'w')

                for directory in files[1]:
                    temp_File.write('<a href=".\\'+temp_FileName.strip(msg_HTML_Dir)+directory+'.html" target="rightbotFrame">'+directory+'<br>\n')

                for messages in files[2]:
                    file_Count = file_Count + 1
                    attachment_Mapping = pre_Email_Mapping(messages,files[0])

                    temp_File.write('<a href="..\\..\\'+ page_Title[len(page_Title)-1] + files[0].strip('.') + '\\' + messages+'" target="righttopFrame">'+messages.strip('.txt')+'</a>\n')

                    if len(attachment_Mapping) != 0:
                        #temp_File.write('<a href="..\\..\\'+ page_Title[len(page_Title)-1] + files[0].strip('.') + '\\' + messages+'" target="righttopFrame">'+messages+'</a>&#x9; Attachments ===>\n')
                        temp_File.write('&#x9; Attachments ===>')
                        for each_Attachment in attachment_Mapping:
                            att_Folder = att_Folder_Path.split('\\')
                            temp_File.write('&#x9;|| '+ '<a href="..\\..\\'+ att_Folder[len(att_Folder)-1] + files[0].strip('.') + '\\' + each_Attachment +'" target="righttopFrame">'+each_Attachment+'</a>&#x9;\n')
                        temp_File.write('<br><br>\n')
                    else:
                        temp_File.write('<br><br>\n')
                        #temp_File.write('<a href="..\\..\\'+ page_Title[len(page_Title)-1] + files[0].strip('.') + '\\' + messages+'" target="righttopFrame">'+messages+'</a><br>\n')

                
                temp_File.close()

