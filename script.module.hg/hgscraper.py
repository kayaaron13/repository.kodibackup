# -*- coding: utf-8 -*-
import string,urllib2,requests,re,os,sys
from os.path import join
from resources.lib._addon import *
from resources.lib._common import *
from datetime import datetime, timedelta
#    import datetime as D-T 
one_day = timedelta(days=1)
one_hour = timedelta(hours=1)
timeShift = timedelta(hours=1)

#        today=datetime.now().strftime('%d-%b-%Y')
print '\n'+'Date - '+str (datetime.now().strftime('%d-%b-%Y'))
# find the folder script is running in
# to use as location for ant file reads / writes
myPath = sys.path[0]

# flags for testing
saveXML = 'no'
scriptTest = 'no'

###################
# needed for scrape inside addon
#    if scriptTest == 'no':
    #    from resources.lib.modules import dicts
###################
# filenames only reqd for tests
EditDest = str (myPath)
OutputFile = 'HesGoal-OKA-Scrape.xml'

if saveXML == 'yes':
    f2 = open(join(myPath,OutputFile),'w')
    f2.write ('Start of file inside kodi'+'\n')
    f2.write ('\n')
    f2.close()
##############

StrmName = '-'
StrmLink = '-'
iconimage = 'https://i.imgur.com/FZ1wlg4.png'    # your chosen icon
fanart = 'https://i.imgur.com/qXPUn77.jpg'    # your chosen fanart

#### Setup plugins just incase needed
Plug1="plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url="
Plug2="plugin://plugin.video.f4mTester/?url="
Plug2a="&amp;streamtype=HLSRETRY&amp;name=" #    Live-Event"
Plug2b="&amp;streamtype=TSDOWNLOADER&amp;name=" #    Live-Event"
Agent="|User-Agent=Mozilla/5.0"
DummyStream = "FILL-ME-IN"

# URLs for each page to scrape
url = 'http://www.hesgoal.com/'
footballURL= 'http://www.hesgoal.com/league/11/Football_News'
racingURL = 'http://www.hesgoal.com/league/12/Racing_News'

# regex required
Regex1 = 'href="(.+?)"><img src="(.+?)" width.+?alt="(.+?)"'
Regex2 = '<center><iframe.+?src="\/\/(.+?)" width'
Regex3 = 'source:(.+?),'

################
# ensure all lists are empty
webContent = ''
webContent = []
parsedWeb = []
sportList =[]
racingList = []
fullList = []
################

def getHtml(url, referer=None, hdr=None, data=None):
	#################
    # get HTML data from url 
    #################
    USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
    headers = {
        'User-Agent': USER_AGENT,
        'Accept': '*/*',
        'Connection': 'keep-alive'
    }
    if not hdr:
        req = urllib2.Request(url, data, headers)
    else:
        req = urllib2.Request(url, data, hdr)
    if referer:
        req.add_header('Referer', referer)
    response = urllib2.urlopen(req, timeout=120)
    data = response.read()
    response.close()
    #
    #    print '\n'+'\n'+'\n'+'============='
    #    print '============='
    #    print '============='
    #    print '============='
    #    print 'Data from - '+str(url) + '\n ' + str (data)+ '\n '
    return data
    
