import requests
import os
import sys
import getopt
from PyPDF2 import PdfFileMerger
import warnings

merger = PdfFileMerger(strict=False)


class Paper(object):

    def __init__(self, year, month, day):
        self.year = '%04d' % year
        self.month = '%02d' % month
        self.day = '%02d' % day
        self.d = self.year+self.month+self.day
        self.base_url = 'http://paper.people.com.cn/rmrb/page/'
        self.size = 0

    def get_pdf(self, url, filename):
        r = requests.get(url)
        if not r.ok:
            return r.ok
        with open(filename, "wb") as f:
            f.write(r.content)
        pdf_size = len(r.content)/1000000
        self.size += pdf_size
        print('    Retrieving page: '+filename +
              '  |  size: ' + str(round(pdf_size, 2)) + 'mb')
        return r.ok

    def get_page(self, pagenum):
        pagenum = '%02d' % pagenum
        p = self.d+'/rmrb'+self.d+pagenum+'.pdf'
        if not os.path.exists(self.d):
            os.mkdir(self.d)
        pageurl = ''.join([
            self.base_url, self.year, '-',
            self.month, '/', self.day, '/',
            pagenum, '/rmrb', self.d, pagenum, '.pdf'])
        return self.get_pdf(pageurl, p), p

    def get_paper(self):
        print('Downloading pages into temporary directory ...')
        i = 1
        l = []
        while True:
            ok, p = self.get_page(i)
            if not ok:
                break
            l.append(p)
            merger.append(p)
            i += 1

        print('Combining pages ...')
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            merger.write('-'.join([self.year, self.month, self.day])+'.pdf')
            merger.close()

        print('Deleting temporary directory ...')

        for pdf in l:
            os.remove(pdf)

        os.rmdir(self.d)

        print('Done. Total size ' + str(round(self.size, 2)) + 'mb.')


def main():
    opts, args = getopt.getopt(sys.argv[1:], 'd:', ['date='])
    for o, a in opts:
        if o in ['-d', '--date']:
            x = a.split('.')
            year = int(x[0])
            month = int(x[1])
            day = int(x[2])
    p = Paper(year, month, day)
    p.get_paper()


def test():
    pass


if __name__ == '__main__':
    main()
