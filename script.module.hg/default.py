# dicts created in addon
#     sportList.append({'adjTime':adjTime,'EvName':EvName,'EvLeague':EvLeague,'EvLink':EvLink,'EvIcon':EvIcon,'fanart':fanart})
#     racingList.append({'adjTime':adjTime,'EvName':EvName,'EvLeague':EvLeague,'EvLink':EvLink,'EvIcon':EvIcon,'fanart':fanart})

import sys
import xbmc
import xbmcaddon
import xbmcplugin
import urllib
#       import byb_modules as BYB
from resources.lib._addon import *
from resources.lib._common import *

## use std kodi modules 
import xbmcgui
#    import xbmc
#    from xbmcgui import ListItem
from xbmcplugin import addDirectoryItem, endOfDirectory

# Get the plugin url in plugin:// notation. 
pluginUrl = sys.argv[0] 
# Get the plugin handle as an integer number. 
pluginHandle = int(sys.argv[1])

# default artwork setup
myIcon= 'https://i.imgur.com/hz1lR1a.png' # Live TV Icon
myThumb= 'https://i.imgur.com/hz1lR1a.png' # Live TVIcon
myWall = 'https://i.imgur.com/qXPUn77.jpg' # My Wall

###############

def index():
	#   BYB.addDir(hgmain(local_string(30082)),url,1101,iconimage,fanart,'','','','')
	#   BYB.addDir('All Events','',1,addon_icon ,addon_fanart,'','','','')
    print 'Skipping index mode'
   
def hgmain():
    sportList =[]
    racingList = []
    import hgscraper
    hgscraper.scrapeContent()
    #print 'BACK in sport py '
    #print '\n'+'sportList - '+str (sportList)                  
    #print '\n'+'racingList - '+str (racingList)      
    print ('hgscraper.sportList = {}'.format(hgscraper.sportList))
    print ('hgscraper.racingList = {}'.format(hgscraper.racingList))
    for items in hgscraper.sportList: 
        adjTime =items.get('adjTime','Time Missing')
        EvName =items.get('EvName','Title Missing')
        EvLeague =items.get('EvLeague','League Missing')
        EvLink =items.get('EvLink','Link Missing')
        EvIcon =items.get('EvIcon','Icon Missing')
        evFanart =items.get('fanart','Fanart Missing')
        if EvName == 'Main Sports Events':
            title = '[COLOR gold]'+EvName+'[/COLOR]'
            icon = 'https://i.imgur.com/FZ1wlg4.png'
            mode = 4
        else:
            title = '[COLOR red]'+adjTime+' - [COLOR white]'+EvName+'[COLOR FFff8397b0][I] ('+EvLeague+')[/I][/COLOR]'
            icon = EvIcon
            mode = 3 #2 #100
            
        myName = title
        myList = xbmcgui.ListItem(unicode(myName))
        myList.setArt({'thumb': icon , 'icon': icon, 'fanart': myWall})  
        
        #        addDirectoryItem(pluginHandle, EvLink, myList, True)          
        #        BYB.addDir_file(title,EvLink,mode,icon,evFanart,'Hes-Goal Sports Events','','','')
        
        addDirectoryItem(
                    pluginHandle,
                    EvLink,
                    myList, False, True)
                    #    myList, True)
#         for reference
#        xbmcplugin.addDirectoryItem(handle=addon_handle, listitem=li, isFolder=False, isPlayable = False)

                                    
        #    endOfDirectory(pluginHandle)
		
    for items in hgscraper.racingList:
        adjTime =items.get('adjTime','Time Missing')
        EvName =items.get('EvName','Title Missing')
        EvLeague =items.get('EvLeague.replace','League Missing')
        EvLink =items.get('EvLink','Link Missing')
        EvIcon =items.get('EvIcon','Icon Missing')
        evFanart =items.get('fanart','Fanart Missing')
        if EvName == 'Racing Events':
            title = '[COLOR gold]'+EvName+'[/COLOR]'
            icon = 'https://i.imgur.com/FZ1wlg4.png'
            mode = 4
        else:
            title = '[COLOR red]'+adjTime+' - [COLOR white]'+EvName+'[COLOR FFff8397b0][I] ('+EvLeague+')[/I][/COLOR]'
            icon = EvIcon
            mode = 3 #2 #100
            
        myName = title
        myList = xbmcgui.ListItem(unicode(myName))
        myList.setArt({'thumb': icon , 'icon': icon, 'fanart': myWall})  
        
        #         addDirectoryItem(pluginHandle, EvLink, myList, True)           
        #         BYB.addDir_file(title,EvLink,2,icon,evFanart,'Hes-Goal Racing Events','','','')
        addDirectoryItem(
                    pluginHandle,
                    EvLink,
                    myList, False, True)
                    #    myList, True)
        endOfDirectory(pluginHandle)
#         for reference
#        xbmcplugin.addDirectoryItem(handle=addon_handle, listitem=li, isFolder=False, isPlayable = False)
        
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
            params=sys.argv[2]
            cleanedparams=params.replace('?','')
            if (params[len(params)-1]=='/'):
                params=params[0:len(params)-2]
            pairsofparams=cleanedparams.split('&')
            param={}
            for i in range(len(pairsofparams)):
                splitparams={}
                splitparams=pairsofparams[i].split('=')
                if (len(splitparams))==2:
                    param[splitparams[0]]=splitparams[1]
        return param
xbmcplugin.setContent(int(sys.argv[1]), 'movies')

params=get_params()
url=None
name=None
mode=None
playlist=None
iconimage=None
fanart=addon_fanart
playlist=None
fav_mode=None
regexs=None
description=None


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass


if mode==None:
    print ('Opening NEW Main Index mode = {}'.format(mode))
    # index()
    hgmain()

# modes below are byb legacy
# & may not be reqd   
elif mode==1:
    print ('Opening NEW HG Main Index mode = {}'.format(mode))
    hgmain()

elif mode==2:
    print ('using BYB player - attempting to play url = {} mode = {}'.format(url,mode))
    PLAY = BYB.xbmc_player()
    PLAY.play(url)

elif mode==3:
    print ('using std xbmc player - attempting to play url = {} mode = {}'.format(url,mode))
    PLAY = xbmc.Player()
    
elif mode==4:
    print ('url passed = {} mode = {}'.format(url,mode))
    pass

xbmcplugin.endOfDirectory(int(sys.argv[1]))