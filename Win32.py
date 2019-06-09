import sys

import win32file, win32api, pywintypes

import struct


IOCTL_DISK_GET_DRIVE_GEOMETRY = 7<<16

def GetDistGeometry(s):
    """Cylinders, MediaType, TracksPerCylinder, SectorsPerTrack, BytesPerSector"""
    return struct.unpack("QIIII", s)


class Win32RAWIO:
    def __init__(self, device, mode='r'):
        if 'w' in mode or '+' in mode:
            modes = win32file.GENERIC_READ|win32file.GENERIC_WRITE
        else:
            modes = win32file.GENERIC_READ
        
        try:
            self.iohandle = win32file.CreateFile(
                device,
                modes,
                win32file.FILE_SHARE_READ|win32file.FILE_SHARE_WRITE,
                None,
                win32file.OPEN_EXISTING,
                win32file.FILE_ATTRIBUTE_READONLY|win32file.FILE_FLAG_RANDOM_ACCESS,
                None
            )
            
            diskGeometry = win32file.DeviceIoControl(
                self.iohandle,
                IOCTL_DISK_GET_DRIVE_GEOMETRY,
                '',
                24,
                None
            )
            #~ win32file.GetDiskFreeSpaceEx(device)
        except pywintypes.error, e:     #convert exceptions
            raise IOError(str(e))
        
        self.cylinders, self.mediatype, self.trackspercylinder, self.sectorspertrack, self.bytespersector = GetDistGeometry(diskGeometry)
       
        self.blocksize = self.bytespersector
        #total size of the physical device not the logical drive size...
        self.size = self.cylinders*self.trackspercylinder*self.sectorspertrack*self.bytespersector #size sometimes missreported by win...
        self.offset = 0
        #self.ActualSize = win32file.GetFileSize(self.iohandle)
        
    def seek(self, position, origin=0):
        if origin == 0:
            self.offset = position
        elif origin == 1:
            self.offset += position
        elif origin == 2:
            self.offset = self.size - position
        
        if self.offset >= self.size:
            self.offset = self.size
        
        #~ win32file.SetFilePointer(self.iohandle, position, win32file.FILE_BEGIN)

    def tell(self):
        return self.offset
        #~ return win32file.SetFilePointer(self.iohandle, 0, win32file.FILE_CURRENT)
    
    def read(self, size):
        #clip at the end of the file
        if self.offset + size > self.size:
            size = max(0, self.size - self.offset)
        #calculate in blocks
        start_block = self.offset / self.blocksize              #starting sector
        start_offset = self.offset % self.blocksize             #offset of desired data in sector
        num_blocks = (start_offset + size) / self.blocksize     #rounded down number of required sectors
        if (start_offset + size) % self.blocksize:              #check if req data is in the next sector too
            num_blocks += 1
        #seek to the strt cluster and read
        win32file.SetFilePointer(self.iohandle, start_block*self.blocksize, win32file.FILE_BEGIN)
        rc, data = win32file.ReadFile(self.iohandle, int(self.blocksize*num_blocks))
        #adjust filepos
        self.offset += size
        #return only requested data
        return data[start_offset:start_offset+size]
        
    def write(self, data):
        size = len(data)
        start_block = self.offset / self.blocksize              #starting sector
        start_offset = self.offset % self.blocksize             #offset of desired data in sector
        num_blocks = (start_offset + size) / self.blocksize     #rounded down number of required sectors
        if (start_offset + size) % self.blocksize:              #check if req data is in the next sector too
            num_blocks += 1
        #~ print start_block, num_blocks
        
        win32file.SetFilePointer(self.iohandle, start_block*self.blocksize, win32file.FILE_BEGIN)
        rc, sdata = win32file.ReadFile(self.iohandle, int(self.blocksize*num_blocks))
        
        data = ''.join([sdata[:start_offset], data, sdata[start_offset+size:]])
        print repr(sdata), len(data)
        print repr(data), len(data)
        win32file.SetFilePointer(self.iohandle, start_block*self.blocksize, win32file.FILE_BEGIN)
        rc, data = win32file.WriteFile(self.iohandle, data)

    def close(self):
        if self.iohandle is not None:
            win32file.CloseHandle(self.iohandle)
            self.iohandle = None
            self.size = 0

    def flush(self):
        pass

#rootPath is root drive such as C:\\ or F:\\
#returns tuple of freespace and total drive size in bytes
def GetDiskFreeSpace(rootPath):
    return win32api.GetDiskFreeSpace(rootPath)
    """
    driveSize = c*spc*bps
    freeSpace = fc*spc*bps
    return (freeSpace, driveSize)
    """
    
def GetWin32LogicalDrives():
    things = []
    drives=win32api.GetLogicalDriveStrings()
    #print drives
    #drivesLetter = drives.split('\0')
    """
    for letter in drivesLetter:
        if letter:
            print "%s info: %s" %(letter, win32api.GetVolumeInformation(letter))
    """      
    things.extend([ r'\\.\%s:' % letter[0] for letter in drives.split('\0') if letter])
    #how to get valid number from the os?
    for i in range(5):
        things.append(r'\\.\PhysicalDrive%d' % i)
    return things

