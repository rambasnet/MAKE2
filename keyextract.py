import os
import shutil
import string
import re
import time

#User Input
msg_Folder_Path = "E:\\mailtest\\Emails\\Messages"
result_Dir_Path = "E:\\search Results"
file_Name = "E:\\keywords.txt"

#auto Input
key_List = []
find_Word = 'Attachments:'
attach_Exp = re.compile(find_Word,re.IGNORECASE)

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
            
    TimeElapsed += '%.1f' %secs + " secs "
    return TimeElapsed


def emailAttachmentMapping(msg_File,attach_Files,file_Path):
    attached_FileName = []

    file_Handler = open(file_Path+'\\'+msg_File,'r')

    for each_Line in file_Handler.readlines():
        if attach_Exp.findall(each_Line):
            attached_FileName = each_Line.strip('Attachments:').strip('\n').split(',')

    file_Handler.close()

    for each_Attached_FileName in attached_FileName:
        each_Attached_FileName = each_Attached_FileName.strip(' ')

        for attach_FileNames in attach_Files:
            if attach_FileNames.find(each_Attached_FileName) != -1:
                target_File_Fields = attach_FileNames.split('-')

                fileName_Fields = msg_File.split('-')

                if target_File_Fields[0] == fileName_Fields[0] and target_File_Fields[1] == fileName_Fields[1] and target_File_Fields[2] == fileName_Fields[2]:
                    if target_File_Fields[len(target_File_Fields)-1].strip(' ') == each_Attached_FileName or target_File_Fields[len(target_File_Fields)-2].strip(' ') == each_Attached_FileName:
                        return attach_FileNames
                    else:
                        return 'No Attachments'
                else:
                    return 'No Attachments'


def pre_Email_Mapping(email,file_Path):
    att_Folder_Path = '..\\Attachments'
    os.chdir(att_Folder_Path)

    attachments = []
    
    for attachment_Contents in os.walk(file_Path):
        for each_Contents in attachment_Contents[2]:
            attachments.append(each_Contents)

    os.chdir(msg_Folder_Path)
    
    if len(attachments) != 0:
        mapped_FileName = emailAttachmentMapping(email,attachments,file_Path)
        return mapped_FileName
    else:
        return 'No Attachments'


"""
Ram: I've put all the lines below this into the DoIt funtion as it is
    so that I can call it from the interface module
"""
def DoIt():
    start_Time = time.time()
    ti1 = str(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()))

    for keyword in open(file_Name,"r"):
        key_List.append(keyword.strip('\n'))


    os.chdir(msg_Folder_Path)
    for files in os.walk('.\\'):
        test_Dir = files[0].strip('.').strip(' ').split('\\')

        for messages in files[2]:
            infile_Path = files[0] + '\\' + messages

            print 'Working on --->  ' + messages

            infile = open(infile_Path,"r")
            file_Buf = infile.readlines()
            infile.close()

            for key in key_List:
                key_Exp = re.compile(key,re.IGNORECASE)

                for each_Lines in file_Buf:
                    if key_Exp.findall(each_Lines):
                        key_Msg_Dir = result_Dir_Path + '\\Messages' + files[0].strip('.') + '\\' + key
                        key_Attach_Dir = result_Dir_Path + '\\Attachments' + files[0].strip('.') + '\\' + key

                        if not os.path.exists(key_Msg_Dir):
                            os.makedirs(key_Msg_Dir)
                            
                        outfile_Path = key_Msg_Dir + '\\' + messages
                        shutil.copyfile(infile_Path,outfile_Path)

                        attachment_Mapping = pre_Email_Mapping(messages,files[0])

                        if attachment_Mapping != 'No Attachments':
                            os.chdir('..\\Attachments')
                            attachment_Path = files[0] +'\\'+ attachment_Mapping
                            output_Path = key_Attach_Dir + '\\' + attachment_Mapping

                            if not os.path.exists(key_Attach_Dir):
                                os.makedirs(key_Attach_Dir)

                            shutil.copyfile(attachment_Path,output_Path)
                            os.chdir(msg_Folder_Path)

                        break
                    


    end_Time = time.time()
    ti2 = str(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()))

    time_Diff = (end_Time - start_Time)

    time_Taken = ConvertSecondsToDayHourMinSec(time_Diff)

    print ti1
    print ti2
    print time_Taken


    print 'Keyword Search Done'
