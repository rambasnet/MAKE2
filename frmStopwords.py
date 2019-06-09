#Boa:Frame:frmStopwrods

import wx
from wx.lib.anchors import LayoutAnchors
import wx.lib.filebrowsebutton
#from MySqlDatabase import *
from SqliteDatabase import *
import Globals
import Constants
import DBFunctions
import images

def create(parent, IsEmail=False, Stopwords=set([])):
    return frmStopwrods(parent, IsEmail, Stopwords)

[wxID_FRMSTOPWRODS, wxID_FRMSTOPWRODSBTNBROWSE, wxID_FRMSTOPWRODSBTNCLOSE, 
 wxID_FRMSTOPWRODSBTNSAVE, wxID_FRMSTOPWRODSLBLSTOPWORDS, 
 wxID_FRMSTOPWRODSPANEL1, wxID_FRMSTOPWRODSSTATICTEXT1, 
 wxID_FRMSTOPWRODSSTATICTEXT2, wxID_FRMSTOPWRODSTXTFILENAME, 
 wxID_FRMSTOPWRODSTXTSTOPWORDS, 
] = [wx.NewId() for _init_ctrls in range(10)]

class frmStopwrods(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_FRMSTOPWRODS, name=u'frmStopwrods',
              parent=prnt, pos=wx.Point(669, 190), size=wx.Size(805, 563),
              style=wx.DEFAULT_FRAME_STYLE, title=u'Stopwords List')
        self.SetClientSize(wx.Size(797, 532))
        self.SetWindowVariant(wx.WINDOW_VARIANT_MINI)
        self.SetCursor(wx.STANDARD_CURSOR)
        self.Center(wx.BOTH)
        self.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.SetAutoLayout(True)

        self.btnSave = wx.Button(id=wxID_FRMSTOPWRODSBTNSAVE,
              label='&Save And Close', name='btnSave', parent=self,
              pos=wx.Point(659, 494), size=wx.Size(120, 23), style=0)
        self.btnSave.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              'Arial'))
        self.btnSave.SetConstraints(LayoutAnchors(self.btnSave, False, False,
              True, True))
        self.btnSave.Bind(wx.EVT_BUTTON, self.OnBtnSaveButton,
              id=wxID_FRMSTOPWRODSBTNSAVE)

        self.btnClose = wx.Button(id=wxID_FRMSTOPWRODSBTNCLOSE, label='&Cancel',
              name='btnClose', parent=self, pos=wx.Point(547, 494),
              size=wx.Size(96, 23), style=0)
        self.btnClose.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              'Arial'))
        self.btnClose.SetConstraints(LayoutAnchors(self.btnClose, False, False,
              True, True))
        self.btnClose.Bind(wx.EVT_BUTTON, self.OnBtnCloseButton,
              id=wxID_FRMSTOPWRODSBTNCLOSE)

        self.panel1 = wx.Panel(id=wxID_FRMSTOPWRODSPANEL1, name='panel1',
              parent=self, pos=wx.Point(16, 16), size=wx.Size(763, 462),
              style=wx.TAB_TRAVERSAL)
        self.panel1.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.panel1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              u'Tahoma'))
        self.panel1.SetConstraints(LayoutAnchors(self.panel1, True, True, True,
              True))

        self.staticText1 = wx.StaticText(id=wxID_FRMSTOPWRODSSTATICTEXT1,
              label=u'Stopwords List', name='staticText1', parent=self.panel1,
              pos=wx.Point(16, 16), size=wx.Size(120, 19),
              style=wx.ALIGN_CENTRE)
        self.staticText1.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, 'Tahoma'))
        self.staticText1.SetForegroundColour(wx.Colour(0, 0, 255))

        self.staticText2 = wx.StaticText(id=wxID_FRMSTOPWRODSSTATICTEXT2,
              label=u'Choose Text File with Stopwords:', name='staticText2',
              parent=self.panel1, pos=wx.Point(16, 48), size=wx.Size(161, 13),
              style=0)
        self.staticText2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, u'Tahoma'))

        self.lblStopwords = wx.StaticText(id=wxID_FRMSTOPWRODSLBLSTOPWORDS,
              label=u'Stopwords Found In File:', name=u'lblStopwords',
              parent=self.panel1, pos=wx.Point(16, 80), size=wx.Size(158, 16),
              style=0)
        self.lblStopwords.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Tahoma'))
        self.lblStopwords.SetForegroundColour(wx.Colour(0, 0, 255))

        self.txtFileName = wx.TextCtrl(id=wxID_FRMSTOPWRODSTXTFILENAME,
              name=u'txtFileName', parent=self.panel1, pos=wx.Point(184, 48),
              size=wx.Size(499, 21), style=wx.TE_READONLY, value=u'')
        self.txtFileName.SetConstraints(LayoutAnchors(self.txtFileName, True,
              True, True, False))

        self.btnBrowse = wx.Button(id=wxID_FRMSTOPWRODSBTNBROWSE,
              label=u'Browse...', name=u'btnBrowse', parent=self.panel1,
              pos=wx.Point(691, 48), size=wx.Size(59, 23), style=0)
        self.btnBrowse.SetConstraints(LayoutAnchors(self.btnBrowse, False, True,
              True, False))
        self.btnBrowse.Bind(wx.EVT_BUTTON, self.OnBtnBrowseButton,
              id=wxID_FRMSTOPWRODSBTNBROWSE)

        self.txtStopwords = wx.TextCtrl(id=wxID_FRMSTOPWRODSTXTSTOPWORDS,
              name=u'txtStopwords', parent=self.panel1, pos=wx.Point(16, 104),
              size=wx.Size(731, 342),
              style=wx.TE_LINEWRAP | wx.TE_MULTILINE | wx.TE_READONLY | wx.VSCROLL,
              value=u'')
        self.txtStopwords.SetConstraints(LayoutAnchors(self.txtStopwords, True,
              True, True, True))

    def __init__(self, parent, IsEmail=False, Stopwords=[]):
        self._init_ctrls(parent)
        self.SetIcon(images.getMAKE2Icon())
        
        self.IsEmail = IsEmail
        
        self.FileName = ""
        self.Stopwords = Stopwords
        self.StopwordsValue = ""
        self.StopwordsFromDB = False
        self.lblStopwords.SetLabel("No Stopword found!")
        
        if len(self.Stopwords) > 0:
            self.StopwordsFromDB = True
            #for word in Globals.Stopwords:
            #    self.Stopwords.add(word)
            
            self.lblStopwords.SetLabel("Stopwords found in Database:")
            
        """
        if not self.IsEmail:
            if len(Globals.Stopwords) > 0:
                self.StopwordsFromDB = True
                for word in Globals.Stopwords:
                    self.Stopwords.add(word)
                
                self.lblStopwords.SetLabel("Stopwords found in Project Settings:")
        else:
            if len(Globals.EmailsStopwords) > 0:
                self.StopwordsFromDB = True
                for word in Globals.EmailsStopwords:
                    self.Stopwords.add(word)
                    
                self.lblStopwords.SetLabel("Stopwords found in Emails Settings:")
        """
              
        #self.MakeStopwordsList()
            
        self.txtStopwords.SetValue(";".join(self.Stopwords)) #Value)
        
    def MakeStopwordsList(self):
        i = 0
        for word in Globals.Stopwords:
            if i == 0:
                self.StopwordsValue += word
            else:
                self.StopwordsValue += "; " + word
            i += 1
        
    def OnBtnCloseButton(self, event):
        self.Close()
        event.Skip()

    def OnBtnSaveButton(self, event):
        if not self.IsEmail:
            db = SqliteDatabase(Globals.TextCatFileName)
        else:
            db = SqliteDatabase(Globals.EmailsFileName)
            
        if not db.OpenConnection():
            return False
        
        self.SetCursor(wx.HOURGLASS_CURSOR)
        
        query = "DROP TABLE IF EXISTS %s;"%(Constants.StopwordsTable)
        db.ExecuteNonQuery(query)
        
        query = """CREATE TABLE %s ( 
            Stopword text )"""%Constants.StopwordsTable
            
        db.ExecuteNonQuery(query)
    
        #query = "delete from " + Constants.StopwordsTable + ";"
        #db.ExecuteNonQuery(query)
        
        query = "insert into %s (Stopword)  values (?);"%Constants.StopwordsTable
        manyValues = []
        for word in self.Stopwords:
            if not self.IsEmail:
                Globals.Stopwords.add(word)
            else:
                Globals.EmailsStopwords.add(word)
                
            manyValues.append((word,))
            #kword = tuple(word)
            #values.append(kword)
            #value = db.SqlSQuote(word) + ")"
            #print str(query) + str(values)
            #if len(self.Stopwords) > 0:
        
            #print query
            #print manyValues
            
        db.ExecuteMany(query, manyValues)
        
        db.CloseConnection()
        self.SetCursor(wx.STANDARD_CURSOR)
        self.Destroy()
        #self.Close()
        event.Skip()
        
        
    def OnBtnBrowseButton(self, event):
        dlg = wx.FileDialog(self, "Open Text File", ".", "", "*.*", wx.OPEN)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                self.SetCursor(wx.HOURGLASS_CURSOR)
                self.FileName = dlg.GetPath()
                self.txtFileName.SetValue(self.FileName)
                self.ReadStopwordsFromFile(self.FileName)
                self.txtStopwords.SetValue(self.StopwordsValue)
                self.lblStopwords.SetLabel("Stopwords read from file:")
                self.SetCursor(wx.STANDARD_CURSOR)
            else:
                return None
        finally:
            dlg.Destroy()


    def ReadStopwordsFromFile(self, fileName):
        fin = open(fileName, "rb")
        i = 0
        self.StopwordsValue = ""
        self.Stopwords = set([])
        while True:
            lines = fin.readlines()
            if not lines:
                break
            for word in lines:
                self.Stopwords.add(word.strip())
                """
                if i == 0:
                    self.StopwordsValue += word.strip()
                else:
                    self.StopwordsValue += "; " + word.strip()
                i += 1
                """
                   
        self.StopwordsValue = ";".join(self.Stopwords)              
        fin.close()




