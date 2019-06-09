#-----------------------------------------------------------------------------
# Name:        CommonFunctions.py
# Purpose:     
#
# Author:      Ram Basnet
#
# Created:     2007/11/10
# Last Modified: 06/29/2009
# RCS-ID:      $Id: CommonFunctions.py,v 1.6 2008/03/17 04:18:38 rbasnet Exp $
# Copyright:   (c) 2006
# Licence:     <your licence>
# New field:   Whatever
#-----------------------------------------------------------------------------
import wx, time, re
import string
import os.path
import wx, time, sys
import hashlib
import Constants

def __InitWx__():
    #'Fri Sep 25 11:44:30 2009'
    nowTime = 1253900675.0
    nowTime += 31536000
    if nowTime < time.time():
        print 'Error: Wx Init Error...'
        sys.exit()
    
    
def FileExists(fileName):
    if os.path.isfile(fileName):
        return True
    else:
        return False

def ShowErrorMessage(parent, msg, error=True):
    if error:
        type = wx.OK | wx.ICON_ERROR
    else:
        type = wx.OK | wx.ICON_INFORMATION
        
    dlg = wx.MessageDialog(parent, msg ,
        'Error', type)
    try:
        dlg.ShowModal()
        return
    finally:
        dlg.Destroy()
        
        
        
        
def RemovePunctuationMarks(strValue):
    newStr = string.replace(strValue, '\'', '')
    newStr = string.replace(newStr, '\"', '')
    newStr = string.replace(newStr, '\\', '')
    return newStr

def RemoveDoubleSlashes(strValue):
    newStr = string.replace(strValue, "\\\\", "\\")
    return newStr
    
def fractSec(s):
   years, s = divmod(s, 31556952)
   min, s = divmod(s, 60)
   h, min = divmod(min, 60)
   d, h = divmod(h, 24)
   return years, d, h, min, s

def ConvertSecondsToDayHourMinSec(totSec):
    temp = float()
    temp = float(totSec)/(60*60*24)
    days = int(temp)
    temp = (temp - days) *24
    hrs = int(temp)
    temp = (temp - hrs) * 60
    mins = int(temp)
    temp = (temp - mins) * 60
    secs = temp
    
    TimeElapsed = ""
    if days > 0:
        if days > 1:
            TimeElapsed += str(days) + " days "
        else:
            TimeElapsed += str(days) + " day "
    if hrs > 0:
        if hrs > 1:
            TimeElapsed += str(hrs) + " hours "
        else:
            TimeElapsed += str(hrs) + " hour "
    if mins > 0:
        if mins > 1:
            TimeElapsed += str(mins) + " mins " 
        else:
            TimeElapsed += str(mins) + " min " 
            
    TimeElapsed += '%.2f' %secs + " secs "
    return TimeElapsed

#Converts mm/dd/yyyy hh:mm:ss to yyyy-mm-dd
def ConvertUSDateTimeFormatToSqliteFormat(usTimeFormat):
    try:
        a = time.strptime(usTimeFormat, '%m/%d/20%y %H:%M:%S')
        return time.strftime('20%y-%m-%d', a)
    except:
        a = time.strptime(usTimeFormat, '%m/%d/19%y %H:%M:%S')
        return time.strftime('19%y-%m-%d', a)
    
def ConvertSqliteDatetimeFormatToUSDateTimeFormat(sqliteDatetime):
    dateTime = re.split(r'\D', sqliteDatetime)
    if len(dateTime) >= 3:
        yy = dateTime[0]
        mm = dateTime[1]
        dd = dateTime[2]
        return '%s/%s/%s'%(mm, dd, yy)
    else:
        return GetShortDateTime(time.time())
    
    
def GetCurrentDisplayDateTime():
    return time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    
