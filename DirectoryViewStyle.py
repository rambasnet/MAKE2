import Globals
import wx
import PlatformMethods

class DirectoryTreeView:
    def __init__(self, parentWin, treeDirList):
        self.parentWindow = parentWin
        self.treeDirList = treeDirList
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
        self.UpdateDirectoryList()
                    
        
    def UpdateDirectoryList(self):
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
        parentItem = self.root
        childrenDirList = dirList[1:]
        for dirName in dirList:
            if not dirName:
                continue
            #always start from directories in the drive e.g. C:\NMT\Research\AJAX
            #dirName = dirList[i]
            siblingItem = self.GetSiblingItem(parentItem, dirName)
            #no directory with that name found in this level, so add it
            if not siblingItem:
                if parentItem == self.root:
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


    def GetDriveItem(self, driveName):
        rootDirItem = self.treeDirList.GetFirstChild(self.root)[0]
        while rootDirItem:
            if self.GetItemText(rootDirItem) == driveName:
                break
            parentItem = self.treeDirList.GetNextSibling(rootDirItem)
        return rootDirItem
    
    
    def AddDirectoryTreeNodes(self):
        self.treeDirList.DeleteAllItems()
        #tbd: add image for the root
        self.root = self.treeDirList.AddRoot("Folders (" + str(Globals.CurrentProject.TotalDirectories) + ")")
        fullDirPath = Globals.DirectoryList[0]
        fullPathList = fullDirPath.split(PlatformMethods.GetDirSeparator())
        
        for dirPath in Globals.DirectoryList:
            self.AddDirectoryTreeNode(dirPath)
                        
        self.treeDirList.SortChildren(self.root)
        self.treeDirList.Expand(self.root)
        return self.root
        
        
    def GetTreeItemText(self, item):
        if item:
            return self.treeDirList.GetItemText(item)
        else:
            return ""