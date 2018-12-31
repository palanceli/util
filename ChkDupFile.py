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

    def MainProc(self):
        for root, dirs, files in os.walk(self.root):
            for name in files:
                filePath = os.path.join(root, name)
                fileSize = os.path.getsize(filePath)
                if fileSize < 1024 * 1024 * 10:
                    continue
                fileMd5 = self.calcMd5(filePath)
                self.data.append([fileMd5, fileSize, filePath])
                self.data.sort(key=lambda item:item[1])

    def Print(self):
        for item in self.data:
            logging.debug('%s %8.2fM %s' % (item[0], item[1] * 1.0 / 1024 / 1024, item[2]))


class MainApp(unittest.TestCase):
    def setUp(self):
        logFmt = '%(asctime)s %(lineno)04d %(levelname)-8s %(message)s'
        logging.basicConfig(level=logging.DEBUG, format=logFmt, datefmt='%H:%M',)

    def tcMain(self):
        root = '/Volumes/WD/典藏'
        # root = '/Users/palance/Documents/Github/libei_private'
        fileInfoSpider = FileInfoSpider(root)
        fileInfoSpider.MainProc()
        fileInfoSpider.Print()

if __name__ == '__main__':
    logFmt = '%(asctime)s %(lineno)04d %(levelname)-8s %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=logFmt, datefmt='%H:%M',)
    unittest.main()
    # cmd: python -m main Main.case1
