'''****************************************************************************/
/*************************** Research project *********************************/
/*************************** Author: MadhuKumar *******************************/
/************************** Date: April 3 2008 ********************************/
/******************** Modified: April 14 2008 11:55 AM *************************/
/** Description: The program is to create a webpage for the email verification*/
/********** and associating corresponding emails with its attachments *********/
/****************************************************************************'''

# importing the library to use the modules in our program
import os
import string
import re
import urllib
import time

#User Input
msg_Folder_Path = "E:\\search Results\\Messages"
att_Folder_Path = "E:\\search Results\\Attachments"

#Auto Input
msg_HTML_Dir = "..\\html\\msg\\"
att_HTML_Dir = "..\\html\\att\\"
find_Word = 'Attachments:'
attach_Exp = re.compile(find_Word,re.IGNORECASE)


# This function finds the files attached to the corresponding email files
def emailAttachmentMapping(msg_File,attach_Files,file_Path):
    found_Files = []

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
                        found_Files.append(attach_FileNames)
                        
    return found_Files


def pre_Email_Mapping(email,file_Path):
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
        return attachments


# This function converts total number of seconds to time taken
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


def create_OpenPage():
    if not os.path.exists('..\\html'):
        os.makedirs('..\\html\\msg')
        os.makedirs('..\\html\\att')

    page_Title = msg_Folder_Path.strip('\\n').split('\\')

    indexPage_Filename = '..\\html\\verify.html'
    indexPage_File = open(indexPage_Filename,'w')
    indexPage_File.write('<html><head><title>EmailSearch</title></head>'+'\n')
    indexPage_File.write('<frameset rows="*" cols="15%,*" framespacing="0" frameborder="yes" border="3">'+'\n')
    indexPage_File.write('<frame src=".\\msg\\'+page_Title[len(page_Title)-1]+'.html" name="leftFrame" scrolling="yes" noresize="noresize" id="leftFrame" title="messagesFrame" />'+'\n')
    indexPage_File.write('<frameset rows="60%,*" cols="*" framespacing="0" frameborder="yes" border="3">'+'\n')
    indexPage_File.write('<frame src="righttop.html" name="righttopFrame" scrolling="yes" id="righttopFrame" title="righttopFrame" />'+'\n')
    indexPage_File.write('<frame src="rightbot.html" name="rightbotFrame" scrolling="yes" id="rightbotFrame" title="rightbotFrame" />'+'\n')
    #
    #indexPage_File.write('<frameset rows="*" cols="50%,*" framespacing="0" frameborder="yes" border="3">'+'\n')
    #indexPage_File.write('<frame src="rightbotleft.html" name="rightbotleftFrame" scrolling="yes" id="rightbotleftFrame" title="rightbotleftFrame" />'+'\n')
    #indexPage_File.write('<frame src="rightbotright.html" name="rightbotrightFrame" scrolling="yes" id="rightbotrightFrame" title="rightbotrightFrame" />'+'\n')
    #
    indexPage_File.write('</frameset>'+'\n')
    indexPage_File.write('<noframes><body></body></noframes></html>'+'\n')
    indexPage_File.close()

    indexPage_Filename = '..\\html\\righttop.html'
    indexPage_File = open(indexPage_Filename,'w')
    indexPage_File.write('<html><head><title>Emails Information Display Window</title></head><body>'+'\n')
    indexPage_File.write('<p><B><I> Email information display Pane </I></B></P>'+'\n')
    indexPage_File.write('</body></html>'+'\n')
    indexPage_File.close()


    indexPage_Filename = '..\\html\\rightbot.html'
    indexPage_File = open(indexPage_Filename,'w')
    indexPage_File.write('<html><head><title>Emails Information Display Window</title></head><body>'+'\n')
    indexPage_File.write('<p><B><I> Email Listing Display pane </I></B></P>'+'\n')
    indexPage_File.write('</body></html>'+'\n')
    indexPage_File.close()

    #
    #indexPage_Filename = '..\\html\\rightbotright.html'
    #indexPage_File = open(indexPage_Filename,'w')
    #indexPage_File.write('<html><head><title>Emails Attachment Display Window</title></head><body>'+'\n')
    #indexPage_File.write('<p><B><I> Email Attachment Listing Display pane </I></B></P>'+'\n')
    #indexPage_File.write('</body></html>'+'\n')
    #indexPage_File.close()
    #
    

def create_Interface():
    start_Time = time.time()
    ti1 = str(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()))

    os.chdir(msg_Folder_Path)
    create_OpenPage()

    count = 0
    file_Count = 0

    for files in os.walk('.\\'):
        temp = files[0].strip('.').strip('\\').split('\\')
        temp_FileName = ''

        if count == 0:
            page_Title = msg_Folder_Path.strip('\\n').split('\\')
            temp_FileName = msg_HTML_Dir+page_Title[len(page_Title)-1]+'.html'
            #print temp_FileName
            temp_File = open(temp_FileName,'w')
            temp_File.write('<html><head><title>MessageIndex</title></head><body>'+'\n')
            temp_File.write('<a href="..\\verify.html" target="_parent"> Home </a><br>'+'\n')
            temp_File.write('<B>Click for Contents</B><br><br>')

            for directory in files[1]:
                temp_File.write('<a href=".\\'+directory+'.html" target="rightbotFrame">'+directory+'<br>\n')
            temp_File.close()
            count = 1
        else:
            for names in temp:        
                temp_FileName = temp_FileName + names

            temp_FileName = msg_HTML_Dir+temp_FileName+'.html'
            temp_File = open(temp_FileName,'w')

            for directory in files[1]:
                temp_File.write('<a href=".\\'+temp_FileName.strip(msg_HTML_Dir)+directory+'.html" target="rightbotFrame">'+directory+'<br>\n')

            for messages in files[2]:
                file_Count = file_Count + 1
                attachment_Mapping = pre_Email_Mapping(messages,files[0])

                if len(attachment_Mapping) != 0:
                    temp_File.write('<a href="..\\..\\'+ page_Title[len(page_Title)-1] + files[0].strip('.') + '\\' + messages+'" target="righttopFrame">'+messages+'</a>&#x9; Attachments ===>\n')
                    for each_Attachment in attachment_Mapping:
                        att_Folder = att_Folder_Path.split('\\')
                        temp_File.write('&#x9; '+ '<a href="..\\..\\'+ att_Folder[len(att_Folder)-1] + files[0].strip('.') + '\\' + each_Attachment +'" target="righttopFrame">'+each_Attachment+'</a>&#x9;\n')
                    temp_File.write('\n')
                else:
                    temp_File.write('<a href="..\\..\\'+ page_Title[len(page_Title)-1] + files[0].strip('.') + '\\' + messages+'" target="righttopFrame">'+messages+'</a><br>\n')
            
            temp_File.close()
    end_Time = time.time()
    ti2 = str(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()))

    time_Diff = (end_Time - start_Time)

    time_Taken = ConvertSecondsToDayHourMinSec(time_Diff)

    print ti1
    print ti2
    print time_Taken


    print 'Email Mapping is Done'

            
if __name__ == "__main__":
    
    create_Interface()

    