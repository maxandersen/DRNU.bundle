import time
####################################################################################################

VIDEO_PREFIX = "/video/drnu"
MUSIC_PREFIX = "/music/drnu"

APIURL = "http://www.dr.dk/NU/api/%s"
RADIO_NOWNEXT_URL = "http://www.dr.dk/tjenester/LiveNetRadio/datafeed/programInfo.drxml?channelId=%s"
RADIO_TRACKS_URL = "http://www.dr.dk/tjenester/LiveNetRadio/datafeed/trackInfo.drxml?channelId=%s"
NAME  = "DR NU"
ART   = 'art-default.jpg'
ICON  = 'DR_icon-default.png'
ICON_DR1 = "DR1_icon-default.png"
ICON_DR2 = "DR2_icon-default.png"
ICON_DRK = "DRK_icon-default.png"
ICON_DRR = "DR_RAMASJANG_icon-default.png"
ICON_DRU = "DR_UPDATE_icon-default.png"

EPG_TV = { "DR1":"http://www.dr.dk/Tjenester/epglive/epg.DR1.drxml",
		"DR2": "http://www.dr.dk/Tjenester/epglive/epg.DR2.drxml",
		"DRU": "http://www.dr.dk/Tjenester/epglive/epg.DRUpdate.drxml",
		"RAM": "http://www.dr.dk/Tjenester/epglive/epg.DRRamasjang.drxml",
		"DRK": "http://www.dr.dk/Tjenester/epglive/epg.DRK.drxml"
		}

HTTP.CacheTime = 3600

####################################################################################################

def Start():
	Plugin.AddPrefixHandler(VIDEO_PREFIX, VideoMainMenu, NAME, ICON, ART)
	Plugin.AddPrefixHandler(MUSIC_PREFIX, MusicMainMenu, NAME, ICON, ART)
	Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
	Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
	MediaContainer.art = R(ART)
	MediaContainer.title1 = NAME
	DirectoryItem.thumb = R(ICON)
	HTTP.Headers['User-Agent'] = "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13"

def VideoMainMenu():
	dir = MediaContainer(viewGroup="List")
	dir.Append(Function(DirectoryItem(ProgramSerierMenu,"Programmer",subtitle="Alle Programserier", summary="",thumb=R(ICON),art=R(ART)),id=None,title="Programmer"))
	dir.Append(Function(DirectoryItem(NewestMenu,"Nyeste",subtitle="De nyeste videoer", summary="",thumb=R(ICON),art=R(ART)),id=None, title="Nyeste"))
	dir.Append(Function(DirectoryItem(SpotMenu,"Spot",subtitle="Spot light", summary="",thumb=R(ICON),art=R(ART)),id=None, title="Spot"))
	dir.Append(Function(DirectoryItem(MostViewedMenu,"Mest Sete",subtitle="Mest Sete", summary="",thumb=R(ICON),art=R(ART)),id=None, title="Mest Sete"))
	dir.Append(Function(DirectoryItem(LiveTVMenu, "Live TV", subtitle="Live TV", summary="", thumb=R(ICON), art=R(ART))))
	return dir


def MusicMainMenu():
	dir = MediaContainer(viewGroup="List")
	dir.Append(Function(DirectoryItem(LiveRadioMenu, "Live Radio", subtitle="Live Radio", summary="", thumb=R(ICON), art=R(ART))))
	return dir

