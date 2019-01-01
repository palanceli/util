# -*- coding:utf-8 -*-

import logging
import os
import unittest
import hashlib

## 长期备份会产生一些重复文件，此代码遍历目标目录root，记录所有文件的[md5, 尺寸, 路径]，并按尺寸降序排序

class FileInfoSpider(object):
    def __init__(self, root):
        self.root = root
        self.data = []  # [[md5, size, path], *]

    def calcMd5(self, filePath):
        ml = hashlib.md5()
        try:
            with open(filePath, 'rb') as f:
                ml.update(f.read())
                md5 = ml.hexdigest()
                return md5
        except:
            logging.error('FAILED to proc : %s' % filePath)

    def MainProc(self, outFile):
        i = 0
        for root, dirs, files in os.walk(self.root):
            for name in files:
                filePath = os.path.join(root, name)
                fileSize = os.path.getsize(filePath)
                # if fileSize < 1024 * 1024 * 100:
                    # continue
                fileMd5 = self.calcMd5(filePath)
                self.data.append([fileMd5, fileSize, filePath])
                self.data.sort(key=lambda item:item[1])

        with open(outFile, 'w') as f:
            for item in self.data:
                f.write('%s %8.2fM %s\n' % (item[0], item[1] * 1.0 / 1024 / 1024, item[2]))

    def Print(self):
        for item in self.data:
            logging.debug('%s %8.2fM %s' % (item[0], item[1] * 1.0 / 1024 / 1024, item[2]))

class FileInfoParser(object):
    def __init__(self, infoFilePath):
        self.infoFilePath = infoFilePath

    def MainProc(self):
        lastItems = None
        lastLine = None
        with open(self.infoFilePath) as f:
            for line in f:
                line = line.strip()
                items = line.split(' ')
                if not lastItems is None:
                    if lastItems[0] == items[0]:
                        if os.path.exists(lastItems[-1]) and os.path.exists(items[-1]):
                            print(lastLine)
                            print(line)
                lastItems = items
                lastLine = line

class MainApp(unittest.TestCase):
    def setUp(self):
        logFmt = '%(asctime)s %(lineno)04d %(levelname)-8s %(message)s'
        logging.basicConfig(level=logging.DEBUG, format=logFmt, datefmt='%H:%M',)

    def tcSaveInfo(self):
        root = '/Volumes/WDMini/2018'
        outFile = 'out.txt'
        # root = '/Users/palance/Documents/Github/libei_private'
        fileInfoSpider = FileInfoSpider(root)
        fileInfoSpider.MainProc(outFile)

    def tcParseInfo(self):
        infoFilePath = 'out.txt'
        fileInfoParser = FileInfoParser(infoFilePath)
        fileInfoParser.MainProc()

if __name__ == '__main__':
    logFmt = '%(asctime)s %(lineno)04d %(levelname)-8s %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=logFmt, datefmt='%H:%M',)
    unittest.main()
    # cmd: python -m main Main.case1
