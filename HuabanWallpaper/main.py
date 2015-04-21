#! /usr/bin/env python
#! encoding:utf-8
# Filename: main.py
# Find help at 'http://conglang.github.io/2015/04/18/scrapy-huaban-wallpaper/'

from Tkinter import *
import sys, os, random
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals, project
from scrapy.settings import Settings
sys.path.append("huaban")
from huaban.spiders.huabanSpider import huabanSpider
from huaban.spiders.downloadSpider import downloadSpider
from huaban import settings
from billiard import Process
import urllib
from gi.repository import Gio
import platform
import re

# ------------------------------------------------
# gui setting
# ------------------------------------------------
# set up canvas
root = Tk()
root.title("HuabanWallpaper")

# entry for enter board url
url_text = StringVar()
url_entry = Entry(root, width=30, textvariable=url_text)
url_entry.pack()

# button to apply board url and start crawling
def crawling_all_pics():
    start_crawling(url_text.get())
Button(root, text="Apply",command=crawling_all_pics).pack()

# button for download all picture
def download_all_pics():
    start_downloading("pic_urls", False)
Button(root, text="Download Board", command=download_all_pics).pack()

# button for randomly choose a picture as wallpaper
def shuffle_wallpaper():
    start_downloading("pic_urls", True)
    set_wallpaper()
Button(root, text="Shuffle Wallpaper", command=shuffle_wallpaper).pack()
# ------------------------------------------------
# scrapy setting
# ------------------------------------------------
# start log
log.start()

# to avoid ReactorNotRestartable issue
class UrlCrawlerScript(Process):
    def __init__(self, spider):
        Process.__init__(self)
        setting = Settings()
        setting.setmodule(settings,1)
        self.crawler = Crawler(setting)

        if not hasattr(project, 'crawler'):
            self.crawler.configure()
            self.crawler.signals.connect(reactor.stop, signal = signals.spider_closed)
        self.spider = spider

    def run(self):
        self.crawler.crawl(self.spider)
        self.crawler.start()
        reactor.run()

# start collecting all picture urls from inputed board
# and store them in a xml file
def start_crawling(url):
    spider = huabanSpider(domain=url)
    crawler = UrlCrawlerScript(spider)
    crawler.start()
    crawler.join()

# start downloading picture from the urls stored in xml
def start_downloading(filename, chooseone):
    spider = downloadSpider(domain=filename,chooseone=chooseone)
    crawler = UrlCrawlerScript(spider)
    crawler.start()
    crawler.join()

# ------------------------------------------------
# desktop setting
# ------------------------------------------------
def set_wallpaper():
    sys_str = platform.system()
    if sys_str == 'Windows':
        #set_window7_wallpaper()
        pass
    elif sys_str == 'Linux':
        set_ubuntu_wallpaper()

def get_picture_list(filedir):
    filelist = os.listdir(filedir)
    pic = ""
    if any(filelist):
        while(len(pic) == 0 or not os.path.isfile(filedir+pic)):
            #print(filedir+pic)
            #print(pic)
            rn = random.randint(0, len(filelist)-1)
            pic = filelist[rn]
    return pic

def get_dir_list(topdir):
    filelist = os.listdir(topdir)
    subdir = ""
    if any(filelist):
        while (len(subdir) == 0 or not os.path.isdir(topdir+subdir)):
            print(topdir+'/'+subdir)
            rn = random.randint(0, len(filelist)-1)
            subdir = filelist[rn]
    return subdir

def set_ubuntu_wallpaper():
    board = ''
    if re.findall('\d+',url_text.get()):
        board = re.findall('\d+',url_text.get())[-1]
    if len(board) == 0:
        board = get_dir_list(os.path.abspath(".")+"/pic/")
    if len(board) == 0:
        return
    filedir = os.path.abspath(".")+"/pic/%s/" %board
    pic = get_picture_list(filedir)
    path = filedir + "/" + pic
    #os.system('DISPLAY=:0 GSETTINGS_BACKEND=dconf gsettings set org.gnome.desktop.background picture-uri "%s"' %(path))    # notice this doesn't work
    path = path.encode('utf-8')
    uri = 'file://' + urllib.quote(path)
    bg_setting = Gio.Settings.new('org.gnome.desktop.background')
    bg_setting.set_string('picture-uri', uri)
    bg_setting.apply()
    os.system('gsettings set org.gnome.desktop.background picture-options "spanned"')

#def set_window7_wallpaper():
    #filedir = os.path.abspath(".")+"/pic/full"
    #pic = get_picture_list(filedir)
    #path = filedir + "/" + pic

# ------------------------------------------------
# running
# ------------------------------------------------
root.mainloop()