def ProgramSerierMenu(sender,id,title):
	dir=MediaContainer(title1="DR NU", title2=title)
	
	JSONObject=JSON.ObjectFromURL(APIURL % "programseries.json")

	bucket = dict()
	letter = ''
	for program in JSONObject:
		slug=program["slug"]
		title=program["title"]
		if program["videoCount"] > 1:
			title = title + " (" + str(program["videoCount"]) + " afs.)"
		subtitle=", ".join(program["labels"])
		
		summary=program["description"]
		thumb=APIURL % "programseries/" + slug + "/images/600x600.jpg"

		letter = title[0].upper()
		if letter not in bucket:
			bucket[letter] = list()
		tuple = dict(title=title,subtitle=subtitle,thumb=thumb,summary=summary,id=slug)
		bucket[letter].append(tuple)

	for firstChar in sorted(bucket.iterkeys()):
		serier = bucket[firstChar]
		if Prefs['group_per_letter']:
			dir.Append(Function(DirectoryItem(LetterMenu, title=firstChar, subtitle= str(len(serier)) + " programmer"),serier=serier, title=firstChar))
		else:
			for serie in serier:
				dir.Append(Function(DirectoryItem(ProgramMenu,**serie),id=serie["id"],title=serie["title"]))
	return dir

def LetterMenu(sender,title, serier):
	dir=MediaContainer(title1="DR NU", title2=title)
	for serie in serier:
		dir.Append(Function(DirectoryItem(ProgramMenu,**serie),id=serie["id"],title=serie["title"]))
	return dir

		
def NewestMenu(sender,id, title):
        return CreateVideoItem(sender, id=id, title=title, items=JSON.ObjectFromURL(APIURL % "videos/newest.json"))

def MostViewedMenu(sender,id, title):
        return CreateVideoItem(sender, id=id, title=title, items=JSON.ObjectFromURL(APIURL % "videos/mostviewed.json"))

def SpotMenu(sender,id, title):
        return CreateVideoItem(sender, id=id, title=title, items=JSON.ObjectFromURL(APIURL % "videos/spot.json"))

def ProgramMenu(sender,id, title):
	return CreateVideoItem(sender, id=id, title=title, items=JSON.ObjectFromURL(APIURL % "programseries/" + id + "/videos"))

def LiveTVMenu(sender):
	drRTMP = "rtmp://rtmplive.dr.dk/live"
	dir = MediaContainer(title1="DR NU - Live TV", title2="Live TV")	
	dir.Append(RTMPVideoItem(drRTMP, clip="livedr01astream3", width=830, height=467, live=True, title="DR1", summary=getTVLiveMetadata("DR1"), thumb=R(ICON_DR1), art=R(ART) ) )
	dir.Append(RTMPVideoItem(drRTMP, clip="livedr02astream3", width=830, height=467, live=True, title="DR2", summary=getTVLiveMetadata("DR2"), thumb=R(ICON_DR2), art=R(ART) ) )
	dir.Append(RTMPVideoItem(drRTMP, clip="livedr03astream3", width=830, height=467, live=True, title="DR Update", summary=getTVLiveMetadata("DR Update"), thumb=R(ICON_DRU), art=R(ART) ) )
	dir.Append(RTMPVideoItem(drRTMP, clip="livedr04astream3", width=830, height=467, live=True, title="DR K", summary=getTVLiveMetadata("DR K"), thumb=R(ICON_DRK), art=R(ART) ) )
	dir.Append(RTMPVideoItem(
							drRTMP, 
							clip="livedr05astream3", 
							width=830, 
							height=467, 
							live=True, 
							title="DR Ramsjang", 
							summary=getTVLiveMetadata("DR Ramasjang"), 
							thumb=R(ICON_DRR), 
							art=R(ART) ) )

	return dir


