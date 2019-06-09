#-----------------------------------------------------------------------------
# Name:        MDIChildTimeline.py
# Purpose:     
#
# Author:      Ram Basnet & William Baker
#
# Created:     2007/11/10
# RCS-ID:      $Id: MDIChildTimeline.py,v 1.13 2007/11/23 05:50:14 rbasnet Exp $
# Copyright:   (c) 2006
# Licence:     <your licence>
# New field:   Whatever
#-----------------------------------------------------------------------------


# import the wxPython GUI package
import wx,os,sys,time,calendar
import  wx.lib.scrolledpanel as scrolled
import wx.aui
import  images
from wx.lib.anchors import LayoutAnchors
import wx.lib.buttons
import  wx.lib.mixins.listctrl  as  listmix
from CustomControls import *
import PlatformMethods
import CommonFunctions
import Constants

import Globals
from FileCategoryView import *


#this function taken from the wxPython Demo files
def opj(path):
	"""Convert paths to the platform-specific separator"""
	str = apply(os.path.join, tuple(path.split('/')))
	# HACK: on Linux, a leading / gets lost...
	if path.startswith('/'):
		str = '/' + str
	return str

def DisplayMonthDate(timenumber):
    #return time.strftime("%d/%m/%Y, %H:%M:%S",time.gmtime(timenumber))
    try:
        #gmTime = time.gmtime(timenumber)
        #timenumber = time.mktime(gmTime)
        dateStr = time.ctime(timenumber)
        dateTimeList = dateStr.split()
        return dateTimeList[1] + " " + str(dateTimeList[2]) + ", " + str(dateTimeList[4])
        #return time.strftime("%m/%d/%Y",time.gmtime(timenumber))
    except:
        #print "Timenumber = %d"%timenumber
        return "00/00/0000"
    #return str(timenumber)

def DisplayDate(timenumber):
    try:
        return time.strftime("%m/%d/%Y", time.localtime(timenumber))
    except:
        return "MM/DD/YYYY"

def disptimespan(timenumber):
    #gm = time.gmtime(timenumber)
    #newSecs = time
    gm = time.gmtime(timenumber)
    #print gm
    baseTime = time.gmtime(0)
    #print baseTime
    
    """
    year =gm[0] - baseTime[0] 
    month = gm[1]%baseTime[1]
    if month > 0:
        year -= 1
        
    day = gm[2]%baseTime[2]
    if day > 0:
        
        
    """
    timeList = []
    for i in range(6):
        #if i == 0:
        timeList.append(gm[i]-baseTime[i])
        #else:
            #value = gm[i]%baseTime[i]
        #    timeList.append(gm[i]%baseTime[i])
     
    #timeTuple = 
    timeStr = ""
    for i in range(6):
        if timeList[i] < 0:
            timeList[i-1] -= 1
            timeList[i] *=-1
    timeStr += str(timeList[1]) + "/" + str(timeList[2]) + "/" + str(timeList[0]) + " " + str(timeList[3]) + ":" + str(timeList[4]) + ":" + str(timeList[5])
    #print tuple(timeList)
    return timeStr # time.strftime("%m/%d/%Y %H:%M:%S", tuple(timeList))
    #return partA+str(partL)+partB


def filesizedisp(bytes):
	if (bytes > 1000):
		bytes = bytes/1000
		if (bytes > 1000):
			bytes = bytes/1000
			if (bytes > 1000):
				bytes = bytes/1000
				if (bytes > 1000):
					bytes = bytes/1000
					return str(int(bytes))+" TB"
				else:
					return str(int(bytes))+" GB"
			else:
				return str(int(bytes))+" MB"
		else:
			return str(int(bytes))+" KB"
	else:
		return str(bytes)+" Bytes"
	return "error"

def filenamelimiter(filename):
	if (len(filename) > 13):
		filename = filename[:6]+"..."+filename[-5:]
	return filename

def gettime(timestring):
    try:
        if timestring.find(',') > -1:
            tval = time.strptime(timestring,"%m/%d/%Y, %H:%M:%S")
        else:
            if timestring.find(":") > -1:
                tval = time.strptime(timestring,"%m/%d/%Y %H:%M:%S")
            else:
                tval = time.strptime(timestring,"%m/%d/%Y")
        #return calendar.timegm(tval)
        return time.mktime(tval)
        
    except:
        return (-1)

def GetGIF(filename):
	return wx.Image(opj(filename), wx.BITMAP_TYPE_GIF).ConvertToBitmap()

def GetPNG(filename):
	bmp = wx.Bitmap(opj(filename))
	if "gtk1" in wx.PlatformInfo:
		# Try to make up for lack of alpha support in wxGTK
		#taken from ImageAlpha example in the wxPython Demo suite
		img = bmp.ConvertToImage()
		img.ConvertAlphaToMask(220)
		bmp = img.ConvertToBitmap()
	return bmp



def create(prnt, TimelinesDict=None):
    return MDIChildTimeline(prnt, TimelinesDict)


