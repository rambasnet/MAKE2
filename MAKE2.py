#!/usr/bin/env python
#Boa:App:BoaApp

import wx

import MDIMainFrame
import Globals

modules ={'MDIMainFrame': [1, 'Main frame of Application', 'MDIMainFrame.py']}

class BoaApp(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        #self.main = MDIMainFrame.create(None)
        Globals.frmGlobalMainForm = MDIMainFrame.create(None)
        #self.main.Show()
        Globals.frmGlobalMainForm.Show()
        #self.SetTopWindow(self.main)
        self.SetTopWindow(Globals.frmGlobalMainForm)
        #Setup.SetupDB()
        #Setup.LoadSetupSettings()
        #Setup.CreateReportFolders()
        return True

def main():
    application = BoaApp(0)
    application.MainLoop()

if __name__ == '__main__':
    main()