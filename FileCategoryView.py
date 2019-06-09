#-----------------------------------------------------------------------------
# Name:        FileCategoryView.py
# Purpose:     
#
# Author:      Ram B. Basnet
#
# Created:     2007/11/10
# RCS-ID:      $Id: FileCategoryView.py,v 1.3 2007/11/13 19:52:48 rbasnet Exp $
# Copyright:   (c) 2006
# Licence:     <your licence>
# New field:   Whatever
#-----------------------------------------------------------------------------
import Globals
import wx
import PlatformMethods

class FileCategoryView:
    def __init__(self, parentWin, treeFileType, MimeTypeSet = None):
        self.parentWindow = parentWin
        self.treeFileType = treeFileType
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
        self.treeFileType.AssignImageList(dirIL)
        self.MimeTypeSet = MimeTypeSet
        if not self.MimeTypeSet:
            self.MimeTypeSet = Globals.MimeTypeSet
            
        #self.SetTreeButtons()
        #self.UpdateDirectoryList()
        #self.AddCategoryTreeNodes()
        
    def AddCategories(self):
        self.treeFileType.DeleteAllItems()
        self.root = self.treeFileType.AddRoot("All File Types")
        #print self.MimeTypeSet
        for mType in self.MimeTypeSet:
            #print mType
            childItem = self.treeFileType.AppendItem(self.root, mType) # + " (" + str(self.MimeTypeSet[mType]['TotalFiles']) + ")")
            self.treeFileType.SetItemImage(childItem, self.fldridx, wx.TreeItemIcon_Normal)
            self.treeFileType.SetItemImage(childItem, self.fldropenidx, wx.TreeItemIcon_Expanded)
        self.treeFileType.SortChildren(self.root)
        self.treeFileType.Expand(self.root)      
        return self.root
        
    def GetRoot(self):
        return self.root
    
    """
    def UpdateFileTypeList(self):
        if len(Globals.DirectoryList) == 0:
            dirSet = set()
            for file in Globals.FileInfoList:
                dirSet.add(file.DirectoryPath)
            Globals.DirectoryList = list(dirSet)
            
        
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
        #self.treeFileType.SetButtonsImageList(il)
        self.treeFileType.AssignButtonsImageList(il)
        
    def GetParentItem(self, parentName):
        parentItem = self.treeFileType.GetFirstChild(self.root)[0]
        while parentItem:
            if self.GetItemText(parentItem) == parentName:
                return parentItem
            parentItem = self.treeFileType.GetNextSibling(parentItem)
        return parentItem
    
    
    def AddCategoryTreeNode(self, fileType):
        typeList = fileType.split("/")
        #print typeList
        parentItem = self.root
        childrenCatList = typeList[1:]
        for fileType in typeList:
            if not fileType:
                continue
            #always start from directories in the drive e.g. C:\NMT\Research\AJAX
            #fileType = typeList[i]
            siblingItem = self.GetSiblingItem(parentItem, fileType)
            #no category with that name found in this level, so add it
            if not siblingItem:
                if parentItem == self.root:
                    #add image
                    siblingItem = self.treeFileType.AppendItem(parentItem, fileType)
                    self.treeFileType.SetItemImage(siblingItem, self.fldridx, wx.TreeItemIcon_Normal)
                    self.treeFileType.SetItemImage(siblingItem, self.fldropenidx,
                               wx.TreeItemIcon_Expanded)
                else:
                    siblingItem = self.treeFileType.AppendItem(parentItem, fileType)
                    self.treeFileType.SetItemImage(siblingItem, self.fldridx, wx.TreeItemIcon_Normal)
                    self.treeFileType.SetItemImage(siblingItem, self.fldropenidx,
                               wx.TreeItemIcon_Expanded)
                self.AddSubCategories(siblingItem, childrenCatList)
                break
            else:
                childrenCatList = childrenCatList[1:]
                parentItem = siblingItem
                
        self.treeFileType.SortChildren(parentItem)
                
    
    #dir List without drive
    def AddSubCategories(self, parentItem, childrenCatList):
        for fileType in childrenCatList:
            #Insert new node as parent Item
            parentItem = self.treeFileType.AppendItem(parentItem, fileType)
            self.treeFileType.SetItemImage(parentItem, self.fldridx, wx.TreeItemIcon_Normal)
            self.treeFileType.SetItemImage(parentItem, self.fldropenidx,
                               wx.TreeItemIcon_Expanded)
                    
    
    def GetSiblingItem(self, parentItem, fileType):
        siblingItem = self.treeFileType.GetFirstChild(parentItem)[0]
        while siblingItem:
            if self.GetTreeItemText(siblingItem) == fileType:
                break
            siblingItem = self.treeFileType.GetNextSibling(siblingItem)
        return siblingItem


    def GetDriveItem(self, driveName):
        rootDirItem = self.treeFileType.GetFirstChild(self.root)[0]
        while rootDirItem:
            if self.GetItemText(rootDirItem) == driveName:
                break
            parentItem = self.treeFileType.GetNextSibling(rootDirItem)
        return rootDirItem
 
    def AddCategoryTreeNodes(self):
        self.treeFileType.DeleteAllItems()
        #tbd: add image for the root
        self.root = self.treeFileType.AddRoot("File Types")
        for mtype in self.MimeTypeSet:
       
            if file.MimeType == "Unknown":
                if file.Description == "Unknown":
                    self.AddCategoryTreeNode(file.MimeType)
                else:
                    self.AddCategoryTreeNode(file.Description)
            else:
                self.AddCategoryTreeNode(file.MimeType)

            self.AddCategoryTreeNone(mtype)
                        
        self.treeFileType.SortChildren(self.root)
        self.treeFileType.Expand(self.root)
        return self.root
    
    def GetTreeItemText(self, item):
        if item:
            return self.treeFileType.GetItemText(item)
        else:
            return ""
        
    """

        
