#-----------------------------------------------------------------------------
# Name:        DirectoryTreeView.py
# Purpose:     
#
# Author:      Ram Basnet
#
# Created:     2007/11/01
# RCS-ID:      $Id: ImageDirectoryTreeView.py,v 1.3 2008/03/12 04:04:03 rbasnet Exp $
# Copyright:   (c) 2007
# Licence:     All Rights Reserved.
# New field:   Whatever
#-----------------------------------------------------------------------------
import Globals
import wx
import PlatformMethods
import os.path
from SqliteDatabase import *

import time
import CommonFunctions
import cPickle
import Constants
import DBFunctions

class ImageDirectoryTreeView:
    def __init__(self, parentWin, treeCtrl, EvidencesDict):
        self.parentWindow = parentWin
        self.treeDirList = treeCtrl
        #self.evidenceName = evidenceName
        #self.evidencePath = evidencePath
        self.EvidencesDict = EvidencesDict
        #self.ImagesDict = ImagesDict
        # Create an image list
        dirIL = wx.ImageList(16,16, True)
        
        # Get some standard images from the art provider and add them
        # to the image list
        self.fldridx = dirIL.Add(
            wx.ArtProvider.GetBitmap(wx.ART_FOLDER, 
                wx.ART_OTHER, (16,16)))
                
        self.fldropenidx = dirIL.Add(
            wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN,   
                wx.ART_OTHER, (16,16)))
        #Give the tree the image list
        self.treeDirList.AssignImageList(dirIL)
        #self.SetTreeButtons()
        #self.UpdateDirectoryList()
        #self.AddDirectories()
      
        
    def SetTreeButtons(self):

        bitmap_plus = PlatformMethods.ConvertFilePath("Images/Bitmaps/plus4.ico")
        bitmap_minus = PlatformMethods.ConvertFilePath("Images/Bitmaps/minus4.ico")
        
        bitmap = wx.Bitmap(bitmap_plus, wx.BITMAP_TYPE_ICO)
        width = bitmap.GetWidth()
        
        il = wx.ImageList(width, width)
        
        il.Add(wx.Bitmap(bitmap_plus, wx.BITMAP_TYPE_ICO))
        #il.Add(wx.Bitmap(bitmap_plus, wx.BITMAP_TYPE_ICO))
        il.Add(wx.Bitmap(bitmap_minus, wx.BITMAP_TYPE_ICO))
        #il.Add(wx.Bitmap(bitmap_minus, wx.BITMAP_TYPE_ICO))

        self.buttonsIL = il                
        #self.treeDirList.SetButtonsImageList(il)
        self.treeDirList.AssignButtonsImageList(il)
      
    def GetParentItem(self, parentName):
        parentItem = self.treeDirList.GetFirstChild(self.root)[0]
        while parentItem:
            if self.GetItemText(parentItem) == parentName:
                return parentItem
            parentItem = self.treeDirList.GetNextSibling(parentItem)
        return parentItem
    
    
    def AddDirectoryTreeNode(self, dirPath):
        dirList = dirPath.split(PlatformMethods.GetDirSeparator())
        #print dirList
        parentItem = self.myRoot
        if dirList[0]:
            childrenDirList = dirList[1:]
        else:
            childrenDirList = dirList[2:]
            
        for dirName in dirList:
            if not dirName:
                continue
            #always start from directories in the drive e.g. C:\NMT\Research\AJAX
            #dirName = dirList[i]
            #if self.EvidencesDict[evidenceID]['NewLocation']:
                #print 'new', self.EvidencesDict[evidenceID]['NewLocation']
             #   dirName = self.EvidencesDict[evidenceID]['NewLocation']
            siblingItem = self.GetSiblingItem(parentItem, dirName)
            #no directory with that name found in this level, so add it
            if not siblingItem:
                if parentItem == self.myRoot:
                    #add drive and image
                    siblingItem = self.treeDirList.AppendItem(parentItem, dirName)
                    self.treeDirList.SetItemImage(siblingItem, self.fldridx, wx.TreeItemIcon_Normal)
                    self.treeDirList.SetItemImage(siblingItem, self.fldropenidx,
                               wx.TreeItemIcon_Expanded)
                else:
                    siblingItem = self.treeDirList.AppendItem(parentItem, dirName)
                    self.treeDirList.SetItemImage(siblingItem, self.fldridx, wx.TreeItemIcon_Normal)
                    self.treeDirList.SetItemImage(siblingItem, self.fldropenidx,
                               wx.TreeItemIcon_Expanded)
                self.AddSubDirectories(siblingItem, childrenDirList)
                break
            else:
                childrenDirList = childrenDirList[1:]
                parentItem = siblingItem
                
        self.treeDirList.SortChildren(parentItem)
                
    
    #dir List without drive
    def AddSubDirectories(self, parentItem, childrenDirList):
        for dirName in childrenDirList:
            #Insert new node as parent Item
            parentItem = self.treeDirList.AppendItem(parentItem, dirName)
            self.treeDirList.SetItemImage(parentItem, self.fldridx, wx.TreeItemIcon_Normal)
            self.treeDirList.SetItemImage(parentItem, self.fldropenidx,
                               wx.TreeItemIcon_Expanded)
                    
    
    def GetSiblingItem(self, parentItem, dirName):
        siblingItem = self.treeDirList.GetFirstChild(parentItem)[0]
        while siblingItem:
            if self.GetTreeItemText(siblingItem) == dirName:
                break
            siblingItem = self.treeDirList.GetNextSibling(siblingItem)
        return siblingItem


    
    def AddDirectories(self):
        self.treeDirList.DeleteAllItems()
        #tbd: add image for the root
        self.root = self.treeDirList.AddRoot("Case - Evidences")
        self.treeDirList.SetItemImage(self.root, self.fldridx, wx.TreeItemIcon_Normal)
        self.treeDirList.SetItemImage(self.root, self.fldropenidx, wx.TreeItemIcon_Expanded)
        #parentName = "Case"
        #parentItem = self.root
        #currentName = ""
        #currentItem = None
        #grandParentItem = None
        #self.evidencePath = 'C:\\NMT\\Research\\ForensicsTool\\Montoya'
        
        for evidenceID in self.EvidencesDict:
            #print 'evidenceID = ', evidenceID
            self.db = SqliteDatabase(Globals.FileSystemName)
            if not self.db.OpenConnection():
                return
            
            self.query = "select distinct DirPath from %s where Category='image';"%(evidenceID)
            location = self.EvidencesDict[evidenceID]['Location']
            newLocation = location
            
            if self.EvidencesDict[evidenceID]['NewLocation']:
                #print 'new', self.EvidencesDict[evidenceID]['NewLocation']
                newLocation = self.EvidencesDict[evidenceID]['NewLocation']
                
            self.myRoot = self.treeDirList.AppendItem(self.root, newLocation)
            self.treeDirList.SetItemImage(self.myRoot, self.fldridx, wx.TreeItemIcon_Normal)
            self.treeDirList.SetItemImage(self.myRoot, self.fldropenidx, wx.TreeItemIcon_Expanded)
            #self.AddChildrenNodes(self.myRoot, self.DirDict[key]['children'])
            #self.myParentItem = self.myRoot
            #subDirs = self.EvidencesDict[evidenceID]['DirTree'][location]
            rows = self.db.FetchAllRows(self.query)
            self.db.CloseConnection()
            #self.root = self.treeDirList.AddRoot("Folders (" + str(Globals.CurrentProject.TotalDirectories) + ")")
            #fullDirPath = Globals.DirectoryList[0]
            #fullPathList = fullDirPath.split(PlatformMethods.GetDirSeparator())
            
            for row in rows:
                self.AddDirectoryTreeNode(row[0].replace(location, ""))
                            
            #self.treeDirList.SortChildren(self.root)
            self.treeDirList.Expand(self.root)
            
            return self.root
    
    def GetTreeItemText(self, item):
        if item:
            return self.treeDirList.GetItemText(item)
        else:
            return ""
          
     
    def AddDirectoriesOld(self):
        """
        for key in self.EvidencesDict:
            #location = self.EvidencesDict[evidenceID]['Location']
            for subkey in self.EvidencesDict[key]['DirTree']:
                print subkey, " ", self.EvidencesDict[key]['DirTree'][subkey]
        
        
        
        for adir in self.ImagesDict['Evidence1']:
            print adir
            
        """
            
        """
        print rootDir
        for dir in DirectoryDict[rootDir]['children']:
        dirPath = join(rootDir, dir)
        print rootDir, ' child ', dir
        GetSubDirs(dirPath)
        """
        self.treeDirList.DeleteAllItems()
        #tbd: add image for the root
        self.root = self.treeDirList.AddRoot("Case - Evidences")
        self.treeDirList.SetItemImage(self.root, self.fldridx, wx.TreeItemIcon_Normal)
        self.treeDirList.SetItemImage(self.root, self.fldropenidx, wx.TreeItemIcon_Expanded)
        #parentName = "Case"
        #parentItem = self.root
        #currentName = ""
        #currentItem = None
        #grandParentItem = None
        #self.evidencePath = 'C:\\NMT\\Research\\ForensicsTool\\Montoya'
        
        for evidenceID in self.EvidencesDict:
            #print 'evidenceID = ', evidenceID
            location = self.EvidencesDict[evidenceID]['Location']
            self.myRoot = self.treeDirList.AppendItem(self.root, location)
            self.treeDirList.SetItemImage(self.myRoot, self.fldridx, wx.TreeItemIcon_Normal)
            self.treeDirList.SetItemImage(self.myRoot, self.fldropenidx, wx.TreeItemIcon_Expanded)
            #self.AddChildrenNodes(self.myRoot, self.DirDict[key]['children'])
            #self.myParentItem = self.myRoot
            subDirs = self.EvidencesDict[evidenceID]['DirTree'][location]
            for dirName in subDirs:
                #print 'dirName = ', dirName
                #for adir in subDirs
                newPath = os.path.join(location, dirName)
                if self.ImagesDict[evidenceID].has_key(newPath):
                    #print '%s has images in %s'%(dirName, newPath)
                    myItem = self.treeDirList.AppendItem(self.myRoot, dirName)
                    self.treeDirList.SetItemImage(myItem, self.fldridx, wx.TreeItemIcon_Normal)
                    self.treeDirList.SetItemImage(myItem, self.fldropenidx, wx.TreeItemIcon_Expanded)
                    self.AddSubDirs(evidenceID, myItem, newPath)
               
                else:
                    if self.CheckSubDirsHasImage(evidenceID, newPath):
                        myItem = self.treeDirList.AppendItem(self.myRoot, dirName)
                        self.treeDirList.SetItemImage(myItem, self.fldridx, wx.TreeItemIcon_Normal)
                        self.treeDirList.SetItemImage(myItem, self.fldropenidx, wx.TreeItemIcon_Expanded)
                        self.AddSubDirs(evidenceID, myItem, newPath)
                        
                """
                elif self.EvidencesDict[evidenceID]['DirTree'].has_key(newPath):
                    subDirs = self.EvidencesDict[evidenceID]['DirTree'][dirPath]
                """
                
        #self.treeDirList.SortChildren(self.root)
        self.treeDirList.Expand(self.root)
        return self.root
        
  
        