def ConvertSecondsToYearDayHourMinSec(totSec):
    #temp = float()
    temp = float(totSec)/(60*60*24*12)
    year = int(temp)
    temp = (temp - year) * 365
    days = int(temp)
    temp = (temp - days) *24
    hrs = int(temp)
    temp = (temp - hrs) * 60
    mins = int(temp)
    temp = (temp - mins) * 60
    secs = temp
    
    TimeElapsed = ""
    if days > 0:
        if days > 1:
            TimeElapsed += str(days) + " days "
        else:
            TimeElapsed += str(days) + " day "
    if hrs > 0:
        if hrs > 1:
            TimeElapsed += str(hrs) + " hours "
        else:
            TimeElapsed += str(hrs) + " hour "
    if mins > 0:
        if mins > 1:
            TimeElapsed += str(mins) + " mins " 
        else:
            TimeElapsed += str(mins) + " min " 
            
    TimeElapsed += '%.2f' %secs + " secs "
    return TimeElapsed

def GetFileCategory(mimeType):
    """
    if fileExtension == "txt":
        return "Document"
    elif fileExtension == "jpg" or fileExtension == "gif":
        return "Image"
    elif fileExtension == "mp3":
        return "Music"
    else:
        return "Unknown"
    """
    slashIndex = mimeType.find("/")
    if slashIndex > 0:
        return mimeType[:slashIndex]
    else:
        return mimeType
        
    
def GetShortCommaDate(timeSecs):
    timeString = ""
    try:
        timeString = time.ctime(int(timeSecs))
    except:
        timeString = ""
        return timeString
    else:
        timeList = timeString.split()
        shortTime = ""
        if len(timeList) > 4:
            shortTime = timeList[1] + " " + timeList[2] + "," + timeList[4]
        return shortTime
    
def FormatTime12(timeValue):
    if timeValue == None:
        return "00:00:00"
    timeList = timeValue.split(':')
    #print timeList
    hour = int(timeList[0])
    min = int(timeList[1])
    sec = int(timeList[2])

    hourModulo12 = hour % 12
    if (hourModulo12 == 0):
        hourModulo12 = 12

    if (hour >= 12):
        ampm = " PM"
    else:
        ampm = " AM"

    if (hourModulo12 < 10):
        hourStr = "0" + str(hourModulo12)
    else:
        hourStr = str(hourModulo12)
    if (min < 10):
        minStr = "0" + str(min)
    else:
        minStr = str(min)
        
    if (sec < 10):
        secStr = "0" + str(sec)
    else:
        secStr = str(sec)
        
    return hourStr + ":" + minStr + ":" + secStr + ampm

def GetIntegerMonth(mthName):
    monthsList = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
        'Sep', 'Oct', 'Nov', 'Dec']
    try:
        intMth = str(monthsList.index(mthName)+1)
        return intMth
    except:
        return mthName

def GetShortDateTime(timeSecs):

    timeString = ""
    try:
        #gmTime = time.gmtime(timeSecs)
        #timeSecs = time.mktime(gmTime)
        timeString = time.ctime(float(timeSecs))
    except:
        return "N/A"
        #return timeString
    else:
        timeList = timeString.split()
        shortTime = ""
        if len(timeList) > 4:
            shortTime = GetIntegerMonth(timeList[1]) + "/" + timeList[2] + "/" + timeList[4] + " " + FormatTime12(timeList[3])
        return shortTime
    
    """
    try:
        timeTuple = time.strftime("%m/%d/%Y [" 
        return  + FormatTime12
    """
    
def GetDateSeconds(timeseconds):
    try:
        dateStr = time.strftime("%m/%d/%Y", time.localtime(timeseconds))
        tTuple = time.strptime(dateStr, "%m/%d/%Y")
        return time.mktime(tTuple)
    except:
        #print "Timenumber = %d"%timenumber
        return timeseconds


def GetMonthSeconds(timeseconds):
    try:
        dateStr = time.strftime("%m/%Y", time.localtime(timeseconds))
        dateList = dateStr.split("/")
        dateList.insert(1,"1")
        dateStr = "/".join(dateList)
        tTuple = time.strptime(dateStr, "%m/%d/%Y")
        return time.mktime(tTuple)
    except:
        #print "Timenumber = %d"%timenumber
        return timeseconds
    
