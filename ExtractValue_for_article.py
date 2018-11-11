# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 23:15:01 2018

@author: Юлия
"""

import gdal
import os
def GetIndexForNP(ds, coordinates):
    import math
    dataset=gdal.Open(ds)
    if dataset==None:
        raise Exception("ERROR: gdal can't open file, check the directory")
    if type(coordinates)!=list:
        raise Exception("ERROR: coordinates type is wrong! should be list")
    info=dataset.GetGeoTransform()
    FirstPixelCoordinates=[]
    FirstPixelCoordinates.append(info[0])
    FirstPixelCoordinates.append(info[3])
    PixelWidth=info[1]
    PixelHeight=info[5]
    CoordinateXDifference=coordinates[1]-FirstPixelCoordinates[1]
    CoordinateYDifference=coordinates[0]-FirstPixelCoordinates[0]
    PixelXIndex=math.ceil(CoordinateXDifference/PixelWidth)
    PixelYIndex=math.ceil(CoordinateYDifference/PixelHeight)
    if PixelXIndex<0:
        PixelXIndex=PixelXIndex*-1
    if PixelYIndex<0:
        PixelYIndex=PixelYIndex*-1
    CellIndexes=[PixelXIndex, PixelYIndex]
    return(CellIndexes)
print('Выберите режим: 1-пакетный, 2-отдельный файл')
mode = int(input())
if mode!=1 and mode!=2:
    raise Exception("Ошибка: неверный код режима")
if mode==1:
    print('Введите расположение папки с файлами:')
    directory = str(input())
    folder=os.listdir(directory)
    directories=[]
    for i in range (len(folder)):
        path=directory+'\\'+folder[i]                         
        directories.append(path)
        projection=[]
        for i in range (len(directories)):
            OpenedFile=gdal.Open(directories[i])
            if OpenedFile==None:
                raise Exception('Ошибка в чтении файла ' + directories[i])
            projection.append(OpenedFile.GetProjection())
            if i !=0:
                if projection[i]!=projection[0]:
                    raise Exception("Ошибка: один или несколько снимков находятся в разных проекциях. Для корректного ввода координат приведите данные к одной проекции")
    print('Введите координаты в формате "x,y":')
    into=[]
    into=(input()).split(',')
    coordinates=[]
    coordinates.append(float(into[0]))
    coordinates.append(float(into[1]))
    print('Введите имя выходного файла(вместе с его расположением):')
    name=str(input())
    with open (name, 'a') as outFile:
        outFile.write('Имя_файла   координаты   значение'+'\n')
    print('Введите значение ScaleFactor (если оно отсутствует, введите 1):')
    ScaleFactor=float(input())
    print('Идет запись файла...')
    for i in range (len(directories)):
        list_of_dir=directories[i].split('\\')
        FileName=list_of_dir[-1]
        indexes=GetIndexForNP(directories[i],coordinates)
        x=indexes[0]
        y=indexes[1]
        dataset=gdal.Open(directories[i])
        massive=dataset.GetRasterBand(1).ReadAsArray()
        value=massive[x][y]
        value_end=value*ScaleFactor
        with open (name, 'a') as outFile:
            outFile.write(str(FileName) + '   ' + str(coordinates[0])+','+str(coordinates[1]) + '   ' +str(value_end) + '\n')
    print('Файл успешно записан')
if mode==2:
    print('Введите расположение файла:') 
    path=str(input())
    OpenedFile=gdal.Open(path)
    if OpenedFile==None:
        raise Exception('Ошибка в чтении файла' + path)
    print('Введите координаты в формате "x,y":')
    into=[]
    into=(input()).split(',')
    coordinates=[]
    coordinates.append(float(into[0]))
    coordinates.append(float(into[1]))
    print('Введите значение ScaleFactor (если оно отсутствует, введите 1):')
    ScaleFactor=float(input())
    list_of_dir=path.split('\\')
    FileName=list_of_dir[-1]
    indexes=GetIndexForNP(path,coordinates)
    x=indexes[0]
    y=indexes[1]
    dataset=gdal.Open(path)
    massive=dataset.GetRasterBand(1).ReadAsArray()
    value=massive[x][y]
    value_end=value*ScaleFactor
    print('Вывести результат в консоль - введите 1, записать результат в файл - введите 2:' )
    mode2 = int(input())
    if mode2!=1 and mode!=2:
        raise Exception("Ошибка: неверный код режима")
    if mode2==1:
        print('Имя_файла   координаты   значение')
        print(str(FileName) + '   ' + str(coordinates) + '   ' +str(value_end))
    if mode2==2:
        print('Введите имя выходного файла(вместе с его расположением):')
        name=str(input())
        print('Идет запись файла...')
        with open (name, 'a') as outFile:
            outFile.write('Имя_файла   координаты   значение'+'\n')
            outFile.write(str(FileName) + '   ' + str(coordinates[0])+','+str(coordinates[1]) + '   ' +str(value_end) )
        print('Файл успешно записан')
        