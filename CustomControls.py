#-----------------------------------------------------------------------------
# Name:        CustomControls.py
# Purpose:     
#
# Author:      Ram Basnet
#
# Created:     2007/11/12
# RCS-ID:      $Id: CustomControls.py,v 1.2 2007/11/13 19:52:48 rbasnet Exp $
# Copyright:   (c) 2006
# Licence:     <your licence>
# New field:   Whatever
#-----------------------------------------------------------------------------
import wx
import  wx.lib.mixins.listctrl  as  listmix

class CustomListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        
class DragShape:
    def __init__(self, bmp, ID=""):
        self.bmp = bmp
        self.ID = ID
        self.pos = (0,0)
        self.shown = True
        self.text = None
        self.fullscreen = True

    def HitTest(self, pt):
        rect = self.GetRect()
        return rect.InsideXY(pt.x, pt.y)
    
    def GetPosition(self):
        return self.pos

    def GetRect(self):
        return wx.Rect(self.pos[0], self.pos[1],
                      self.bmp.GetWidth(), self.bmp.GetHeight())

    def Draw(self, dc, op = wx.COPY):
        if self.bmp.Ok():
            memDC = wx.MemoryDC()
            memDC.SelectObject(self.bmp)

            dc.Blit(self.pos[0], self.pos[1],
                    self.bmp.GetWidth(), self.bmp.GetHeight(),
                    memDC, 0, 0, op, True)

            return True
        else:
            return False
