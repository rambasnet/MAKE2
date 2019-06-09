#-----------------------------------------------------------------------------
# Name:        MDIChildTextCat.py
# Purpose:     
#
# Author:      Ram B. Basnet
#
# Created:     2008/07/09
# Last Modified: 6/30/2009
# RCS-ID:      $Id: MDIChildTextCat.py $
# Copyright:   (c) 2006
# Licence:     All Rights Reserved.
#-----------------------------------------------------------------------------

import wx, sys, os
import re, string
from wx.lib.anchors import LayoutAnchors
import  wx.lib.mixins.listctrl  as  listmix

from SqliteDatabase import *
import Globals
import PlatformMethods
import CommonFunctions
import Constants
import DBFunctions

import  images

def create(parent):
    return MDIChildTextCat(parent)

class CustomListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        
        
[wxID_MDICHILDTEXTCAT, wxID_MDICHILDTEXTCATBTNCLOSE, 
 wxID_MDICHILDTEXTCATBTNEXPORTSTEMMEDWORDS, 
 wxID_MDICHILDTEXTCATBTNEXPORTWORDFEATURES, 
 wxID_MDICHILDTEXTCATBTNPREPROCESSING, wxID_MDICHILDTEXTCATLBLKEYWORDSSEARCH, 
 wxID_MDICHILDTEXTCATPANSTOPWORDS, 
] = [wx.NewId() for _init_ctrls in range(7)]