def LiveRadioMenu(sender):
	drRTMP = "rtmp://live.gss.dr.dk/live/"
	dir=MediaContainer(title1="DR NU - Live Radio", title2="Live Radio")
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel3_HQ", width=0, height=0, live=True, title="P1", summary=getRadioMetadata('P1'), thumb=R(ICON),art=R(ART)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel4_HQ", width=0, height=0, live=True, title="P2", summary=getRadioMetadata('P2'), thumb=R(ICON),art=R(ART)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel15_HQ", width=0, height=0, live=True, title="P3", summary=getRadioMetadata('P3'), thumb=R(ICON),art=R(ART)))
	dir.Append(Function(DirectoryItem(LiveRadioP4Menu,"P4",subtitle="P4", summary="Vælg din regionale P4",thumb=R(ICON),art=R(ART))))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel25_HQ", width=0, height=0, live=True, title="DR P5", summary=getRadioMetadata('P5'), thumb=R(ICON),art=R(ART)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel29_HQ", width=0, height=0, live=True, title="DR P6 Beat", summary=getRadioMetadata('P6'), thumb=R(ICON),art=R(ART)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel21_HQ", width=0, height=0, live=True, title="DR P7 Mix", summary=getRadioMetadata('P7'), thumb=R(ICON),art=R(ART)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel24_HQ", width=0, height=0, live=True, title="DR Ramasjang Radio", summary=getRadioMetadata('RAM'), thumb=R(ICON),art=R(ART)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel26_HQ", width=0, height=0, live=True, title="DR R&B", summary=getRadioMetadata('ROB'), thumb=R(ICON),art=R(ART)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel18_HQ", width=0, height=0, live=True, title="DR Boogieradio", summary=getRadioMetadata('SK1'), thumb=R(ICON),art=R(ART)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel27_HQ", width=0, height=0, live=True, title="DR Rock", summary=getRadioMetadata('ROC'), thumb=R(ICON),art=R(ART)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel10_HQ", width=0, height=0, live=True, title="DR Dansktop", summary=getRadioMetadata('DAN'), thumb=R(ICON),art=R(ART)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel19_HQ", width=0, height=0, live=True, title="DR Jazz", summary=getRadioMetadata('JAZ'), thumb=R(ICON),art=R(ART)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel23_HQ", width=0, height=0, live=True, title="DR Klassisk", summary=getRadioMetadata('DAB'), thumb=R(ICON),art=R(ART)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel2_HQ", width=0, height=0, live=True, title="DR Nyheder", summary=getRadioMetadata('NEWS'), thumb=R(ICON),art=R(ART)))	
	return dir

def LiveRadioP4Menu(sender):
	drRTMP = "rtmp://live.gss.dr.dk/live/"
	dir=MediaContainer(title1="DR NU - P4", title2="P4")
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel18_HQ", width=0, height=0, live=True, title="P4 København", summary=getRadioMetadata('KH4'), thumb=R(ICON),art=R(ART)))	
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel11_HQ", width=0, height=0, live=True, title="P4 Sjælland", summary=getRadioMetadata('NV4'), thumb=R(ICON),art=R(ART)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel14_HQ", width=0, height=0, live=True, title="P4 Østjylland", summary='', thumb=R(ICON),art=R(ART)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel12_HQ", width=0, height=0, live=True, title="P4 Syd", summary='', thumb=R(ICON),art=R(ART)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel17_HQ", width=0, height=0, live=True, title="P4 Fyn", summary=getRadioMetadata('OD4'), thumb=R(ICON),art=R(ART)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel10_HQ", width=0, height=0, live=True, title="P4 Nordjylland", summary='', thumb=R(ICON),art=R(ART)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel9HQ", width=0, height=0, live=True, title="P4 Midt & Vest", summary=getRadioMetadata('HO4'), thumb=R(ICON),art=R(ART)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel13_HQ", width=0, height=0, live=True, title="P4 Trekanten", summary=getRadioMetadata('TR4'), thumb=R(ICON),art=R(ART)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel6_HQ", width=0, height=0, live=True, title="P4 Bornholm", summary='', thumb=R(ICON),art=R(ART)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel15_HQ", width=0, height=0, live=True, title="P4 Esbjerg", summary=getRadioMetadata('ES4'), thumb=R(ICON),art=R(ART)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel11_HQ", width=0, height=0, live=True, title="P4 NordvestSjælland", summary=getRadioMetadata('NS4'), thumb=R(ICON),art=R(ART)))
	return dir	