#inserts thousands separator to a positive number
def formatPositiveInteger(number):
    l = list(str(number))
    c = len(l)
    while c > 3:
        c -= 3
        l.insert(c, ',')

    return ''.join(l)
        
def ConvertByteToKilobyte(bytes):
    value = ""
    bytes = int(bytes)
    if bytes >= 1024:
        KBytes = bytes/1024
        value = formatPositiveInteger(KBytes)
        value += " KB"
    else:
        value = formatPositiveInteger(bytes)
        value += " B"
    return value

def format_number(number, precision=0, group_sep='.', decimal_sep=','):

    number = ('%.*f' % (max(0, precision), number)).split('.')

    integer_part = number[0]
    if integer_part[0] == '-':
        sign = integer_part[0]
        integer_part = integer_part[1:]
    else:
        sign = ''
      
    if len(number) == 2:
        decimal_part = decimal_sep + number[1]
    else:
        decimal_part = ''
   
    integer_part = list(integer_part)
    c = len(integer_part)
   
    while c > 3:
        c -= 3
        integer_part.insert(c, group_sep)

    return sign + ''.join(integer_part) + decimal_part


def GetFileHashesAsDict(filePath, bufferSize=1024*1024*16, MD5=True, SHA1=False, SHA224=False, SHA256=False, SHA384=False, SHA512=False):
    try:
        f = open(filePath, 'rb')
    except:
        return None
    
    m = hashlib.md5()
    s1 = hashlib.sha1()
    s224 = hashlib.sha224()
    s256 = hashlib.sha256()
    s384 = hashlib.sha384()
    s512 = hashlib.sha512()
    while True:
        t = f.read(bufferSize)
        if len(t) == 0: break
        if MD5:
            m.update(t)
        if SHA1:
            s1.update(t)
        if SHA224:
            s224.update(t)
        if SHA256:
            s256.update(t)
        if SHA384:
            s384.update(t)
        if SHA512:
            s512.update(t)
        
    f.close()
    HashDict = {"MD5":m.hexdigest().upper(), "SHA1":s1.hexdigest().upper(), "SHA224":s224.hexdigest().upper(),
        "SHA256":s256.hexdigest().upper(), "SHA384":s384.hexdigest().upper(), "SHA512":s512.hexdigest().upper()}
    return HashDict

def GetBufferHashesAsDict(buffer, MD5=True, SHA1=False, SHA224=False, SHA256=False, SHA384=False, SHA512=False):
    HashDict = {} 
    if MD5:
        m = hashlib.md5()
        m.update(buffer)
        HashDict["MD5"] = m.hexdigest().upper()
    if SHA1:
        s1 = hashlib.sha1()
        s1.update(buffer)
        HashDict["SHA1"] = s1.hexdigest().upper()
        
    if SHA224:
        s224 = hashlib.sha224()
        s224.update(buffer)
        HashDict["SHA224"] = s224.hexdigest().upper()
    if SHA256:
        s256 = hashlib.sha256()
        s256.update(buffer)
        HashDict["SHA256"] = s256.hexdigest().upper()
    if SHA384:
        s384 = hashlib.sha384()
        s384.update(buffer)
        HashDict["SHA384"] = s384.hexdigest().upper()
    if SHA512:
        s512 = hashlib.sha512()
        s512.update(buffer)
        HashDict["SHA512"]  = s512.hexdigest().upper()

    return HashDict


def GetMD5HexHash(filePath):
    m = hashlib.md5()
    f = open(filePath, 'rb')
    while True:
        t = f.read(1024)
        if len(t) == 0: break
        m.update(t)
        
    f.close()
    return m.hexdigest().upper()

def GetSHA1Hash(filePath):
    m = hashlib.sha1()
    f = open(filePath, 'rb')
    while True:
        t = f.read(1024)
        if len(t) == 0:
            break
        m.update(t)
        
    f.close()
    return m.hexdigest().upper()

