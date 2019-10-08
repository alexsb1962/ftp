# -*- coding: utf8 -*-
import datetime as dt
import os
import sys
import ftplib

print('Start')

class ftpplus( ftplib.FTP):


    def feat(self,func=None):
        cmd = 'FEAT'
        func = None
        self.retrlines(cmd, func)



def around(f,recursive=False,mustload=False):
    """
     Входной параметр - открытое ftp подключение
    :rtype: None
    """
    start_path=os.getcwd()


    for elem in f.mlsd():

        fname=''
        fname,dict=elem
        #fname=fname.encode('latin-1').decode('utf-8')


        if dict['type'] == 'pdir': continue
        if dict['type'] == 'cdir': continue
        if dict['type']=='dir':
            print('Рекурсивный переход в ',start_path+'\\'+fname)
            try:
                f.cwd(fname)
            except:
                print(fname,'--',len(fname))
                print(fname.encode('latin-1').decode('utf-8'))
                exit(0)
            try:
                os.mkdir(fname)
            except FileExistsError:
                pass
            if recursive:
                os.chdir(fname)
                around(f,recursive)
                os.chdir('..')
                f.cwd('..')
        if dict['type']=='file':
            ext = fname.split('.')[-1]
            #if ext == 'jpg' or ext == 'gif':
            if ext == 'jpg1' or ext == 'gif1':
                # загрузка
                with open(fname, 'wb') as fp:
                    try:
                        if mustload:
                            print('Попытка загрузки ', start_path + '/' + fname)
                            f.retrbinary('RETR ' + fname, fp.write)
                        else:
                            print('Имитация загрузки ', start_path + '/' + fname)
                    except:
                        print('Не возможно принять файл '+fname)
                        print(s)



try:

    f=ftpplus()
    f.encoding = 'utf-8'
    f.connect(host='home.dimonius.ru')
    f.login(user='furry',passwd='letsgo')

    response=f.sendcmd('TYPE A')
    response=f.sendcmd('FEAT')
    if not 'UTF8' in response:
        print('Не найдена поддержка UTF8')
        exit(0)
    else:
        print('Найдена поддержка UTF8')
        resp = f.sendcmd('CLNT')
        resp = f.sendcmd('OPTS UTF8 ON')

    f.set_pasv(True)


    f.cwd('//Furry_Archive//Art//Brian Wear/')



    names=[]
    for lst in f.mlsd():
        name,attrs=lst
        names.append(name)

    name=names[-1]
    print(name)
    f.cwd(name)
    exit(0)

    # корневой каталог (начало работы)
    day=dt.datetime.today()
    dirname=str(day.year)+'_'+str(day.month)+'_'+str(day.day)
    dirname=dirname+'_T'+str(day.hour)+'_'+str(day.minute)+'_'+str(day.second)+'_'+str(day.microsecond)
    try:
        os.mkdir(dirname)
    except  FileExistsError:
        pass
    os.chdir(dirname)
    around(f,recursive=True,mustload=False)

finally:
    pass
print('The END')