def GetWin32LogicalDrivesForDisplay():
    driveList = []
    detailList = []
    drives=win32api.GetLogicalDriveStrings()
    #print drives
    #drivesLetter = drives.split('\0')

    driveList.extend([ '%s:\\' % letter[0] for letter in drives.split('\0') if letter])
    for drive in driveList:
        try:
            volumeSet = win32api.GetVolumeInformation(drive)
            #print volumeSet
            detailList.append("%s - %s [%s]"%(drive, volumeSet[0], volumeSet[4]))
        except:
            detailList.append("%s"%drive)
    return detailList
    
def GetFileAttributes(fileName):
    print win32file.GetFileAttributesW(fileName)
    #return fileAttributes


if __name__ == '__main__':
    
    import time
    win32file.SetVolumeMountPoint("C:\\MountPoint\\", "C:\\NMT\\Research\\DiskImages\\thumb.dd\\")
    #win32file.DeleteVolumeMountPoint("C:\\MountPoint\\")
        
    """
    rfin = Win32RAWIO(r'\\.\C:\NMT\Research\DiskImages\thumb.dd', 'r')
    print "size %dB  %.2fMB" % (rfin.size, rfin.size/1024./1024)
    print "Cylinders = %s"%rfin.cylinders
    print "Mediatype = %s"%rfin.mediatype
    
    rfin.close()
    """
    
    #import TextCat.AnchorParser
    #print GetWin32LogicalDrives()
    #print win32api.GetLogicalDrives()
    #print win32api.GetLogicalDriveStrings()
    #print GetLogicalDriveSize(r"\\.\E:")
    #print win32api.GetVolumeInformation("C:\\")
    #print win32api.GetDiskFreeSpace("C:\\")
    #file attributes works...needs to use to to get the file attribures on fileviewer
    #print win32file.GetFileAttributes('C:\\AUTOEXEC.BAT')
    #print GetWin32LogicalDrivesForDisplay()
    #rfin = Win32RAWIO(r'\\.\F:\\', 'r')
    #print rfin.read(20)
    #rfin.close()
    
    #try:
        #wout = Win32RAWIO(r'\\.\F:\Hello.txt', 'w')
        #wout.write('hell0')
        #wout.commit()
    
    """
    rfin = Win32RAWIO(r'\\.\M:', 'r')
    print "size %dB  %.2fMB" % (rfin.size, rfin.size/1024./1024)
    print "Cylinders = %s"%rfin.cylinders
    print "Mediatype = %s"%rfin.mediatype
    print "Tracks/Cylinder = %s"%rfin.trackspercylinder
    print "Sectors/Track = %s"%rfin.sectorspertrack
    print "Bytes/Sector = %s"%rfin.bytespersector
    size = rfin.cylinders*rfin.trackspercylinder*rfin.sectorspertrack*rfin.bytespersector
    print "size=%s"%(size)
    print "sized = %dB"%size
    #print "Actual size=%s"%rfin.ActualSize
    rfin.close()
    """
  
    
    
    
    """
    #fin = open(r'\\.\F:\\Abstract.doc', 'rb')   
    #print win32file.GetFileSize(fin)
    #print fin.read(20)
    #fin.close()
    
   
        rfout = open("C:\\MyE.dd", 'w+b')
        print "Startime = %s"%time.asctime()
        while True:
            data = rfin.read(1024*1024)
            if len(data) == 0:
                break
            rfout.write(data)
       
        rfin.close()
        rfout.close()
        print "Endtime = %s"%time.asctime()
        
        
    except:
        print "Exception occured: %s"%sys.exc_info()[0]
     
   
    
    #print GetFileAttributes(r'\\.\C:\dlbu.lgo')
    print win32file.GetFileAttributes('C:\\AUTOEXEC.BAT')
    print win32api.GetFileAttributes('C:\\AUTOEXEC.BAT')
    #print win32file.GetFileSize('C:\\AUTOEXEC.BAT')
    print win32file.GetDriveType('D:')
    
    
    r = Win32RAWIO(r'\\.\F:', 'r')
    #r = Win32RAWIO(r'\\.\physicaldrive1', 'r')
    
    
    print r.tell()
    r.seek(512)
    print r.tell()
    #~ r.seek(0)
    #~ print r.tell()
    
    print r.read(512)
    
    #~ f = hexedit.BinFile(r)
    #~ print f.read(0,512)
    #~ for offset, block in f.blockReader(0, 16, 512):
        #~ print formater.format(offset, block)

    #!!DANGER!!  !!DANGER!!  !!DANGER!!  !!DANGER!!  !!DANGER!!
    #~ f.write(7, 'hello')
    #~ f.commit()
    #~ r.flush()
    """