# Create a new frame class, derived from the wxPython Frame.
class MDIChildTimeline(wx.MDIChildFrame, listmix.ColumnSorterMixin):
    def __init__(self, prnt, TimelinesDict):#as a frame, it needed title also
        wx.MDIChildFrame.__init__(self, id=wx.NewId(),
            name=u'MDIChildTimeline', parent=prnt, pos=wx.Point(0, 0),
            size=wx.Size(960, 590), style=wx.DEFAULT_FRAME_STYLE,
            title=u'Timelines')
        
        #1051,687
        #self.SetClientSize(wx.Size(1043, 656))
        self.SetBackgroundColour(wx.Colour(125, 152, 221))
        self.SetAutoLayout(True)
        self.SetIcon(images.getMAKE2Icon())
        
        self.initdone = 0
        self.usingrepainttimer = False
        self.hasSelection = False
        
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.aui.EVT_AUI_RENDER, self.OnAUIRender) #gets called but doesn't help much
        #self.Bind(wx.EVT_SASH_DRAGGED, self.OnSashDragged) -- doesn't work
        
        self.auiManager = wx.aui.AuiManager()
        self.auiManager.SetManagedWindow(self)
        
        self._perspectives = []
        self.n = 0
        self.x = 0
        #self.FIL = FIL
        
        self.edge = 8
        self.woff = 0
        self.MinX = self.edge
        self.MaxX = 8
        
        self.InitPanes()
        
        self.auiManager.GetArtProvider().SetMetric(wx.aui.AUI_DOCKART_CAPTION_SIZE, 20)
        self.auiManager.GetArtProvider().SetColor(wx.aui.AUI_DOCKART_BACKGROUND_COLOUR, wx.Colour(125, 152, 221))
        self.auiManager.GetArtProvider().SetColor(wx.aui.AUI_DOCKART_SASH_COLOUR, wx.Colour(125, 152, 221))
        self.auiManager.GetArtProvider().SetColor(wx.aui.AUI_DOCKART_INACTIVE_CAPTION_COLOUR, wx.Colour(183, 183, 255))
        self.auiManager.GetArtProvider().SetColor(wx.aui.AUI_DOCKART_INACTIVE_CAPTION_GRADIENT_COLOUR, wx.Colour(125, 152, 221))
        self.auiManager.Update()
        
        self.selXStart = 0
        self.selYStart = 0
        self.selXEnd = 0
        self.selYEnd = 0
        self.selMode = 0
        

        self.paintready = 0
        self.orbsready = 0
        self.repaintrequest = 1
        self.RepaintTimer = wx.Timer(self)
        self.minT = -1
        self.maxT = -1
        self.fileCategory = "All Categories"
        self.TimelinesDict = TimelinesDict
        if self.TimelinesDict is None:
            self.TimelinesDict = Globals.TimelinesDict
            if not self.TimelinesDict:
                DBFunctions.LoadMACMinMaxValues()
            
            
        self.TimelineID = ""
        self.DateSliderOn = 0
        
       
        self.ClearSelections()
        #self.FileObjectList = FIL
        
        #self.storeFIL= self.FileObjectList
        filecount = 0
            
        
        #CRAZYNESS
        self.TimelinesDict['Created']['MinDate'] = -60
        self.TimelinesDict['Created']['MaxDate'] = +60
        self.TimelinesDict['Created']['MinMonth'] = -60
        self.TimelinesDict['Created']['MaxMonth'] = +60
        self.TimelinesDict['Modified']['MinDate'] = -60
        self.TimelinesDict['Modified']['MaxDate'] = +60
        self.TimelinesDict['Modified']['MinMonth'] = -60
        self.TimelinesDict['Modified']['MaxMonth'] = +60
        self.TimelinesDict['Accessed']['MinDate'] = -60
        self.TimelinesDict['Accessed']['MaxDate'] = +60
        self.TimelinesDict['Accessed']['MinMonth'] = -60
        self.TimelinesDict['Accessed']['MaxMonth'] = +60
        
        for key in Constants.TimelineKeys:
            self.TimelinesDict[key]['FromTime'] = self.TimelinesDict[key]['MinDate']
            self.TimelinesDict[key]['ToTime'] = self.TimelinesDict[key]['MaxDate']
        
        self.initdone = 1
        self.draw()
        self.SelectedFiles = []
        self.fileCategoryView = FileCategoryView(self, self.treeCatList, Globals.MimeTypeList)
        self.root = self.fileCategoryView.AddCategories()
        
        self.db = SqliteDatabase(Globals.MACFileName)
        self.db.OpenConnection()
            
    
    def OnAUIRender(self, evt):
        self.draw()
        #self.auiManager.Update()
        evt.Skip()
        
    def OnPanMainTimelineSize(self, evt): 
        self.draw()
        
    def OnSize(self, event):
        self.draw()
        event.Skip()

    def OnPaint(self,event):
        event.Skip()
		
    def CreateTimelinesPanel(self):
        self.panMainTimelines = wx.Panel(id=wx.NewId(), parent=self, pos=wx.Point(0, 0), size=wx.Size(400, 160))
        self.panMainTimelines.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.panMainTimelines.SetAutoLayout(True)
        #self.panMainTimelines.SetConstraints(LayoutAnchors(self.panMainTimelines, True, True, True, False))
        self.panMainTimelines.Bind(wx.EVT_SIZE, self.OnPanMainTimelineSize)
        
        self.panTimelines = wx.Panel(id = wx.NewId(), parent=self.panMainTimelines, name='Timelines',
              pos=wx.Point(0, 0), size=wx.Size(392, 128))
        self.panTimelines.SetConstraints(LayoutAnchors(self.panTimelines, True, True, True, False))
        
        self.panTimelines.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.panTimelines.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.panTimelines.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.panTimelines.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseOut)
        
        self.ClientDC = wx.ClientDC(self.panTimelines)
        #self.creationImage = GetGIF('TimelineImages/create_line.gif')
        self.creationImage = images.getTLineCreatedLineBitmap()
        #self.creationImageLeft = GetGIF('TimelineImages/create_line_l.gif')
        self.creationImageLeft = images.getTLineCreatedLineLeftBitmap()
        self.creationImageRight = images.getTLineCreatedLineRightBitmap()#GetGIF('TimelineImages/create_line_r.gif')
        self.modifiedImage = images.getTLineModifiedLineBitmap()#GetGIF('TimelineImages/modify_line.gif')
        self.modifiedImageLeft = images.getTLineModifiedLineLeftBitmap()#GetGIF('TimelineImages/modify_line_l.gif')
        self.modifiedImageRight = images.getTLineModifiedLineRightBitmap()#GetGIF('TimelineImages/modify_line_r.gif')
        self.accessedImage = images.getTLineAccessLineBitmap()#GetGIF('TimelineImages/access_line.gif')
        self.accessedImageLeft = images.getTLineAccessLineLeftBitmap()#GetGIF('TimelineImages/access_line_l.gif')
        self.accessedImageRight = images.getTLineAccessLineRightBitmap() #GetGIF('TimelineImages/access_line_r.gif')
        self.selectoinImage = images.getTLineSelectionBitmap() #GetGIF('TimelineImages/selection.gif')
        self.selectoinImage.SetMask(wx.Mask(images.getTLineSelectionMaskBitmap(),wx.Colour(255,255,255)))
        self.selectedImage = images.getTLineSelectedBitmap() #GetGIF('TimelineImages/selected.gif')
        
        self.ImageEdgeWidth = self.creationImageLeft.GetWidth()
        #self.ImageEdgeWidth = self.creationImageRight.GetWidth()
        
        self.ImageTimelineHeight = self.creationImage.GetHeight()
        
        self.shapes = []
        self.dragImage = None
        self.dragShape = None
        self.hiliteShape = None
        
        self.CreatedLineY = 30-10
        self.ModifiedLineY = 60-10
        self.AccessedLineY = 90-10
        bmp = images.getCreatedSliderBitmap()
        self.SliderHalfWidth = int(bmp.GetWidth()/2)
        self.MinX = self.edge - self.SliderHalfWidth
        shape = DragShape(bmp, "Created")
        shape.pos = (self.MinX, self.CreatedLineY)
        self.shapes.append(shape)
        
        bmp = images.getModifiedSliderBitmap()
        shape = DragShape(bmp, "Modified")
        shape.pos = (self.MinX, self.ModifiedLineY)
        self.shapes.append(shape)
        
        bmp = images.getAccessedSliderBitmap()
        shape = DragShape(bmp, "Accessed")
        shape.pos = (self.MinX, self.AccessedLineY)
        self.shapes.append(shape)
        

        #self.selectedImage.SetMask(wx.Mask(GetGIF('TimelineImages/selectedmask.gif'),wx.Colour(255,255,255)))
        #print 'Create line height = %d'%self.creationImage.GetHeight()
        #print 'Modified height %d'% self.modifiedImage.GetHeight()
        #print 'Accessed height %d'%self.accessedImage.GetHeight()
        
        self.FileImage = images.getTLineFileImageBitmap() #GetGIF('TimelineImages/FileImage.gif')
        self.btnViewSelected = wx.Button(self.panMainTimelines, -1, "View Selected", pos=wx.Point(8, 128), size=wx.Size(88, 23), style=0)
        self.Bind(wx.EVT_BUTTON, self.OnViewClick, self.btnViewSelected)

        """
        self.btnViewAll = wx.Button(self.panMainTimelines, -1, "View All", pos=wx.Point(112, 128), size=wx.Size(64, 24), style=0)
        self.Bind(wx.EVT_BUTTON, self.OnViewAllClick, self.btnViewAll)
        """
        
        self.btnZoomSelection = wx.Button(self.panMainTimelines, -1, "Zoom Selection", pos=wx.Point(128, 128), size=wx.Size(88, 23), style=0)
        self.Bind(wx.EVT_BUTTON, self.OnZoomSelClick, self.btnZoomSelection)

        self.btnZoomAll = wx.Button(self.panMainTimelines, -1, "Zoom All", pos=wx.Point(232, 128), size=wx.Size(64, 23), style=0)
        self.Bind(wx.EVT_BUTTON, self.OnZoomAllClick, self.btnZoomAll)
        
      
        self.staticText3 = wx.StaticText(id=-1, label='Timpe Span:', name='staticText3', parent=self.panMainTimelines,
              pos=wx.Point(344, 136), size=wx.Size(69, 13), style=0)
        self.staticText3.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))
              
        self.lblTimeSpan = wx.StaticText(id=-1, label='00/00/0000 00:00:00', parent=self.panMainTimelines,
            pos=wx.Point(426, 136), size=wx.Size(103, 13), style=0)
        
        self.staticText5 = wx.StaticText(id=-1, label='Mouse At:', parent=self.panMainTimelines,
              pos=wx.Point(544, 136), size=wx.Size(56, 13), style=0)
        self.staticText5.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))
        
        self.lblMouseAt = wx.StaticText(id=-1, label='00/00/0000 00:00:00 ', parent=self.panMainTimelines,
            pos=wx.Point(608, 136), size=wx.Size(109, 13), style=0)
              
        self.staticText7 = wx.StaticText(id=-1, label='File Stats:', parent=self.panMainTimelines,
              pos=wx.Point(794, 136), size=wx.Size(55, 13), style=0)
        self.staticText7.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))
              
        self.lblFileStat = wx.StaticText(id=-1, label='100000 files, 1029GB', parent=self.panMainTimelines,
              pos=wx.Point(858, 136), size=wx.Size(-1, -1), style=0)
        
        return self.panMainTimelines
        
        
    # Go through our list of shapes and draw them in whatever place they are.
    def DrawShapes(self, dc):
        for shape in self.shapes:
            if shape.shown:
                shape.Draw(dc)
                
                
    def InitPanes(self):
        # add bunch of floatable panes
        self.auiManager.AddPane(self.CreateFileList(), wx.aui.AuiPaneInfo().Name("FileListView").
                          CenterPane())
        self.auiManager.AddPane(self.CreateTimelinesPanel(), wx.aui.AuiPaneInfo().
                        Name("Timelines").Caption("Timelines").
                        Bottom().Layer(1).Position(1).CloseButton(True).PinButton(True))
        
        self.auiManager.AddPane(self.CreateTextTimelines(), wx.aui.AuiPaneInfo().
                        Name("TextTimelines").Caption("Timelines").
                        Bottom().Layer(2).Position(1).CloseButton(True).PinButton(True))
        self.Bind(wx.aui.EVT_AUI_PANE_CLOSE, self.OnPaneClose)
        
        
    def OnPaneClose(self, event):
        name = event.GetPane().name
        if name == "Timelines":
            self.auiManager.GetPane("TextTimelines").Show(True)
        elif name == "TextTimelines":
            self.auiManager.GetPane("Timelines").Show(True)
        event.GetPane().Hide()
        self.auiManager.Update()
        
    
    def CreateTextTimelines(self):
        self.panTextTimelines = wx.Panel(id=-1, name='panTextTimeline', parent=self, 
            size=wx.Size(888, 86), style=wx.CLIP_CHILDREN | wx.TAB_TRAVERSAL)
        self.panTextTimelines.SetBackgroundColour(wx.Colour(225, 236, 255))
        
        self.lblCTimeFrom = wx.StaticText(id=-1,
              label='From:', name='txtCrFrom', parent=self.panTextTimelines,
              pos=wx.Point(616, 26), size=wx.Size(28, 13), style=0)

        self.staticText10 = wx.StaticText(id=-1,
              label='To:', name='staticText10', parent=self.panTextTimelines,
              pos=wx.Point(624, 50), size=wx.Size(16, 13), style=0)

        self.txtATimeTo = wx.TextCtrl(id=-1,
              name='txtATimeTo', parent=self.panTextTimelines, pos=wx.Point(648,
              50), size=wx.Size(120, 21), style=0, value='00/00/0000 00:00:00')

        self.txtATimeFrom = wx.TextCtrl(id=-1,
              name='txtATimeFrom', parent=self.panTextTimelines,
              pos=wx.Point(648, 26), size=wx.Size(120, 21), style=0,
              value='00/00/0000 00:00:00')

        id = wx.NewId()
        self.btnATimeZoom = wx.Button(id=id,
              label='Zoom', name='btnATimeZoom', parent=self.panTextTimelines,
              pos=wx.Point(784, 50), size=wx.Size(80, 23), style=0)
        self.btnATimeZoom.Bind(wx.EVT_BUTTON, self.OnBtnATimeZoomButton, id=id)

        self.staticBox2 = wx.StaticBox(id=-1,
              label='Created Time', name='staticBox2',
              parent=self.panTextTimelines, pos=wx.Point(8, 8), size=wx.Size(280,
              72), style=0)

        self.staticBitmap4 = wx.StaticBitmap(bitmap=self.creationImage, id=-1,
              name='staticBitmap4', parent=self.panTextTimelines,
              pos=wx.Point(88, 8), size=wx.Size(184, 8), style=0)

        self.staticText11 = wx.StaticText(id=-1,
              label='From:', name='staticText11', parent=self.panTextTimelines,
              pos=wx.Point(22, 26), size=wx.Size(28, 13), style=0)

        self.staticText9 = wx.StaticText(id=-1,
              label='To:', name='staticText9', parent=self.panTextTimelines,
              pos=wx.Point(32, 50), size=wx.Size(16, 13), style=0)

        self.txtCTimeFrom = wx.TextCtrl(id=-1,
              name='txtCTimeFrom', parent=self.panTextTimelines, pos=wx.Point(56,
              26), size=wx.Size(120, 21), style=0, value='00/00/0000 00:00:00')

        self.txtCTimeTo = wx.TextCtrl(id=-1,
              name='txtCTimTo', parent=self.panTextTimelines, pos=wx.Point(56,
              50), size=wx.Size(120, 21), style=0, value='00/00/0000 00:00:00')

        id = wx.NewId()
        self.btnCTimeZoom = wx.Button(id=id,
              label='Zoom', name='btnCTimeZoom', parent=self.panTextTimelines,
              pos=wx.Point(192, 50), size=wx.Size(80, 23), style=0)
        self.btnCTimeZoom.Bind(wx.EVT_BUTTON, self.OnBtnCTimeZoomButton, id=id)

        self.staticBox1 = wx.StaticBox(id=-1,
              label='Accessed Time', name='staticBox1',
              parent=self.panTextTimelines, pos=wx.Point(600, 8),
              size=wx.Size(280, 72), style=0)

        id = wx.NewId()
        self.btnCTViewFiles = wx.Button(id=id, label='View Files', name='btnCTViewFiles',
              parent=self.panTextTimelines, pos=wx.Point(192, 26), size=wx.Size(80, 23), style=0)
        self.btnCTViewFiles.Bind(wx.EVT_BUTTON, self.OnBtnCTViewFilesButton, id=id)

        id = wx.NewId()
        self.btnATimeViewFiles = wx.Button(id=id, label='View Files', name='btnATimeViewFiles', 
            parent=self.panTextTimelines, pos=wx.Point(784, 26), size=wx.Size(80, 23), style=0)
        self.btnATimeViewFiles.Bind(wx.EVT_BUTTON,   self.OnBtnATimeViewFilesButton, id=id)

        self.staticBitmap1 = wx.StaticBitmap(bitmap=self.accessedImage, id=-1,
              name='staticBitmap1', parent=self.panTextTimelines,
              pos=wx.Point(688, 8), size=wx.Size(176, 8), style=0)

        self.txtMTimeTo = wx.TextCtrl(id=-1, name='txtMTimeTo', parent=self.panTextTimelines, pos=wx.Point(352,
              50), size=wx.Size(120, 21), style=0, value='00/00/0000 00:00:00')

        self.staticBox3 = wx.StaticBox(id=-1, label='Modified Time', name='staticBox3',
              parent=self.panTextTimelines, pos=wx.Point(304, 8), size=wx.Size(280, 72), style=0)

        self.staticText13 = wx.StaticText(id=-1, label='To:', name='staticText13', parent=self.panTextTimelines,
              pos=wx.Point(328, 50), size=wx.Size(16, 16), style=0)

        id = wx.NewId()
        self.btnMTimeZoom = wx.Button(id=id, label='Zoom', name='btnMTimeZoom', parent=self.panTextTimelines,
              pos=wx.Point(488, 50), size=wx.Size(80, 23), style=0)
        self.btnMTimeZoom.Bind(wx.EVT_BUTTON, self.OnBtnMTimeZoomButton, id=id)

        id = wx.NewId()
        self.btnMTimeViewFiles = wx.Button(id=id, label='View Files', name='btnMTimeViewFiles',
              parent=self.panTextTimelines, pos=wx.Point(488, 26), size=wx.Size(80, 23), style=0)
        self.btnMTimeViewFiles.Bind(wx.EVT_BUTTON, self.OnBtnMTimeViewFilesButton, id=id)

        self.txtMTimeFrom = wx.TextCtrl(id=-1,
              name='txtMTimeFrom', parent=self.panTextTimelines,
              pos=wx.Point(352, 26), size=wx.Size(120, 21), style=0,
              value='00/00/0000 00:00:00')

        self.staticBox3 = wx.StaticBox(id=-1,
              label='Modified Time', name='staticBox3',
              parent=self.panTextTimelines, pos=wx.Point(304, 8),
              size=wx.Size(280, 72), style=0)

        self.staticText12 = wx.StaticText(id=-1,
              label='From:', name='staticText12', parent=self.panTextTimelines,
              pos=wx.Point(320, 26), size=wx.Size(28, 13), style=0)

        self.staticBitmap3 = wx.StaticBitmap(bitmap=self.modifiedImage, id=-1,
              name='staticBitmap3', parent=self.panTextTimelines,
              pos=wx.Point(384, 8), size=wx.Size(184, 8), style=0)
              
        self.staticBox4 = wx.StaticBox(id=-1,
              label='MAC Timelines', name='staticBox4',
              parent=self.panTextTimelines, pos=wx.Point(888, 8),
              size=wx.Size(272, 72), style=0)
            
        self.staticBitmap2 = wx.StaticBitmap(bitmap=self.modifiedImage,
                id=-1, name='staticBitmap2', parent=self.panTextTimelines,
                pos=wx.Point(1032, 8), size=wx.Size(56, 8), style=0)

        self.staticBitmap4 = wx.StaticBitmap(bitmap=self.creationImage, id=-1,
              name='staticBitmap4', parent=self.panTextTimelines,
              pos=wx.Point(968, 8), size=wx.Size(64, 8), style=0)
              
        self.staticBitmap1 = wx.StaticBitmap(bitmap=self.accessedImage, id=-1,
              name='staticBitmap1', parent=self.panTextTimelines,
              pos=wx.Point(1088, 8), size=wx.Size(64, 8), style=0)
              
        self.txtMACTimeFrom = wx.TextCtrl(id=-1,
              name='textCtrl4', parent=self.panTextTimelines, pos=wx.Point(928,
              26), size=wx.Size(128, 21), style=0, value='00/00/0000 00:00:00')

        self.staticText1 = wx.StaticText(id=-1,
              label='From:', name='staticText1', parent=self.panTextTimelines,
              pos=wx.Point(896, 26), size=wx.Size(28, 13), style=0)

        self.staticText2 = wx.StaticText(id=-1,
              label='To:', name='staticText2', parent=self.panTextTimelines,
              pos=wx.Point(904, 50), size=wx.Size(16, 13), style=0)

        self.txtMACTimeTo = wx.TextCtrl(id=-1,
              name='textCtrl2', parent=self.panTextTimelines, pos=wx.Point(928,
              50), size=wx.Size(128, 21), style=0, value='00/00/0000 00:00:00')
              
        id = wx.NewId()
        self.btnMACViewFiles = wx.Button(id=id,
              label='View Files', name='btnMACViewFiles',
              parent=self.panTextTimelines, pos=wx.Point(1072, 24),
              size=wx.Size(80, 23), style=0)
        self.btnMACViewFiles.Bind(wx.EVT_BUTTON, self.OnBtnMACViewFilesButton, id=id)

        id = wx.NewId()
        self.btnMACZoom = wx.Button(id=id, label='Zoom', name='btnMACZoom', parent=self.panTextTimelines,
              pos=wx.Point(1072, 48), size=wx.Size(80, 23), style=0)
        self.btnMACZoom.Bind(wx.EVT_BUTTON, self.OnBtnMACZoomButton, id=id)
              
        return self.panTextTimelines
    
    def CreateFileList(self):
        self.splitterWinFileList = wx.SplitterWindow(id=-1,
              name=u'splitterWinFileList', parent=self, size=wx.Size(600, 200), style=wx.SP_3D)
        self.splitterWinFileList.SetMinimumPaneSize(20)
        self.splitterWinFileList.SetAutoLayout(False)
        self.splitterWinFileList.SetConstraints(LayoutAnchors(self.splitterWinFileList,
              True, True, True, True))

        self.panFileList = wx.Panel(id=-1,
              name=u'panFileList', parent=self.splitterWinFileList,
              pos=wx.Point(204, 0), size=wx.Size(400, 200), style=wx.TAB_TRAVERSAL)
        self.panFileList.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.panFileList.SetAutoLayout(True)

        self.staticTextPage = wx.StaticText(id=wx.NewId(),
              label='Page', name='staticTextPage', parent=self.panFileList,
              pos=wx.Point(16, 48), size=wx.Size(28, 13), style=0)
        self.staticTextPage.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, 'Tahoma'))
              
        self.lblFileListCount = wx.StaticText(id=wx.NewId(),
              label='of 0: Showing 0 File', name='lblFileListCount', parent=self.panFileList,
              pos=wx.Point(136, 48), size=wx.Size(35, 13), style=0)
        self.lblFileListCount.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, 'Tahoma'))
              
        choiceId = wx.NewId()
        self.choiceFileListPageNum = wx.Choice(choices=['0'],
            id=choiceId, name='choiceFileListPageNum',
            parent=self.panFileList, pos=wx.Point(56, 40), size=wx.Size(64,
            21), style=0)
        self.choiceFileListPageNum.Bind(wx.EVT_CHOICE, self.OnChoiceFileListPageNumChoice,
          id=choiceId)
              
        self.lblListViewTitle = wx.StaticText(id=-1,
              label=u'', name=u'lblDirectoryName', parent=self.panFileList,
              pos=wx.Point(8, 8), size=wx.Size(26, 16), style=0)
        self.lblListViewTitle.SetForegroundColour(wx.Colour(0, 0, 187))
        self.lblListViewTitle.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Tahoma'))
        self.lblListViewTitle.SetConstraints(LayoutAnchors(self.lblListViewTitle,
              True, True, False, False))

        self.panTree = wx.Panel(id=-1,
              name=u'panTree', parent=self.splitterWinFileList, pos=wx.Point(0,
              0), size=wx.Size(200, 200), style=wx.TAB_TRAVERSAL)
        self.panTree.SetAutoLayout(True)
        self.panTree.SetBackgroundColour(wx.Colour(225, 236, 255))
        self.splitterWinFileList.SplitVertically(self.panTree, self.panFileList, 200)

        id = wx.NewId()
        self.btnShowTimelines = wx.Button(id=id, label='Show Timelines',
              parent=self.panFileList, pos=wx.Point(200, 8), size=wx.Size(99, 23), style=0)
        self.btnShowTimelines.SetConstraints(LayoutAnchors(self.btnShowTimelines, False, True, True, False))
        self.btnShowTimelines.Bind(wx.EVT_BUTTON, self.OnBtnShowTimelinesButton, id=id)
              
        btnCloseID = wx.NewId()
        self.btnClose = wx.Button(id=btnCloseID,
              label=u'Close', name=u'btnClose', parent=self.panFileList,
              pos=wx.Point(312, 8), size=wx.Size(75, 23), style=0)
        self.btnClose.SetConstraints(LayoutAnchors(self.btnClose, False, True, True, False))
        self.btnClose.Bind(wx.EVT_BUTTON, self.OnBtnCloseButton, id=btnCloseID)

       
        treeCatListID = wx.NewId()
        self.treeCatList = wx.TreeCtrl(id=treeCatListID,
              name=u'treeCatList', parent=self.panTree, pos=wx.Point(8, 36),
              size=wx.Size(184, 156), style=wx.HSCROLL | wx.VSCROLL | wx.TR_HAS_BUTTONS)
        self.treeCatList.SetConstraints(LayoutAnchors(self.treeCatList, True,
              True, True, True))
        #self.treeCatList.Show(False)
        self.treeCatList.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL, False, 'Tahoma'))
        self.treeCatList.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnTreeCatListTreeSelChanged, id=treeCatListID)

        self.lblCategories = wx.StaticText(id=-1, label='Filter by File Type', parent=self.panTree,
              pos=wx.Point(8, 8), size=wx.Size(88, 20), style=0)
        self.lblCategories.SetForegroundColour(wx.Colour(0, 0, 187))
        self.lblCategories.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, u'Tahoma'))
        
       
        listID = wx.NewId()
        self.listFilesDetails = CustomListCtrl(self.panFileList, listID, pos=wx.Point(8,72), size=wx.Size(380, 116),
                                 style=wx.LC_REPORT | wx.BORDER_NONE | wx.LC_SORT_ASCENDING )
        
        self.listFilesDetails.SetConstraints(LayoutAnchors(self.listFilesDetails, True,
              True, True, True))
        self.listFilesDetails.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, u'Tahoma'))
              
        # Now that the list exists we can init the other base class,
        # see wx/lib/mixins/listctrl.py
        listmix.ColumnSorterMixin.__init__(self, 14)
        
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnListColClick, self.listFilesDetails)
        self.listFilesDetails.Bind(wx.EVT_LEFT_DCLICK, self.OnListFilesDoubleClick)
        self.listFilesDetails.Bind(wx.EVT_CONTEXT_MENU, self.OnListFilesDetailsRightUp)
        self.AddListColumnHeadings()
        #self.imageListSmallIcon = None
        self.imageListSmallIcon = wx.ImageList(16, 16)
        #self.IconDict = {}
        #tbd: get file specific icon and display
        #self.idx1 = self.imageListSmallIcon.Add(images.getSmilesBitmap())
        self.sm_up = self.imageListSmallIcon.Add(images.getSmallUpArrowBitmap())
        self.sm_dn = self.imageListSmallIcon.Add(images.getSmallDnArrowBitmap())
        return self.splitterWinFileList

    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetListCtrl(self):
        return self.listFilesDetails

    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetSortImages(self):
        return (self.sm_dn, self.sm_up)
       
    def OnListColClick(self, event):
        event.Skip()
        
    def AddListColumnHeadings(self):
        #want to add images on the column header..
        info = wx.ListItem()
        info.m_mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_IMAGE | wx.LIST_MASK_FORMAT
        info.m_image = -1
        info.m_format = 0
        #info.m_text = "dabc"
        #self.listFilesDetails.InsertColumnInfo(0, info)
        
        info.m_text = "Name"
        self.listFilesDetails.InsertColumnInfo(0, info)
        
        info.m_format = wx.LIST_FORMAT_RIGHT
        info.m_text = "Size"
        self.listFilesDetails.InsertColumnInfo(1, info)
        
        info.m_format = wx.LIST_FORMAT_LEFT
        info.m_text = "Created Time"
        self.listFilesDetails.InsertColumnInfo(2, info)
        
        info.m_text = "Modified Time"
        self.listFilesDetails.InsertColumnInfo(3, info)
        
        info.m_text = "Accessed Time"
        self.listFilesDetails.InsertColumnInfo(4, info)
        info.m_text = "Category"
        self.listFilesDetails.InsertColumnInfo(5, info)
        info.m_text = "File Type"
        self.listFilesDetails.InsertColumnInfo(6, info)
        info.m_text = "Description"
        self.listFilesDetails.InsertColumnInfo(7, info)
        info.m_text = "MD5 Hash"
        self.listFilesDetails.InsertColumnInfo(8, info)
        info.m_text = "Known"
        self.listFilesDetails.InsertColumnInfo(9, info)
        info.m_text = "SHA1 Hash"
        self.listFilesDetails.InsertColumnInfo(10, info)
        info.m_text = "SHA224 Hash"
        self.listFilesDetails.InsertColumnInfo(11, info)
        info.m_text = "SHA256 Hash"
        self.listFilesDetails.InsertColumnInfo(12, info)
        info.m_text = "SHA384 Hash"
        self.listFilesDetails.InsertColumnInfo(13, info)
        info.m_text = "SHA512 Hash"
        self.listFilesDetails.InsertColumnInfo(14, info)
            
    def OnClose(self, event):
        self.auiManager.UnInit()
        self.Destroy()
        event.Skip()        
 
        
    def BlitArea(self,destDC,x,y,width,height,sourceBMP):
		self.BlitAreaFinal(destDC,x,y,width,height,sourceBMP,0)

    def BlitAreaMasked(self,destDC,x,y,width,height,sourceBMP):
		self.BlitAreaFinal(destDC,x,y,width,height,sourceBMP,1)

    def BlitAreaFinal(self, destDC, x, y, width, height, sourceBMP, useMask):
		sourceDC = wx.MemoryDC(sourceBMP)
		sw = sourceBMP.GetWidth()
		sh = sourceBMP.GetHeight()
		if sw < width or sh < height:
			xoff = 0
			while xoff <= width:
				yoff = 0
				while yoff <= height:
					destDC.Blit(x+xoff, y+yoff, width-xoff, height-yoff, sourceDC, 0, 0, wx.COPY, useMask, 0, 0)
					yoff +=sh
				xoff += sw
		else:
			destDC.Blit(x, y, width, height, sourceDC, 0, 0, wx.COPY, useMask, 0, 0)
			
    def draw(self):
        if (self.initdone == 0):
            return

        #edge = self.edge
        woff = 0 #self.woff
        width = self.panMainTimelines.GetSize().width
        height = self.panMainTimelines.GetSize().height
        self.bmp = wx.EmptyBitmap(width, height)

        self.MaxX = width - (2*self.edge) # - self.SliderHalfWidth#(2*self.ImageEdgeWidth) # - self.ImageEdgeWidth
        
        #self.ImageEdgeWidth = self.creationImageLeft.GetWidth()
        #self.ImageEdgeWidth = self.creationImageRight.GetWidth()
        
        #self.ImageTimelineHeight
        self.dc = wx.MemoryDC(self.bmp)
        if not self.dc.Ok():
            print 'dc not okay'
            return
            
        self.dc.SetBackground(wx.Brush(wx.Colour(255,255,255),wx.SOLID))
        self.dc.Clear()

        #newtotalpixels = width - (2*self.edge) - self.woff - 4
        newtotalpixels = width - (2*self.edge) - 4
        pixelChanged = False
        for key in Constants.TimelineKeys: #("Created", "Modified", "Accessed"):
            if (self.TimelinesDict[key]['TotalPixels'] != newtotalpixels):
                #self.totalpixels = newtotalpixels
                self.TimelinesDict[key]['TotalPixels'] = newtotalpixels
                pixelChanged = True
                self.TimelinesDict[key]['Selected'] = True
                
        if pixelChanged:
            self.ClearSelections()
            self.orbsready = 0
            
        self.pixeloffset = self.edge + 2
        self.panTimelines.SetSize((width, 112))
        
        #imageHeight = self.creationImageLeft.GetHeight()#5
        
        self.BlitArea(self.dc, self.edge, 30-8, self.creationImageLeft.GetWidth(), self.ImageTimelineHeight, self.creationImageLeft)
        self.BlitArea(self.dc, self.edge+self.creationImageLeft.GetWidth(), 30-8,
            width-self.edge-self.edge-self.creationImageRight.GetWidth()-woff, self.ImageTimelineHeight, self.creationImage)
        self.BlitArea(self.dc, width - self.edge - self.creationImageRight.GetWidth()-woff, 30-8,
            self.creationImageRight.GetWidth(), self.ImageTimelineHeight, self.creationImageRight)

        self.BlitArea(self.dc, self.edge, 60-8, self.modifiedImageLeft.GetWidth(), self.modifiedImageLeft.GetHeight(), self.modifiedImageLeft)	
        self.BlitArea(self.dc, self.edge+self.modifiedImageLeft.GetWidth(), 60-8,
            width-self.edge-self.edge-self.modifiedImageRight.GetWidth()-woff, self.modifiedImage.GetHeight(), self.modifiedImage)
        self.BlitArea(self.dc, width-self.edge-self.modifiedImageRight.GetWidth()-woff, 60-8,
            self.modifiedImageRight.GetWidth(), self.modifiedImageRight.GetHeight(), self.modifiedImageRight)

        self.BlitArea(self.dc, self.edge, 90-8, self.accessedImageLeft.GetWidth(), self.accessedImageLeft.GetHeight(), self.accessedImageLeft)
        self.BlitArea(self.dc, self.edge+self.accessedImageLeft.GetWidth(), 90-8,
            width-self.edge-self.edge-self.accessedImageRight.GetWidth()-woff, self.accessedImage.GetHeight(), self.accessedImage)
        self.BlitArea(self.dc, width-self.edge-self.accessedImageRight.GetWidth()-woff, 90-8,
            self.accessedImageRight.GetWidth(), self.accessedImageRight.GetHeight(), self.accessedImageRight)

        self.paintready = 1
        #self.dc.EndDrawing()
        self.Update()


    def Update(self):
        if (self.paintready == 0):
            self.draw()
            return

        if (self.orbsready == 0):
            #self.lefttime = self.minT
            #self.righttime = self.maxT
            self.CalculateTimeOrbs()
            return

        width = self.panTimelines.GetSize().width
        height = self.panTimelines.GetSize().height
        self.bmp = wx.EmptyBitmap(width, height)

        dc = wx.MemoryDC(self.bmp)
        if not dc.Ok():
            print 'dc not okay'
            return
        #dblbuff = wx.BufferedDC(dblbuffsur)
        
        dc.Clear()
        dc.Blit(0, 0, width, height, self.dc, 0, 0)

        #totalpixels = self.totalpixels
        #pixeloffset = self.pixeloffset

        for key in Constants.TimelineKeys: #(1,2,3):
            #pixel = 0
            drawmode = 0
            startdraw = 0
            thispixelarray = self.TimelinesDict[key]['Selections']
            #print "thispixelarray = "
            #print thispixelarray
            thispixelarray.append(0)
            timeLine = Constants.TimelineKeys.index(key)
            #if (t-1 == 0 and self.CTimeSelected) or (t-1 == 1 and self.MTimeSelected) or (t-1==2 and self.ATimeSelected):
            for pixel in range(self.TimelinesDict[key]['TotalPixels']+1): # < totalpixels+1:
                if (drawmode == 0):
                    if (thispixelarray[pixel] > 0):
                        startdraw = pixel
                        drawmode = 1
                if (drawmode == 1):
                    if (thispixelarray[pixel] == 0 or pixel == self.TimelinesDict[key]['TotalPixels']+1):
                        self.BlitAreaMasked(dc, startdraw + self.pixeloffset, (timeLine + 1)*30-8-12, pixel-startdraw, 12, self.selectedImage)
                        drawmode = 0
                #p = p + 1

        for key in Constants.TimelineKeys:
            drawmode = 0
            startdraw = 0
            thispixelarray = self.TimelinesDict[key]['PixelArrays']
            
            thispixelarray.append(0)
            timeLine = Constants.TimelineKeys.index(key)
            #if (t-1 == 0 and self.CTimeSelected) or (t-1 == 1 and self.MTimeSelected) or (t-1==2 and self.ATimeSelected):
            for pixel in range(self.TimelinesDict[key]['TotalPixels']+1): # < totalpixels+1:
                if (drawmode == 0):
                    if (thispixelarray[pixel] > 0):
                        startdraw = pixel
                        drawmode = 1
                if (drawmode == 1):
                    if (thispixelarray[pixel] == 0 or pixel == self.TimelinesDict[key]['TotalPixels']+1):
                        self.BlitArea(dc, startdraw + self.pixeloffset, (timeLine+1)*30-3-14, pixel-startdraw, 15, self.FileImage)
                        drawmode = 0
                #p = p + 1
                
        if (self.selMode == 1):
            tarX = self.selXStart
            tarY = self.selYStart
            if (self.selXStart < self.selXEnd):
                tarW = self.selXEnd-self.selXStart
            else:
                tarW = self.selXStart-self.selXEnd
                tarX = self.selXEnd
            if (self.selYStart < self.selYEnd):
                tarH = self.selYEnd-self.selYStart
            else:
                tarH = self.selYStart-self.selYEnd
                tarY = self.selYEnd
            self.BlitAreaMasked(dc, tarX, tarY, tarW, tarH, self.selectoinImage)
            
        self.ClientDC.Blit(0, 0, width, height, dc, 0, 0)
        self.DrawShapes(self.ClientDC)

    def GetMACTime(self, FileObj, key):
        if key == 'Created':
            return int(FileObj.CreatedTime)
        elif key == 'Modified':
            return int(FileObj.ModifiedTime)
        else:
            return int(FileObj.AccessedTime)
        
    def CalculateTimeOrbs(self):
        
        self.txtCTimeFrom.SetValue(DisplayDate(self.TimelinesDict['Created']['FromTime']))
        self.txtCTimeTo.SetValue(DisplayDate(self.TimelinesDict['Created']['ToTime']))
        
        self.txtMTimeFrom.SetValue(DisplayDate(self.TimelinesDict['Modified']['FromTime']))
        self.txtMTimeTo.SetValue(DisplayDate(self.TimelinesDict['Modified']['ToTime']))
        
        self.txtATimeFrom.SetValue(DisplayDate(self.TimelinesDict['Accessed']['FromTime']))
        self.txtATimeTo.SetValue(DisplayDate(self.TimelinesDict['Accessed']['ToTime']))
        self.ClearSelections()
        self.SelectedFiles = []
        for key in Constants.TimelineKeys: #('Created', 'Modified', 'Accessed'):
            if self.TimelinesDict[key]['Selected']:
                self.TimelinesDict[key]['TimeSpan'] = self.TimelinesDict[key]['ToTime'] - self.TimelinesDict[key]['FromTime'] #self.righttime-self.lefttime
                #totalpixels = self.totalpixels
                if self.TimelinesDict[key]['TotalPixels'] == 0:
                    self.TimelinesDict[key]['TotalPixels'] = 1
                    
                
                self.TimelinesDict[key]['TimePerPixel'] = 1.0*self.TimelinesDict[key]['TimeSpan'] / self.TimelinesDict[key]['TotalPixels']
                
                if self.TimelinesDict[key]['TimePerPixel'] == 0:
                    self.TimelinesDict[key]['TimePerPixel'] = 1
                
                self.TimelinesDict[key]['PixelPerTime'] = 1.0 / self.TimelinesDict[key]['TimePerPixel']
                
                self.TimelinesDict[key]['PixelArrays'] = []
                for p in range(self.TimelinesDict[key]['TotalPixels']+1):
                    self.TimelinesDict[key]['PixelArrays'].append(0)
                    self.TimelinesDict[key]['PixelSizeArrays'].append(0)

        #o = 0
        #mo = len(self.FileObjectList)
        #while o < mo:
        #Update Files List to blit
        #for fileObj in self.FileObjectList:
        for key in Constants.TimelineKeys:
            if self.TimelinesDict[key]['Selected']:
                #macTime = self.GetMACTime(fileObj, key)
                timeIndex = Constants.TimelineKeys.index(key)
                for dateKey in self.TimelinesDict[key]['Files']:
                    #if (self.FileObjectList[o][key] >= self.lefttime and self.FileObjectList[o][a] <= self.righttime):

                    #if (self.FileObjectList[o][timeIndex] >= self.TimelinesDict[key]['FromTime'] and self.FileObjectList[o][timeIndex] <= self.TimelinesDict[key]['ToTime']):
                    
                    #if ( macTime >= self.TimelinesDict[key]['FromTime'] and macTime <= self.TimelinesDict[key]['ToTime']):
                    if (dateKey >= self.TimelinesDict[key]['FromTime'] and dateKey <= self.TimelinesDict[key]['ToTime']):
                        
                        #index = int((self.FileObjectList[o][a]-self.lefttime)*pixelspertime)
                        #print 'PixelPerTime = %f'%self.TimelinesDict[key]['PixelPerTime']
                        #print 'FileObjectsTime = %d' %(self.FileObjectList[o][timeIndex])
                        #print 'FromTime = %d'%self.TimelinesDict[key]['FromTime']
                        #print 'F-FromTime = %d'%(self.FileObjectList[o][timeIndex]-self.TimelinesDict[key]['FromTime'])
                        #index = int((self.FileObjectList[o][timeIndex]-self.TimelinesDict[key]['FromTime'])*self.TimelinesDict[key]['PixelPerTime'])
                        #index = int((self.GetMACTime(fileObj, key) - self.TimelinesDict[key]['FromTime']) * self.TimelinesDict[key]['PixelPerTime'])
                        index = int((dateKey - self.TimelinesDict[key]['FromTime']) * self.TimelinesDict[key]['PixelPerTime'])
                        #if (index >= 0 and index <= totalpixels):
                        #print 'index = %d'%index
                        #print 'TotalPixels = %d'%self.TimelinesDict[key]['TotalPixels']
                        if (index >= 0 and index <= self.TimelinesDict[key]['TotalPixels']):
                            #self.pixelarrays[a][index] = self.pixelarrays[a][index]+1
                            self.TimelinesDict[key]['PixelArrays'][index] = self.TimelinesDict[key]['PixelArrays'][index] + 1
                            #self.pixelsizearrays[a][index] = self.pixelsizearrays[a][index]+self.FileObjectList[0][3]
                            self.TimelinesDict[key]['PixelSizeArrays'][index] = len(self.TimelinesDict[key]['Files'][dateKey]) #fileObj.Size #self.FileObjectList[o][3]
                        #else:
                        #    print 'outside:: ',index,', ',self.GetMACTime(fileObj,key),', ',self.TimelinesDict[key]['FromTime'],', ',self.TimelinesDict[key]['PixelPerTime']
        
        self.orbsready = 1
        self.Update()
	
    def ClearSelections(self):
        for key in Constants.TimelineKeys:
            self.TimelinesDict[key]['Selections'] = []
            for p in range(self.TimelinesDict[key]['TotalPixels']+1):
                self.TimelinesDict[key]['Selections'].append(0)
        
    def AddSelection(self, timelineKey, begin, end):
        while begin <= end:
            self.TimelinesDict[timelineKey]['Selections'][begin] = 1
            begin += 1
        
       
        
    def OnViewClick(self, event):
        self.SelectedFiles = []
        
        if not self.TimelinesDict['Modified']['Selected'] and not self.TimelinesDict['Accessed']['Selected'] and not self.TimelinesDict['Created']['Selected']:
            return
        
        self.FileCategory = "All Categories"
        self.AddSelectedFiles()

        self.AddItemsToListView()
        event.Skip()

    def OnViewAllClick(self, event):
        self.FileCategory = "All Categories"
        for key in Constants.TimelineKeys:
            self.TimelinesDict[key]['StartSelection'] = self.TimelinesDict[key]['FromTime']
            self.TimelinesDict[key]['EndSelection'] = self.TimelinesDict[key]['ToTime']
            self.TimelinesDict[key]['Selected'] = True
        
        self.TimelineID = "MAC"
        self.AddSelectedFiles()

        self.AddItemsToListView()
        event.Skip()

		
    def OnZoomSelClick(self, event):
        hasProperZoom = False
        for key in Constants.TimelineKeys:
            if self.TimelinesDict[key]['Selected']:
                minpix = self.TimelinesDict[key]['TotalPixels']
                maxpix = 0
                for pix in range(self.TimelinesDict[key]['TotalPixels']):
                    if (self.TimelinesDict[key]['Selections'][pix] > 0):
                        if (pix < minpix):
                            minpix = pix
                        if (pix > maxpix):
                            maxpix = pix
                if (minpix <= maxpix):
                    hasProperZoom = True
                    self.TimelinesDict[key]['FromTime'] = self.TimelinesDict[key]['FromTime'] + (minpix*self.TimelinesDict[key]['TimePerPixel'])
                    self.TimelinesDict[key]['ToTime'] = self.TimelinesDict[key]['ToTime'] - ((self.TimelinesDict[key]['TotalPixels'] - maxpix)*self.TimelinesDict[key]['TimePerPixel'])
        if hasProperZoom:
            self.CalculateTimeOrbs()
            
        event.Skip()

    def OnZoomAllClick(self,event):
        for key in Constants.TimelineKeys:
            self.TimelinesDict[key]['FromTime'] = self.TimelinesDict[key]['MinDate']
            self.TimelinesDict[key]['ToTime'] = self.TimelinesDict[key]['MaxDate']
            self.TimelinesDict[key]['Selected'] = True
        
        self.CalculateTimeOrbs()
        event.Skip()

    
    def TxtEnter_LT(self,event):
		newtime = gettime(self.txtLeftTime.GetValue())
		if (newtime == -1):
			self.txtLeftTime.SetValue(DisplayDate(self.lefttime))
		else:
			self.lefttime = newtime
			self.CalculateTimeOrbs()
			
    def TxtEnter_RT(self,event):
		newtime = gettime(self.txtRightTime.GetValue())
		if (newtime == -1):
			self.txtLeftTime.SetValue(DisplayDate(self.righttime))
		else:
			self.righttime = newtime
			self.CalculateTimeOrbs()
		
		
    # This is actually a sophisticated 'hit test', but in this
    # case we're also determining which shape, if any, was 'hit'.
    def FindShape(self, pt):
        for shape in self.shapes:
            if shape.HitTest(pt):
                return shape
        return None
    
    def OnLeftDown(self, event):
        
        #if there was some previous selection..erase it..
        self.ClearSelections()
        if self.hasSelection:
            self.Update()
        # Did the mouse go down on one of our sliders?
        shape = self.FindShape(event.GetPosition())

        # If a shape was 'hit', then set that as the shape we're going to
        # drag around. Get our start position. Dragging has not yet started.
        # That will happen once the mouse moves, OR the mouse is released.
        if shape:
            self.dragShape = shape
            self.dragStartPos = wx.Point(self.dragShape.pos[0], self.dragShape.pos[1])#event.GetPosition()
        
        else:

            self.selXStart = event.m_x
            self.selYStart = event.m_y
            self.selMode = 1

            
        #event.Skip()

    def OnLeftUp(self, event):
 
        if self.dragImage or self.dragShape:

            # Hide the image, end dragging, and nuke out the drag image.
            if self.dragImage:
                self.dragImage.Hide()
                self.dragImage.EndDrag()
                self.dragImage = None

            if self.hiliteShape:
                self.RefreshRect(self.hiliteShape.GetRect())
                self.hiliteShape = None

            # reposition and draw the shape
            posX = self.dragShape.pos[0] + event.GetPosition()[0] - self.dragStartPos[0]
            if posX < self.MinX:
                posX = self.MinX
                    
            if posX > self.MaxX:
                posX = self.MaxX
                    
            self.dragShape.pos = (posX, self.dragShape.pos[1])
                
            self.dragShape.shown = True
            self.RefreshRect(self.dragShape.GetRect())
                
            #if self.TimelineID >= 0 and self.DateSliderOn > 0:
            self.TimelineID = self.dragShape.ID
            mouseAt = (posX - self.edge+self.SliderHalfWidth)*self.TimelinesDict[self.TimelineID]['TimePerPixel']+self.TimelinesDict[self.TimelineID]['FromTime']
            self.DateSliderOn = CommonFunctions.GetDateSeconds(mouseAt)
            wx.BeginBusyCursor()
            self.AddSliderOnDateFiles()
            self.AddItemsToListView()
    
            wx.EndBusyCursor()
            
            self.dragShape = None

        else:
            #if not self.dragImage or not self.dragShape:
            self.dragImage = None
            self.dragShape = None
            self.selXEnd = event.m_x
            self.selYEnd = event.m_y
            self.selMode = 0

            if (self.selXStart > self.selXEnd):
                temp = self.selXStart
                self.selXStart = self.selXEnd
                self.selXEnd = temp
            if (self.selYStart > self.selYEnd):
                temp = self.selYStart
                self.selYStart = self.selYEnd
                self.selYEnd = temp

            
            for key in Constants.TimelineKeys:
                self.TimelinesDict[key]['Selected'] = False
            
            #see if it is a click
            if (self.selYEnd-self.selYStart < 5 and self.selXEnd-self.selXStart < 5):
                #we'll call this a click
                self.hasSelection = False
                timeline = -1
                if (self.selYEnd >= 0 and self.selYEnd <= 41): #y = 22 + height = 9 = 31
                    timeline = 0
                elif (self.selYEnd >= 42 and self.selYEnd <= 71): #y = 60-8=52 + height = 9 = 61
                    timeline = 1
                elif (self.selYEnd >= 72 and self.selYEnd <= 112): #y = 82 + height = 9 = 91 total height = 112
                    timeline = 2

                if (timeline > -1):
                    key = Constants.TimelineKeys[timeline]
                    #if (self.selXEnd < self.totalpixels+self.pixeloffset and self.selXEnd > self.pixeloffset):
                    if (self.selXEnd <= self.TimelinesDict[key]['TotalPixels']+self.pixeloffset and self.selXEnd >= self.pixeloffset):
                        #if (self.pixelarrays[timeline][self.selXEnd-self.pixeloffset] > 0):
                        if (self.TimelinesDict[key]['PixelArrays'][self.selXEnd-self.pixeloffset] > 0):
                            self.hasSelection = True
                            useXs = self.selXEnd - self.pixeloffset
                            useXe = self.selXEnd - self.pixeloffset
                            #while (a >= 0 and self.pixelarrays[timeline][a] > 0):
                            while (useXs >= 0 and self.TimelinesDict[key]['PixelArrays'][useXs] > 0):
                                useXs = useXs - 1
                            #while (b <= self.totalpixels and self.pixelarrays[timeline][b] > 0):
                            while (useXe <= self.TimelinesDict[key]['TotalPixels'] and self.TimelinesDict[key]['PixelArrays'][useXe] > 0):
                                useXe = useXe + 1
                            useXs+=1
                            useXe-=1
                            self.TimelinesDict[key]['StartSelection'] = useXs*self.TimelinesDict[key]['TimePerPixel']+self.TimelinesDict[key]['FromTime'] #start time
                            self.TimelinesDict[key]['EndSelection'] = (useXe+1)*self.TimelinesDict[key]['TimePerPixel']+self.TimelinesDict[key]['FromTime'] #end time
                            self.TimelinesDict[key]['Selected'] = True
                            self.AddSelection(key, useXs, useXe)
                            self.lblTimeSpan.SetLabel(disptimespan(self.TimelinesDict[key]['EndSelection'] - self.TimelinesDict[key]['StartSelection']))
                
                if not self.hasSelection:
                    self.ClearSelections()

            else:
                #if not a click, then process selected areas
                self.hasSelection = True
                
                for key in Constants.TimelineKeys:
                    timeLine = Constants.TimelineKeys.index(key)
                    if (self.selYStart < 30*(timeLine+1) + 1 and self.selYEnd > 30*(timeLine+1)+1):
                        useXs = self.selXStart - self.pixeloffset #start pixel
                        useXe = self.selXEnd - self.pixeloffset #end pixel

                        if (useXs < 0):
                            useXs = 0
                        if (useXe < 0):
                            useXe = 0
                        if (useXs > self.TimelinesDict[key]['TotalPixels']):
                            useXs = self.TimelinesDict[key]['TotalPixels']
                        if (useXe > self.TimelinesDict[key]['TotalPixels']):
                            useXe = self.TimelinesDict[key]['TotalPixels']
                        self.TimelinesDict[key]['StartSelection'] = useXs*self.TimelinesDict[key]['TimePerPixel']+self.TimelinesDict[key]['FromTime'] #start time
                        self.TimelinesDict[key]['EndSelection'] = useXe*self.TimelinesDict[key]['TimePerPixel']+self.TimelinesDict[key]['FromTime']
                        #mouseAt = (event.m_x-self.edge)*self.TimelinesDict[key]['TimePerPixel']+self.TimelinesDict[key]['FromTime']
                        
                        self.lblTimeSpan.SetLabel(disptimespan(self.TimelinesDict[key]['EndSelection'] - self.TimelinesDict[key]['StartSelection']))
                        self.AddSelection(key, useXs, useXe)
                        self.TimelinesDict[key]['Selected'] = True
                        
            self.Update()
     
        event.Skip()
        
    # Remove a shape from the display
    def EraseShape(self, shape, dc):
        r = shape.GetRect()
        dc.SetClippingRect(r)
        #self.TileBackground(dc)
        self.DrawShapes(dc)
        dc.DestroyClippingRegion()
        
        
    def OnMouseMove(self, evt):
        # Ignore mouse movement if we're not dragging.
        labelUpdated = False
        #if evt.Dragging() or evt.LeftIsDown():
        if self.dragShape:
            # if we have a shape, but haven't started dragging yet
            if self.dragShape and not self.dragImage:

                # only start the drag after having moved a couple pixels
                tolerance = 2
                pt = evt.GetPosition()
                #ptX = pt.x
                
                dx = abs(pt.x - self.dragStartPos.x)
                #dy = abs(pt.y - self.dragStartPos.y)
                if dx <= tolerance: # and dy <= tolerance:
                    return
                
                #check min and max x boundaries
                if pt.x < self.MinX:
                    pt.x = self.MinX
                    
                if pt.x > self.MaxX:
                    pt.x = self.MaxX
                
                # erase the shape since it will be drawn independently now
                #dc = wx.ClientDC(self)
                self.dragShape.shown = False
                self.EraseShape(self.dragShape, self.ClientDC)
                self.RefreshRect(self.dragShape.GetRect())
                self.Update()
                posY = self.dragShape.pos[1]

                self.dragImage = wx.DragImage(self.dragShape.bmp, wx.StockCursor(wx.CURSOR_HAND))

                hotspot = self.dragStartPos - self.dragShape.pos
                self.dragImage.BeginDrag(hotspot, self.panTimelines, self.dragShape.fullscreen)
                
                self.dragImage.Move(wx.Point(pt.x, posY))
                self.dragImage.Show()


            # if we have shape and image then move it, posibly highlighting another shape.
            elif self.dragShape and self.dragImage:
                onShape = self.FindShape(evt.GetPosition())
                unhiliteOld = False
                hiliteNew = False

                # figure out what to hilite and what to unhilite
                if self.hiliteShape:
                    if onShape is None or self.hiliteShape is not onShape:
                        unhiliteOld = True

                if onShape and onShape is not self.hiliteShape and onShape.shown:
                    hiliteNew = True

                # if needed, hide the drag image so we can update the window
                if unhiliteOld or hiliteNew:
                    self.dragImage.Hide()

                if unhiliteOld:
                    #dc = wx.ClientDC(self)
                    self.hiliteShape.Draw(self.ClientDC)
                    self.hiliteShape = None

                if hiliteNew:
                    #dc = wx.ClientDC(self)
                    self.hiliteShape = onShape
                    self.hiliteShape.Draw(self.ClientDC, wx.INVERT)

                # now move it and show it again if needed
                posX = evt.GetPosition()[0]
                posY = self.dragShape.pos[1]
                #check min and max x boundaries
                if posX < self.MinX:
                    posX = self.MinX
                    
                if posX > self.MaxX:
                    posX = self.MaxX
                    
                self.dragImage.Move(wx.Point(posX, posY))
                if unhiliteOld or hiliteNew:
                    self.dragImage.Show()
                    
            self.TimelineID = self.dragShape.ID
            mouseAt = (evt.m_x-self.edge+self.SliderHalfWidth)*self.TimelinesDict[self.TimelineID]['TimePerPixel']+self.TimelinesDict[self.TimelineID]['FromTime']
            #self.DateSliderOn = CommonFunctions.GetDateSeconds(mouseAt)
            self.lblMouseAt.SetLabel(self.TimelineID + " - " + DisplayMonthDate(mouseAt))
            a = evt.m_x - self.pixeloffset
            self.lblFileStat.SetLabel(str(self.TimelinesDict[self.TimelineID]['PixelSizeArrays'][a])+" files")
        
        else:
            #**************************************
            self.selXEnd = evt.m_x
            self.selYEnd = evt.m_y
            if self.selMode == 1:
                self.Update()
            toTime = self.maxT
            #get info for what the mouse is over
            self.lblMouseAt.SetLabel(" ")
            self.lblFileStat.SetLabel(" ")
            #foundcell = 0
            timeline = -1
            tLine = ""
            if (self.selYEnd >= 0 and self.selYEnd <= 41): #y = 22 + height = 9 = 31
                timeline = 0
                tLine = "Created - "
            
            elif (self.selYEnd >= 42 and self.selYEnd <= 71): #y = 60-8=52 + height = 9 = 61
                timeline = 1
                tLine = "Modified - "
            elif (self.selYEnd >= 72 and self.selYEnd <= 112): #y = 82 height = 9   total height = 112
                timeline = 2
                tLine = "Accessed - "
                
            if (timeline > -1):
                #self.TimelineID = timeline

                key = Constants.TimelineKeys[timeline]
                if (evt.m_x < self.edge or evt.m_x > self.TimelinesDict[key]['TotalPixels']+self.edge):
                    self.lblMouseAt.SetLabel(" ")
                    evt.Skip()
                    return
                else:
                    mouseAt = (evt.m_x-self.edge)*self.TimelinesDict[key]['TimePerPixel']+self.TimelinesDict[key]['FromTime']
                    #self.DateSliderOn = CommonFunctions.GetDateSeconds(mouseAt)
                    self.lblMouseAt.SetLabel(tLine + DisplayMonthDate(mouseAt))
                #if (self.selXEnd < self.totalpixels+self.pixeloffset and self.selXEnd > self.pixeloffset):
                if (self.selXEnd <= self.TimelinesDict[key]['TotalPixels']+self.pixeloffset and self.selXEnd >= self.pixeloffset):
                    if (self.TimelinesDict[key]['PixelArrays'][self.selXEnd-self.pixeloffset] > 0):
                        #foundcell = 1
                        a = self.selXEnd - self.pixeloffset
                        
                        """
                        b = self.selXEnd - self.pixeloffset
                        fc = 0
                        fs = 0
                        while (a >= 0 and self.TimelinesDict[key]['PixelArrays'][a] > 0):
                            a = a - 1
                        #while (b <= self.totalpixels and self.pixelarrays[timeline][b] > 0):
                        while (b <= self.TimelinesDict[key]['TotalPixels'] and self.TimelinesDict[key]['PixelArrays'][b] > 0):
                            b = b + 1
                        while (a <= b):
                            #fc = fc + self.pixelarrays[timeline][a]
                            #fc = fc + self.TimelinesDict[key]['PixelArrays'][a]
                            #fs = fs + self.pixelsizearrays[timeline][a]
                            fs = fs + self.TimelinesDict[key]['PixelSizeArrays'][a]
                            a = a + 1
                        """
                        self.lblFileStat.SetLabel(str(self.TimelinesDict[key]['PixelSizeArrays'][a])+" files")
                

        evt.Skip()
        

    def OnMouseOut(self, event):
		self.selXEnd = 0
		self.selYEnd = 0
		self.selXStart = 0
		self.selYStart = 0
		self.selMode = 0
		self.Update()
		self.lblMouseAt.SetLabel(" ")		
		self.lblFileStat.SetLabel(" ")
		event.Skip()


			
    def OnBtnCloseButton(self, event):
        self.Close()
        #self.auiManager.GetPane("Timelines").Show(True)
        #self.auiManager.GetPane("TextTimelines").Show(True)
        #self.auiManager.Update()
        event.Skip()

    def OnListFilesIconsLeftDclick(self, event):
        event.Skip()
    
    def OnListFilesIconsRightUp(self, event):
        event.Skip()

    def OnBtnCategoryViewButton(self, event):
        event.Skip()
        
    def OnBtnDirTreeViewButton(self, event):
        event.Skip()
        
    def OnTreeCatListTreeSelChanged(self, event):
        event.Skip()
        
    def OnTreeDirListTreeSelChanged(self, event):
        event.Skip()
        
    def OnTreeDirListRightUp(self, event):
        event.Skip()
    
    def SetSelectedTimelines(self, key):
        for myKey in Constants.TimelineKeys:
            if myKey == key:
                self.TimelinesDict[myKey]['Selected'] = True
            else:
                self.TimelinesDict[myKey]['Selected'] = False
    
    def OnBtnATimeZoomButton(self, event):
        wx.BeginBusyCursor()
        fromTime = gettime(self.txtATimeFrom.GetValue().strip())
        toTime = gettime(self.txtATimeTo.GetValue().strip())
        msg = ""
        if fromTime == -1:
            msg = "Invalid From Time Entered for Accessed Time!"
        if toTime == -1:
            msg = "Invalid To Time Entered for Accessed Time!"
        
        if not msg == "":
            dlg = wx.MessageDialog(self, msg ,
                'Error', wx.OK | wx.ICON_ERROR)
            try:
                dlg.ShowModal()
                return
            finally:
                wx.EndBusyCursor()
                dlg.Destroy()
        
        self.SetSelectedTimelines('Accessed')
        #print "FromTime = %s"%time.gmtime(fromTime)
        #print "ToTime = %s"%time.gmtime(toTime)
        
        self.TimelinesDict['Accessed']['FromTime'] = fromTime
        self.TimelinesDict['Accessed']['ToTime'] = toTime
        
        self.CalculateTimeOrbs()
        wx.EndBusyCursor()
        event.Skip()

    def OnBtnCTimeZoomButton(self, event):
        wx.BeginBusyCursor()
        fromTime = gettime(self.txtCTimeFrom.GetValue().strip())
        toTime = gettime(self.txtCTimeTo.GetValue().strip())
        msg = ""
        if fromTime == -1:
            msg = "Invalid From Time Entered for Created Time!"
        if toTime == -1:
            msg = "Invalid To Time Entered for Created Time!"
        
        if not msg == "":
            dlg = wx.MessageDialog(self, msg ,
                'Error', wx.OK | wx.ICON_ERROR)
            try:
                dlg.ShowModal()
                return
            finally:
                wx.EndBusyCursor()
                dlg.Destroy()
        
        self.SetSelectedTimelines('Created')
        #print "FromTime = %s"%time.gmtime(fromTime)
        #print "ToTime = %s"%time.gmtime(toTime)
        
        self.TimelinesDict['Created']['FromTime'] = fromTime
        self.TimelinesDict['Created']['ToTime'] = toTime
        
        self.CalculateTimeOrbs()
        wx.EndBusyCursor()
        event.Skip()

    def OnBtnCTViewFilesButton(self, event):
        wx.BeginBusyCursor()
        fromTime = gettime(self.txtCTimeFrom.GetValue().strip())
        toTime = gettime(self.txtCTimeTo.GetValue().strip())
        msg = ""
        if fromTime == -1:
            msg = "Invalid From Time Entered for Created Time!"
        if toTime == -1:
            msg = "Invalid To Time Entered for Created Time!"
        
        if not msg == "":
            dlg = wx.MessageDialog(self, msg ,
                'Error', wx.OK | wx.ICON_ERROR)
            try:
                dlg.ShowModal()
                return
            finally:
                wx.EndBusyCursor()
                dlg.Destroy()
        
        self.TimelineID = 'Created'
        self.SetSelectedTimelines('Created')
        #print "FromTime = %s"%time.gmtime(fromTime)
        #print "ToTime = %s"%time.gmtime(toTime)
        self.FileCategory = "All Categories"
        self.TimelinesDict['Created']['StartSelection'] = fromTime
        self.TimelinesDict['Created']['EndSelection'] = toTime
        self.AddSelectedFiles()
        self.AddItemsToListView()
        
        wx.EndBusyCursor()
        event.Skip()

        
        #self.CalculateTimeOrbs()
        event.Skip()

    def OnBtnATimeViewFilesButton(self, event):
        wx.BeginBusyCursor()
        fromTime = gettime(self.txtATimeFrom.GetValue().strip())
        toTime = gettime(self.txtATimeTo.GetValue().strip())
        msg = ""
        if fromTime == -1:
            msg = "Invalid From Time Entered for Accessed Time!"
        if toTime == -1:
            msg = "Invalid To Time Entered for Accessed Time!"
        
        if not msg == "":
            dlg = wx.MessageDialog(self, msg ,
                'Error', wx.OK | wx.ICON_ERROR)
            try:
                dlg.ShowModal()
                return
            finally:
                wx.EndBusyCursor()
                dlg.Destroy()
        
        self.TimelineID = 'Accessed'
        self.SetSelectedTimelines('Accessed')
        #print "FromTime = %s"%time.gmtime(fromTime)
        #print "ToTime = %s"%time.gmtime(toTime)
        
        self.TimelinesDict['Accessed']['StartSelection'] = fromTime
        self.TimelinesDict['Accessed']['EndSelection'] = toTime
        
        self.AddSelectedFiles()
        self.AddItemsToListView()
        wx.EndBusyCursor()
        event.Skip()
        
    def OnBtnMTimeViewFilesButton(self, event):
        wx.BeginBusyCursor()
        fromTime = gettime(self.txtMTimeFrom.GetValue().strip())
        toTime = gettime(self.txtMTimeTo.GetValue().strip())
        msg = ""
        if fromTime == -1:
            msg = "Invalid From Time Entered for Modified Time!"
        if toTime == -1:
            msg = "Invalid To Time Entered for Modified Time!"
        
        if not msg == "":
            dlg = wx.MessageDialog(self, msg ,
                'Error', wx.OK | wx.ICON_ERROR)
            try:
                dlg.ShowModal()
                return
            finally:
                wx.EndBusyCursor()
                dlg.Destroy()
        
        self.TimelineID = 'Modified'
        self.SetSelectedTimelines('Modified')
        #print "FromTime = %s"%time.gmtime(fromTime)
        #print "ToTime = %s"%time.gmtime(toTime)
        
        self.TimelinesDict['Modified']['StartSelection'] = fromTime
        self.TimelinesDict['Modified']['EndSelection'] = toTime
        
        self.AddSelectedFiles()
        self.AddItemsToListView()
        wx.EndBusyCursor()
        event.Skip()

        
    def OnBtnMACViewFilesButton(self, event):
        wx.BeginBusyCursor()
        fromTime = gettime(self.txtMACTimeFrom.GetValue().strip())
        toTime = gettime(self.txtMACTimeTo.GetValue().strip())
        msg = ""
        if fromTime == -1:
            msg = "Invalid From Time Entered for MAC Time!"
        if toTime == -1:
            msg = "Invalid To Time Entered for MAC Time!"
        
        if not msg == "":
            dlg = wx.MessageDialog(self, msg ,
                'Error', wx.OK | wx.ICON_ERROR)
            try:
                dlg.ShowModal()
                wx.EndBusyCursor()
                return
            finally:
                dlg.Destroy()
        
        for key in Constants.TimelineKeys:
            self.TimelinesDict[key]['Selected'] = True
            
            self.TimelinesDict[key]['StartSelection'] = fromTime
            self.TimelinesDict[key]['EndSelection'] = toTime
        
        self.TimelineID = "MAC - "
        self.AddSelectedFiles()
        self.AddItemsToListView()
        wx.EndBusyCursor()
        event.Skip()

    def OnBtnMTimeZoomButton(self, event):
        wx.BeginBusyCursor()
        fromTime = gettime(self.txtMTimeFrom.GetValue().strip())
        toTime = gettime(self.txtMTimeTo.GetValue().strip())
        msg = ""
        if fromTime == -1:
            msg = "Invalid From Time Entered for Modified Time!"
        if toTime == -1:
            msg = "Invalid To Time Entered for Modified Time!"
        
        if not msg == "":
            dlg = wx.MessageDialog(self, msg ,
                'Error', wx.OK | wx.ICON_ERROR)
            try:
                dlg.ShowModal()
                wx.EndBusyCursor()
                return
            finally:
                dlg.Destroy()
        
        self.SetSelectedTimelines('Modified')
        #print "FromTime = %s"%time.gmtime(fromTime)
        #print "ToTime = %s"%time.gmtime(toTime)
        
        self.TimelinesDict['Modified']['FromTime'] = fromTime
        self.TimelinesDict['Modified']['ToTime'] = toTime
        
        self.CalculateTimeOrbs()
        wx.EndBusyCursor()
        event.Skip()

        
    def OnBtnMACZoomButton(self, event):
        fromTime = gettime(self.txtMACTimeFrom.GetValue().strip())
        toTime = gettime(self.txtMACTimeTo.GetValue().strip())
        msg = ""
        if fromTime == -1:
            msg = "Invalid From Time Entered for MAC Time!"
        if toTime == -1:
            msg = "Invalid To Time Entered for MAC Time!"
        
        if not msg == "":
            dlg = wx.MessageDialog(self, msg ,
                'Error', wx.OK | wx.ICON_ERROR)
            try:
                dlg.ShowModal()
                return
            finally:
                dlg.Destroy()
        
        for key in Constants.TimelineKeys:
            self.TimelinesDict[key]['Selected'] = True
            
            self.TimelinesDict[key]['FromTime'] = fromTime
            self.TimelinesDict[key]['ToTime'] = toTime
        
        self.CalculateTimeOrbs()
        event.Skip()
        
    def OnListFilesDoubleClick(self, event):
        if self.IsFileSelected():
            self.OpenFile()
        event.Skip()
    
    def GetTreeItemText(self, item):
        if item:
            text = self.treeCatList.GetItemText(item)
            return text[:text.rfind("(")-1]
        else:
            return ""
        
    def GetPathName(self, item, treeCtrl):
        pathName = []
        pathName.append(self.GetTreeItemText(item))
        parentItem = treeCtrl.GetItemParent(item)
        while not (parentItem == self.root):
            pathName.insert(0, self.GetTreeItemText(parentItem))
            #parentItem = self.treeDirList.GetItemParent(parentItem)
            parentItem = treeCtrl.GetItemParent(parentItem)
        
        return "/".join(pathName)
    
    def OnTreeCatListTreeSelChanged(self, event):
        #self.OnTreeDirListTreeSelChanged(event, self.treeCatList)
        #if treeCtrl == None:
        #    treeCtrl = self.treeDirList
        #print treeCtrl.Name
        wx.BeginBusyCursor()
        item = self.treeCatList.GetSelection()
        #
        if item == self.root:
            self.fileCategory = "All Categories"
        else:
            self.fileCategory = self.GetPathName(item,  self.treeCatList)
            #dirPath += self.treeDirList.GetItemText(item)
            #self.fileCategory += self.GetTreeItemText(item)
        #print dirPath
        """
        if self.treeDirView:
            if self.dirPath.count(PlatformMethods.GetDirSeparator()) == 0:
                 self.dirPath += PlatformMethods.GetDirSeparator()

            self.dirPath = PlatformMethods.ConvertFilePath(self.dirPath)
        """
        #self.UpdateFilesInDirectory()
        self.InitializeFileListStuff()
        fileIndex = 0
        category = self.fileCategory.split("/")
        for fileInfo in self.SelectedFiles:
            found = False
            if not item == self.root:
                #if self.fileCategory == "Unknown":
                #    if fileInfo.MimeType == "Unknown" and fileInfo.Description == "Unknown":
                #        found = True
                #else:
                
                """
                category = self.dirPath.split("/")
                for aFile in Globals.FilesMimeTypesDict[category[0]]:
                    if aFile.MimeType.find(category[1]) > 0:
                        self.FilesList.append(aFile)
                for aFile in Globals.FilesMimeTypesDict[category[0]]:
                    if fileInfo.MimeType.find(category[1]) > 0:
                        self.CreateListItem(fileInfo, fileIndex)
                """
                #for cat in category:
                if fileInfo.MimeType.find(self.fileCategory) >= 0:
                    self.CreateListItem(fileInfo, fileIndex)
                
                """
                if not found:
                    if fileInfo.Description == self.fileCategory and fileInfo.MimeType == "Unknown":
                        found = True
                if found:
                    self.CreateListItem(fileInfo, fileIndex)
                """
            else:
                self.CreateListItem(fileInfo, fileIndex)
            fileIndex += 1
                    
        self.AddItemsToListView()
        wx.EndBusyCursor()
        event.Skip()
    
    def OnListFilesDetailsRightUp(self, event):
        self.listFilesDetails.PopupMenu(self.popupMenuFile)
        event.Skip()
    
    def InitializeFileListStuff(self):
        self.FileInfo = {}
        self.listFilesDetails.DeleteAllItems()
        self.IconDict = {}
        
    def AddSelectedFiles(self):
        self.InitializeFileListStuff()
        fileIndex = 0
        self.TimelineID = ""
        #for fileObj in self.FileObjectList:
        for key in Constants.TimelineKeys:
            if self.TimelinesDict[key]['Selected']:
                if self.TimelineID == "":
                    self.TimelineID += key
                else:
                    self.TimelineID += " - " + key
                #timeIndex = Constants.TimelineKeys.index(key)
                for dateKey in self.TimelinesDict[key]['Files']:
                    #macTime = self.GetMACTime(fileObj, key)
                    if ( dateKey >= self.TimelinesDict[key]['StartSelection'] and dateKey <= self.TimelinesDict[key]['EndSelection']):
                        for fileObj in self.TimelinesDict[key]['Files'][dateKey]:
                            self.SelectedFiles.append(fileObj)
                            self.CreateListItem(fileObj, fileIndex)
                            fileIndex += 1
                        
                        
    def AddSliderOnDateFiles(self):
        self.InitializeFileListStuff()
        fileIndex = 0
        if self.TimelinesDict[self.TimelineID]['Files'].has_key(self.DateSliderOn):
            #for dateKey in self.TimelinesDict[key]['Files'][self.DateSliderOn]:
                #macTime = self.GetMACTime(fileObj, key)
                #if ( dateKey >= self.TimelinesDict[key]['StartSelection'] and dateKey <= self.TimelinesDict[key]['EndSelection']):
            for fileObj in self.TimelinesDict[self.TimelineID]['Files'][self.DateSliderOn]:
                self.SelectedFiles.append(fileObj)
                self.CreateListItem(fileObj, fileIndex)
                fileIndex += 1

                        
    def AddItemsToListView(self):
        self.listFilesDetails.SetImageList(self.imageListSmallIcon, wx.IMAGE_LIST_SMALL)
        #self.CreateFileIconList(iconInfo)
        self.itemDataMap = self.FileInfo       
        items = self.FileInfo.items()
        #print items
        #print len(self.FileInfo)
        #print len(items)
        for key, data in items:
        #print str(key) + str(data)
        #try:
            index = self.listFilesDetails.InsertImageStringItem(sys.maxint, data[0], self.IconDict[key])
            self.listFilesDetails.SetStringItem(index, 1, data[1])
            self.listFilesDetails.SetStringItem(index, 2, data[2])
            self.listFilesDetails.SetStringItem(index, 3, data[3])
            self.listFilesDetails.SetStringItem(index, 4, data[4])
            self.listFilesDetails.SetStringItem(index, 5, data[5])
            self.listFilesDetails.SetStringItem(index, 6, data[6])
            self.listFilesDetails.SetStringItem(index, 7, data[7])
            self.listFilesDetails.SetStringItem(index, 8, data[8])
            self.listFilesDetails.SetStringItem(index, 9, data[9])
            self.listFilesDetails.SetStringItem(index, 10, data[10])
            self.listFilesDetails.SetStringItem(index, 11, data[11])
            self.listFilesDetails.SetStringItem(index, 12, data[12])
            self.listFilesDetails.SetStringItem(index, 13, data[13])
            self.listFilesDetails.SetItemData(index, key)
        
        self.listFilesDetails.SetColumnWidth(0, 250)
        self.listFilesDetails.SetColumnWidth(1, 50)
        self.listFilesDetails.SetColumnWidth(2, 100)
        self.listFilesDetails.SetColumnWidth(3, 100)
        self.listFilesDetails.SetColumnWidth(4, 100)
        self.listFilesDetails.SetColumnWidth(5, 50)
        self.listFilesDetails.SetColumnWidth(6, 100)
        self.listFilesDetails.SetColumnWidth(7, 100)
        self.listFilesDetails.SetColumnWidth(8, 125)
        
        value = "file"
        if len(self.FileInfo) > 0:
            value = "files"
        self.lblListViewTitle.SetLabel(self.TimelineID + " - " + PlatformMethods.Convert(self.fileCategory) + " ( " + str(len(self.FileInfo)) + " " + value + " )")
        self.SetCursor(wx.STANDARD_CURSOR)             
        #wx.EndBusyCursor()
                        
    def CreateListItem(self, fileInfo, fileIndex):
        #totalFiles = totalFiles += 1
        #print "totalFiles = " + str(totalFiles)
        listItem = []
        listItem.append(os.path.join(PlatformMethods.Convert(fileInfo.DirPath), PlatformMethods.Convert(fileInfo.Name)))
        listItem.append(CommonFunctions.ConvertByteToKilobyte(fileInfo.Size))
        listItem.append(CommonFunctions.GetShortDateTime(fileInfo.Created))
        listItem.append(CommonFunctions.GetShortDateTime(fileInfo.Modified))
        listItem.append(CommonFunctions.GetShortDateTime(fileInfo.Accessed))
        listItem.append(fileInfo.Category)
        listItem.append(PlatformMethods.Convert(fileInfo.MimeType))
        listItem.append(PlatformMethods.Convert(fileInfo.Description))
        listItem.append(fileInfo.MD5)
        listItem.append(fileInfo.SHA1)
        listItem.append(fileInfo.SHA224)
        listItem.append(fileInfo.SHA256)
        listItem.append(fileInfo.SHA384)
        listItem.append(fileInfo.SHA512)
        #self.listFilesDetails.Append(listItem)
        #print listItem
        self.FileInfo[fileIndex] = tuple(listItem)
        #print self.FileInfo
        iconFound = False
        if not (fileInfo.Name.rfind('.') == -1):
            fileExtension = fileInfo.Name[fileInfo.Name.rfind('.'):]
            fileType = wx.TheMimeTypesManager.GetFileTypeFromExtension(fileExtension)
            if fileType:
                #fullFileName = os.path.join(self.dirPath, data[0])
                try:
                    info = fileType.GetIconInfo()
                    if info:
                        icon, file, idx = info
                        #print icon
                        if icon.Ok():
                            #iconInfo[totalFiles] = icon
                            #bmp = wx.Image(opj('bitmaps/image.bmp'), wx.BITMAP_TYPE_BMP).ConvertToBitmap()
                            icon.SetSize(wx.Size(16, 16))
                            self.IconDict[fileIndex] = self.imageListSmallIcon.AddIcon(icon)
                            iconFound = True
                except:
                    print 'error occured'
                    
        if not iconFound:
            bmp = images.getNoFile16Icon()
            self.IconDict[fileIndex] = self.imageListSmallIcon.AddIcon(bmp)

    def OnBtnShowTimelinesButton(self, event):
        self.auiManager.GetPane("TextTimelines").Show(True)
        self.auiManager.GetPane("Timelines").Show(True)
        self.auiManager.Update()
        event.Skip()
       

if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = MDIChildTimeline(None, None)
    frame.Show(True)
    app.MainLoop()