class MDIChildTextCat(wx.MDIChildFrame, listmix.ColumnSorterMixin):

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.MDIChildFrame.__init__(self, id=wxID_MDICHILDTEXTCAT,
              name=u'MDIChildTextCat', parent=prnt, pos=wx.Point(529, 333),
              size=wx.Size(1040, 680), style=wx.DEFAULT_FRAME_STYLE,
              title=u'Text Categorization')
        self.SetClientSize(wx.Size(1040, 680))
        self.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.SetAutoLayout(True)

        self.panTextMining = wx.Panel(id=wxID_MDICHILDTEXTCATPANSTOPWORDS,
              name=u'panStopwords', parent=self, pos=wx.Point(4, 4),
              size=wx.Size(1032, 672), style=wx.TAB_TRAVERSAL)
        self.panTextMining.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.panTextMining.SetConstraints(LayoutAnchors(self.panTextMining, True,
              True, True, True))

        self.btnClose = wx.Button(id=wxID_MDICHILDTEXTCATBTNCLOSE,
              label=u'Close', name=u'btnClose', parent=self.panTextMining,
              pos=wx.Point(791, 8), size=wx.Size(75, 23), style=0)
        self.btnClose.SetConstraints(LayoutAnchors(self.btnClose, False, True,
              True, False))
        self.btnClose.Bind(wx.EVT_BUTTON, self.OnBtnCloseButton,
              id=wxID_MDICHILDTEXTCATBTNCLOSE)

        self.lblKeywordsSearch = wx.StaticText(id=wxID_MDICHILDTEXTCATLBLKEYWORDSSEARCH,
              label=u'Text Preprocessing...', name=u'lblKeywordsSearch',
              parent=self.panTextMining, pos=wx.Point(16, 8), size=wx.Size(136,
              16), style=0)
        self.lblKeywordsSearch.SetForegroundColour(wx.Colour(0, 0, 187))
        self.lblKeywordsSearch.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Tahoma'))
        self.lblKeywordsSearch.SetConstraints(LayoutAnchors(self.lblKeywordsSearch,
              True, True, False, False))

        self.btnPreprocessing = wx.Button(id=wxID_MDICHILDTEXTCATBTNPREPROCESSING,
              label=u'Text Preprocessing...', name=u'btnPreprocessing',
              parent=self.panTextMining, pos=wx.Point(176, 8), size=wx.Size(128,
              24), style=0)
        self.btnPreprocessing.Bind(wx.EVT_BUTTON, self.OnBtnPreprocessingButton,
              id=wxID_MDICHILDTEXTCATBTNPREPROCESSING)

        self.btnExportWordFeatures = wx.Button(id=wxID_MDICHILDTEXTCATBTNEXPORTWORDFEATURES,
              label='Export Words', name='btnExportWordFeatures',
              parent=self.panTextMining, pos=wx.Point(176, 56), size=wx.Size(128,
              24), style=0)
        self.btnExportWordFeatures.Bind(wx.EVT_BUTTON,
              self.OnBtnExportWordFeaturesButton,
              id=wxID_MDICHILDTEXTCATBTNEXPORTWORDFEATURES)

        self.btnExportStemmedWords = wx.Button(id=wxID_MDICHILDTEXTCATBTNEXPORTSTEMMEDWORDS,
              label='Export Stemmed Words', name='btnExportStemmedWords',
              parent=self.panTextMining, pos=wx.Point(336, 56), size=wx.Size(128,
              24), style=0)
        self.btnExportStemmedWords.Bind(wx.EVT_BUTTON,
              self.OnBtnExportStemmedWordsButton,
              id=wxID_MDICHILDTEXTCATBTNEXPORTSTEMMEDWORDS)

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.SetIcon(images.getMAKE2Icon())
        
        self.CreateSettingsTable()
    
    def CreateSettingsTable(self):
        db = SqliteDatabase(Globals.TextCatFileName)
        if not db.OpenConnection():
            return
                
        
        query = "CREATE TABLE IF NOT EXISTS " + Constants.TextCatSettingsTable + " ( "
        query += "Stemmer text, DirList text, CategoryList text )"
               
        db.ExecuteNonQuery(query)
        db.CloseConnection()
        return None
      
    def OnBtnCloseButton(self, event):
        self.Close()

    def OnBtnPreprocessingButton(self, event):
        import frmTextPreprocessing
        textPreprocessing = frmTextPreprocessing.create(self)
        textPreprocessing.Show()
        event.Skip()

    def OnBtnExportWordFeaturesButton(self, event):
        db = SqliteDatabase(Globals.TextCatFileName)
        if not db.OpenConnection():
            return
                
        dlg = wx.FileDialog(self, "Save Words List", ".", "", "*.csv", wx.SAVE)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                fileName = dlg.GetPath()
                busy = wx.BusyInfo("It might take some time depending on the total number of unique words...")
                wx.Yield()
                fout = open(fileName, 'wb')
                #query = "select ID, `Word` from " + Constants.TextCatWordsTable + " order by `ID`; "
                query = "select words.word, count(WordLocation.WordID) as total from words left join WordLocation on words.rowid = wordlocation.wordid "
                query += "group by wordlocation.wordid order by total desc;"
                #print 'before'
                rows = db.FetchAllRows(query)
                #rint 'after'
                i = 1
                for row in rows:
                    #print row
                    #if i == 0:
                        #try:
                    fout.write(PlatformMethods.Encode(row[0]))
                    fout.write(" (%d)"%row[1])
                    #fout.write(row[1])
                    #i += 1
                    #except Exception, value:
                    #    print "Error: writing word: ", value
                    #else:
                        #try:
                    fout.write(", ,")
                    #fout.write(row[0])
                    #fout.write(" - %d"%row[1])
                    #fout.write(row[1])
                    i += 1
                    if i == 4:
                        i = 0
                        fout.write("\n")
                        #except Exception, value:
                        #    print "Error: writing word: ", value

                db.CloseConnection()
                fout.close()
        except Exception, value:
            db.CloseConnection()
            fout.close()
            CommonFunctions.ShowErrorMessage(self, "Failed to Export Word List. Error: %s"%value)
        finally:
            dlg.Destroy()

    def OnBtnExportStemmedWordsButton(self, event):
        db = SqliteDatabase(Globals.TextCatFileName)
        if not db.OpenConnection():
            return
                
        CommonFunctions.ShowErrorMessage(self, 'This is not yet implemented!', False)
        return
    
        dlg = wx.FileDialog(self, "Save Stemmed Words List", ".", "", "*.csv", wx.SAVE)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                fileName = dlg.GetPath()
                busy = wx.BusyInfo("It might take some time depending on the word feature size...")
                wx.Yield()
                fout = open(fileName, 'w')
                query = "select stemmedwords.word, sum(bagofstemmedwords.frequency) as total from stemmedwords left join bagofstemmedwords on stemmedwords.id = bagofstemmedwords.wordid "
                query += " group by bagofstemmedwords.wordid order by total desc;"
                #print 'before'
                rows = db.FetchAllRows(query)
                #rint 'after'
                i = 1
                for row in rows:
                    #print row
                    #if i == 0:
                        #try:
                    fout.write(row[0])
                    fout.write(" (%d)"%row[1])
                        #fout.write(row[1])
                        #i += 1
                        #except Exception, value:
                        #    print "Error: writing word: ", value
                    #else:
                        #try:
                    fout.write(", ,")
                    #fout.write(row[0])
                    #fout.write(" - %d"%row[1])
                    #fout.write(row[1])
                    i += 1
                    if i == 4:
                        i = 0
                        fout.write("\n")

                db.CloseConnection()
                fout.close()
        except Exception, value:
            db.CloseConnection()
            fout.close()
            CommonFunctions.ShowErrorMessage(self, "Failed to Export Word List. No Indexing has been done! Error: %s"%value)
        finally:
            dlg.Destroy()
                

    
if __name__ == "__main__":
    db = SqliteDatabase("caseNew.tce")
    if db.OpenConnection():
            
        query = "select `Word` from " + Constants.TextCatWordsTable + " order by `Word`; "
        
        words = db.FetchOneRow(query)
        while words:
            print words[0]
            words = db.FetchOneRow(query)
            
        """
        for word in words:
            print word
        """
