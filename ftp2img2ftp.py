# -*- coding: utf8 -*-
import datetime as dt
import os
import sys
import argparse
import ftplib

print('Start')


class ftpplus(ftplib.FTP):
    pass


def around(f, recursive=False, mustload=False):
    """
     Входной параметр - открытое ftp подключение
    :rtype: None
    """
    start_path = os.getcwd()

    for elem in f.mlsd():

        fname, dict = elem

        if dict['type'] == 'pdir': continue
        if dict['type'] == 'cdir': continue
        if dict['type'] == 'dir':
            print('Переход в ', start_path + '\\' + fname)
            try:
                f.cwd(fname)
            except:
                print('Безуспешный переход ', start_path, '\\', fname)
                exit(0)
            try:
                os.mkdir(fname)
            except FileExistsError:
                pass
            if recursive:
                os.chdir(fname)
                around(f, recursive)
                os.chdir('..')
                f.cwd('..')
        if dict['type'] == 'file':
            ext = fname.split('.')[-1]
            if ext == 'jpg' or ext == 'gif':
                # загрузка
                with open(fname, 'wb') as fp:
                    try:
                        if mustload:
                            print('Загрузка ', start_path + '/' + fname)
                            f.retrbinary('RETR ' + fname, fp.write)
                        else:
                            print('Имитация загрузки ', start_path + '\\' + fname)
                    except:
                        print('Не возможно принять файл ' + fname)
                        print(s)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-url', default='home.dimonius.ru')
    parser.add_argument('-l', default='')
    parser.add_argument('-d', default='')
    parser.add_argument('-u', default='furry')
    parser.add_argument('-p', default='letsgo')
    names = parser.parse_args()
    user_name = names.u
    url = names.url
    password = names.p
    local = names.l
    nlocal = names.d

    try:
        f = ftpplus()
        f.encoding = 'utf-8'
        f.connect(host=url)
        f.login(user=user_name, passwd=password)

        response = f.sendcmd('TYPE A')
        response = f.sendcmd('FEAT')
        if not 'UTF8' in response:
            print('Не найдена поддержка UTF8')
            exit(0)
        else:
            print('Найдена поддержка UTF8')
            resp = f.sendcmd('CLNT')
            resp = f.sendcmd('OPTS UTF8 ON')

        f.set_pasv(True)

        # корневой каталог (начало работы)
        if nlocal:
            try:
                f.cwd(nlocal)
            except:
                print('Не удалось перейти на ', nlocal)
            finally:
                exit(0)
        if local:
            dirname = local
        else:
            day = dt.datetime.today()
            dirname = str(day.year) + '_' + str(day.month) + '_' + str(day.day)
            dirname = dirname + '_T' + str(day.hour) + '_' + str(day.minute) + '_' + str(day.second) + '_' + str(
                day.microsecond)
        try:
            os.mkdir(dirname)
        except  FileExistsError:
            pass
        os.chdir(dirname)

        around(f, recursive=True, mustload=True)

    finally:
        pass
    print('The END')

else:
    pass
