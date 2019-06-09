#-----------------------------------------------------------------------------
# Name:        frmTextPreprocessing.py
# Purpose:     
#
# Author:      Ram Basnet
#
# Created:     2007/11/17
# RCS-ID:      $Id: frmTextPreprocessing.py,v 1.10 2008/03/29 05:18:46 rbasnet Exp $
# Copyright:   (c) 2006
# Licence:     <your licence>
# New field:   Whatever
#-----------------------------------------------------------------------------
#Boa:Frame:frmTextPreprocessing

import wx
import os
import wx.lib.buttons
from wx.lib.anchors import LayoutAnchors
#from MySqlDatabase import *
from SqliteDatabase import *
import Globals
import Constants

from DirectoryCheckView import *
from FileCategoryCheckView import *
import PlatformMethods
import CommonFunctions
import images

def create(parent):
    return frmTextPreprocessing(parent)

[wxID_FRMTEXTPREPROCESSING, wxID_FRMTEXTPREPROCESSINGBTNCLOSE, 
 wxID_FRMTEXTPREPROCESSINGBTNPREPROCESS, wxID_FRMTEXTPREPROCESSINGBTNSAVE, 
 wxID_FRMTEXTPREPROCESSINGBTNSELECTFOLDER, 
 wxID_FRMTEXTPREPROCESSINGBTNSTOPWORDS, 
 wxID_FRMTEXTPREPROCESSINGCHOICESTEMMERS, 
 wxID_FRMTEXTPREPROCESSINGPANTEXTPREPROCESSING, 
 wxID_FRMTEXTPREPROCESSINGSTATICTEXT1, wxID_FRMTEXTPREPROCESSINGSTATICTEXT10, 
 wxID_FRMTEXTPREPROCESSINGSTATICTEXT2, wxID_FRMTEXTPREPROCESSINGSTATICTEXT3, 
 wxID_FRMTEXTPREPROCESSINGSTATICTEXT4, wxID_FRMTEXTPREPROCESSINGSTATICTEXT5, 
 wxID_FRMTEXTPREPROCESSINGSTATICTEXT6, wxID_FRMTEXTPREPROCESSINGSTATICTEXT7, 
 wxID_FRMTEXTPREPROCESSINGSTATICTEXT8, wxID_FRMTEXTPREPROCESSINGSTATICTEXT9, 
 wxID_FRMTEXTPREPROCESSINGTXTPATH, 
] = [wx.NewId() for _init_ctrls in range(19)]