def CreateVideoItem(sender,id, title, items):
	dir=MediaContainer(title1="DR NU", title2=title)

	titles = set()
	for item in items:
		key=APIURL % "videos/" + str(item["id"])
		thumb=APIURL % "videos/" + str(item["id"]) + "/images/600x600.jpg"

		if 'imagePath' in item:
			art="http://dr.dk/nu" + item["imagePath"]
		elif 'programSerieSlug' in item:
			art="http://dr.dk/nu/api/programseries/" + item['programSerieSlug'] + "/images/1024x768.jpg"
		else:
			art=thumb

			
		if 'spotTitle' in item:
			title=item["spotTitle"]
		elif 'name' in item:
			Log("Name is " + item["name"])
			title=item["name"]
		else:
			title=item["title"]

		if 'isPremiere' in item:
			isPremiere = item["isPremiere"]
		elif 'premiere' in item:
			isPremiere = item['premiere']

		if isPremiere:
			title = title + " *PREMIERE* "
			
		if 'spotSubTitle' in item:
			summary=item["spotSubTitle"]
			subtitle=None
		else:
			summary=item["description"]
			if item['broadcastChannel'] and item['formattedBroadcastTime'] is None:
				subtitle=item["broadcastChannel"]
			elif item['broadcastChannel'] is None and item['formattedBroadcastTime']:
				subtitle=str(item["formattedBroadcastTime"])
			else:
				subtitle=str(item["formattedBroadcastTime"]) + " on " + str(item["broadcastChannel"])
			
			if 'duration' in item:
				subtitle = subtitle + " ["+ str(item["duration"]) + "]"

		if 'videoResourceUrl' in item:
			JSONvideoUrl=item["videoResourceUrl"]
		else:
			JSONvideoUrl = str(JSON.ObjectFromURL(key)["videoResourceUrl"])

		Log("Adding video from " + JSONvideoUrl)

		content = JSON.ObjectFromURL(JSONvideoUrl)

		if 'restrictedToDenmark' in content:
			dkOnly = content['restrictedToDenmark']
		else:
			dkOnly = false

		if "name" in content:  ## this is the case for some entries in TV AVISEN
			title = content["name"]

		## hack to get repeated shows to show up with dates
		if title.upper() in titles:
			if 'formattedBroadcastTime' in item:
				title = title + " " + str(item['formattedBroadcastTime'])
			else:
				title = title + " " + subtitle

		if dkOnly and Locale.Geolocation != "DK":
			title = title + " [DK Only] " 

		titles.add(title.upper())
		# get mp4 first (i.e. Barda only has mp4 and wmv, but no quality)
		videos = content["links"]
		videos = [elem for elem in videos if elem["fileType"] == "mp4" and elem["linkType"] == "Streaming" ]
		
		if not videos:
			## TODO: figure out a better way to show info about no videos available
			##title = "Not Found: " + title
			dir.Append(RTMPVideoItem("novideourl", clip="novideofound", live=False, title=title, summary=summary, thumb=thumb,subtitle=subtitle))
		else:
			map = dict()
			for video in videos:
				# get the qualities
				if 'bitrateKbps' in video:
					quality=int(video["bitrateKbps"])
					uri = video["uri"]
					map[quality] = uri
				
			if map:
				if Prefs['quality'] == "high":
					idx = sorted(map)[-1] ## highest bitrate by using -1 (last element)
					
				elif Prefs['quality'] == "low":
					idx = sorted(map)[0] ## 0 for first element with lowest bitrate
				else:
					if len(map) <= 2:
						idx = sorted(map)[0]
					elif len(map) > 2:
						idx = sorted(map)[len(map)/2]
				bestUri = map[idx]
			else:
				bestUri = videos[0]["uri"]

			baseUrl = "rtmp://vod.dr.dk/cms/"
		       	clip = "mp4:" + bestUri.split(":")[2]

	       		
       			if 'width' not in content and 'height' not in content:
				dir.Append(RTMPVideoItem(baseUrl,
							 clip=clip,
							 live=False, title=title, summary=summary, thumb=thumb,subtitle=subtitle ))
			else:
				dir.Append(RTMPVideoItem(baseUrl,
							 clip=clip,
							 width=content['width'], height=content['height'],
							 live=False, title=title, summary=summary, thumb=thumb,subtitle=subtitle ))
	return dir

