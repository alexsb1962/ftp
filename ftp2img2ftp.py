
import datetime as dt
import os
import ftplib

print('Start')


def around(f):
    """
     Входной параметр - открытое ftp подключение
    :rtype: None
    """
    start_path=os.getcwd()

    dirlist = []
    f.dir(lambda s: dirlist.append(s))

    for s in dirlist:
        #todo имена файлов могут содержать пробелы
        words=s.split() # начиная с девятого элемента выдачи list
        fname=s[s.find(s.split()[8]) :]


        if fname == '.': continue
        if fname == '..': continue
        if s[0]=='d':
            print('Переход в ',fname,' с рекурсивным вызовом')
            f.cwd(fname)
            try:
                os.mkdir(fname)
            except FileExistsError:
                pass
            os.chdir(fname)
            around(f)
            os.chdir('..')Л
            f.cwd('..')
        else:
            ext = fname.split('.')[-1]
            if ext == 'jpg' or ext == 'gif':
                # загрузка
                with open(fname, 'wb') as fp:
                    try:
                        f.retrbinary('RETR ' + fname, fp.write)
                    except:
                        print('Не возможно принять файл '+fname)
                        print(s)

with ftplib.FTP(host='home.dimonius.ru',user='furry',passwd='letsgo' ) as f:
    # корневой каталог (начало работы)
    day=dt.datetime.today()
    dirname=str(day.day)+'_'+str(day.month)+'_'+str(day.year)
    dirname=dirname+'T'+str(day.hour)+'_'+str(day.minute)+'_'+str(day.second)+'_'+str(day.microsecond)
    try:
        os.mkdir(dirname)
    except  FileExistsError:
        pass
    os.chdir(dirname)
    around(f)

print('The END')


