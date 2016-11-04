# -*- coding: utf-8 -*- 
#-------------LicenseHeader--------------
# plugin.video.Mediathek - Gives access to most video-platforms from German public service broadcasters
# Copyright (C) 2010  Raptor 2101 [raptor2101@gmx.de]
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>. 

from mediathek import DisplayObject, Mediathek, SimpleLink, TreeNode
import json, time, urllib2

CONFIG_CDN = 'https://config-cdn.cellular.de/zdf/mediathek/config/android/4_0/zdf_mediathek_android_live_4_0.json'

def jsonItem(url, *path):
    """Return the item from the JSON at the given :url.
    """
    res = json.loads(urllib2.urlopen(url, None, 60).read())
    for i in path:
        res = res[i]
    return res

def teaserBild(teaserBild):
    """Pick the first resolution above 640.
    """
    largest = None
    for res, bild in teaserBild.iteritems():
        largest = bild
        if 640 <= int(res):
            break
    return largest

class ZDFMediathek(Mediathek):
  def __init__(self, simpleXbmcGui):
    self.gui = simpleXbmcGui
    zdfCategoriesPage = jsonItem(CONFIG_CDN, 'urlConfig', 'zdfCategoriesPage');
    self.menuTree = []
    for cat in jsonItem(zdfCategoriesPage, 'cluster'):
        if 'teaser' in cat:
            i = len(self.menuTree)
            self.menuTree.append(
                TreeNode('%d' % i, cat['name'], '', False, [
                    TreeNode(
                        '%d.%d' % (i, j),
                        tease['titel'],
                        tease['url'],
                        True
                    )
                    for j, tease in enumerate(cat['teaser'])
                ])
            )

  @classmethod
  def name(self):
    return "ZDF"
    
  def isSearchable(self):
    return False

  def buildPageMenu(self, link, initCount):
    self.gui.log('buildPageMenu(%r, %r)' % (link, initCount))
    for cluster in jsonItem(link, 'cluster'):
        for teaser in cluster['teaser']:
            if 'brand' == teaser['type']:
                self.gui.buildVideoLink(
                    DisplayObject(
                        teaser['titel'], '',
                        teaserBild(teaser['teaserBild'])['url'],
                        teaser['beschreibung'],
                        False
                    ),
                    self,
                    teaser['videoCount']
                )
            elif 'video' == teaser['type']:
                links = {}
                for formitaet in jsonItem(teaser['url'], 'document', 'formitaeten'):
                    if -1 < formitaet['type'].find('http_na_na'):
                        q =      0 if 'low' == formitaet['quality'] \
                            else 1 if 'high' == formitaet['quality'] \
                            else 2
                        links[q] = SimpleLink(formitaet['url'], 0)

                self.gui.buildVideoLink(
                    DisplayObject(
                        teaser['brandTitle'],
                        teaser['titel'],
                        teaserBild(teaser['teaserBild'])['url'],
                        teaser['beschreibung'],
                        links,
                        True,
                        time.strptime(teaser['airtime'], "%d.%m.%Y %H:%M")
                                if 'airtime' in teaser
                                else None,
                        int(teaser['length'])
                    ),
                    self,
                    1
                )
            else:
                raise 'Unknown teaser type %r' % teaser['type']
