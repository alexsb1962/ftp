
import datetime as dt
import os
import ftplib

print('Start')

class ftpplus( ftplib.FTP):

    def listdir(self):
        ret=[]
        l=[]
        self.dir(lambda s: l.append(s))
        for s in l:
            dir=  s[0]=='d'
            fname = s[s.find(s.split()[8]):]
            ret.append((dir,fname))
    # похоже отдельный класс нафиг не нужен
    pass


def around(f,recursive=False,mustload=False):
    """
     Входной параметр - открытое ftp подключение
    :rtype: None
    """
    start_path=os.getcwd()

    dirlist = []
    f.dir(lambda s: dirlist.append(s))

    for s in dirlist:
        #todo имена файлов могут содержать пробелы
        fname=s[s.find(s.split()[8]) :]


        if fname == '.': continue
        if fname == '..': continue
        if s[0]=='d':
            print('Рекурсивный переход в ',fname)
            f.cwd(fname)
            try:
                os.mkdir(fname)
            except FileExistsError:
                pass
            if recursive
                os.chdir(fname)
                around(f,recursive)
                os.chdir('..')
                f.cwd('..')
        else:
            ext = fname.split('.')[-1]
            if ext == 'jpg' or ext == 'gif':
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



with ftplib.FTP(host='home.dimonius.ru',user='furry',passwd='letsgo' ) as f:
    # корневой каталог (начало работы)
    day=dt.datetime.today()
    dirname=str(day.year)+'_'+str(day.month)+'_'+str(day.day)
    dirname=dirname+'_T'+str(day.hour)+'_'+str(day.minute)+'_'+str(day.second)+'_'+str(day.microsecond)
    try:
        os.mkdir(dirname)
    except  FileExistsError:
        pass
    os.chdir(dirname)
    around(f,recursive=True,load=True)

print('The END')


