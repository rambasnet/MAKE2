#-----------------------------------------------------------------------------
# Name:        DirectoryTreeView.py
# Purpose:     
#
# Author:      Ram Basnet
#
# Created:     2007/11/01
# RCS-ID:      $Id: DirectoryTreeView.py,v 1.4 2007/11/23 05:50:14 rbasnet Exp $
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

class DirectoryTreeView:
    def __init__(self, parentWin, treeCtrl, EvidencesDict):
        self.parentWindow = parentWin
        self.treeDirList = treeCtrl
        #self.evidenceName = evidenceName
        #self.evidencePath = evidencePath
        self.EvidencesDict = EvidencesDict
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
        self.AddDirectories()
      
        
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


    def GetTreeItemText(self, item):
        if item:
            return self.treeDirList.GetItemText(item)
        else:
            return ""
        
    

    
    def AddDirectoriesOld1(self):
        self.treeDirList.DeleteAllItems()
        #tbd: add image for the root
        self.root = self.treeDirList.AddRoot("Case - Evidences")
        self.treeDirList.SetItemImage(self.root, self.fldridx, wx.TreeItemIcon_Normal)
        self.treeDirList.SetItemImage(self.root, self.fldropenidx, wx.TreeItemIcon_Expanded)
        
        for evidenceID in self.EvidencesDict:
            #print 'evidenceID = ', evidenceID
            self.db = SqliteDatabase(Globals.FileSystemName)
            if not self.db.OpenConnection():
                return
            
            self.query = "select DirPath, SubDirList from %s%s order by DirPath"%(evidenceID, Constants.DirListTable)
            location = self.EvidencesDict[evidenceID]['Location']
            self.myRoot = self.treeDirList.AppendItem(self.root, location)
            self.treeDirList.SetItemImage(self.myRoot, self.fldridx, wx.TreeItemIcon_Normal)
            self.treeDirList.SetItemImage(self.myRoot, self.fldropenidx, wx.TreeItemIcon_Expanded)
            rows = self.db.FetchAllRows(self.query)
            
            #self.root = self.treeDirList.AddRoot("Folders (" + str(Globals.CurrentProject.TotalDirectories) + ")")
            #fullDirPath = Globals.DirectoryList[0]
            #fullPathList = fullDirPath.split(PlatformMethods.GetDirSeparator())
            
            for row in rows:
                self.AddDirectoryTreeNode(row[0].replace(location, ""))
                            
            #self.treeDirList.SortChildren(self.root)
            self.treeDirList.Expand(self.root)
       
            return self.root
        
    
    def AddSubDirsOld(self, evidenceID, parentItem, dirPath):
        rows = self.db.FetchAllRows(self.query+self.db.SqlSQuote(dirPath))
        for row in rows:
            #subDirs = 
            #print subDirs
            #if self.EvidencesDict[evidenceID]['DirTree'].has_key(dirPath):
            #subDirs = self.EvidencesDict[evidenceID]['DirTree'][dirPath]
            for dirName in cPickle.loads(str(row[0])):
                newPath = os.path.join(dirPath, dirName)
                #print dirPath, ' child ', dir
                myItem = self.treeDirList.AppendItem(parentItem, dirName)
                self.treeDirList.SetItemImage(myItem, self.fldridx, wx.TreeItemIcon_Normal)
                self.treeDirList.SetItemImage(myItem, self.fldropenidx, wx.TreeItemIcon_Expanded)
                self.AddSubDirs(evidenceID, myItem, newPath)
                #GetSubDirs(aPath)

    def AddSubDirsOld(self, evidenceID, parentItem, subDir):
        rows = self.db.FetchAllRows(self.query+self.db.SqlSQuote(dirPath))
        for row in rows:
            #subDirs = 
            #print subDirs
            #if self.EvidencesDict[evidenceID]['DirTree'].has_key(dirPath):
            #subDirs = self.EvidencesDict[evidenceID]['DirTree'][dirPath]
            for dirName in cPickle.loads(str(row[0])):
                newPath = os.path.join(dirPath, dirName)
                #print dirPath, ' child ', dir
                myItem = self.treeDirList.AppendItem(parentItem, dirName)
                self.treeDirList.SetItemImage(myItem, self.fldridx, wx.TreeItemIcon_Normal)
                self.treeDirList.SetItemImage(myItem, self.fldropenidx, wx.TreeItemIcon_Expanded)
                self.AddSubDirs(evidenceID, myItem, newPath)
                #GetSubDirs(aPath)
    
    def GetSubDirs(self, dirPath):
        index = 0
        #print 'testing ', dirPath
        for row in self.rows:
            #print 'row ', row
            
            #if row[0].encode('utf-8', 'replace') == dirPath.encode('utf-8', 'replace'):
            #database row[0] value is already in utf-8; so shouldn't be converted
            #gives error when tried to convert utf-8 to utf-8...
            if row[0] == PlatformMethods.Encode(dirPath):
                self.rows.pop(index)
                #print 'popped'
                return cPickle.loads(str(row[1]))
            
            index += 1
            
        return []
    
    def AddSubDirs(self, evidenceID, parentItem, dirPath):
        #rows = self.db.FetchAllRows(self.query+self.db.SqlSQuote(dirPath))
        dirList = self.GetSubDirs(dirPath)
        #print 'dir List ', dirList
        for dirName in dirList:
            #subDirs = 
            #print subDirs
            #if self.EvidencesDict[evidenceID]['DirTree'].has_key(dirPath):
            #subDirs = self.EvidencesDict[evidenceID]['DirTree'][dirPath]
            #for dirName in cPickle.loads(str(row[0])):
            #newPath = os.path.join(dirPath, dirName)
            #print dirPath, ' child ', dir
            myItem = self.treeDirList.AppendItem(parentItem, dirName)
            self.treeDirList.SetItemImage(myItem, self.fldridx, wx.TreeItemIcon_Normal)
            self.treeDirList.SetItemImage(myItem, self.fldropenidx, wx.TreeItemIcon_Expanded)
        
        #for dirName in dirList:
        if parentItem:
            parentItem = self.treeDirList.GetFirstChild(parentItem)[0]
            
        while parentItem:
            newPath = os.path.join(dirPath, self.GetTreeItemText(parentItem))
            self.AddSubDirs(evidenceID, parentItem, newPath)
            parentItem = self.treeDirList.GetNextSibling(parentItem)
            
    
    def AddDirectories(self):
        
        self.treeDirList.DeleteAllItems()
        #tbd: add image for the root
        self.root = self.treeDirList.AddRoot("Case - Evidences")
        self.treeDirList.SetItemImage(self.root, self.fldridx, wx.TreeItemIcon_Normal)
        self.treeDirList.SetItemImage(self.root, self.fldropenidx, wx.TreeItemIcon_Expanded)
        for evidenceID in self.EvidencesDict:
            #print 'evidenceID = ', evidenceID
            self.db = SqliteDatabase(Globals.FileSystemName)
            if not self.db.OpenConnection():
                return
            
            self.query = "select DirPath, SubDirList from %s%s"%(evidenceID, Constants.DirListTable)
            self.location = PlatformMethods.Encode(self.EvidencesDict[evidenceID]['Location'])
            self.newLocation = self.location
                
            if self.EvidencesDict[evidenceID]['NewLocation']:
                #print 'new', self.EvidencesDict[evidenceID]['NewLocation']
                self.newLocation = self.EvidencesDict[evidenceID]['NewLocation']
                
            self.myRoot = self.treeDirList.AppendItem(self.root, self.newLocation)
            self.treeDirList.SetItemImage(self.myRoot, self.fldridx, wx.TreeItemIcon_Normal)
            self.treeDirList.SetItemImage(self.myRoot, self.fldropenidx, wx.TreeItemIcon_Expanded)
            #self.AddChildrenNodes(self.myRoot, self.DirDict[key]['children'])
            self.myParentItem = self.myRoot
            #subDirs = self.EvidencesDict[evidenceID]['DirTree'][location]
            self.rows = self.db.FetchAllRows(self.query)# + self.db.SqlSQuote(self.location))
            #subDirs = []
            #for row in self.rows:
            dirList = self.GetSubDirs(self.location)
            for dirName in dirList:
                myItem = self.treeDirList.AppendItem(self.myParentItem, dirName)
                self.treeDirList.SetItemImage(myItem, self.fldridx, wx.TreeItemIcon_Normal)
                self.treeDirList.SetItemImage(myItem, self.fldropenidx, wx.TreeItemIcon_Expanded)
                #self.AddSubDirs(evidenceID, myItem, newPath)
                
                #for adir in subDirs
            #if parentItem:
            if self.myParentItem:
                parentItem = self.treeDirList.GetFirstChild(self.myParentItem)[0]
            while parentItem:
                
                dirPath = PlatformMethods.Encode(os.path.join(self.location, self.GetTreeItemText(parentItem)))
                #print 'dir Path ',dirPath
                self.AddSubDirs(evidenceID, parentItem, dirPath)
                parentItem = self.treeDirList.GetNextSibling(parentItem)
            
                #parentItem = self.treeDirList.GetNextSibling(parentItem)
                #print 'newPath = ', newPath
          
            if self.db:
                self.db.CloseConnection()
        #self.treeDirList.SortChildren(self.root)
        self.treeDirList.Expand(self.root)
        #self.treeDirList.Expand(self.myRoot)
        return self.root
        
    
    def AddDirectoriesNew(self):
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
        #self.db = None
        for evidenceID in self.EvidencesDict:
            #print 'evidenceID = ', evidenceID
            self.db = SqliteDatabase(Globals.FileSystemName)
            if not self.db.OpenConnection():
                return
            
            self.query = "select DirPath, SubDirList from %s%s order by DirPath"%(evidenceID, Constants.DirListTable)
            self.location = self.EvidencesDict[evidenceID]['Location']
            self.newLocation = self.location
                
            if self.EvidencesDict[evidenceID]['NewLocation']:
                #print 'new', self.EvidencesDict[evidenceID]['NewLocation']
                self.newLocation = self.EvidencesDict[evidenceID]['NewLocation']
                
            self.myRoot = self.treeDirList.AppendItem(self.root, self.newLocation)
            self.treeDirList.SetItemImage(self.myRoot, self.fldridx, wx.TreeItemIcon_Normal)
            self.treeDirList.SetItemImage(self.myRoot, self.fldropenidx, wx.TreeItemIcon_Expanded)
            #self.AddChildrenNodes(self.myRoot, self.DirDict[key]['children'])
            self.myParentItem = self.myRoot
            #subDirs = self.EvidencesDict[evidenceID]['DirTree'][location]
            self.rows = self.db.FetchAllRows(self.query)# + self.db.SqlSQuote(self.location))
            #subDirs = []
            i = 0
            for row in self.rows:
                #subDirs.extend(cPickle.loads(str(row[0])))
                #print cPickle.loads(str(row[0]))
                for dirName in cPickle.loads(str(row[1])):
                    #for adir in subDirs
                    newPath = os.path.join(self.location, dirName)
                    #print 'newPath = ', newPath
                    myItem = self.treeDirList.AppendItem(self.myParentItem, dirName)
                    self.treeDirList.SetItemImage(myItem, self.fldridx, wx.TreeItemIcon_Normal)
                    self.treeDirList.SetItemImage(myItem, self.fldropenidx, wx.TreeItemIcon_Expanded)
                    self.AddSubDirs(evidenceID, myItem, newPath)
                
          
            if self.db:
                self.db.CloseConnection()
        #self.treeDirList.SortChildren(self.root)
        self.treeDirList.Expand(self.root)
        #self.treeDirList.Expand(self.myRoot)
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
    

