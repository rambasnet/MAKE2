#-----------------------------------------------------------------------------
# Name:        EmailMapWindow.py
# Purpose:     
#
# Author:      Ram B. Basnet
#
# Created:     2007/10/31
# RCS-ID:      $Id: EmailMapWindow.py,v 1.6 2008/03/29 05:18:46 rbasnet Exp $
# Copyright:   (c) 2006
# Licence:     <your licence>
# New field:   Whatever
#-----------------------------------------------------------------------------

import wx, re
import wx.lib.ogl as ogl
import math
import Globals
import Constants
import EmailUtilities
import CommonFunctions
import images

firstEmailID = ""
#toAddress = 

class TestTransientPopup(wx.PopupTransientWindow):
    """Adds a bit of text and mouse movement to the wx.PopupWindow"""
    def __init__(self, parent, style, text):
        wx.PopupWindow.__init__(self, parent, style)
        #self.log = log
        self.SetBackgroundColour(wx.Colour(205, 235, 203))
        st = wx.StaticText(self, -1,
                          text                          ,
                          pos=(10,10))
        sz = st.GetBestSize()
        self.SetSize( (sz.width+20, sz.height+20) )
                
        st.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
        st.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        st.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
        st.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
        
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
        self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)

        wx.CallAfter(self.Refresh)

    def OnMouseLeftDown(self, evt):
        self.Refresh()
        self.ldPos = evt.GetEventObject().ClientToScreen(evt.GetPosition())
        self.wPos = self.ClientToScreen((0,0))
        self.CaptureMouse()

    def OnMouseMotion(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            dPos = evt.GetEventObject().ClientToScreen(evt.GetPosition())
            nPos = (self.wPos.x + (dPos.x - self.ldPos.x),
                    self.wPos.y + (dPos.y - self.ldPos.y))
            self.Move(nPos)

    def OnMouseLeftUp(self, evt):
        self.ReleaseMouse()

    def OnRightUp(self, evt):
        self.Show(False)
        self.Destroy()
        
    #def ProcessLeftDown(self, evt):
    #print "ProcessLeftDown\n")
    #    return False

    #def OnDismiss(self):
    #print "OnDismiss\n")

class RoundedRectangleShape(ogl.RectangleShape):
    def __init__(self, displayName, color=wx.Colour(225, 236, 255), id=-1, width=100, height=25):
        ogl.RectangleShape.__init__(self, width, height)
        self.SetPen(wx.BLACK_PEN)
        self.SetBrush(wx.Brush(color))
        self.SetCornerRadius(-0.1)
        self.DisplayName = displayName
        self.ID = id
        for line in self.DisplayName.split('\n'):
            self.AddText(line)
        

class CenterEllipseShape(ogl.EllipseShape):
    def __init__(self, displayName, id=-1, width=170, height=40): 
        ogl.EllipseShape.__init__(self, width, height)
        self.SetPen(wx.Pen(wx.BLUE, 3))
        self.SetBrush(wx.Brush(wx.Colour(225, 236, 255)))
        self.DisplayName = displayName
        self.ID = id
        #for line in self.DisplayName.split('\n'):
        self.AddText(self.DisplayName)


class CenterCircleShape(ogl.CircleShape):
    def __init__(self, displayName, id=-1, radius=150): 
        ogl.CircleShape.__init__(self, radius)
        self.SetPen(wx.Pen(wx.BLUE, 3))
        self.SetBrush(wx.Brush(wx.Colour(225, 236, 255)))
        self.DisplayName = displayName
        self.ID = id
        #for line in self.DisplayName.split('\n'):
        self.AddText(self.DisplayName)
    
#----------------------------------------------------------------------

class MyEvtHandler(ogl.ShapeEvtHandler):
    def __init__(self, parent, frame, EmailDict, CentralID=""):
        ogl.ShapeEvtHandler.__init__(self)
        self.parent = parent
        self.frame = frame
        self.EmailsDict = EmailDict
        self.CentralID = CentralID
        self.EmailRE = re.compile('([\W]*)([A-Z0-9._%-]+@[A-Z0-9._%-]+\.[A-Z]+)([\W]*)', re.I)
        #self.statbarFrame = frame
        #global fromAddress
        #self.fromAddress = ""

    def OnLeftClick(self, x, y, keys=0, attachment=0):
        shape = self.GetShape()
        canvas = shape.GetCanvas()
        dc = wx.ClientDC(canvas)
        canvas.PrepareDC(dc)

        if shape.Selected():
            shape.Select(False, dc)
            canvas.Redraw(dc)
        else:
            redraw = False
            shapeList = canvas.GetDiagram().GetShapeList()
            toUnselect = []

            for s in shapeList:
                if s.Selected():
                    # If we unselect it now then some of the objects in
                    # shapeList will become invalid (the control points are
                    # shapes too!) and bad things will happen...
                    toUnselect.append(s)

            shape.Select(True, dc)

            if toUnselect:
                for s in toUnselect:
                    s.Select(False, dc)

                canvas.Redraw(dc)

    def OnLeftDoubleClick(self, x, y, keys=0, attachment=0):
        shape = self.GetShape()
        #global firstEmailID
        CentralID = shape.DisplayName
        #print CentralID
        if CentralID == self.CentralID:
            return
        
        if not Globals.EmailsDict.has_key(CentralID):
            if not self.EmailRE.search(CentralID):
                CentralID = EmailUtilities.LookupEmailID(CentralID).lower()
            
            if not Globals.EmailsDict.has_key(CentralID):
                CommonFunctions.ShowErrorMessage(self.frame, "Central ID: %s is not found in database!"%CentralID)
                return
            
        
        GroupEmailsDict = {}
            
        #if CentralID != self.CentralID or self.GroupEmailsDict != Globals.GroupEmailsDict:
        #Globals.GroupEmailsDict = self.GroupEmailsDict
        #Globals.CentralID = self.CentralID
        OrderedEmailDict = {}
        emailsInfoDict = EmailUtilities.OrderEmailsToCentralEmail(CentralID, Globals.EmailsDict, OrderedEmailDict, GroupEmailsDict)
        map = WindowHolder(Globals.frmGlobalMainForm, OrderedEmailDict, emailsInfoDict, CentralID)
        map.Show(True)
        #print firstEmailID

    def OnEndDragLeft(self, x, y, keys=0, attachment=0):
        shape = self.GetShape()
        ogl.ShapeEvtHandler.OnEndDragLeft(self, x, y, keys, attachment)

        if not shape.Selected():
            self.OnLeftClick(x, y, keys, attachment)


    def OnSizingEndDragLeft(self, pt, x, y, keys, attch):
        ogl.ShapeEvtHandler.OnSizingEndDragLeft(self, pt, x, y, keys, attch)


    def OnMovePost(self, dc, x, y, oldX, oldY, display):
        ogl.ShapeEvtHandler.OnMovePost(self, dc, x, y, oldX, oldY, display)


    def OnRightClick(self, x, y, keys=0, attachment=0):
        global firstEmailID
        shape = self.GetShape()
        toEmail = shape.DisplayName
        emailReceived = 0
        emailSent = 0
        DisplayInfo = ""
        toName = ""
        if self.CentralID:
            toName = EmailUtilities.LookupName(toEmail)
            if toName == None or toName.strip() == "":
                toName = toEmail
            if toEmail == self.CentralID:
                DisplayInfo = "%s\n<%s>\n"%(toName, toEmail)
                DisplayInfo += "Received: %d\n"%Globals.CentralEmailReceived
                DisplayInfo += "Sent: %d\n"%(Globals.CentralEmailSent)
                
            else:
                #firstEmailID = self.CentralID
                id = self.GetShape().ID
                emailReceived = self.EmailsDict[id]['Sent']
                #if self.EmailsDict[toEmail].has_key(firstEmailID):
                emailSent = self.EmailsDict[id]['Received']
                
                DisplayInfo = "%s\n<%s>\n"%(toName, toEmail)
                DisplayInfo += "Received: %d\n"%emailReceived
                DisplayInfo += "Sent: %d\n"%(emailSent)
                DisplayInfo += "%.02f"%(self.EmailsDict[id]['Percent']) + " %"
        else:
            if self.EmailsDict[firstEmailID].has_key(toEmail):
                emailReceived = self.EmailsDict[firstEmailID][toEmail]['Emails']
            if self.EmailsDict[toEmail].has_key(firstEmailID):
                emailSent = self.EmailsDict[toEmail][firstEmailID]['Emails']
                
        #print DisplayInfo
        win = TestTransientPopup(self.parent, wx.SIMPLE_BORDER, DisplayInfo )
        
        # Show the popup right at where the mouse is clicked
        #btn = evt.GetEventObject()
        #pos = (self.GetShape().GetX()+50, self.GetShape().GetY())
        
        
        #pos = self.parent.ClientToScreen(pos)
        #print pos s
        #shape object doesn't have clienttoscreen method
        #pos = shape.ClientToScreen( (0,0) )
        pos = (x, y)
        #print pos
        pos = self.ConvertCoords(pos[0], pos[1])
        size = (150, 150)
        win.Position(pos, size)

        win.Show(True)

    def ConvertCoords(self, x, y):
        xView, yView = self.parent.GetViewStart()
        #print 'view start ', self.parent.GetViewStart()
        xDelta, yDelta = self.parent.GetScrollPixelsPerUnit()
        return (x - (xView * xDelta), y - (yView * yDelta))
            
#----------------------------------------------------------------------

class EmailMapWindow(ogl.ShapeCanvas):
    def __init__(self, parent, emailsDict, emailsInfoDict, CentralID):
        ogl.ShapeCanvas.__init__(self, parent)
        self.frame = parent
        #self.EmailRE = re.compile('([\W]*)([A-Z0-9._%-]+@[A-Z0-9._%-]+\.[A-Z]+)([\W]*)', re.I)
        
        self.EmailsDict = emailsDict
        self.CentralID = CentralID
        self.EmailsInfoDict = emailsInfoDict
        
        self.totalShapes = 0
        if self.CentralID:
            #if not self.EmailRE.search(self.CentralID):
            #    self.CentralID = EmailUtilities.LookupEmailID(self.CentralID).lower()
                
            #self.CentralID = self.CentralID.lower() 
            self.shapesToDraw = self.EmailsDict[self.CentralID]
            self.totalShapes = len(self.shapesToDraw)
            if self.totalShapes == 0:
                CommonFunctions.ShowErrorMessage(self.frame, "No Emails found for CentralID %s"%self.CentralID)
                return
        else:
            self.shapesToDraw = self.EmailsDict
               
        self.XGap = 40
        self.YGap = 20
        self.rectHeight = 25
        self.rectWidth = 100
        self.ellipseWidth = 170
        self.ellipseHeight = 40
        sqrtValue = int(math.sqrt(self.totalShapes)+1)
        self.maxWidth = sqrtValue*self.rectWidth + sqrtValue*self.XGap
        self.maxHeight = sqrtValue*self.rectWidth + sqrtValue*self.YGap
        #self.SetClientSize(wx.Size(self.maxWidth, self.maxHeight))
        #SetScrollbars(self, int pixelsPerUnitX, int pixelsPerUnitY, int noUnitsX, 
        #   int noUnitsY, int xPos=0, int yPos=0, bool noRefresh=False)
        virtualWidth = self.maxWidth/20
        virtualHeight = self.maxHeight/20
        #xScrollPos = 20*virtualWidth/2
        #yScrollPos = 20*virtualHeight/2
        
        if self.maxWidth < 1280:
            self.maxWidth = 1280
        if self.maxHeight < 1024:
            self.maxHeight = 1024
        self.SetVirtualSize((self.maxWidth, self.maxHeight))
        #print 'Parent size = ', parent.GetSize()
        self.virtualSize = self.GetVirtualSize()
        #print 'virtual size ', self.virtualSize
        self.CenterX = self.virtualSize[0]/2
        self.CenterY = self.virtualSize[1]/2
        #self.SetScrollbars(20, 20, virtualWidth, virtualHeight, xScrollPos, yScrollPos)
        
        self.SetScrollRate(20, 20)
        xDelta, yDelta = self.GetScrollPixelsPerUnit()
        xScroll = (self.CenterX - parent.GetSize()[0]/2) / xDelta
        yScroll = (self.CenterY - parent.GetSize()[1]/2) / yDelta
        #print 'xScroll, yScroll ', xScroll, " ", yScroll
        #if yScroll > 0 or xScroll > 0:
        self.Scroll(xScroll, yScroll)
        
        """
        print 'centerX = %d'%self.CenterX
        print 'CenterY = %d'%self.CenterY
        print 'x scroll position', self.GetScrollPos(0)
        print 'y scroll position', self.GetScrollPos(1)
        print self.GetClientSizeTuple()
        print 'width = %d'%self.GetSizeTuple()[0]
        print 'height = %d'%self.GetSizeTuple()[1]
        print 'max width = %d'%self.GetMaxWidth()
        print 'max height = %d'%self.GetMaxHeight()
        print 'screen position ', self.GetScreenPositionTuple()
        """
        
        self.SetBackgroundColour(wx.WHITE)
        self.diagram = ogl.Diagram()
        self.SetDiagram(self.diagram)
        self.diagram.SetCanvas(self)
        self.shapes = {}
        self.save_gdi = []
        
        
        brush = wx.Brush(wx.Colour(225, 236, 255), wx.SOLID)
        rRectBrush = wx.Brush("MEDIUM TURQUOISE", wx.SOLID)
        dsBrush = wx.Brush("WHEAT", wx.SOLID)
        
        #self.maxWidth/2*10 and self.maxHeight/2*10 gives the right bottom corner
        self.CommColors = {}
        
       
        if self.CentralID:
            #self.shapesToDraw = self.EmailsDict[self.CentralID]  
            #self.MyAddShape(CenterEllipseShape(self.CentralID), self.CenterX, self.CenterY)
            self.MyAddShape(CenterCircleShape(self.CentralID), self.CenterX+10, self.CenterY-5)
            #self.ShowShape(self.CentralID)
            self.totalEmails = self.EmailsInfoDict['CentralEmailSent'] + self.EmailsInfoDict['CentralEmailReceived'] #EmailUtilities.GetCentralTotalEmails(self.CentralID, self.EmailsDict)
            if self.totalEmails == 0:
                CommonFunctions.ShowErrorMessage(self.frame, "No emails found for CentralID %s"%self.CentralID)
                return
            
            maxPercent = self.EmailsInfoDict['CentralMaxEmails']/float(self.totalEmails)*100
            minPercent = self.EmailsInfoDict['CentralMinEmails']/float(self.totalEmails)*100
            #print 'max percent ', maxPercent
            #print 'min percent ', minPercent
            
            range = maxPercent - minPercent
            totalColors = 5
            diff = range/float(totalColors)
            percent = maxPercent - diff
            #print ' 1 ', percent
            self.CommColors[1] = {'Percent':percent, 'Color':wx.Color(255, 99, 71)}
            percent = percent - diff
            self.CommColors[2] = {'Percent':percent, 'Color':wx.Color(240, 128, 128)}
            percent = percent - diff
            self.CommColors[3] = {'Percent':percent, 'Color':wx.Color(255, 255, 0)}
            percent = percent - diff
            self.CommColors[4] = {'Percent':percent, 'Color':wx.Color(154,205,50)}
            percent = percent - diff
            #print ' 5 ', percent
            self.CommColors[5] = {'Percent':percent, 'Color':wx.Color(176, 196, 222)}
            
        else:
            self.totalEmails = Globals.TotalEmails
        
        self.Circle90Count =  len(self.EmailsDict)
        totalAccounts = len(self.EmailsDict)
        xStart = self.CenterX - (self.ellipseWidth) - self.XGap
        yStart = self.CenterY

        #print self.EmailsDict
        
        #percent = int(float(self.shapesToDraw[1]['Sent']+self.shapesToDraw[1]['Received'])/float(self.totalEmails)*100)
        #self.shapesToDraw[1]['Percent'] = percent
        #self.MyAddShape(RoundedRectangleShape(self.shapesToDraw[1]['Email'], self.GetColor(percent), 1), xStart, yStart)
        x = xStart #+self.XGap
        y = yStart #+self.YGap
        #yMax = yStart + 100
        #yMin = yStart - circle*100
        #circle = 1
        fromShape = self.shapes[self.CentralID]['Shape']
        
        
        for id in self.shapesToDraw:
            #if not fromEmail == self.CentralID:
            
            percent = float(self.shapesToDraw[id]['Sent']+self.shapesToDraw[id]['Received'])/float(self.totalEmails)*100
            self.shapesToDraw[id]['Percent'] = percent
            self.MyAddShape(RoundedRectangleShape(self.shapesToDraw[id]['Email'], self.GetColor(percent), id), x, y)
            self.AddLineShape(fromShape, id)
            #self.ShowShape(self.shapesToDraw[id]['Email'])
            #print 'x = %d'%x
            #print 'y= %d'%y
            if x >= self.CenterX:
                
                if y <= self.CenterY:
                    x -= self.XGap
                    #y -= self.YGap
                else: #y < yMax:
                    x += self.XGap
                y -= self.YGap            
                #i += 1
            else:
                y += self.YGap
                if y < self.CenterY:
                    x -= self.XGap
                    #y -= self.YGap
                else: # y < yMax:
                    x += self.XGap
             
            if x <= xStart and y == yStart :
                xStart -= (self.rectWidth  + self.XGap + 10)
                x = xStart
                
            

        dc = wx.ClientDC(self)
        self.PrepareDC(dc)
        self.ShowShapes()
        
        

    def AddLineShape(self, fromShape, id):
        if self.shapesToDraw[id]['Sent'] > 0 and self.shapesToDraw[id]['Received'] > 0:
            line = ogl.LineShape()
            line.SetCanvas(self)
            line.SetPen(wx.RED_PEN)
            line.SetBrush(wx.RED_BRUSH)
            line.AddArrow(ogl.ARROW_ARROW, end=ogl.ARROW_POSITION_END)
            line.Draggable()
            line.MakeLineControlPoints(2)
            toEmail = self.shapesToDraw[id]['Email']
            toShape = self.shapes[toEmail]['Shape']
            fromShape.AddLine(line, toShape)
            self.diagram.AddShape(line)
            line.Show(True)
        else: #there is only one way communication, find out which way and draw blue line with single arrow head
            #if only sent to other account
            if self.shapesToDraw[id]['Sent'] > 0:
                line = ogl.LineShape()
                line.SetCanvas(self)
                line.SetPen(wx.Pen(wx.BLUE))
                line.SetBrush(wx.Brush(wx.BLUE))
                line.AddArrow(ogl.ARROW_ARROW, end=ogl.ARROW_POSITION_END)
                line.Draggable()
                line.MakeLineControlPoints(2)
                toEmail = self.shapesToDraw[id]['Email']
                toShape = self.shapes[toEmail]['Shape']
                fromShape.AddLine(line, toShape)
                self.diagram.AddShape(line)
                line.Show(True)
            #must have only received emails
            #
            elif self.shapesToDraw[id]['Received'] > 0:
                line = ogl.LineShape()
                line.SetCanvas(self)
                line.SetPen(wx.Pen(wx.GREEN))
                line.SetBrush(wx.Brush(wx.GREEN))
                line.AddArrow(ogl.ARROW_ARROW, end=ogl.ARROW_POSITION_END)
                line.Draggable()
                line.MakeLineControlPoints(2)
                toEmail = self.shapesToDraw[id]['Email']
                toShape = self.shapes[toEmail]['Shape']
                toShape.AddLine(line, fromShape)
                self.diagram.AddShape(line)
                line.Show(True)
        
    def MyAddShape(self, shape, x, y):
        shape.SetDraggable(True, True)
        shape.SetCanvas(self)
        shape.SetX(x)
        shape.SetY(y)
        #shape.SetShadowMode(ogl.SHADOW_RIGHT)
        #self.diagram.AddShape(shape)
        #shape.Show(True)

        evthandler = MyEvtHandler(self, self.frame, self.shapesToDraw, self.CentralID)
        evthandler.SetShape(shape)
        evthandler.SetPreviousHandler(shape.GetEventHandler())
        shape.SetEventHandler(evthandler)

        self.shapes[shape.DisplayName] = {'Shape': shape}
        return shape

    def ShowShape(self, dispName):
        self.diagram.AddShape(self.shapes[dispName]['Shape'])
        self.shapes[dispName]['Shape'].Show(True)
        
    def ShowShapes(self):
        for dispName in self.shapes:
            self.diagram.AddShape(self.shapes[dispName]['Shape'])
            self.shapes[dispName]['Shape'].Show(True)

    def GetColor(self, percent):
        #print percent
        for id in self.CommColors:
            if percent >= self.CommColors[id]['Percent']:
                return self.CommColors[id]['Color']
        return wx.Color(217, 217, 217)
        """
        if percent >= 90:
            return (wx.Color(255, 99, 71))
        elif percent >= 80:
            return wx.Color(240, 128, 128)
        elif percent >= 70:
            return wx.Color(255, 215, 0)
        elif percent >= 60:
            return wx.Color(255, 255, 0)
        elif percent >= 50:
            return wx.Color(238, 221, 130)
        elif percent >= 40:
            return wx.Color(154,205,50)
        elif percent >= 30:
            return wx.Color(173, 255, 47)
        elif percent >= 20:
            return wx.Color(135, 206, 250)
        elif percent >= 10:
            return wx.Color(176, 196, 222)
        else:
            return wx.Color(217, 217, 217)
        """

class WindowHolder(wx.Frame):
    def __init__(self, prnt, EmailsDict, EmailsInfoDict, CentralID=""):
		# First, call the base class' __init__ method to create the frame
        wx.Frame.__init__(self, id=wx.NewId(), name='emailMapFrame', parent=prnt,
            pos=wx.Point(0, 0), size=wx.Size(1280, 1024),
            style=wx.DEFAULT_FRAME_STYLE, title="Email - Social Network")
              
        #self.SetClientSize(wx.Size(1280, 1024))
        #self.SetScrollbars(50, 50, 1280/10, 1024/10, 48, 42)
        # This creates some pens and brushes that the OGL library uses.
        # It should be called after the app object has been created, but
        # before OGL is used.
        #self.SetVirtualSize((680, 560))
        #self.SetIcon(wx.Icon('./Images/FNSFIcon.ico',wx.BITMAP_TYPE_ICO))
        
        self.SetIcon(images.getMAKE2Icon())
        self.Maximize(True)
        ogl.OGLInitialize()
        #self.EmailsDict = {}
        #emails['b@nmt.edu'] = {'Name': 'Mr. B B', 'c@nmt.edu':{'Emails': 15}}
        #self.EmailRE = re.compile('([\W]*)([A-Z0-9._%-]+@[A-Z0-9._%-]+\.[A-Z]+)([\W]*)', re.I)            
        #print Globals.EmailsDict
        #print Globals.AddressBookDict
        """
        self.EmailsDict['rambasnet@nmt.edu'] = {'rbasnet@nmt.edu':{'Emails': 1}}
        self.EmailsDict['rambasnet@nmt.edu']['rambasnet@hotmail.com'] = {'Emails': 2}
        self.EmailsDict['rbasnet@nmt.edu'] = {'rambasnet@nmt.edu': {'Emails': 1}}
        self.EmailsDict['rambasnet@hotmail.com'] = {}
        """
        """
        self.totalShapes = 0
        self.CentralID = 'montoya_y@aps.edu'
        self.CentralID = self.CentralID.lower() 
        self.shapesToDraw = self.OrderedEmailDict[self.CentralID]
        self.totalShapes = len(self.shapesToDraw)
               
        self.XGap = 40
        self.YGap = 20
        self.rectHeight = 25
        self.rectWidth = 100
        self.ellipseWidth = 170
        self.ellipseHeight = 40
        sqrtValue = int(math.sqrt(self.totalShapes)+1)
        self.maxWidth = sqrtValue*self.rectWidth + sqrtValue*self.XGap
        self.maxHeight = sqrtValue*self.rectWidth + sqrtValue*self.YGap
        #self.SetClientSize(wx.Size(self.maxWidth, self.maxHeight))
        #SetScrollbars(self, int pixelsPerUnitX, int pixelsPerUnitY, int noUnitsX, 
        #   int noUnitsY, int xPos=0, int yPos=0, bool noRefresh=False)
        virtualWidth = self.maxWidth/20
        virtualHeight = self.maxHeight/20
        xScrollPos = 20*virtualWidth/2
        yScrollPos = 20*virtualHeight/2
        self.SetVirtualSize(wx.Size(self.maxWidth, self.maxHeight))
        print "frame's virutal size = ", self.GetVirtualSize()
        #self.SetScrollbars(20, 20, virtualWidth, virtualHeight, xScrollPos, yScrollPos)
        """
        
        self.CentralID = CentralID
        #self.EmailsInfoDict = EmailsInfoDict
        if self.CentralID:
            self.OrderedEmailDict = EmailsDict
            self.emailMap = EmailMapWindow(self, self.OrderedEmailDict, EmailsInfoDict, self.CentralID)


            

    
# Every wxWidgets application must have a class derived from wx.App
class MyApp(wx.App):

	# wxWindows calls this method to initialize the application
	def OnInit(self):

		# Create an instance of our customized Frame class
		frame = WindowHolder(None, -1, "Email Map Viewer")
		frame.Show(True)

		# Tell wxWindows that this is our main window
		self.SetTopWindow(frame)

		# Return a success flag
		return True


if __name__ == "__main__":
    app = MyApp(0)	# Create an instance of the application class
    app.MainLoop()	# Tell it to start processing events
    

    


