import wx
import util
import hexedit
from wx.lib.anchors import LayoutAnchors

#constants for the hex view
EDIT_BYTES        = 1
EDIT_NIBBLE_LOW   = 2
EDIT_NIBBLE_HIGH  = 4
EDIT_NIBBLES      = 6   #mask

#key to hex nibble translation table
hex2bin = {
    ord('0'): 0,
    ord('1'): 1,
    ord('2'): 2,
    ord('3'): 3,
    ord('4'): 4,
    ord('5'): 5,
    ord('6'): 6,
    ord('7'): 7,
    ord('8'): 8,
    ord('9'): 9,
    ord('a'): 10, ord('A'): 10,
    ord('b'): 11, ord('B'): 11,
    ord('c'): 12, ord('C'): 12,
    ord('d'): 13, ord('D'): 13,
    ord('e'): 14, ord('E'): 14,
    ord('f'): 15, ord('F'): 15,
}

    
class TextViewWindow(wx.ScrolledWindow, util.Subject):
    
    def __init__(self, parent, lblStatus, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize):
                
        wx.ScrolledWindow.__init__(self, parent, id, pos=pos, size=size)
        
        self.lblStatus = lblStatus
        
        util.Subject.__init__(self)
        self.EnableScrolling(True, True)
        self.InitFont()
        self.MapEvents()
        self.model              = None
        self.lines              = 0
        #~ self.model.attach(self)
        
        self.color_text         = wx.NamedColour('black')
        self.color_background   = wx.NamedColour('white')
        #self.color_mark         = wx.NamedColour('blue')
        self.color_mark = wx.Colour(225, 236, 255)
        self.color_cursor       = wx.NamedColour('red')
        self.color_lines        = wx.NamedColour('navy')
        self.color_lines_weak   = wx.NamedColour('light blue')
        self.color_bookmark     = wx.NamedColour('red')
        
        self.sx                 = 0L
        self.sy                 = 0L
        
        self.offset             = 0L
        self.editmode           = EDIT_NIBBLE_HIGH
        self.reload             = True
        
        self.selection_start    = None
        self.selection_end      = None
        self.leftdragging       = False
        self.redo_list          = []
        self._mouse_lastoffset  = None
        
        self.formater = hexedit.TextFormater()
        self.address_end, self.hex_start, self.hex_end, self.ascii_start, self.ascii_end = self.formater.getPositions()
        #self.bookmarks = Bookmarks()
        self.OnSize(None)       #init double buffering

    def MapEvents(self):
        wx.EVT_SCROLLWIN(self,  self.OnScroll)
        wx.EVT_PAINT(self,      self.OnPaint)
        wx.EVT_SIZE(self,       self.OnSize)
        wx.EVT_ERASE_BACKGROUND(self, self.OnEraseBackground)
        wx.EVT_LEFT_DOWN(self,  self.OnMouseButtonEvent)
        wx.EVT_LEFT_UP(self,    self.OnMouseButtonEvent)
        wx.EVT_MOTION(self,     self.OnMouseButtonEvent)
        wx.EVT_CHAR(self,       self.OnChar)

    def setModel(self, model):
        """change model"""
        if self.model is not None:
            self.model.detatch(self)
        self.model = model
        self.model.attach(self)
        self.reset()
        self.update()

    def UpdateView(self, dc = None):
        if dc is None:
            cdc = wx.ClientDC(self)
            dc = wx.BufferedDC(cdc, self.bmp)
            #~ dc = wx.MemoryDC()
            #~ dc.SelectObject(self.bmp)
        if dc.Ok():
            if self.model is not None:
                self.draw(dc)
                #~ self.Refresh()

    def OnPaint(self, event):
        #~ print "OnPaint"
        #would be nice, but does bad scrolling :-(
        #~ dc = wx.BufferedPaintDC(self, self.bmp)
        #update display w/o scrolling of the virtual area
        dc = wx.PaintDC(self)
        xy = wx.Point(0,0)
        dc.DrawBitmapPoint(self.bmp, xy, False)

    def OnEraseBackground(self, evt):
        pass

    def OnSize(self, event):
        """called on window resize, also used to init double buffering"""
        self.bw, self.bh = self.GetClientSizeTuple()
        self.bmp = wx.EmptyBitmap(max(1,self.bw), max(1,self.bh))
        if self.model is not None:
            self.update()       #calls AdjustScrollbars, UpdateView, etc
        else:
            self.AdjustScrollbars()

    def InitFont(self, font=None):
        dc = wx.ClientDC(self)
        if font is None:
            self.font = self.NiceFontForPlatform()
        else:
            self.font = font
        dc.SetFont(self.font)
        self.fw = dc.GetCharWidth()
        self.fh = dc.GetCharHeight()

    def NiceFontForPlatform(self):
        if wx.Platform == "__WXMSW__":
            return wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL)
        else:
            return wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False)

    def SetCharDimensions(self):
        self.sh = self.bh / self.fh
        self.sw = (self.bw / self.fw) - 1

    def OnScroll(self, event):
        #~ print "OnScroll", self.sy, self.lines
        eventType = event.GetEventType()
        if   eventType == wx.wxEVT_SCROLLWIN_LINEUP:
            self.sy -= 1
        elif eventType == wx.wxEVT_SCROLLWIN_LINEDOWN:
            self.sy += 1
        elif eventType == wx.wxEVT_SCROLLWIN_PAGEUP:
            self.sy -= self.sh
        elif eventType == wx.wxEVT_SCROLLWIN_PAGEDOWN:
            self.sy += self.sh
        #~ elif eventType == wx.wxEVT_SCROLLWIN_TOP:
            #~ self.sy = 0
        #~ elif eventType == wx.wxEVT_SCROLLWIN_BOTTOM:
            #~ self.sy = self.lines - self.sh
        else:
            self.sy = event.GetPosition()
            
        self.sy = max(0, min(self.sy, self.lines - self.sh))
        #~ self.offset = self.sy*16 + (self.offset % 16)
        self.reload = True
        self.AdjustScrollbars()
        self.UpdateView()

    def AdjustScrollbars(self):
        self.SetCharDimensions()
        self.sy = max(0, min(self.sy, self.lines - self.sh))
        if self.lines < 2**25:      #hide scollbars after a certain size
            self.SetScrollbars(self.fw, self.fh,
                               self.sw, self.lines+1,       #XXX +1 HACK
                               #~ self.sw, self.lines,
                               self.sx, self.sy)
        else:
            self.SetScrollbars(self.fw, self.fh,
                               self.sw, 0,
                               self.sx, 0)

    def getLine(self, line):
        """cache formated lines for faster screen updates"""
        try:
            return self.linecache[line]
        except KeyError:
            offset = line*self.formater.width
            #self.linecache[line] = self.formater.format(offset, self.model.bin.read(offset, self.formater.width))
            self.linecache[line] = self.model.bin.read(offset, self.formater.width)
            #self.UpdateLinecache(line, lines)
            
        return self.linecache[line]

    def UpdateLinecache(self, curLine, lineList):
        for line in lineList:
            #range(curLine, curLine+len(lineList)):
            self.linecache[curLine] = line
            curLine += 1
            
        
    #~ _draw = 0
    def draw(self, dc):
        #~ print "draw %d" % self._draw, self.reload; self._draw += 1
        if self.reload == True:
            self.linecache = {}
            self.reload = False
        dc.BeginDrawing()
        dc.SetFont(self.font)
        dc.SetBackgroundMode(wx.SOLID)
        dc.SetBackground(wx.Brush(self.color_background))
        dc.SetTextForeground(self.color_text)
        dc.Clear()
        
        #numbers
        linewidth       = self.formater.width
        visible_start   = self.sy*linewidth
        visible_end     = (self.sy + self.sh)*linewidth
        
        #selection
        if self.selection_start is not None and self.selection_end is not None:
            if self.selection_start > self.selection_end: #swap if start > end
                selection_start, selection_end = self.selection_end, self.selection_start
            else:
                selection_start, selection_end = self.selection_start, self.selection_end
            
            dc.SetPen(wx.Pen(self.color_mark, 1))
            dc.SetBrush(wx.Brush(self.color_mark))
            
            
            #start to end of mark/end of line
            if visible_start <= selection_start < visible_end:
                xb, xa, y = self._offset2XXY(selection_start)
                width = min(selection_end - selection_start, (linewidth-1) - selection_start % linewidth)
                #dc.DrawRectangle(xb, y, self.fw*width, self.fh)
                dc.DrawRectangle(xa, y, self.fw*(1 + width), self.fh)
            
            
            #end to start of mark or start of line
            if visible_start <= selection_end < visible_end:
                xb, xa, y = self._offset2XXY(selection_end)
                width = min(selection_end - selection_start, selection_end % linewidth)
                #dc.DrawRectangle(xb-self.fw*width, max(0, y), self.fw*width, self.fh)
                dc.DrawRectangle(xa-self.fw*width, max(0, y), self.fw*(width + 1), self.fh)
            
            
            #whole lines in between
            sel_startline = max(0, selection_start / linewidth - self.sy + 1)
            sel_endline   = max(0, min(self.sh, selection_end / linewidth - self.sy))
            visible_lines = sel_endline - sel_startline
            if visible_lines:
                #xb = self.fw*self.hex_start
                xa = self.fw*self.ascii_start
                wb = self.fw*(linewidth - 1)
                wa = self.fw*linewidth
                y  = sel_startline * self.fh
                for i in range(visible_lines):
                    #dc.DrawRectangle(xb, y, wb, self.fh)
                    dc.DrawRectangle(xa, y, wa, self.fh)
                    y += self.fh

        dc.SetBackgroundMode(wx.TRANSPARENT)
        y = 0
        for line in range(self.sy, min(self.sy + self.sh, self.lines)):
            #hack...needs to be decoded as latin-1, gives error UnicodeDecodeError otherwise...
            try:
                dc.DrawText(self.getLine(line).decode('latin-1'), 0, y)
            except:
                pass
            
            y += self.fh
        
        dc.EndDrawing()

 
    def _offset2XXY(self, offset):
        """offset to character coordinates, hex and ascii dump x offsets"""
        d, m = divmod(offset, self.formater.width)
        return (self.fw * (m * 3 + self.hex_start),
                self.fw * (m + self.ascii_start), #-1
                self.fh * (d - self.sy))
 

    def OnMouseButtonEvent(self, event):
        """mouse events, handle selection, clicks"""
        fullline = False
        update = False
        x, y = event.GetX(), event.GetY()
        line = (y / self.fh + self.sy)
        offset = offset_line = line * self.formater.width #calculate offset of fist char in line, x handled below
        xchar = x / self.fw
        """
        if xchar < self.hex_start:              #address area
            fullline = True
            editmode = EDIT_NIBBLE_HIGH
        elif xchar < self.hex_end:              #hex area
            offset += (xchar - self.hex_start) / 3
            if ((xchar - self.hex_start) % 3 < 1) or fullline:
                editmode = EDIT_NIBBLE_HIGH
            else:
                editmode = EDIT_NIBBLE_LOW
        """
        if xchar < self.ascii_start:          #between hex and ascii area
            fullline = True
            editmode = EDIT_BYTES
        elif xchar < self.ascii_end:            #ascii area
            offset += xchar - self.ascii_start
            editmode = EDIT_BYTES
        else:                                   #right of ascii area
            fullline = True
            editmode = EDIT_BYTES
        
        size = max(0, self.model.size() - 1)
        offset = util.limit(0, size, offset)
        
        if event.LeftDown():
            self.CaptureMouse()
            self.leftdragging = True
            if fullline:
                offset = util.limit(0, size, offset_line + self.formater.width - 1)
                self.selection_start = offset_line
            else:
                self.selection_start = offset
            self.selection_end = self.offset = offset
            update = True
        elif event.Dragging() and self.leftdragging:
            if fullline:
                offset = util.limit(0, size, offset_line + self.formater.width - 1)
            if self._mouse_lastoffset != offset:
                self.selection_end = self.offset = offset
                update = True
        elif event.LeftUp():
            if self.leftdragging:
                self.ReleaseMouse()
                self.leftdragging = False
            if fullline:
                offset = util.limit(0, size, offset_line + self.formater.width - 1)
            if self.leftdragging:
                if self.selection_end != offset:
                    self.selection_end = offset
                    update = True
        
        if update:
            self.editmode = editmode
            self.ensureVisible()
        
        self._mouse_lastoffset = offset
    
    def OnChar(self, event):
        """key events, input and movements"""
        move = False
        update = False
        update_selection_end = False
        keycode = event.GetKeyCode()
        #controls
        if keycode == 0x08:                     #backspace
            self.offset -= 1
            update = True
        elif keycode == 0x1b:                   #ESC ->toggle hex/ascii edit
            if self.editmode == EDIT_BYTES:
                self.editmode = EDIT_NIBBLE_HIGH
            else:
                self.editmode = EDIT_BYTES
            self.ensureVisible()
        elif keycode == 127:                    #DELETE
            pass
            #~ self.model.bin.write(self.offset, '\0')
        elif 32 <= keycode < 256:               #ascii text
            #~ print "Key %d: %c" % (keycode, keycode)
            #hex edit mode
            if self.editmode & EDIT_NIBBLES:
                if keycode == 0x20: #space -> swap nibbles
                    if self.editmode == EDIT_NIBBLE_HIGH:
                        self.editmode = EDIT_NIBBLE_LOW
                    else:
                        self.editmode = EDIT_NIBBLE_HIGH
                    update = True
                else:
                    if self.model.isReadonly():
                        wx.Bell()       #TODO dialog box?
                    else:
                        try:
                            value = hex2bin[keycode]
                        except KeyError:
                            #~ print "not a hex character"     #XXX DEBUG
                            event.Skip()
                        else:
                            if self.editmode == EDIT_NIBBLE_HIGH:
                                value = (value << 4) | (ord(self.model.bin.read(self.offset, 1)) & 0x0f)
                                self.editmode = EDIT_NIBBLE_LOW
                                self.model.bin.write(self.offset, chr(value))
                            else:
                                value = value | (ord(self.model.bin.read(self.offset, 1)) & 0xf0)
                                self.editmode = EDIT_NIBBLE_HIGH
                                self.model.bin.write(self.offset, chr(value))
                                self.offset += 1
                            del self.redo_list[:]
                            update = True
            #ascii edit mode
            elif self.editmode == EDIT_BYTES:
                if self.model.isReadonly():
                    wx.Bell()       #TODO dialog box?
                else:
                    self.model.bin.write(self.offset, chr(keycode))
                    del self.redo_list[:]
                    self.offset += 1
                    update = True
        else:   #special keys
            if keycode == wx.WXK_RIGHT:
                self.offset += 1
                move = True
                if event.ShiftDown():
                    update_selection_end = True
            elif keycode == wx.WXK_LEFT:
                self.offset -= 1
                move = True
                if event.ShiftDown():
                    update_selection_end = True
            elif keycode == wx.WXK_DOWN:
                self.offset += self.formater.width
                move = True
                if event.ShiftDown():
                    update_selection_end = True
            elif keycode == wx.WXK_UP:
                self.offset -= self.formater.width
                move = True
                if event.ShiftDown():
                    update_selection_end = True
            elif keycode == wx.WXK_NEXT:
                self.offset += self.sh*self.formater.width
                move = True
                if event.ShiftDown():
                    update_selection_end = True
            elif keycode == wx.WXK_PRIOR:
                self.offset -= self.sh*self.formater.width
                move = True
                if event.ShiftDown():
                    update_selection_end = True
            elif keycode == wx.WXK_HOME:
                if event.ControlDown():
                    self.offset = 0L
                else:
                    self.offset -= self.offset % self.formater.width
                move = True
                if event.ShiftDown():
                    update_selection_end = True
            elif keycode == wx.WXK_END:
                if event.ControlDown():
                    self.offset = long(self.model.size())
                else:
                    self.offset += (self.formater.width - 1) - (self.offset % self.formater.width)
                move = True
                if event.ShiftDown():
                    update_selection_end = True
            else:
                print "Key %d s:%s c:%s a:%s m:%s" % (
                    keycode, event.ShiftDown(), event.ControlDown(),
                    event.AltDown(), event.MetaDown()
                )
                event.Skip()
        
        if move or update:      #update screen if needed
            if self.offset < 0:
                self.offset = 0L
            elif self.offset >= self.model.size():
                self.offset = max(0, self.model.size() - 1L)
            
            if move:            #nibble edit: select high nibble after moves
                if self.editmode & EDIT_NIBBLES:
                    self.editmode = EDIT_NIBBLE_HIGH
            
            #update selection with keyboard (shift+movement)?
            if update_selection_end:
                #update selection
                self.selection_end = self.offset
            else:
                #reset selection otherwise
                self.selection_start = self.selection_end = self.offset
            self.ensureVisible()

    def reset(self):
        """reset view, empty"""
        self.sy = self.sx = 0L
        self.offset = 0L
        self.lines = 0L
        self.selection_start = self.selection_end = 0L
        self.reload = True
    
    def ensureVisible(self, offset=None):
        """ensure that the cursor is visible, if offset is given, set cursor on that location"""
        if offset is not None:
            self.offset = offset
            #~ print "ensureVisible(0x%08x)" % (offset)
        #check if cursor is in currently visible area
        visible_start = self.sy * self.formater.width
        visible_end   = min(self.sy + self.sh, self.lines) * self.formater.width
        if visible_start <= self.offset < visible_end:
            pass
        else:
            #scroll to new position, try to place it at 1/3rd of the view
            self.sy = max(0, min(self.offset/self.formater.width - self.sh/3, self.lines))
            self.reload = True
        self.AdjustScrollbars()
        self.UpdateView()
        self.updateStatus()
        self.notify()

    def setSelection(self, start=None, end=None, offset=None):
        """set selection to include the given start and end offset
        if offset is given , move cursor there.
        if end is not given, select a single character, given by start
        if either start not end is given, remove selection
        """
        if start is None:
            start = self.offset
        if end is None:
            end = start
        self.selection_start = start
        self.selection_end = end
        if offset is not None:
            self.ensureVisible(offset)
        else:
            self.update()

    def getSelection(self):
        """get selection as tuple (start,end), ensures that
        start <= end, None if nothing selected."""
        if self.selection_start > self.selection_end:
            return (self.selection_end, self.selection_start)
        else:
            return (self.selection_start, self.selection_end)


    def update(self, subject=None):
        """update view"""
        size = self.model.size()
        if size:
            a, b = divmod(len("%x" % (size - 1)), 4)
            self.formater.address_width = (a + (b != 0))*4
            #print 'fw=%s'%self.fw
            #print '0tuple=%s'%self.GetSizeTuple()[0]
            
            width = self.formater.bestFit(self.GetSizeTuple()[0]/self.fw)
            self.formater.width = width
            #self.formater.width = self.formater.width/self.fw
            #print 'width= %s'%width
            self.address_end, self.hex_start, self.hex_end, self.ascii_start, self.ascii_end = self.formater.getPositions()
            self.lines = self.model.size() / self.formater.width
            if self.model.size() % self.formater.width:
                self.lines += 1
            #print 'lines=%s'%self.lines
            self.sy = max(0L, min(self.lines-self.sh, self.sy))
            #~ self.offset = self.sy*16
        else:
            self.lines = self.sy = 0
            self.formater.address_width = 8
        self.reload = True
        #~ self.AdjustScrollbars()
        #~ self.UpdateView()
        self.ensureVisible()
        

    def updateStatus(self):
        start, end = self.getSelection()
        if start is not None and end is not None:
            selsize = end - start + 1
        else:
            selsize = 0
        self.lblStatus.SetLabel('%d byte%s selected' % (
            selsize, selsize != 1 and 's' or ''))