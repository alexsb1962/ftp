

import ftplib

print('Start')

def func(s):
    l=s.rsplit()
    d.append( l[-1] )

def around(f,folder=''):
    if folder=='':
        f.cwd('Furry_Archive/Logos')
    d = []
    f.dir(lambda s:d.append(s.split()[-1]))

    for entry in d:
        if entry=='.': continue
        if entry=='..': continue
        ext=entry.split('.')[-1]
        if ext=='jpg' or ext=='gif':
            # загрузка
            with open(entry, 'wb') as fp:
                f.retrbinary('RETR '+entry, fp.write)

with ftplib.FTP(host='home.dimonius.ru',user='furry',passwd='letsgo' ) as f:
    #создать папку
    around(f,'')


print(d)


