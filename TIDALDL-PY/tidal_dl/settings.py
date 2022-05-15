#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   settings.py
@Time    :   2020/11/08
@Author  :   Yaronzz
@Version :   2.0
@Contact :   yaronhuang@foxmail.com
@Desc    :
'''
import base64
import json
import os

from aigpy.fileHelper import getContent, write
from aigpy.modelHelper import dictToModel, modelToDict, ModelBase
from tidal_dl.enums import AudioQuality, VideoQuality


def __encode__(string):
    sw = bytes(string, 'utf-8')
    return base64.b64encode(sw)


def __decode__(string):
    try:
        sr = base64.b64decode(string)
        return sr.decode()
    except:
        return string


def getSettingsPath():
    if "XDG_CONFIG_HOME" in os.environ:
        return os.environ['XDG_CONFIG_HOME']
    elif "HOME" in os.environ:
        return os.environ['HOME']
    elif "HOMEDRIVE" in os.environ and "HOMEPATH" in os.environ:
        return os.environ['HOMEDRIVE'] + os.environ['HOMEPATH']
    else:
        return os.path.abspath("./")


def getLogPath():
    return f'{getSettingsPath()}/.tidal-dl.log'


class TokenSettings(ModelBase):
    userid = None
    countryCode = None
    accessToken = None
    refreshToken = None
    expiresAfter = 0

    @staticmethod
    def read():
        path = TokenSettings.__getFilePath__()
        txt = getContent(path)
        if txt == "":
            return TokenSettings()
        txt = __decode__(txt)
        data = json.loads(txt)
        ret = dictToModel(data, TokenSettings())
        if ret is None:
            return TokenSettings()
        return ret

    @staticmethod
    def save(model):
        data = modelToDict(model)
        txt = json.dumps(data)
        txt = __encode__(txt)
        path = TokenSettings.__getFilePath__()
        write(path, txt, 'wb')

    @staticmethod
    def __getFilePath__():
        return f'{getSettingsPath()}/.tidal-dl.token.json'


class Settings(ModelBase):
    addLyrics = False
    lyricsServerProxy = ''
    downloadPath = "./download/"
    onlyM4a = False
    addExplicitTag = True
    addHyphen = True
    addYear = False
    useTrackNumber = True
    audioQuality = AudioQuality.Normal
    videoQuality = VideoQuality.P360
    checkExist = True
    artistBeforeTitle = False
    includeEP = True
    addAlbumIDBeforeFolder = False
    saveCovers = True
    language = 0
    usePlaylistFolder = True
    multiThreadDownload = True
    albumFolderFormat = R"{ArtistName}/{Flag} {AlbumTitle} [{AlbumID}] [{AlbumYear}]"
    trackFileFormat = R"{TrackNumber} - {ArtistName} - {TrackTitle}{ExplicitFlag}"
    videoFileFormat = R"{VideoNumber} - {ArtistName} - {VideoTitle}{ExplicitFlag}"
    showProgress = True
    showTrackInfo = True
    saveAlbumInfo = False
    lyricFile = False
    apiKeyIndex = 0
    addTypeFolder = True

    @staticmethod
    def getDefaultAlbumFolderFormat():
        return R"{ArtistName}/{Flag} {AlbumTitle} [{AlbumID}] [{AlbumYear}]"

    @staticmethod
    def getDefaultTrackFileFormat():
        return R"{TrackNumber} - {ArtistName} - {TrackTitle}{ExplicitFlag}"
    
    @staticmethod
    def getDefaultVideoFileFormat():
        return R"{VideoNumber} - {ArtistName} - {VideoTitle}{ExplicitFlag}"

    @staticmethod
    def read():
        path = Settings.__getFilePath__()
        txt = getContent(path)
        if txt == "":
            return Settings()
        data = json.loads(txt)
        ret = dictToModel(data, Settings())
        if ret is None:
            return Settings()
        ret.audioQuality = Settings.getAudioQuality(ret.audioQuality)
        ret.videoQuality = Settings.getVideoQuality(ret.videoQuality)
        ret.usePlaylistFolder = ret.usePlaylistFolder == True or ret.usePlaylistFolder is None
        ret.multiThreadDownload = ret.multiThreadDownload == True or ret.multiThreadDownload is None
        ret.addTypeFolder = ret.addTypeFolder == True or ret.addTypeFolder is None
        if ret.albumFolderFormat is None:
            ret.albumFolderFormat = Settings.getDefaultAlbumFolderFormat()
        if ret.trackFileFormat is None:
            ret.trackFileFormat = Settings.getDefaultTrackFileFormat()
        if ret.apiKeyIndex is None:
            ret.apiKeyIndex = 0
        return ret

    @staticmethod
    def save(model):
        data = modelToDict(model)
        data['audioQuality'] = model.audioQuality.name
        data['videoQuality'] = model.videoQuality.name
        txt = json.dumps(data)
        path = Settings.__getFilePath__()
        write(path, txt, 'w+')

    @staticmethod
    def getAudioQuality(value):
        return next(
            (item for item in AudioQuality if item.name == value),
            AudioQuality.Normal,
        )

    @staticmethod
    def getVideoQuality(value):
        return next(
            (item for item in VideoQuality if item.name == value),
            VideoQuality.P360,
        )

    @staticmethod
    def __getFilePath__():
        return f'{getSettingsPath()}/.tidal-dl.json'
