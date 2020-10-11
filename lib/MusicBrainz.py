# -*- coding: utf8 -*-

import urllib.parse
import re
import json
import xbmcgui

from lib.kodi65 import addon
from lib.kodi65 import utils
from lib.kodi65 import ItemList

BASE_URL = 'https://musicbrainz.org/ws/2/'
BASE_FMT = 'json'
SEARCH_STR = '{0}{1}?query={2}:{3}&limit={4}&offset={5}&fmt={6}'

def search_MusicBrainz(type, search_str):
    if type==0:
        result = search_artist(search_str)
    elif type==1:
        result = search_album(search_str)
    elif type==2:
        result = search_song(search_str)

def search_artist(str, offset=0, limit=25):
    # https://musicbrainz.org/ws/2/artist?query=artist:accept&limit=25&offset=0&fmt=json
    url = SEARCH_STR.format(BASE_URL, 'artist', 'artist', urllib.parse.quote_plus(str), limit, offset, BASE_FMT)
    result = utils.get_JSON_response(url=url, cache_days=30, folder="MusicBrainz")
    if result['count'] > 0:
        utils.log('artists count %s' % result['count'])
        text = ''
        for artist in result['artists']:
            text = text + 'id: {0}\n'.format(artist['id'])
            text = text + 'name: {0}\n'.format(artist['name'])
            if 'type' in artist:
                text = text + 'type: {0}\n'.format(artist['type'])
            if 'score' in artist:
                text = text + 'score: {0}\n'.format(artist['score'])
            if 'country' in artist:
                text = text + 'country: {0}\n'.format(artist['country'])
            if 'disambiguation' in artist:
                text = text + 'disambiguation: {0}\n'.format(artist['disambiguation'])
            if 'tags' in artist:
                atag = []
                for tag in artist['tags']:
                    if 'name' in tag:
                        atag.append(tag['name'])
                text = text + 'tags: {0}\n'.format(' / '.join(atag))
            text = text + '\n'
        xbmcgui.Dialog().textviewer(addon.LANG(32177), text)
        return True
    else:
        return False

def search_album(str, offset=0, limit=25):
    # https://musicbrainz.org/ws/2/release-group?query=release:accept&limit=25&offset=0&fmt=json
    url = SEARCH_STR.format(BASE_URL, 'release-group', 'release', urllib.parse.quote_plus(str), limit, offset, BASE_FMT)
    result = utils.get_JSON_response(url=url, cache_days=30, folder="MusicBrainz")
    if result['count'] > 0:
        utils.log('release-group count %s' % result['count'])
        text = ''
        for releasegroup in result['release-groups']:
            text = text + 'id: {0}\n'.format(releasegroup['id'])
            text = text + 'title: {0}\n'.format(releasegroup['title'])
            if 'primary-type' in releasegroup:
                text = text + 'primary-type: {0}\n'.format(releasegroup['primary-type'])
            if 'secondary-types' in releasegroup:
                text = text + 'secondary-types: {0}\n'.format(', '.join(releasegroup['secondary-types']))
            if 'score' in releasegroup:
                text = text + 'score: {0}\n'.format(releasegroup['score'])
            if 'count' in releasegroup:
                text = text + 'count: {0}\n'.format(releasegroup['count'])
            if 'artist-credit' in releasegroup:
                aartist = []
                for artistcredit in releasegroup['artist-credit']:
                    if 'artist' in artistcredit:
                        if 'name' in artistcredit['artist']:
                            aartist.append(artistcredit['artist']['name'])
                text = text + 'artist(s): {0}\n'.format(', '.join(aartist))
            text = text + '\n'
        xbmcgui.Dialog().textviewer(addon.LANG(32177), text)
        return True
    else:
        return False

def search_song(str, offset=0, limit=25):
    # https://musicbrainz.org/ws/2/recording?query=recording:paranoid&limit=25&offset=0&fmt=json
    url = SEARCH_STR.format(BASE_URL, 'recording', 'recording', urllib.parse.quote_plus(str), limit, offset, BASE_FMT)
    result = utils.get_JSON_response(url=url, cache_days=30, folder="MusicBrainz")
    if result['count'] > 0:
        utils.log('recordings count %s' % result['count'])
        text = ''
        for record in result['recordings']:
            text = text + 'id: {0}\n'.format(record['id'])
            text = text + 'title: {0}\n'.format(record['title'])
            if 'score' in record:
                text = text + 'score: {0}\n'.format(record['score'])
            if 'length' in record:
                text = text + 'length: {0}\n'.format(record['length'])
            if 'artist-credit' in record:
                aartist = []
                for artistcredit in record['artist-credit']:
                    if 'artist' in artistcredit:
                        if 'name' in artistcredit['artist']:
                            aartist.append(artistcredit['artist']['name'])
                text = text + 'artist(s): {0}\n'.format(', '.join(aartist))
            text = text + '\n'
        xbmcgui.Dialog().textviewer(addon.LANG(32177), text)
        return True
    else:
        return False