def NoVideos(sender,id):
	return

def getRadioMetadata(channelId):
	
	# This is a undocumented feature that might break the plugin.
	JSONobj = JSON.ObjectFromURL(RADIO_NOWNEXT_URL % channelId, cacheTime = 60)
	title_now = ""
	description_now = ""
	start_now = ""
	stop_now = "" 
	title_next = "" 
	description_next = "" 
	start_next = ""
	stop_next = ""
	trackop = ""
	
	if JSONobj['currentProgram']:
		if JSONobj['currentProgram']['title']:
			title_now = String.StripTags(JSONobj['currentProgram']['title']).replace("'","\'")
		if JSONobj['currentProgram']['description']:
			description_now = "\n" +String.StripTags(JSONobj['currentProgram']['description']).replace("'","\'")
		if JSONobj['currentProgram']['start'] and JSONobj['currentProgram']['stop']:
			start_now = "'\n" +JSONobj['currentProgram']['start'].split('T')[1].split(':')[0]+":"+JSONobj['currentProgram']['start'].split('T')[1].split(':')[1]
			stop_now = "-"+JSONobj['currentProgram']['stop'].split('T')[1].split(':')[0]+":"+JSONobj['currentProgram']['stop'].split('T')[1].split(':')[1]

	if JSONobj['nextProgram']:
		if JSONobj['nextProgram']['title']:
			title_next = "\n\n" + String.StripTags(JSONobj['nextProgram']['title']).replace("'","\'")
		if JSONobj['nextProgram']['description']:
			description_next = "\n" + String.StripTags(JSONobj['nextProgram']['description']).replace("'","\'")
		if JSONobj['nextProgram']['start'] and JSONobj['nextProgram']['stop']:
			start_next = "\n" + JSONobj['nextProgram']['start'].split('T')[1].split(':')[0]+":"+JSONobj['nextProgram']['start'].split('T')[1].split(':')[1]
			stop_next = "-" + JSONobj['nextProgram']['stop'].split('T')[1].split(':')[0]+":"+JSONobj['nextProgram']['stop'].split('T')[1].split(':')[1]

	try:
		JSONobjTracks = JSON.ObjectFromURL(RADIO_TRACKS_URL % channelId, cacheTime=30, errors='Ingore')
		if JSONobjTracks['tracks']:
			pre1 = "\n\nSeneste Titel: "
			for track in JSONobjTracks['tracks']:
				if track['displayArtist']:
					trackop = trackop + pre1 + track['displayArtist']
				if track['title']:
					trackop = trackop + "\n" + track['title'] + "\n\n"
				pre1 = "Forrige: "
	except:pass			
					
	strNowNext = title_now + description_now + start_now + stop_now + title_next + description_next + start_next + stop_next + trackop
		
	Log.Debug(strNowNext)
	return strNowNext

def getTVLiveMetadata(channelID):
	# this is a undocumented feature that might break the plugin

	channels = JSON.ObjectFromURL("http://www.dr.dk/nu/api/nownext", cacheTime=60)
	title_now = "Ingen titel tilgængenlig"
	title_next = "Ingen titel tilgængenlig"
	description_now = ""
	description_next = ""
				
	for channel in channels["channels"]:
		if channelID in channel['channel'] :
			if channel['current']:
				if channel['current']['programTitle']:
					title_now = L(channel['current']['programTitle'])
					Log.Debug(title_now)
				if channel['current']['description']:
					description_now = (channel['current']['description'])
					Log.Debug(description_now)
			if channel['next']:
				if channel['next']['programTitle']:
					title_next = L(channel['next']['programTitle'])
					Log.Debug(title_next)
				if channel['next']['description']:
					description_next = L(channel['next']['description'])
					Log.Debug(description_next)
			break
				
	title = "Nu: " + title_now + "\n" + description_now  + "\n\nNaeste: " + title_next + "\n" + description_next
			
	Log.Debug(title)		
	return str(title)