class TestWindow(wx.Frame):
    def __init__(self, prnt):
		# First, call the base class' __init__ method to create the frame
        wx.Frame.__init__(self, id=-1, name='', parent=prnt,
            pos=wx.Point(0, 0), size=wx.Size(600, 600),
            style=wx.DEFAULT_FRAME_STYLE, title="Dir tree view")

        self.panViewFolders = wx.Panel(id=-1,
              name='panViewFolders', parent=self, pos=wx.Point(8, 176),
              size=wx.Size(500, 500), style=wx.TAB_TRAVERSAL)
        self.panViewFolders.SetBackgroundColour(wx.Colour(225, 236, 255))
        #self.panViewFolders.SetAutoLayout(True)
        
        self.treeViewFolders = wx.TreeCtrl(id=wx.NewId(), name='treeViewFolders', parent=self.panViewFolders,
            pos=wx.Point(0, 0), size=wx.Size(600, 600),
            style=wx.HSCROLL | wx.VSCROLL | wx.TR_HAS_BUTTONS)
        
        
        self.DirectoryDict = {}
        """
        print "start walking at ", time.ctime()
        startTime = time.time()
        self.WalkDir()
        
        print "end walking at ", time.ctime()
        
        endTime = time.time()
        print "Time taken to walk ", CommonFunctions.ConvertSecondsToDayHourMinSec(endTime - startTime)
        
        startTime = time.time()
        #save in db
   
        DBFunctions.SetupProjectEvidencesTable("caseNew.cfi", True)
        db = SqliteDatabase("caseNew.cfi")
        if db.OpenConnection():
            query = "insert into " + Constants.ProjectEvidencesTable + " (ID, DisplayName, Location, DirTree) values (?, ?, ?, ?)"
            db.ExecuteMany(query, [(1, self.evidenceName, self.evidencePath, cPickle.dumps(self.DirectoryDict[self.evidenceName]))] )
            db.CloseConnection()
        endTime = time.time()
        
        print "Time taken to add in db ", CommonFunctions.ConvertSecondsToDayHourMinSec(endTime - startTime)
        """
        
        print 'start time load ', time.ctime()
        startTime = time.time()
        db = SqliteDatabase("caseNew.cfi")
        if db.OpenConnection():
            query = "select Location, DisplayName, DirTree from " + Constants.EvidencesTable;
            row = db.FetchOneRow(query)
            self.evidencePath = row[0]
            self.evidenceName = row[1]
            self.DirectoryDict = cPickle.loads(str(row[2]))
            
        print "end time ", time.ctime()
        endTime = time.time()
        print "Time taken to load db ", CommonFunctions.ConvertSecondsToDayHourMinSec(endTime - startTime)
        
        print "start build tree time ", time.ctime()
        startTime = time.time()
        self.treeDir = DirectoryTreeView(self, self.treeViewFolders, self.DirectoryDict, self.evidenceName, self.evidencePath) 
        print "end build tree time ", time.ctime()
        endTime = time.time()
        print "Time taken ", CommonFunctions.ConvertSecondsToDayHourMinSec(endTime - startTime)
        

    def WalkDir(self):
        import os
        #from os.path import join
        i = 1
        #DirList = []
        self.evidenceName = 'Evdi1'
        self.evidencePath = 'C:\\'
        self.DirectoryDict[self.evidenceName] = {}
        
        for root, dirs, files in os.walk(self.evidencePath):
            #print root
            #DirList.append(root)
            #DirList.append(dirs)
            if len(dirs) > 0:
                self.DirectoryDict[self.evidenceName][root] = {'children':dirs}
            #i += 1
            #print dirs
            #print files
            
            """
            print sum([getsize(join(root, name)) for name in files]),
            print "bytes in", len(files), "non-directory files"
            if 'CVS' in dirs:
                dirs.remove('CVS')  # don't visit CVS directories
            """
        #print DirectoryDict
        

if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = TestWindow(None)
    frame.Show(True)
    app.MainLoop()
    

