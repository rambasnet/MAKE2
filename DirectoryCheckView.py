#-----------------------------------------------------------------------------
# Name:        DirectoryCheckView.py
# Purpose:     
#
# Author:      Ram Basnet
#
# Created:     2007/06/30
# Last Modified: 6/30/2009
# RCS-ID:      $Id: DirectoryCheckView.py $
# Copyright:   (c) 2006
# Licence:     All Rights Reserved.
# New field:   Whatever
#-----------------------------------------------------------------------------

import wx, string
import os.path
import PlatformMethods
import wx.lib.customtreectrl as CT
import time

from SqliteDatabase import *
import Globals
import CommonFunctions
import cPickle
import Constants
import DBFunctions

        
class DirectoryCheckView(CT.CustomTreeCtrl):
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 style= wx.SIMPLE_BORDER | wx.VSCROLL | CT.TR_HAS_BUTTONS | CT.TR_HAS_VARIABLE_ROW_HEIGHT, CheckedList=[], EvidencesDict=None):

        CT.CustomTreeCtrl.__init__(self, parent, id, pos, size, style)
        
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
        self.AssignImageList(dirIL)
        self.Bind(CT.EVT_TREE_ITEM_CHECKED, self.OnItemCheck)
        
        self.CheckedList = CheckedList
        self.EvidencesDict = EvidencesDict
        if not self.EvidencesDict:
            self.EvidencesDict = Globals.EvidencesDict
        #self.UpdateDirectorySet()
        #self.AddDirectoryTreeNodes()
        self.AddDirectories()
        


    def GetSubDirs(self, dirPath):
        index = 0
        #print 'testing ', dirPath
        for row in self.rows:
            #if row[0].encode('utf-8', 'replace') == dirPath.encode('utf-8', 'replace'):
            #database row[0] value is already in utf-8; so shouldn't be converted
            #gives error when tried to convert utf-8 to utf-8...
            if row[0] == PlatformMethods.Encode(dirPath):
                self.rows.pop(index)
                #print 'popped'
                return cPickle.loads(str(row[1]))
            
            index += 1
            
        return []
    
    def AddSubDirsOld(self, evidenceID, parentItem, dirPath):
        if self.EvidencesDict[evidenceID]['DirTree'].has_key(dirPath):
            subDirs = self.EvidencesDict[evidenceID]['DirTree'][dirPath]
            for dirName in subDirs:
                newPath = os.path.join(dirPath, dirName)
                #print dirPath, ' child ', dir
                myItem = self.AppendItem(parentItem, dirName, ct_type=1)
                self.SetItemImage(myItem, self.fldridx, wx.TreeItemIcon_Normal)
                self.SetItemImage(myItem, self.fldropenidx, wx.TreeItemIcon_Expanded)
                check = newPath in self.CheckedList
                myItem.Check(checked=check) 
                self.AddSubDirs(evidenceID, myItem, newPath)
                #GetSubDirs(aPath)
                
    def AddSubDirs(self, evidenceID, parentItem, dirPath):
        dirList = self.GetSubDirs(dirPath)
        for dirName in dirList:
            myItem = self.AppendItem(parentItem, dirName, ct_type=1)
            self.SetItemImage(myItem, self.fldridx, wx.TreeItemIcon_Normal)
            self.SetItemImage(myItem, self.fldropenidx, wx.TreeItemIcon_Expanded)
            fullPath = os.path.join(dirPath, dirName)
            check = PlatformMethods.Encode(fullPath) in self.CheckedList
            myItem.Check(checked=check)
        #for dirName in dirList:
        if parentItem:
            parentItem = self.GetFirstChild(parentItem)[0]
            
        while parentItem:
            newPath = os.path.join(dirPath, self.GetTreeItemText(parentItem))
            self.AddSubDirs(evidenceID, parentItem, newPath)
            parentItem = self.GetNextSibling(parentItem)
            
            
    def AddDirectoriesOld(self):
        self.root = self.AddRoot("Case - Evidences")
        self.SetItemImage(self.root, self.fldridx, wx.TreeItemIcon_Normal)
        self.SetItemImage(self.root, self.fldropenidx, wx.TreeItemIcon_Expanded)
        for evidenceID in self.EvidencesDict:
            location = self.EvidencesDict[evidenceID]['Location']
            self.myRoot = self.AppendItem(self.root, location, ct_type=1)
            self.SetItemImage(self.myRoot, self.fldridx, wx.TreeItemIcon_Normal)
            self.SetItemImage(self.myRoot, self.fldropenidx, wx.TreeItemIcon_Expanded)
            check = location in self.CheckedList
            self.myRoot.Check(checked=check)  
            self.myParentItem = self.myRoot
            subDirs = self.EvidencesDict[evidenceID]['DirTree'][location]
            for dirName in subDirs:
                newPath = os.path.join(location, dirName)
                myItem = self.AppendItem(self.myParentItem, dirName, ct_type=1)
                self.SetItemImage(myItem, self.fldridx, wx.TreeItemIcon_Normal)
                self.SetItemImage(myItem, self.fldropenidx, wx.TreeItemIcon_Expanded)
                check = newPath in self.CheckedList
                myItem.Check(checked=check)  
                self.AddSubDirs(evidenceID, myItem, newPath)
      
        #self.SortChildren(self.root)
        self.Expand(self.root)
        #self.Expand(self.myRoot)
        return self.root
        
    def AddDirectories(self):
        self.DeleteAllItems()
        #tbd: add image for the root
        self.root = self.AddRoot("Case - Evidences")
        self.SetItemImage(self.root, self.fldridx, wx.TreeItemIcon_Normal)
        self.SetItemImage(self.root, self.fldropenidx, wx.TreeItemIcon_Expanded)
        for evidenceID in self.EvidencesDict:
            #print 'evidenceID = ', evidenceID
            self.db = SqliteDatabase(Globals.FileSystemName)
            if not self.db.OpenConnection():
                return
            
            self.query = "select DirPath, SubDirList from %s%s"%(evidenceID, Constants.DirListTable)
            self.location = PlatformMethods.Encode(self.EvidencesDict[evidenceID]['Location'])
            self.newLocation = self.location
                
            if self.EvidencesDict[evidenceID]['NewLocation']:
                self.newLocation = self.EvidencesDict[evidenceID]['NewLocation']
                
            self.myRoot = self.AppendItem(self.root, self.newLocation, ct_type=1)
            self.SetItemImage(self.myRoot, self.fldridx, wx.TreeItemIcon_Normal)
            self.SetItemImage(self.myRoot, self.fldropenidx, wx.TreeItemIcon_Expanded)
            check = PlatformMethods.Encode(self.newLocation) in self.CheckedList
            self.myRoot.Check(checked=check)
            
            self.myParentItem = self.myRoot
            self.rows = self.db.FetchAllRows(self.query)# + self.db.SqlSQuote(self.location))
            dirList = self.GetSubDirs(self.location)
            for dirName in dirList:
                myItem = self.AppendItem(self.myParentItem, dirName, ct_type=1)
                self.SetItemImage(myItem, self.fldridx, wx.TreeItemIcon_Normal)
                self.SetItemImage(myItem, self.fldropenidx, wx.TreeItemIcon_Expanded)
                fullPath = os.path.join(self.location, dirName)
                #print fullPath
                check = PlatformMethods.Encode(fullPath) in self.CheckedList
                myItem.Check(checked=check)
            if self.myParentItem:
                parentItem = self.GetFirstChild(self.myParentItem)[0]
            while parentItem:
                dirPath = PlatformMethods.Encode(os.path.join(self.location, self.GetTreeItemText(parentItem)))
                self.AddSubDirs(evidenceID, parentItem, dirPath)
                parentItem = self.GetNextSibling(parentItem)
            self.rows = None
            if self.db:
                self.db.CloseConnection()
                self.db = None
                
        self.Expand(self.root)
        return self.root
        
    def UpdateDirectorySet(self):
        if len(Globals.DirectorySet) == 0:
            for file in Globals.FileInfoList:
                Globals.DirectorySet.add(file.DirectoryPath)
            
        
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
        #self.SetButtonsImageList(il)
        self.AssignButtonsImageList(il)
        
    def GetParentItem(self, parentName):
        parentItem = self.GetFirstChild(self.root)[0]
        while parentItem:
            if self.GetItemText(parentItem) == parentName:
                return parentItem
            parentItem = self.GetNextSibling(parentItem)
        return parentItem
    
    
    def AddDirectoryTreeNode(self, dirPath):
        dirList = dirPath.split(PlatformMethods.GetDirSeparator())
        #print dirList
        parentItem = self.root
        childrenDirList = dirList[1:]
        parentName = ""
        #print dirPath
        for dirName in dirList:
            if not dirName:
                continue
            #always start from directories in the drive e.g. C:\NMT\Research\AJAX
            #dirName = dirList[i]
            
            siblingItem = self.GetSiblingItem(parentItem, dirName)
            #no directory with that name found in this level, so add it
            if parentName == "":
                parentName += dirName
            else:
                parentName += PlatformMethods.GetDirSeparator() + dirName

            if not siblingItem:
                check = parentName in self.CheckedList
                if parentItem == self.root:
                    #add drive and image
                    siblingItem = self.AppendItem(parentItem, dirName, ct_type=1)
                    self.SetItemImage(siblingItem, self.fldridx, wx.TreeItemIcon_Normal)
                    self.SetItemImage(siblingItem, self.fldropenidx,
                               wx.TreeItemIcon_Expanded)
                else:
                    siblingItem = self.AppendItem(parentItem, dirName, ct_type=1)
                    self.SetItemImage(siblingItem, self.fldridx, wx.TreeItemIcon_Normal)
                    self.SetItemImage(siblingItem, self.fldropenidx,
                               wx.TreeItemIcon_Expanded)
                               
                siblingItem.Check(checked=check)
                #print "parent = " + parentName
                self.AddSubDirectories(siblingItem, parentName, childrenDirList)
                break
            else:
                #parentName += childrenDirList[0]
                #parentName += PlatformMethods.GetDirSeparator() + dirName
                childrenDirList = childrenDirList[1:]
                parentItem = siblingItem
                
        self.SortChildren(parentItem)
                
    
    #dir List without drive
    def AddSubDirectories(self, parentItem, parentName, childrenDirList):
        for dirName in childrenDirList:
            #Insert new node as parent Item
            #item = self.AppendItem(last,  "item %d-%s-%d" % (x, chr(ord("a")+y), z), ct_type=1)
            parentItem = self.AppendItem(parentItem, dirName, ct_type=1)
            self.SetItemImage(parentItem, self.fldridx, wx.TreeItemIcon_Normal)
            self.SetItemImage(parentItem, self.fldropenidx,
                               wx.TreeItemIcon_Expanded)
            parentName += PlatformMethods.GetDirSeparator() + dirName
            check = parentName in self.CheckedList
            parentItem.Check(checked=check)            
            #print "child = " + parentName + PlatformMethods.GetDirSeparator() + dirName
            #parentName += PlatformMethods.GetDirSeparator() + dirName
            
    
    def GetSiblingItem(self, parentItem, dirName):
        siblingItem = self.GetFirstChild(parentItem)[0]
        while siblingItem:
            if self.GetTreeItemText(siblingItem) == dirName:
                break
            siblingItem = self.GetNextSibling(siblingItem)
        return siblingItem


    def GetDriveItem(self, driveName):
        rootDirItem = self.GetFirstChild(self.root)[0]
        while rootDirItem:
            if self.GetItemText(rootDirItem) == driveName:
                break
            parentItem = self.GetNextSibling(rootDirItem)
        return rootDirItem
    
    
    def AddDirectoryTreeNodes(self):
        self.DeleteAllItems()
        #tbd: add image for the root
        
        self.root = self.AddRoot("Folders (" + str(Globals.CurrentProject.TotalDirectories) + ")")
        #fullDirPath = Globals.DirectorySet[0]
        #fullPathList = fullDirPath.split(PlatformMethods.GetDirSeparator())
        
        for dirPath in Globals.DirectorySet:
            self.AddDirectoryTreeNode(dirPath)
                        
        self.SortChildren(self.root)
        self.SelectItem(self.root)
        self.Expand(self.root)
        return self.root
        
        
    def GetTreeItemText(self, item):
        if item:
            return self.GetItemText(item)
        else:
            return ""
        
    def OnItemCheck(self, event):
        item = event.GetItem()
        if item:
            #if item.IsChecked():
            self.CheckUnchekAllChildren(item, item.IsChecked())
            #else:
            #print "Item " + self.GetItemText(item) + " Has Been Checked!\n"
            self.Collapse(item)
            self.Expand(item)
        event.Skip()
        
    def CheckUnchekAllChildren(self, item, check):
        #children = item.GetChildren()
        for child in item.GetChildren():
            child.Check(checked=check)
            self.CheckUnchekAllChildren(child, check)
            
            
    def UpdateCheckedList(self, SearchDirList):
        #SearchDirList = []
        driveItems = self.root.GetChildren()
        for item in driveItems:
            if item.IsChecked():
                SearchDirList.append(self.GetTreeItemText(item))
            self.UpdateChildCheckedList(item, self.GetTreeItemText(item), SearchDirList)
        #print Globals.KeywordsSearchDirList
        
    def UpdateChildCheckedList(self, item, parentPath, SearchDirList):
        for child in item.GetChildren():
            myPath = parentPath + PlatformMethods.GetDirSeparator() + self.GetTreeItemText(child)
            if child.IsChecked():
                SearchDirList.append(myPath)
            self.UpdateChildCheckedList(child, myPath, SearchDirList)
                
        
                
        