class frmTextPreprocessing(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRMTEXTPREPROCESSING,
              name=u'frmTextPreprocessing', parent=prnt, pos=wx.Point(511, 24),
              size=wx.Size(512, 734), style=wx.DEFAULT_FRAME_STYLE,
              title=u'Text Preprocessing')
        self.SetClientSize(wx.Size(504, 700))
        self.SetWindowVariant(wx.WINDOW_VARIANT_MINI)
        self.SetCursor(wx.STANDARD_CURSOR)
        self.Center(wx.BOTH)
        self.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.SetAutoLayout(True)

        self.panTextPreProcessing = wx.Panel(id=wxID_FRMTEXTPREPROCESSINGPANTEXTPREPROCESSING,
              name=u'panTextPreProcessing', parent=self, pos=wx.Point(16, 16),
              size=wx.Size(469, 628), style=wx.TAB_TRAVERSAL)
        self.panTextPreProcessing.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.panTextPreProcessing.SetAutoLayout(False)
        self.panTextPreProcessing.SetConstraints(LayoutAnchors(self.panTextPreProcessing,
              True, True, True, True))
        self.panTextPreProcessing.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL,
              wx.NORMAL, False, u'Tahoma'))

        self.btnClose = wx.Button(id=wxID_FRMTEXTPREPROCESSINGBTNCLOSE,
              label='&Cancel', name='btnClose', parent=self, pos=wx.Point(262,
              660), size=wx.Size(96, 23), style=0)
        self.btnClose.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              'Arial'))
        self.btnClose.SetConstraints(LayoutAnchors(self.btnClose, False, False,
              True, True))
        self.btnClose.Bind(wx.EVT_BUTTON, self.OnBtnCloseButton,
              id=wxID_FRMTEXTPREPROCESSINGBTNCLOSE)

        self.btnSave = wx.Button(id=wxID_FRMTEXTPREPROCESSINGBTNSAVE,
              label='&Save And Close', name='btnSave', parent=self,
              pos=wx.Point(370, 662), size=wx.Size(120, 23), style=0)
        self.btnSave.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              'Arial'))
        self.btnSave.SetConstraints(LayoutAnchors(self.btnSave, False, False,
              True, True))
        self.btnSave.Bind(wx.EVT_BUTTON, self.OnBtnSaveButton,
              id=wxID_FRMTEXTPREPROCESSINGBTNSAVE)

        self.btnStopwords = wx.Button(id=wxID_FRMTEXTPREPROCESSINGBTNSTOPWORDS,
              label=u'Stopwords List...', name=u'btnStopwords',
              parent=self.panTextPreProcessing, pos=wx.Point(168, 48),
              size=wx.Size(208, 23), style=0)
        self.btnStopwords.Bind(wx.EVT_BUTTON, self.OnBtnStopwordsButton,
              id=wxID_FRMTEXTPREPROCESSINGBTNSTOPWORDS)

        self.choiceStemmers = wx.Choice(choices=[u'None - Do not Stem Words',
              u'Porter Stemmer'], id=wxID_FRMTEXTPREPROCESSINGCHOICESTEMMERS,
              name=u'choiceStemmers', parent=self.panTextPreProcessing,
              pos=wx.Point(168, 80), size=wx.Size(208, 21), style=0)
        self.choiceStemmers.SetStringSelection(u'None')
        self.choiceStemmers.SetHelpText(u'')
        self.choiceStemmers.SetSelection(0)
        self.choiceStemmers.SetLabel('')

        self.btnPreprocess = wx.Button(id=wxID_FRMTEXTPREPROCESSINGBTNPREPROCESS,
              label=u'Start Indexing', name=u'btnPreprocess',
              parent=self.panTextPreProcessing, pos=wx.Point(48, 591),
              size=wx.Size(128, 23), style=0)
        self.btnPreprocess.SetConstraints(LayoutAnchors(self.btnPreprocess,
              True, False, False, True))
        self.btnPreprocess.Bind(wx.EVT_BUTTON, self.OnBtnPreprocessButton,
              id=wxID_FRMTEXTPREPROCESSINGBTNPREPROCESS)

        self.staticText3 = wx.StaticText(id=wxID_FRMTEXTPREPROCESSINGSTATICTEXT3,
              label=u'3.', name='staticText3', parent=self.panTextPreProcessing,
              pos=wx.Point(16, 116), size=wx.Size(15, 19), style=0)
        self.staticText3.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Tahoma'))

        self.staticText1 = wx.StaticText(id=wxID_FRMTEXTPREPROCESSINGSTATICTEXT1,
              label=u'Get Stopwords List:', name='staticText1',
              parent=self.panTextPreProcessing, pos=wx.Point(48, 56),
              size=wx.Size(94, 13), style=0)

        self.staticText4 = wx.StaticText(id=wxID_FRMTEXTPREPROCESSINGSTATICTEXT4,
              label=u'Text Preprocessing Steps:', name='staticText4',
              parent=self.panTextPreProcessing, pos=wx.Point(16, 16),
              size=wx.Size(213, 19), style=0)
        self.staticText4.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Tahoma'))

        self.staticText5 = wx.StaticText(id=wxID_FRMTEXTPREPROCESSINGSTATICTEXT5,
              label=u'Select a Stemmer:', name='staticText5',
              parent=self.panTextPreProcessing, pos=wx.Point(48, 88),
              size=wx.Size(87, 13), style=0)

        self.staticText6 = wx.StaticText(id=wxID_FRMTEXTPREPROCESSINGSTATICTEXT6,
              label=u'1.', name='staticText6', parent=self.panTextPreProcessing,
              pos=wx.Point(16, 52), size=wx.Size(15, 19), style=0)
        self.staticText6.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Tahoma'))

        self.staticText7 = wx.StaticText(id=wxID_FRMTEXTPREPROCESSINGSTATICTEXT7,
              label='Select A Path to Index Files Recursively:',
              name='staticText7', parent=self.panTextPreProcessing,
              pos=wx.Point(48, 120), size=wx.Size(194, 13), style=0)

        self.staticText8 = wx.StaticText(id=wxID_FRMTEXTPREPROCESSINGSTATICTEXT8,
              label='5.', name='staticText8', parent=self.panTextPreProcessing,
              pos=wx.Point(16, 596), size=wx.Size(15, 19), style=0)
        self.staticText8.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Tahoma'))
        self.staticText8.SetConstraints(LayoutAnchors(self.staticText8, True,
              False, False, True))

        self.staticText9 = wx.StaticText(id=wxID_FRMTEXTPREPROCESSINGSTATICTEXT9,
              label=u'2.', name='staticText9', parent=self.panTextPreProcessing,
              pos=wx.Point(16, 84), size=wx.Size(15, 19), style=0)
        self.staticText9.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Tahoma'))

        self.btnSelectFolder = wx.Button(id=wxID_FRMTEXTPREPROCESSINGBTNSELECTFOLDER,
              label='...', name=u'btnSelectFolder',
              parent=self.panTextPreProcessing, pos=wx.Point(424, 144),
              size=wx.Size(32, 23), style=0)
        self.btnSelectFolder.Bind(wx.EVT_BUTTON, self.OnBtnSelectFolderButton,
              id=wxID_FRMTEXTPREPROCESSINGBTNSELECTFOLDER)

        self.staticText2 = wx.StaticText(id=wxID_FRMTEXTPREPROCESSINGSTATICTEXT2,
              label='4.', name='staticText2', parent=self.panTextPreProcessing,
              pos=wx.Point(16, 172), size=wx.Size(15, 19), style=0)
        self.staticText2.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Tahoma'))

        self.txtPath = wx.TextCtrl(id=wxID_FRMTEXTPREPROCESSINGTXTPATH,
              name='txtPath', parent=self.panTextPreProcessing, pos=wx.Point(48,
              144), size=wx.Size(368, 21), style=0, value='')

        self.staticText10 = wx.StaticText(id=wxID_FRMTEXTPREPROCESSINGSTATICTEXT10,
              label='Select the Known Mime Types to Index:',
              name='staticText10', parent=self.panTextPreProcessing,
              pos=wx.Point(48, 176), size=wx.Size(190, 13), style=0)

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.SetIcon(images.getMAKE2Icon())
        
        self.DirList = ""
        self.CategoryList = ""
        self.LoadSettingsTable()
        #self.InitDirCheckView()
        self.InitCategoryCheckView()
        self.OneFolderList = []
        self.OneFolderSelected = False
        self.OneFolderPath = ""
        if len(Globals.Stopwords) == 0:
            try:
                self.ReadStopwordsFromDB()
            except:
                pass
        
    def InitCategoryCheckView(self):
        #if not Globals.MimeTypeSet:
        # Populate the Known MIME types list with what is in the database
        try:
            mtypes = wx.TheMimeTypesManager.EnumAllFileTypes()
        except wx.PyAssertionError:
            mtypes = []
        
        # TODO: On wxMac, EnumAllFileTypes produces tons of dupes, which
        # causes quirky behavior because the list control doesn't expect
        # dupes, and simply wastes space. So remove the dupes for now,
        # then remove this hack when we fix EnumAllFileTypes on Mac.
        """
        mimes = {}
        for mt in mtypes:
            category = mt.lower().split("/")
            #print category
            if mimes.has_key(category[0]):
                if len(category) >= 2:
                    if category[1] not in mimes[category[0]]:
                        mimes[category[0]].append(category[1])
            else:
                if len(category) >= 2:
                    mimes[category[0]] = [category[1]]
                else:
                    mimes[category[0]] = []
        """
        mimes = set()
        for mime in mtypes:
            if not mime.startswith('image') and not mime.startswith('audio') and not mime.startswith('video'):
                mimes.add(mime)
                        
        #else:
        #    mimes = Globals.MimeTypeSet
                    
        self.treeCategoryCheckView = FileCategoryCheckView(self.panTextPreProcessing, MimeTypeSet=mimes, id=wx.NewId(),pos=wx.Point(16, 200), size=wx.Size(440, 384),
            CheckedList=Globals.TextCatCategoryList) 
        self.treeCategoryCheckView.SetConstraints(LayoutAnchors(self.treeCategoryCheckView,
              True, True, True, True))
        
    def InitDirCheckView(self):

        self.treeDirCheckView = DirectoryCheckView(self.panDirView, id=wx.NewId(), pos=wx.Point(0, 0),
              size=wx.Size(352, 432), CheckedList=Globals.TextCatDirList) 
        self.treeDirCheckView.SetConstraints(LayoutAnchors(self.treeDirCheckView,
              True, True, True, True))
              

        #self.keywordsRoot = self.treeDirCheckView.AddDirectoryTreeNodes()
        
    def OnBtnCloseButton(self, event):
        self.Destroy()

    def OnBtnSaveButton(self, event):
        self.UpdateSettings()
        if not self.CheckSettingsError():
            return
        
        self.Close()
    
    def ReadStopwordsFromDB(self):
        db = SqliteDatabase(Globals.TextCatFileName)
        if not db.OpenConnection():
            return
        
        query = "SELECT Stopword FROM " + Constants.StopwordsTable
        rows = db.FetchAllRows(query)
        #print len(rows)
        #self.StopwordsValue = ""
        #i = 0
        for row in rows:
            #print row[0]
            Globals.Stopwords.add(row[0])
            #if i == 0:
            #    self.StopwordsValue += row[0]
            #else:
            #    self.StopwordsValue += "; " + row[0]
            #i += 1
            
        #print Globals.KeyWords
        db.CloseConnection()
        
    
    def CheckSettingsError(self):
        #Globals.TextCatDirList = []
        #self.treeDirCheckView.UpdateCheckedList(Globals.TextCatDirList)
        #Globals.TextCatCategoryList = []
        #self.treeCategoryCheckView.UpdateCheckedList(Globals.TextCatCategoryList)
        errMsg = ""
        """
        if len(Globals.Keywords) == 0:
            errMsg = "Please import keywords from a text file before start searching.\n File must have one keyword per line."
        """
        if not os.path.isdir(self.txtPath.GetValue()):
            errMsg = "Not a valid Path. Please Enter a valid path for Text Preprocessing!"
            
        elif len(Globals.TextCatDirList) == 0:
            errMsg = "Please select directories to get text for Text Preprocessing."
            
        #elif len(Globals.TextCatCategoryList) == 0:
        #if self.OneFolderSelected:
        #errMsg = "Please select file types / categories to be scanned for Text Clustering."
        
        if not errMsg == "" :
            dlg = wx.MessageDialog(self, errMsg,
              'Error', wx.OK | wx.ICON_ERROR)
            try:
                dlg.ShowModal()
            finally:
                dlg.Destroy()
                return False
        else:
            return True
    
    def LoadSettingsTable(self):
        if len(Globals.TextCatDirList) == 0:
            db = SqliteDatabase(Globals.TextCatFileName)
            if not db.OpenConnection():
                return
            query = "select Stemmer, DirList, CategoryList from " + Constants.TextCatSettingsTable
            rows = db.FetchAllRows(query)
            for row in rows:
                Globals.Stemmer = row[0]
                self.DirList = CommonFunctions.RemoveDoubleSlashes(row[1])
                self.CategoryList = row[2]
            
            Globals.TextCatCategoryList = self.CategoryList.split(';')
            #Globals.TextCatDirList = self.DirList.split(';')
            
            
        self.choiceStemmers.SetStringSelection(Globals.Stemmer)
        self.txtPath.SetValue(self.DirList)
        #print Globals.TextCatCategoryList
        #print Globals.TextCatDirList
            

    def UpdateSettings(self):
        if not os.path.isdir(self.txtPath.GetValue()):
            return
        
        Globals.TextCatCategoryList = []
        Globals.TextCatDirList = []
        
        #self.OneFolderList = []
        Globals.TextCatDirList.append(self.txtPath.GetValue())
        self.DirList = self.txtPath.GetValue()
        
        self.CategoryList = ""
        self.treeCategoryCheckView.UpdateCheckedList(Globals.TextCatCategoryList)
        #self.treeDirCheckView.UpdateCheckedList(Globals.TextCatDirList)
        #UpdateTextCatDirList
        #if self.OneFolderSelected:
        #if self.OneFolderSelected:
        #Globals.TextCatCategoryList.append("text/plain")
        #for adir in self.OneFolderList:
            
        
        #    Globals.TextCatDirList.append(adir)
                
        """
        if self.OneFolderPath:
            Globals.TextCatDirList.append(self.OneFolderPath)
        """
        
        
        Globals.Stemmer = self.choiceStemmers.GetStringSelection()
         
        """           
        for adir in Globals.TextCatDirList:
            if not self.DirList == "":
                self.DirList += ";"
            self.DirList += adir
        """
            
        for cat in  Globals.TextCatCategoryList:
            if not self.CategoryList == "":
                self.CategoryList += ";"
            self.CategoryList += cat
        
        db = SqliteDatabase(Globals.TextCatFileName)
        if not db.OpenConnection():
            return
        
        query = "delete from " + Constants.TextCatSettingsTable + ";"
        db.ExecuteNonQuery(query)
        
        query = "insert into " + Constants.TextCatSettingsTable + " (Stemmer, DirList, CategoryList) values (?,?,?)" 
        db.ExecuteNonQuery(query, (Globals.Stemmer, self.DirList, self.CategoryList,))
        db.CloseConnection()
        
    def OnBtnStopwordsButton(self, event):
        import frmStopwords
        formStopwords = frmStopwords.create(self, IsEmail=False, Stopwords=Globals.Stopwords)
        formStopwords.Show()
        event.Skip()


    def OnBtnPreprocessButton(self, event):
        self.UpdateSettings()
        if not self.CheckSettingsError():
            return
        
        import dlgTextPreprocessingProgress
        textCat = dlgTextPreprocessingProgress.create(self, self.DirList)
        #scanMAC.StartScan(dir)
        #textCat.scanThread.Start()
        textCat.ShowModal()
        #textCat.scanThread.Start()
        self.Close()
        event.Skip()

    def OnBtnSelectFolderButton(self, event):
        #self.OneFolderList = []
        dlg = wx.DirDialog(self)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                #dirPath = dlg.GetPath()
                #self.OneFolderSelected = True
                #self.OneFolderPath = dir
                self.txtPath.SetValue(dlg.GetPath())
                
                """
                for dir in self.OneFolderList:
                    print dir
                """
        finally:
            dlg.Destroy()
        
        event.Skip()