def getStreams(urlUsed,webContent,sportList,racingList):
	###################
    # find streams from html data
    ###################
    searchlines = webContent
    strmCount = 0
    today=datetime.now().strftime('%d-%b-%Y')
    
    if urlUsed == footballURL and strmCount == 0: 
        sectionTitle = 'Main Sports Events'
        sportList.append({'adjTime':today,'EvName':sectionTitle,'EvLeague':' ','EvLink':'ignoreme','EvIcon':iconimage,'fanart':fanart})
    if urlUsed == racingURL and strmCount == 0: 
        sectionTitle = 'Racing Events'
        racingList.append({'adjTime':today,'EvName':sectionTitle,'EvLeague':' ','EvLink':'ignoreme','EvIcon':iconimage,'fanart':fanart})
    print '\n'+'Finding streams on - ' + str (sectionTitle)
    
    if saveXML == 'yes':
        f2 = open(join(myPath,OutputFile),'a')
        f2.write ('<item>'+'\n')
        f2.write ('\t'+'<title>[I][COLOR gold]'+today+' - [COLOR gold]'+sectionTitle+'[/COLOR][/I]</title>'+'\n')
        f2.write ('\t'+'<link>ignoreme</link>'+'\n')
        f2.write ('\t'+'<thumbnail>'+iconimage+'</thumbnail>'+'\n')
        f2.write ('\t'+'<fanart>'+fanart+'</fanart>'+'\n')
        f2.write ('</item>'+'\n')
        f2.write ('\n')
        f2.close()
        
    if scriptTest == 'no':
        print'scriptTest is no'
        #    if not playlist in dicts.PLAYLIST:
            #   dicts.PLAYLIST.append(playlist)
    
    #    print '\n'+ 'In getStreams with url -'+str (urlUsed)+' section title = '+sectionTitle
    #    print 'Data from - '+str(urlUsed) + '\n ' + str (searchlines)+ '\n '
    for i, line in enumerate(searchlines):
        checkline = line
        #    print str (checkline)
        #    stop when reached last event
        if urlUsed == footballURL and '<a href=' in checkline and '><img src=' in checkline and 'Djorkaeff' in checkline:   
            print 'End of streams  on - ' + str (sectionTitle)
            return
        if urlUsed == racingURL and '<a href=' in checkline and '><img src=' in checkline and 'Hamilton' in checkline:   
            print 'End of streams  on - ' + str (sectionTitle)
            return
            
        # get streams etc
        if '<a href=' in checkline and '><img src=' in checkline:    #      and not 'AAAAAAAAA' in checkline:   
            checkline2 = searchlines[i+5]
            SplName = checkline.split('"><img src="')
            SplName1 = checkline.split('alt="')
            SplName2 = SplName[-1].split('" width')
            #
            EvLeague = checkline2.replace('<p>','').replace('</p>','').lstrip().strip()
            EvTemp = EvLeague.split(' ')
            EvTime = EvTemp [-1]
            EvLeague = EvLeague.replace(EvTime,'')
            url2 = SplName[0].replace('<a href="','').lstrip().strip()
            EvIcon = SplName2[0].lstrip().strip()
            EvName = SplName1[-1].replace('" /></a>','').replace('" border="0','').lstrip().strip()
        
            #    tempTime = EvTime.split(':')
            #    oldHour = int(tempTime[0])
            #    newHour = oldHour - 1
            #    if newHour < 0:
                #    newHour = newHour + 24    
            #    gTime = str(newHour) +':'+tempTime[-1]
            
            #BST COVERSION REMOVED
            #    try:
                #    print '----- Attempting try option ----'
                #    today=datetime.now().strftime('%d-%b-%Y')
                #    timeTemp = today+' '+EvTime #   .rstrip ().lstrip ().strip ()
                #    time1 = datetime.strptime(timeTemp, '%d-%b-%Y %H:%M')-timeShift
                #    adjTime = str (time1.strftime('%H:%M (BST)'))
            #    except:
                #    print '----- Try option failed - now in except ----'
                #    today=datetime.now().strftime('%d-%b-%Y')
                #    adjTime = str (EvTime)+' (GMT)'
                #    #    adjTime = '00:00'
            
            today=datetime.now().strftime('%d-%b-%Y')
            adjTime = str (EvTime)+' (GMT)'
		
            
            
            
            #       
            #    print 'url2 (link) =' + url2
            ## print 'EvLink = '+EvLink
            #    print 'EvName = '+EvLeague+' - '+EvName
            #    print 'EvIcon = '+EvIcon
            #    print 'Event Time= '+EvTime
            #### old calc    print 'Adjusted Event Time = '+gTime
            #    print 'Adjusted Event Time = '+adjTime
            #
                
            HTML = getHtml(url2)
            match = re.compile(Regex2).findall(HTML)
            for url3 in match:
                url3 = 'http://'+url3
                #
                #    print '== in url2 - finding url3 == '
                #    print 'url3 (link) =' + url3
                #
        
                HTML = getHtml(url3)
                match = re.compile(Regex3).findall(HTML)
                #    print '== in url3 - finding url4 =='
                for url4 in match:
                    url4 = url4.replace("'http","http").replace(".m3u8'",".m3u8").replace(".m3u'",".m3u").replace(".ts'",".ts").lstrip().strip()
                    EvLink = url4
                    #
                    #    print '== in url3 - found url4 =='
                    #    print 'url4 (link) =' + url4
                    #
                    strmCount = strmCount+1
                    #print 'time1 -'+str (time1.strftime('%H:%M (BST)'))
                    print '========= '+str(strmCount)
                    
                    if '.m3u' in EvLink: EvLink=Plug2+EvLink+Plug2a+EvName
                    elif '.ts' in EvLink: EvLink=Plug2+EvLink+Plug2b+EvName
                    
                    if urlUsed == footballURL:
                        sportList.append({'adjTime':adjTime,'EvName':EvName,'EvLeague':EvLeague,'EvLink':EvLink,'EvIcon':EvIcon,'fanart':fanart})
                    if urlUsed == racingURL:
                        racingList.append({'adjTime':adjTime,'EvName':EvName,'EvLeague':EvLeague,'EvLink':EvLink,'EvIcon':EvIcon,'fanart':fanart})
            
                    if saveXML == 'yes':
                        f2 = open(join(myPath,OutputFile),'a')
                        f2.write ('<item>'+'\n')
                        f2.write ('\t'+'<title>[COLOR red]'+adjTime+' - [COLOR white]'+EvName+'[COLOR FFff8397b0][I] ('+EvLeague+')[/I][/COLOR]</title>'+'\n')
                        f2.write ('\t'+'<link>'+EvLink+'</link>'+'\n')
                        f2.write ('\t'+'<thumbnail>'+EvIcon+'</thumbnail>'+'\n')
                        f2.write ('\t'+'<fanart>'+fanart+'</fanart>'+'\n')
                        f2.write ('</item>'+'\n')
                        f2.write ('\n')
                        f2.close()
                      
        #    exit()
        
####### main script runs from here ###################
#   needs doing for football and racing urls
#   url = foootballURL and racingURL
def scrapeContent():
    Log('going for webContent on Football url')
    webContent = getHtml(footballURL).splitlines(True)
    Log('going to make Football list')
    getStreams (footballURL,webContent,sportList,racingList)
    Log('going for webContent on Racing url')
    webContent = getHtml(racingURL).splitlines(True)
    Log('going to make Racing list')
    getStreams (racingURL,webContent,sportList,racingList)

    Log('sportList - {}'.format(sportList))                 
    Log('racingList - {}'.format(racingList))      
    Log('Leaving hesgoal py') 
     
    #return (sportList,racingList)




