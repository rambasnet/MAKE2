#Boa:Frame:frmCustomizeSearch

import wx
from wx.lib.anchors import LayoutAnchors
import wx.lib.filebrowsebutton
#from MySqlDatabase import *
from SqliteDatabase import *
import Globals
import Constants
import DBFunctions
import images


def create(parent):
    return frmCustomizeSearch(parent)

[wxID_FRMCUSTOMIZESEARCH, wxID_FRMCUSTOMIZESEARCHBTNBROWSE, 
 wxID_FRMCUSTOMIZESEARCHBTNCLOSE, wxID_FRMCUSTOMIZESEARCHBTNSAVE, 
 wxID_FRMCUSTOMIZESEARCHLBLKEYWORDS, wxID_FRMCUSTOMIZESEARCHPANEL1, 
 wxID_FRMCUSTOMIZESEARCHSTATICTEXT1, wxID_FRMCUSTOMIZESEARCHSTATICTEXT2, 
 wxID_FRMCUSTOMIZESEARCHTXTFILENAME, wxID_FRMCUSTOMIZESEARCHTXTKEYWORDS, 
] = [wx.NewId() for _init_ctrls in range(10)]

class frmCustomizeSearch(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_FRMCUSTOMIZESEARCH,
              name='frmCustomizeSearch', parent=prnt, pos=wx.Point(457, 151),
              size=wx.Size(698, 536), style=wx.DEFAULT_FRAME_STYLE,
              title='Customize Keyword Search')
        self.SetClientSize(wx.Size(690, 502))
        self.SetWindowVariant(wx.WINDOW_VARIANT_MINI)
        self.SetCursor(wx.STANDARD_CURSOR)
        self.Center(wx.BOTH)
        self.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.SetAutoLayout(True)

        self.btnSave = wx.Button(id=wxID_FRMCUSTOMIZESEARCHBTNSAVE,
              label='&Save And Close', name='btnSave', parent=self,
              pos=wx.Point(552, 464), size=wx.Size(120, 23), style=0)
        self.btnSave.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              'Arial'))
        self.btnSave.SetConstraints(LayoutAnchors(self.btnSave, False, False,
              True, True))
        self.btnSave.Bind(wx.EVT_BUTTON, self.OnBtnSaveButton,
              id=wxID_FRMCUSTOMIZESEARCHBTNSAVE)

        self.btnClose = wx.Button(id=wxID_FRMCUSTOMIZESEARCHBTNCLOSE,
              label='&Cancel', name='btnClose', parent=self, pos=wx.Point(440,
              464), size=wx.Size(96, 23), style=0)
        self.btnClose.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              'Arial'))
        self.btnClose.SetConstraints(LayoutAnchors(self.btnClose, False, False,
              True, True))
        self.btnClose.Bind(wx.EVT_BUTTON, self.OnBtnCloseButton,
              id=wxID_FRMCUSTOMIZESEARCHBTNCLOSE)

        self.panel1 = wx.Panel(id=wxID_FRMCUSTOMIZESEARCHPANEL1, name='panel1',
              parent=self, pos=wx.Point(16, 16), size=wx.Size(656, 432),
              style=wx.TAB_TRAVERSAL)
        self.panel1.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.panel1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              u'Tahoma'))
        self.panel1.SetConstraints(LayoutAnchors(self.panel1, True, True, True,
              True))

        self.staticText1 = wx.StaticText(id=wxID_FRMCUSTOMIZESEARCHSTATICTEXT1,
              label=u'Keywords List', name='staticText1', parent=self.panel1,
              pos=wx.Point(16, 16), size=wx.Size(113, 19),
              style=wx.ALIGN_CENTRE)
        self.staticText1.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, 'Tahoma'))
        self.staticText1.SetForegroundColour(wx.Colour(0, 0, 255))

        self.staticText2 = wx.StaticText(id=wxID_FRMCUSTOMIZESEARCHSTATICTEXT2,
              label=u'Choose Keyword Text File:', name='staticText2',
              parent=self.panel1, pos=wx.Point(16, 48), size=wx.Size(129, 13),
              style=0)
        self.staticText2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, u'Tahoma'))

        self.lblKeywords = wx.StaticText(id=wxID_FRMCUSTOMIZESEARCHLBLKEYWORDS,
              label=u'Keywords Found In File:', name=u'lblKeywords',
              parent=self.panel1, pos=wx.Point(16, 80), size=wx.Size(152, 16),
              style=0)
        self.lblKeywords.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Tahoma'))
        self.lblKeywords.SetForegroundColour(wx.Colour(0, 0, 255))

        self.txtFileName = wx.TextCtrl(id=wxID_FRMCUSTOMIZESEARCHTXTFILENAME,
              name=u'txtFileName', parent=self.panel1, pos=wx.Point(152, 48),
              size=wx.Size(424, 21), style=wx.TE_READONLY, value=u'')
        self.txtFileName.SetConstraints(LayoutAnchors(self.txtFileName, True,
              True, True, False))

        self.btnBrowse = wx.Button(id=wxID_FRMCUSTOMIZESEARCHBTNBROWSE,
              label=u'Browse...', name=u'btnBrowse', parent=self.panel1,
              pos=wx.Point(584, 48), size=wx.Size(59, 23), style=0)
        self.btnBrowse.SetConstraints(LayoutAnchors(self.btnBrowse, False, True,
              True, False))
        self.btnBrowse.Bind(wx.EVT_BUTTON, self.OnBtnBrowseButton,
              id=wxID_FRMCUSTOMIZESEARCHBTNBROWSE)

        self.txtKeywords = wx.TextCtrl(id=wxID_FRMCUSTOMIZESEARCHTXTKEYWORDS,
              name=u'txtKeywords', parent=self.panel1, pos=wx.Point(16, 104),
              size=wx.Size(624, 312),
              style=wx.TE_LINEWRAP | wx.TE_MULTILINE | wx.TE_READONLY | wx.VSCROLL,
              value=u'')
        self.txtKeywords.SetConstraints(LayoutAnchors(self.txtKeywords, True,
              True, True, True))

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.SetIcon(images.getMAKE2Icon())
        
        self.FileName = ""
        self.Keywords = []
        self.KeywordsValue = ""
        self.KeywordsFromDB = True
        if len(Globals.Keywords) == 0:
            self.ReadKeyWordsFromDatabase()
        else:
            self.MakeKeywordsList()
            
        if self.KeywordsFromDB:
            self.lblKeywords.SetLabel("Keywords found in Project database:")
        else:
            self.lblKeywords.SetLabel("No keyword is found:")
        
        self.txtKeywords.SetValue(self.KeywordsValue)
        
    def MakeKeywordsList(self):
        i = 0
        for word in Globals.Keywords:
            if i == 0:
                self.KeywordsValue += word
            else:
                self.KeywordsValue += "; " + word
            i += 1
        
    def OnBtnCloseButton(self, event):
        
        self.Close()

    def OnBtnSaveButton(self, event):
        db = SqliteDatabase(Globals.KeywordsFileName)
        if not db.OpenConnection():
            return False

        query = "delete from " + Constants.KeywordsTable + ";"
        db.ExecuteNonQuery(query)
        query = "insert into " + Constants.KeywordsTable + " (Keyword)  values ("
        #values = []
        for word in self.Keywords:
            Globals.Keywords.add(word)
            #kword = tuple(word)
            #values.append(kword)
            value = db.SqlSQuote(word) + ")"
        #print str(query) + str(values)
            db.ExecuteNonQuery(query + value)
        
        db.CloseConnection()
        DBFunctions.SetupKeywordsFrequencyTable(Globals.KeywordsFileName)
        Globals.frmGlobalKeywords.AddKeywordsToTree()
        self.Close()
    
    
    def ReadKeyWordsFromDatabase(self):
        db = SqliteDatabase(Globals.KeywordsFileName)
        if not db.OpenConnection():
            return
        """
        if not myDB.OpenConnection():
            dlg = wx.MessageDialog(self, 'Database Connection failed!',
                'Error', wx.OK | wx.ICON_ERROR)
            try:
                dlg.ShowModal()
                return None
            finally:
                dlg.Destroy()
        """
        
        query = "SELECT keyword FROM " + Constants.KeywordsTable
        rows = db.FetchAllRows(query)
        #print len(rows)
        self.KeywordsValue = ""
        i = 0
        if len(rows) > 0:
            self.KeywordsFromDB = True
        for row in rows:
            #print row[0]
            Globals.Keywords.add(row[0])
            if i == 0:
                self.KeywordsValue += row[0]
            else:
                self.KeywordsValue += "; " + row[0]
            i += 1
            
        #print Globals.KeyWords
        db.CloseConnection()
        
    def CreateFrequencyCountsTable(self):
        myDB = MySqlDatabase(Globals.HostName, Globals.Username, 
            Globals.Password, Globals.DatabaseName)
        if not myDB.OpenConnection():
            dlg = wx.MessageDialog(self, 'Database Connection failed!',
                'Error', wx.OK | wx.ICON_ERROR)
            try:
                dlg.ShowModal()
                return None
            finally:
                dlg.Destroy()
                
        query = "DROP TABLE IF EXISTS " + Globals.FrequencyCountsTableName
        myDB.ExecuteNonQuery(query)
        
        query = "CREATE TABLE " + Globals.FrequencyCountsTableName + " ( "
        query += "ID BIGINT unsigned NOT NULL auto_increment, "
        query += "FileName VARCHAR(200) NOT NULL default '', "
        keycolumns = ""
        for keyword in Globals.KeyWords:
            keycolumns += keyword + "_CS INTEGER NOT NULL default '0', "
            if Globals.CaseInsensitive:
                keycolumns += keyword + "_CI INTEGER NOT NULL default '0', "
            
            if Globals.SearchInMiddle:
                keycolumns += keyword + "_EICI INTEGER NOT NULL default '0', "
            if Globals.SearchAsPrefix:
                keycolumns += keyword + "_EBCI INTEGER NOT NULL default '0', "
            if Globals.SearchAsSuffix:
                keycolumns += keyword + "_EECI INTEGER NOT NULL default '0', "
                
        query += keycolumns
        query += "PRIMARY KEY (ID) )"
        
        myDB.ExecuteNonQuery(query)
        myDB.CloseConnection()
        return None
    
    def OnChkCaseInsensitiveCheckbox(self, event):
        event.Skip()

    def OnChkPrefixCheckbox(self, event):
        event.Skip()

    def OnChkSuffixCheckbox(self, event):
        event.Skip()

    def OnChkMiddleCheckbox(self, event):
        event.Skip()

    def OnBtnBrowseButton(self, event):
        dlg = wx.FileDialog(self, "Open Text File", ".", "", "*.*", wx.OPEN)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                self.FileName = dlg.GetPath()
                self.txtFileName.SetValue(self.FileName)
                self.ReadKeywordsFromFile(self.FileName)
                self.txtKeywords.SetValue(self.KeywordsValue)
                self.lblKeywords.SetLabel("Keywords read from File:")
            else:
                return None
        finally:
            dlg.Destroy()


    def ReadKeywordsFromFile(self, fileName):
        fin = open(fileName, "rb")
        i = 0
        self.KeywordsValue = ""
        while True:
            lines = fin.readlines()
            if not lines:
                break
            for word in lines:
                self.Keywords.append(word.strip())
                if i == 0:
                    self.KeywordsValue += word.strip()
                else:
                    self.KeywordsValue += "; " + word.strip()
                i += 1
                                 
     
        fin.close()




