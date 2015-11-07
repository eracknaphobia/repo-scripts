# -*- coding: utf-8 -*-
import os
import xbmc
import xbmcaddon
import xbmcvfs

__addon__ = xbmcaddon.Addon(id='script.ebooks')
__addonid__ = __addon__.getAddonInfo('id')
__icon__ = __addon__.getAddonInfo('icon')


# Common logging module
def log(txt, loglevel=xbmc.LOGDEBUG):
    if (__addon__.getSetting("logEnabled") == "true") or (loglevel != xbmc.LOGDEBUG):
        if isinstance(txt, str):
            txt = txt.decode("utf-8")
        message = u'%s: %s' % (__addonid__, txt)
        xbmc.log(msg=message.encode("utf-8"), level=loglevel)


def os_path_join(dir, file):
    # Check if it ends in a slash
    if dir.endswith("/") or dir.endswith("\\"):
        # Remove the slash character
        dir = dir[:-1]

    # Convert each argument - if an error, then it will use the default value
    # that was passed in
    try:
        dir = dir.decode("utf-8")
    except:
        pass
    try:
        file = file.decode("utf-8")
    except:
        pass
    return os.path.join(dir, file)


# Splits a path the same way as os.path.split but supports paths of a different
# OS than that being run on
def os_path_split(fullpath):
    # Check if it ends in a slash
    if fullpath.endswith("/") or fullpath.endswith("\\"):
        # Remove the slash character
        fullpath = fullpath[:-1]

    try:
        slash1 = fullpath.rindex("/")
    except:
        slash1 = -1

    try:
        slash2 = fullpath.rindex("\\")
    except:
        slash2 = -1

    # Parse based on the last type of slash in the string
    if slash1 > slash2:
        return fullpath.rsplit("/", 1)

    return fullpath.rsplit("\\", 1)


# Checks if a directory exists (Do not use for files)
def dir_exists(dirpath):
    # There is an issue with password protected smb shares, in that they seem to
    # always return false for a directory exists call, so if we have a smb with
    # a password and user name, then we return true
    if '@' in dirpath:
        return True

    directoryPath = dirpath
    # The xbmcvfs exists interface require that directories end in a slash
    # It used to be OK not to have the slash in Gotham, but it is now required
    if (not directoryPath.endswith("/")) and (not directoryPath.endswith("\\")):
        dirSep = "/"
        if "\\" in directoryPath:
            dirSep = "\\"
        directoryPath = "%s%s" % (directoryPath, dirSep)
    return xbmcvfs.exists(directoryPath)


##############################
# Stores Various Settings
##############################
class Settings():
    EBOOK_FORMATS = (
        'epub',
        'mobi',
        'pdf'
    )

    @staticmethod
    def getEbookFolder():
        eBookFolder = None
        if __addon__.getSetting("useEBookFolder") == 'true':
            eBookFolder = __addon__.getSetting("eBooksFolder")
        return eBookFolder

    @staticmethod
    def setEbookFolder(eBooksFolder):
        __addon__.setSetting("useEBookFolder", 'true')
        __addon__.setSetting("eBooksFolder", eBooksFolder)

    @staticmethod
    def getFallbackCoverImage():
        fallbackCover = __addon__.getSetting("fallbackCoverImage")
        if fallbackCover in [None, ""]:
            fallbackCover = __icon__
        return fallbackCover

    @staticmethod
    def onlyShowWholeBookIfChapters():
        return __addon__.getSetting("onlyShowWholeBookIfChapters") == 'true'

    @staticmethod
    def isMarkReadWhenNavToNextChapter():
        return __addon__.getSetting("markReadWhenNavToNextChapter") == 'true'

    @staticmethod
    def usePageNumbersForPdf():
        return __addon__.getSetting("usePageNumbersForPdf") == 'true'

    @staticmethod
    def useWhiteBackground():
        return __addon__.getSetting("useWhiteBackground") == 'true'

    @staticmethod
    def isEbookFormat(filename):
        for ext in Settings.EBOOK_FORMATS:
            if filename.endswith(ext):
                return True
        return False

    @staticmethod
    def getCoverCacheLocation():
        coverCache = xbmc.translatePath('special://profile/addon_data/%s/covers' % __addonid__).decode("utf-8")

        # Make sure the directory to cache the covers exists
        if not dir_exists(xbmc.translatePath('special://profile/addon_data/%s' % __addonid__).decode("utf-8")):
            xbmcvfs.mkdir(xbmc.translatePath('special://profile/addon_data/%s' % __addonid__).decode("utf-8"))
        if not dir_exists(coverCache):
            xbmcvfs.mkdir(coverCache)
        return coverCache

    @staticmethod
    def getTempLocation():
        tmpdestination = xbmc.translatePath('special://profile/addon_data/%s/temp' % __addonid__).decode("utf-8")

        # Make sure the directory to cache the covers exists
        if not dir_exists(xbmc.translatePath('special://profile/addon_data/%s' % __addonid__).decode("utf-8")):
            xbmcvfs.mkdir(xbmc.translatePath('special://profile/addon_data/%s' % __addonid__).decode("utf-8"))
        if not dir_exists(tmpdestination):
            xbmcvfs.mkdir(tmpdestination)
        return tmpdestination

    @staticmethod
    def getOPDSLocation():
        opdsLoc = None
        if __addon__.getSetting("useOPDS") == 'true':
            opdsLoc = __addon__.getSetting("opdsUrl")
            if not opdsLoc.startswith('http'):
                opdsLoc = "http://%s" % opdsLoc
            if opdsLoc.endswith('/'):
                opdsLoc = opdsLoc[:-1]
            if opdsLoc.endswith('/opds'):
                opdsLoc = opdsLoc[:-5]
        return opdsLoc
