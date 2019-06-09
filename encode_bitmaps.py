#-----------------------------------------------------------------------------
# Name:        encode_bitmaps.py
# Purpose:     
#
# Author:      Ram Basnet
#
# Created:     2007/11/12
# RCS-ID:      $Id: encode_bitmaps.py,v 1.5 2007/11/13 19:52:48 rbasnet Exp $
# Copyright:   (c) 2008
# Licence:     All Rights Reserved.
#-----------------------------------------------------------------------------

"""
This is a way to save the startup time when running img2py on lots of
files...
"""

import sys

from wx.tools import img2py



"""
-a -u -n DoubleRightHead Images/Bitmaps/doubleHead.png images.py",
#"-a -u -n SmallUpArrow  -m #0000FF Images/Bitmaps/sm_up.bmp images.py",
"-a -u -n SmallDnArrow  -m #0000FF Images/Bitmaps/sm_down.bmp images.py",
"-a -u -n NoIcon  Images/Bitmaps/noicon.png  images.py",
"-a -u -n Smile -m #FFFFFF Images/Bitmaps/smile.bmp images.py",
"-a -u -i -n Face01 Images/Icons/FACE01.ICO images.py",
"-a -u -i -n Binoculr Images/Icons/BINOCULR.ICO images.py",
"-a -u -i -n ABC Images/Icons/ABC.ICO images.py",
"-a -u -n TimeLine  Images/Bitmaps/TimeLine.png  images.py"
"-a -u -i -n NoFile16 Images/Icons/NoFile16.PNG images.py"
                "-a -u -i -n search Images/Bitmaps/Search.png images.py",
                "-a -u -i -n registryViewer Images/Bitmaps/RegistryViewer.png images.py",
                "-a -u -i -n textCat Images/Bitmaps/TextCat.png images.py",
                "-a -u -i -n timelines Images/Bitmaps/Timelines.png images.py",
                "-a -u -i -n logViewer Images/Bitmaps/LogViewer.png images.py",
                "-a -u -i -n imageViewer Images/Bitmaps/ImageViewer.png images.py",
                "-a -u -i -n emailViewer Images/Bitmaps/EmailViewer.png images.py"
                "-a -u -i -n folderExplorer Images/Bitmaps/folderExplorer.png images.py"
                "-a -u -i -n emailViewer Images/Bitmaps/EmailViewer.png images.py",
                "-a -u -i -n logViewer Images/Bitmaps/LogViewer.png images.py"
                "-a -u -i -n NoFile32 Images/Icons/NoFile.ICO images.py",
                "-a -u -i -n NoFile16 Images/Icons/NoFile16.ICO images.py"
                "-a -u -i -n CreatedSlider TimelineImages/CreatedSlider.gif images.py"
                "-a -u -i -n AccessedSlider TimelineImages/AccessedSlider.gif images.py"
                "-a -u -i -n CreatedSlider TimelineImages/CreatedSlider.gif images.py"
                "-a -u -i -n CreatedSlider TimelineImages/CreatedSlider.gif images.py"
                "-a -u -i -n CreatedSlider TimelineImages/CreatedSlider.gif images.py",
                "-a -u -i -n ModifiedSlider TimelineImages/ModifiedSlider.gif images.py",
                "-a -u -i -n AccessedSlider TimelineImages/AccessedSlider.gif images.py"
                "-a -u -i -n TLineAccessLine TimelineImages/access_line.gif images.py",
                    "-a -u -i -n TLineAccessLineLeft TimelineImages/access_line_l.gif images.py",
                    "-a -u -i -n TLineAccessLineRight TimelineImages/access_line_r.gif images.py",
                    "-a -u -i -n TLineCreatedLine TimelineImages/create_line.gif images.py",
                    "-a -u -i -n TLineCreatedLineLeft TimelineImages/create_line_l.gif images.py",
                    "-a -u -i -n TLineCreatedLineRight TimelineImages/create_line_r.gif images.py",
                    "-a -u -i -n TLineModifiedLine TimelineImages/modify_line.gif images.py",
                    "-a -u -i -n TLineModifiedLineLeft TimelineImages/modify_line_l.gif images.py",
                    "-a -u -i -n TLineModifiedLineRight TimelineImages/modify_line_r.gif images.py",
                    "-a -u -i -n TLineSelected TimelineImages/selected.gif images.py",
                    "-a -u -i -n TLineSelection TimelineImages/selection.gif images.py",
                    "-a -u -i -n TLineSelectionMask TimelineImages/selectionmask.gif images.py",
                    "-a -u -i -n TLineFileImage TimelineImages/FileImage.gif images.py"
                    "-a -u -i -n MAKE2 Images/MAKE2.ico images.py"
                    "-a -u -i -n SpinningWheel Images/Spinning_wheel_throbber.gif images.py"
"""
    
command_lines = ["-a -u -i -n HexView Images/HexView.gif images.py",
                "-a -u -i -n NativeView Images/NativeView.gif images.py",
                "-a -u -i -n TextView Images/TextView.gif images.py",
                "-a -u -i -n SearchDown Images/SearchDown.gif images.py",
                "-a -u -i -n SearchUp Images/SearchUp.gif images.py",
                ]


if __name__ == "__main__":
    for line in command_lines:
        args = line.split()
        img2py.main(args)