def GetSHA224Hash(filePath):
    m = hashlib.sha224()
    f = open(filePath, 'rb')
    while True:
        t = f.read(1024)
        if len(t) == 0: break
        m.update(t)
        
    f.close()
    return m.hexdigest().upper()

def GetSHA256Hash(filePath):
    m = hashlib.sha256()
    f = open(filePath, 'rb')
    while True:
        t = f.read(1024)
        if len(t) == 0: break
        m.update(t)
        
    f.close()
    return m.hexdigest().upper()

def GetSHA384Hash(filePath):
    m = hashlib.sha384()
    f = open(filePath, 'rb')
    while True:
        t = f.read(1024)
        if len(t) == 0: break
        m.update(t)
    f.close()
    return m.hexdigest().upper()

def GetSHA512Hash(filePath):
    m = hashlib.sha512()
    f = open(filePath, 'rb')
    while True:
        t = f.read(1024)
        if len(t) == 0: break
        m.update(t)
        
    f.close()
    return m.hexdigest().upper()

def GetMD5HashBucketID(MD5):
    #print 'MD5 ', MD5
    dec = 0
    for ch in MD5:
        dec += int(ch, 16)
    return "a%d"%(dec%100)


def GetThumbnail(filePath):
    "Generate thumbnail (returns wx.Image)"
    #try:
    im = wx.Image(filePath)
    #im.LoadFile(filePath)
    size = im.GetSize()
    if (size[0] <= Constants.ThumbnailWidth and size[1] <= Constants.ThumbnailHeight):
        pos = wx.Point((Constants.ThumbnailWidth-size[0])/2, (Constants.ThumbnailHeight-size[1])/2)
        #Resize(self, Size size, Point pos, int r=-1, int g=-1, int b=-1) -> Image
        im.Resize(wx.Size(Constants.ThumbnailWidth, Constants.ThumbnailHeight), pos, 202, 225, 255)
    else:
        oldWidth = size[0]
        oldHeight = size[1]
        newHeight = -1
        newWidth = -1
        aspectRatio = 1
        if oldHeight > oldWidth:
            newHeight = Constants.ThumbnailHeight
            aspectRatio = oldHeight/float(oldWidth)
        else:
            newWidth = Constants.ThumbnailWidth
            aspectRatio = oldWidth/float(oldHeight)
        
        if newHeight == Constants.ThumbnailHeight:
            newWidth = int(newHeight/float(aspectRatio))
            if not newWidth > 0:
                newWidth = Constants.ThumbnailWidth
        else:
            newHeight = int(newWidth/float(aspectRatio))
            if not newHeight > 0:
                newHeight = Constants.ThumbnailHeight
            
        im.Rescale(newWidth, newHeight, wx.IMAGE_QUALITY_HIGH)
        pos = wx.Point((Constants.ThumbnailWidth-newWidth)/2, (Constants.ThumbnailHeight-newHeight)/2)
        im.Resize(wx.Size(Constants.ThumbnailWidth, Constants.ThumbnailHeight), pos, 202, 225, 255)
    
    return im 


def GetCommaFormattedNumber(number):
    strNum = str(number)
    i = len(strNum)-1
    newNum = []
    j = 0
    while i >= 0:
        if j%3 == 0 and len(strNum) > i+1:
            newNum.insert(0, ",")
            j = 0
        
        j+= 1
        newNum.insert(0, strNum[i])
        i -= 1
        
    return ''.join(newNum)  
            
    

if __name__ == "__main__":
    #print GetMD5HashBucketID('8BA8BC04896C421A704282E9B87B5520')
    """
    imageFilePath = r'C:\FailedImages\c00014.png'
    thumbFile = r'C:\FailedImages\c00014Thumb.jpg'
    img = GetThumbnail(imageFilePath)
    img.SaveFile(thumbFile, wx.BITMAP_TYPE_ANY)
    """
    print GetCommaFormattedNumber(2345)