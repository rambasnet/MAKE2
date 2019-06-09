#-----------------------------------------------------------------------------
# Name:        FileCategoryCheckView.py
# Purpose:     
#
# Author:      Ram Basnet
#
# Created:     2007/11/01
# Last Modified: 6/30/2009
# RCS-ID:      $Id: FileCategoryCheckView.py,v 1.4 2007/11/23 05:50:14 rbasnet Exp $
# Copyright:   (c) 2007
# Licence:     All Rights Reserved.
# New field:   Whatever
#-----------------------------------------------------------------------------

import Globals
import wx, string
import PlatformMethods
import wx.lib.customtreectrl as CT


class FileCategoryCheckView(CT.CustomTreeCtrl):
    def __init__(self, parent, MimeTypeSet=[], id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 style= wx.SIMPLE_BORDER | wx.VSCROLL | CT.TR_HAS_BUTTONS | CT.TR_HAS_VARIABLE_ROW_HEIGHT, CheckedList=[]):

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
        #self.UpdateFileTypeList()
        self.CheckedList = CheckedList
        self.MimeTypeSet = MimeTypeSet
        
   
        if not self.MimeTypeSet:
            self.MimeTypeSet = Globals.MimeTypeSet
  
         
        #self.AddCategoryTreeNodes()
        self.AddCategories()
    
    def AddCategories(self):
        self.DeleteAllItems()
        self.root = self.AddRoot("All File Types")
        #print self.MimeTypeSet
        for mType in self.MimeTypeSet:
            #print mType
            childItem = self.AppendItem(self.root, mType, ct_type=1) # + " (" + str(self.MimeTypeSet[mType]['TotalFiles']) + ")")
            self.SetItemImage(childItem, self.fldridx, wx.TreeItemIcon_Normal)
            self.SetItemImage(childItem, self.fldropenidx, wx.TreeItemIcon_Expanded)
            check = mType in self.CheckedList
            childItem.Check(checked=check) 
            
        self.SortChildren(self.root)
        self.Expand(self.root)      
        return self.root
        
    def GetRoot(self):
        return self.root

        
    def SetTreeButtons(self):

        bitmap_plus = PlatformMethods.ConvertFilePath("Images/Bitmaps/plus4.ico")
        bitmap_minus = PlatformMethods.ConvertFilePath("Images/Bitmaps/minus4.ico")
        
        bitmap = wx.Bitmap(bitmap_plus, wx.BITMAP_TYPE_ICO)
        width = bitmap.GetWidth()
        
        il = wx.ImageList(width, width)
        
        il.Add(wx.Bitmap(bitmap_plus, wx.BITMAP_TYPE_ICO))
        il.Add(wx.Bitmap(bitmap_minus, wx.BITMAP_TYPE_ICO))

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
    
    
    def AddCategoryTreeNode(self, fileType):
        typeList = fileType.split("/")
        #print typeList
        parentItem = self.root
        childrenCatList = typeList[1:]
        parentName = ""
        for fileType in typeList:
            if not fileType:
                continue
            #always start from directories in the drive e.g. C:\NMT\Research\AJAX
            #fileType = typeList[i]
            siblingItem = self.GetSiblingItem(parentItem, fileType)
            #no category with that name found in this level, so add it
            if parentName == "":
                parentName += fileType
            else:
                parentName += "/" + fileType
                
            if not siblingItem:
                check = parentName in self.CheckedList
                if parentItem == self.root:
                    #add image
                    siblingItem = self.AppendItem(parentItem, fileType, ct_type=1)
                    self.SetItemImage(siblingItem, self.fldridx, wx.TreeItemIcon_Normal)
                    self.SetItemImage(siblingItem, self.fldropenidx,
                               wx.TreeItemIcon_Expanded)
                else:
                    siblingItem = self.AppendItem(parentItem, fileType, ct_type=1)
                    self.SetItemImage(siblingItem, self.fldridx, wx.TreeItemIcon_Normal)
                    self.SetItemImage(siblingItem, self.fldropenidx,
                               wx.TreeItemIcon_Expanded)
                
                siblingItem.Check(checked=check)
                self.AddSubCategories(siblingItem, parentName, childrenCatList)
                break
            else:
                childrenCatList = childrenCatList[1:]
                parentItem = siblingItem
                
        self.SortChildren(parentItem)

    
    #dir List without drive
    def AddSubCategoriesOld(self, parentItem, parentName, childrenCatList):
        for fileType in childrenCatList:
            #Insert new node as parent Item
            parentItem = self.AppendItem(parentItem, fileType, ct_type=1)
            self.SetItemImage(parentItem, self.fldridx, wx.TreeItemIcon_Normal)
            self.SetItemImage(parentItem, self.fldropenidx,
                               wx.TreeItemIcon_Expanded)
            parentName += "/" + fileType
            check = parentName in self.CheckedList
            parentItem.Check(checked=check) 
                   
    
    def GetSiblingItem(self, parentItem, fileType):
        siblingItem = self.GetFirstChild(parentItem)[0]
        while siblingItem:
            if self.GetTreeItemText(siblingItem) == fileType:
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
    
    

    def AddCategoryTreeNodes(self):
        self.DeleteAllItems()
        #tbd: add image for the root
        self.root = self.AddRoot("File Types")
        for file in Globals.FileInfoList:
            if file.MimeType == "Unknown":
                if file.Description == "Unknown":
                    self.AddCategoryTreeNode(file.MimeType)
                else:
                    self.AddCategoryTreeNode(file.Description)
            else:
                self.AddCategoryTreeNode(file.MimeType)
                        
        self.SortChildren(self.root)
        self.Expand(self.root)
        return self.root
    

    
    def AddCategoriesOld(self):
        self.DeleteAllItems()
        self.root = self.AddRoot("File Types", ct_type=1)
        #print self.MimeTypeSet
        #if type(self.MimeTypeSet) is dict:
        for mType in self.MimeTypeSet:
            childItem = self.AppendItem(self.root, mType, ct_type=1)
                
            self.SetItemImage(childItem, self.fldridx, wx.TreeItemIcon_Normal)
            self.SetItemImage(childItem, self.fldropenidx, wx.TreeItemIcon_Expanded)
            check = mType in self.CheckedList
            childItem.Check(checked=check) 
                        
        self.SortChildren(self.root)
        self.Expand(self.root)      
        return self.root
    
    def AddCategoriesOld(self):
        self.DeleteAllItems()
        self.root = self.AddRoot("File Types", ct_type=1)
        #print self.MimeTypeSet
        #if type(self.MimeTypeSet) is dict:
        for mType in self.MimeTypeSet:
            #print mType
            if type(self.MimeTypeSet[mType]) is dict:
                #if self.MimeTypeSet[mType].has_key('TotalFiles'):
                childItem = self.AppendItem(self.root, mType + " (" + str(self.MimeTypeSet[mType]['TotalFiles']) + ")", ct_type=1)
            else:
                childItem = self.AppendItem(self.root, mType, ct_type=1)
                
            self.SetItemImage(childItem, self.fldridx, wx.TreeItemIcon_Normal)
            self.SetItemImage(childItem, self.fldropenidx, wx.TreeItemIcon_Expanded)
            check = mType in self.CheckedList
            childItem.Check(checked=check) 
            for childType in self.MimeTypeSet[mType]:
                if type(self.MimeTypeSet[mType]) is dict:
                    if not childType == "TotalFiles":
                        gcItem = self.AppendItem(childItem, childType + " (" + str(self.MimeTypeSet[mType][childType]) + ")", ct_type=1)
                        self.SetItemImage(gcItem, self.fldridx, wx.TreeItemIcon_Normal)
                        self.SetItemImage(gcItem, self.fldropenidx, wx.TreeItemIcon_Expanded)
                        gcItem.Check(checked=mType in self.CheckedList)
                else:
                    gcItem = self.AppendItem(childItem, childType, ct_type=1)
                    self.SetItemImage(gcItem, self.fldridx, wx.TreeItemIcon_Normal)
                    self.SetItemImage(gcItem, self.fldropenidx, wx.TreeItemIcon_Expanded)
                    gcItem.Check(checked=mType in self.CheckedList)
                
                        
        self.SortChildren(self.root)
        self.Expand(self.root)      
        return self.root
        
        
    def GetTreeItemText(self, item):
        if item:
            text = self.GetItemText(item)
            if text.find("(") > 0:
                return text[:text.find("(")-1]
            else:
                return text
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
            
            
    def UpdateCheckedList(self, CheckedList):
        #CheckedList = []
        driveItems = self.root.GetChildren()
        for item in driveItems:
            if item.IsChecked():
                CheckedList.append(self.GetTreeItemText(item))
            self.UpdateChildCheckedList(item, self.GetTreeItemText(item), CheckedList)
        #print CheckedList
            
        
    def UpdateChildCheckedList(self, item, parentPath, CheckedList):
        for child in item.GetChildren():
            myPath = parentPath + "/" + self.GetTreeItemText(child)
            if child.IsChecked():
                CheckedList.append(myPath)
            self.UpdateChildCheckedList(child, myPath, CheckedList)
                
   
                
        
