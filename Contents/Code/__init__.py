import time
####################################################################################################

VIDEO_PREFIX = "/video/drnu"
MUSIC_PREFIX = "/music/drnu"

APIURL = "http://www.dr.dk/NU/api/%s"
APIURL_RADIO = "http://www.dr.dk/tjenester/nuradio/api/api/%s"
RADIO_NOWNEXT_URL = "http://www.dr.dk/tjenester/LiveNetRadio/datafeed/programInfo.drxml?channelId=%s"
RADIO_TRACKS_URL = "http://www.dr.dk/tjenester/LiveNetRadio/datafeed/trackInfo.drxml?channelId=%s"
NAME  = "DR NU"
ART   = 'art-default.jpg'
ICON  = 'icon-default.png'
BETATAG = " [ BETA ]"

EPG_TV = { "DR1":"http://www.dr.dk/Tjenester/epglive/epg.DR1.drxml",
		"DR2": "http://www.dr.dk/Tjenester/epglive/epg.DR2.drxml",
		"DRU": "http://www.dr.dk/Tjenester/epglive/epg.DRUpdate.drxml",
		"RAM": "http://www.dr.dk/Tjenester/epglive/epg.DRRamasjang.drxml",
		"DRK": "http://www.dr.dk/Tjenester/epglive/epg.DRK.drxml"
		}
DR_LIVE_RADIO_STREAMS = "http://www.dr.dk/LiveNetRadio/datafeed/channels.js.drxml?v=2.2"
DR_LIVE_RADIO_STREAMS_ORDER = ("P1","P2","P3", "P4", "P5","P6","P7","RAM","ROB","SK1","DAN","JAZ","DAB","NEWS")
DR_LIVE_RADIOP4_STREAM_ORDER = ("KH4","NV4","ÅR4","ÅB4","OD4","ÅL4","HO4","TR4","RØ4","ES4","NS4")

DR_TITLE_ICONS = {"DR1": ("DR1", "DR1_icon-default.png"),
				"DR2": ("DR2", "DR2_icon-default.png"),
				"DR K":	("DR K", "DRK_icon-default.png"),
				"DR Ramasjang":	("DR Ramasjang", "DR_RAMASJANG_icon-default.png"),
				"DR Update":	("DR Update", "DR_UPDATE_icon-default.png" )}
DR_LIVE_SORTORDER = ["DR1","DR2","DRU","RAM","DRK"]

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
	dir = ObjectContainer(view_group = "List", title1 = "DR NU", title2 = "TV", art = R(ART))
	dir.add(DirectoryObject(title = "Live TV", summary = "Se Live TV", art = R(ART), thumb=R(ICON), key = Callback(LiveTV)))
	dir.add(DirectoryObject(title = "Programmer", summary = "Alle Programserier", art = R(ART), thumb = R(ICON), key = Callback(ProgramSerierMenu,title = "Programmer")))
	dir.add(DirectoryObject(title = "Nyeste", summary = "De nyeste videos", thumb = R(ICON), art = R(ART), key = Callback(NewestMenu, id=None, title = "Nyeste")))
	dir.add(DirectoryObject(title = "Spot", summary = "Spot light", thumb = R(ICON), art = R(ART), key = Callback(SpotMenu, title="Spot", id = None)))
	dir.add(DirectoryObject(title = "Mest sete", summary = "Mest sete", art = R(ART), thumb = R(ICON),key = Callback(MostViewedMenu, title="Mest sete", id = None)))
	dir.add(DirectoryObject(title = "Radio", summary = "Lyt til radio", art = R(ART), thumb = R(ICON), key = Callback(MusicMainMenu)))
	dir.add(PrefsObject(title = "Indstillinger...", summary="Indstil DR NU plug-in", thumb = R(ICON), art = R(ART)))
	
	return dir


def MusicMainMenu():
	dir = ObjectContainer(view_group="List", title1 = "DR NU", title2 = "Radio", art = R(ART))
	dir.add(DirectoryObject(title = "Live Radio", summary = "Lyt til Live Radio", art = R(ART), thumb = R(ICON), key = Callback(LiveRadioMenu)))
	dir.add(DirectoryObject(title = "Programmer" + BETATAG, summary = "Alle Programserier", art = R(ART), thumb = R(ICON), key = Callback(ProgramSerierMenuRadio, title = "Programmer")))
	dir.add(DirectoryObject(title = "Nyeste" + BETATAG, summary = "De nyeste radioudsendelser", thumb = R(ICON), art = R(ART), key = Callback(NewestMenuRadio, title = "Nyeste", id = None)))
	dir.add(DirectoryObject(title = "Spot" + BETATAG, summary = "Spot light", thumb = R(ICON), art = R(ART), key = Callback(SpotMenuRadio, title="Spot", id = None)))
	dir.add(DirectoryObject(title = "Mest lyttede" + BETATAG, summary = "Mest lyttede", art = R(ART), thumb = R(ICON),key = Callback(MostViewedMenuRadio, title="Mest lyttede", id = None)))
	dir.add(DirectoryObject(title = "TV", summary = "Se TV", art = R(ART), thumb = R(ICON), key = Callback(VideoMainMenu)))
	dir.add(PrefsObject(title = "Indstillinger...", summary="Indstil DR NU plug-in", thumb = R(ICON), art = R(ART)))
	return dir



def LiveRadioMenu():
	x = HTTP.Request(DR_LIVE_RADIO_STREAMS).content
	channels = JSON.ObjectFromString(str.rstrip(str.lstrip(x, "var netradioChannelVars = { channels: '"), "'};"))
	dir = ObjectContainer(view_group = "List", title1 = "DR NU", title2 = "Live Radio", art = R(ART))

 	bP4Menu = False

	for channel in channels:
		if channel['source_url'] in DR_LIVE_RADIO_STREAMS_ORDER:
			if not channel['redirect']:
				vco = VideoClipObject(title = channel['title'], key = channel['mediaFile'][0], summary = "", art = R(ART), thumb = R(ICON))
				for server in channel['mediaFile']:
					serverURL = server.rpartition('/')[0]
					clipURL = server.rpartition('/')[2]
					vco.add(MediaObject(parts = [PartObject(key = RTMPVideoURL(serverURL, clip = clipURL, height = None, width = None, live = True))]))
					## could replace HQ to MQ or LQ for differentation
					
				dir.add(vco)
		elif channel['source_url'] in DR_LIVE_RADIOP4_STREAM_ORDER and bP4Menu is False:
					dir.add(DirectoryObject(title = "P4", summary = String.Encode("Vælg din regionale P4"), art = R(ART),thumb=R(ICON), key = Callback(LiveRadioP4Menu, channels = channels)))		
					bP4Menu = True
	return dir

def LiveRadioP4Menu(channels):
	dir = ObjectContainer(view_group="List",title1 = "DR NU", title2 = "P4", art = R(ART))

	for channel in channels:
		if channel['source_url'] in DR_LIVE_RADIOP4_STREAM_ORDER:
			if not channel['redirect']:
				vco = VideoClipObject(title = channel['title'], key = channel['mediaFile'][0] , summary = "", art = R(ART), thumb = R(ICON))	
				
				for server in channel['mediaFile']:
					serverURL = server.rpartition('/')[0]
					clipURL = server.rpartition('/')[2]
					vco.add(MediaObject(parts = [PartObject(key = RTMPVideoURL(serverURL, clip = clipURL, height = None, width = None, live = True))]))
				dir.add(vco) 

	return dir

def LiveTV():
	dir = ObjectContainer(view_group="List", title1 = "DR NU", title2 = "Live TV", art = R(ART) )
	x = HTTP.Request("http://www.dr.dk/nu/embed/live").content
	xr = str.rpartition(x, "'liveStreams':")[2]
	xl = str.split(xr, "};")[0]
	channels = JSON.ObjectFromString(xl)
	for channel in channels:
		channelObj = VideoClipObject(key = "http://www.dr.dk/nu/live/#" + channel['channelName'],
									title = channel['channelName'],
									thumb = R(DR_TITLE_ICONS[channel['channelName']][1])  )
		for mediaFiles in channel['mediaFiles']:
			bandwidth = mediaFiles['kbps']
			for mediaFile in mediaFiles['mediaFile']:
				medObj = MediaObject(bitrate = bandwidth) 
				server = mediaFile.rpartition('/')[0]
				clip = mediaFile.rpartition("/")[2]
				po = PartObject(key = RTMPVideoURL(server, clip = clip, height = 467, width = 830, live = True))
				medObj.add(po)
				channelObj.add(medObj)
		dir.add(channelObj)
			
	return dir



def ProgramSerierMenu(title):
	dir = ObjectContainer(view_group = "List", title1 = "DR NU", title2 = title )
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
		thumb=APIURL % "programseries/" + slug + "/images/512x512.jpg"
		Log.Debug(thumb)

		letter = title[0].upper()
		if letter not in bucket:
			bucket[letter] = list()
		tuple = dict(title=title,subtitle=subtitle,thumb=thumb,art=thumb,summary=summary,id=slug)
		bucket[letter].append(tuple)

	for firstChar in sorted(bucket.iterkeys()):
		serier = bucket[firstChar]
		if Prefs['group_per_letter']:
			dir.add(DirectoryObject(title = firstChar, 
								art = R(ART), 
								thumb = R(ICON), 
								key = Callback(LetterMenu, 
											title = firstChar, 
											serier = serier
											 )))
		
		else:
			for serie in serier:
				dir.add(DirectoryObject(title = serie['title'], 
									tagline = serie['subtitle'], 
									summary = serie['summary'], 
									art = R(ART), 
									thumb = APIURL % "programseries/" + serie['id'] + "/images/512x512.jpg", 
									key = Callback(ProgramMenu, id = serie['id'], title = serie['title'])))

			
	return dir

def LetterMenu(title, serier):
	dir = ObjectContainer(view_group="List", title1 = "DR NU", title2 = title)
	for serie in serier:
		JSONobj = JSON.ObjectFromURL(APIURL % "Programseries/" + serie['id'] + "/videos")
		dir.add(DirectoryObject(title = serie['title'], summary = serie['summary'], art = R(ART), thumb = APIURL % "programseries/"+serie['id']+"/images/512x512.jpg", key = Callback(CreateVideoItem, items = JSONobj, title = serie['title'], id = serie['id'])))
	return dir

def NewestMenu(id, title):
        return CreateVideoItem(id=id, title=title, items=JSON.ObjectFromURL(APIURL % "videos/newest.json"))

def MostViewedMenu(id, title):
        return CreateVideoItem(id=id, title=title, items=JSON.ObjectFromURL(APIURL % "videos/mostviewed.json"))

def SpotMenu(id, title):
        return CreateVideoItem(id=id, title=title, items=JSON.ObjectFromURL(APIURL % "videos/spot.json"))

def ProgramMenu(id, title):
	Log.Debug(str(id))
	return CreateVideoItem(id=id, title=title, items=JSON.ObjectFromURL(APIURL % "programseries/" + id + "/videos"))



		
def CreateVideoItem(id, items, title):
	dir = ObjectContainer(view_group = "List", title1 = "DR NU", title2 = title)

	titles = set()
	for item in items:
		key=APIURL % "videos/" + str(item['id'])
		thumb=APIURL % "videos/" + str(item['id']) + "/images/512x512.jpg"

		if 'imagePath' in item:
			art="http://dr.dk/nu" + item["imagePath"]
		elif 'programSerieSlug' in item:
			art= APIURL % "programseries/" + item['programSerieSlug'] + "/images/1024x768.jpg"
		else:
			art=thumb
		Log.Debug(art)
			
		if 'spotTitle' in item:
			title=item["spotTitle"]
		elif 'name' in item:
			title=item["name"]
		else:
			title=item["title"]

		if 'isPremiere' in item:
			isPremiere = item["isPremiere"]
		elif 'premiere' in item:
			isPremiere = item['premiere']

		if isPremiere:
			title = str(title) + " *PREMIERE* "
			
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
			Log.Debug(key)
			JSONvideoUrl = str(JSON.ObjectFromURL(key)["videoResourceUrl"])

		content = JSON.ObjectFromURL(JSONvideoUrl)

		if 'restrictedToDenmark' in content:
			dkOnly = content['restrictedToDenmark']
		else:
			dkOnly = false

		if "name" in content:  ## this is the case for some entries in TV AVISEN
			title = content["name"]

	#	if 'broadcastTime' in item:
	#		originally_available_at = item['broadcastTime'].replace(
	#	else:
	#		originally_available_at = Null

		## hack to get repeated shows to show up with dates
		if title.upper() in titles:
			if 'formattedBroadcastTime' in item:
				title = title + " " + str(item['formattedBroadcastTime'])
			else:
				title = title + " " + subtitle

		if dkOnly and Locale.Geolocation != "DK":
			title = title + " [DK Only] " 

		titles.add(title.upper())
		
		## New video adding
		
		vco = VideoClipObject(title = title, art = art, summary = summary, thumb = thumb, key = key)
		if len(content['links'])>0:
			for video in content['links']:
				mo = MediaObject()
				
				if 'bitrateKbps' in video:
					mo.bitrate = video['bitrateKbps']
				else:
					mo.bitrate = 250
					
				if 'height' in video:
					height = video['height']
				else:
					height = None
						
				if 'width' in video:
					width = video['width']
				else:
					width = None 
	
				if video['fileType'] == "mp4":
					baseClip = video['uri'].rpartition(':')
					clip = "mp4:" + baseClip[2]
					baseUrl = baseClip[0].rpartition('/')[0]+"/"
					po = PartObject(key = RTMPVideoURL(baseUrl, clip = clip, height = height, width = width, live = False))
				elif video['fileType'] == "wmv":
					po = PartObject(key = WindowsMediaVideoURL(video['uri'], height = height, width = width))
				else:
					po = PartObject(key = video['uri'])
				mo.add(po)
				vco.add(mo)
		else:
			vco.add(MediaObject(parts = [PartObject(key = JSON.ObjectFromURL(key)["videoManifestUrl"])]))
		dir.add(vco)
	return dir

def getRadioMetadata(channelId):
	
	# This is a undocumented feature that might break the plugin.
#	JSONobj = JSON.ObjectFromURL(RADIO_NOWNEXT_URL % channelId, cacheTime = 60)
#	title_now = ""
#	description_now = ""
#	start_now = ""
#	stop_now = "" 
#	title_next = "" 
#	description_next = "" 
#	start_next = ""
#	stop_next = ""
#	trackop = ""
#	strNowNext = "Fejl under hentning af data"	
#	try:
#		if JSONobj['currentProgram']:
#			if JSONobj['currentProgram']['title']:
#				title_now = String.StripTags(JSONobj['currentProgram']['title']).replace("'","\'")
#			if JSONobj['currentProgram']['description']:
#				description_now = "\n" + String.StripTags(JSONobj['currentProgram']['description']).replace("'","\'")
#			if JSONobj['currentProgram']['start'] and JSONobj['currentProgram']['stop']:
#				start_now = "'\n" +JSONobj['currentProgram']['start'].split('T')[1].split(':')[0]+":"+JSONobj['currentProgram']['start'].split('T')[1].split(':')[1]
#				stop_now = "-"+JSONobj['currentProgram']['stop'].split('T')[1].split(':')[0]+":"+JSONobj['currentProgram']['stop'].split('T')[1].split(':')[1]
#	
#		if JSONobj['nextProgram']:
#			if JSONobj['nextProgram']['title']:
#				title_next = "\n\n" + String.StripTags(JSONobj['nextProgram']['title']).replace("'","\'")
#			if JSONobj['nextProgram']['description']:
#				description_next = "\n" + String.StripTags(JSONobj['nextProgram']['description']).replace("'","\'")
#			if JSONobj['nextProgram']['start'] and JSONobj['nextProgram']['stop']:
#				start_next = "\n" + JSONobj['nextProgram']['start'].split('T')[1].split(':')[0]+":"+JSONobj['nextProgram']['start'].split('T')[1].split(':')[1]
#				stop_next = "-" + JSONobj['nextProgram']['stop'].split('T')[1].split(':')[0]+":"+JSONobj['nextProgram']['stop'].split('T')[1].split(':')[1]
#	
#		
#			JSONobjTracks = JSON.ObjectFromURL(RADIO_TRACKS_URL % channelId, cacheTime=30, errors='Ingore')
#			if JSONobjTracks['tracks']:
#				pre1 = "\n\nSeneste Titel: "
#				for track in JSONobjTracks['tracks']:
#					if track['displayArtist']:
#						trackop = trackop + pre1 + track['displayArtist']
#					if track['title']:
#						trackop = trackop + "\n" + track['title'] + "\n\n"
#					pre1 = "Forrige: "
#		strNowNext = title_now + description_now + start_now + stop_now + title_next + description_next + start_next + stop_next + trackop
#	except:pass
#		
#					
#	
#		
#	return strNowNext
	return ""

def getTVLiveMetadata(channelID):
	# this is a undocumented feature that might break the plugin

	channels = JSON.ObjectFromURL("http://www.dr.dk/nu/api/nownext", cacheTime=60)
	title_now = "Ingen titel tilgængenlig"
	title_next = "Ingen titel tilgængenlig"
	description_now = ""
	description_next = ""
				
	for channel in channels["channels"]:
		if DR_TITLE_ICONS[channelID][0] in channel['channel'] :
			if channel['current']:
				if channel['current']:
					title_now = L(channel['current']['programTitle'])
				if channel['current']['description']:
					description_now = (channel['current']['description'])
			if channel['next']:
				if channel['next']['programTitle']:
					title_next = L(channel['next']['programTitle'])
				if channel['next']['description']:
					description_next = L(channel['next']['description'])
			break
				
	title = "Nu: " + title_now + "\n" + description_now  + "\n\nNaeste: " + title_next + "\n" + description_next
			
	return str(title)

def ProgramSerierMenuRadio(title):
	dir = ObjectContainer(view_group = "List", title1 = "DR NU", title2 = title )
	JSONObject=JSON.ObjectFromURL(APIURL_RADIO % "programseries.json")

	bucket = dict()
	letter = ''
	for program in JSONObject:
		slug=program["slug"]
		title=program["title"]
		if program["videoCount"] > 1:
			title = title + " (" + str(program["videoCount"]) + " afs.)"
		subtitle=", ".join(program["labels"])
		
		summary=program["description"]
		thumb=APIURL % "programseries/" + slug + "/images/512x512.jpg"

		letter = title[0].upper()
		if letter not in bucket:
			bucket[letter] = list()
		tuple = dict(title=title,subtitle=subtitle,thumb=thumb,summary=summary,id=slug)
		bucket[letter].append(tuple)

	for firstChar in sorted(bucket.iterkeys()):
		serier = bucket[firstChar]
		if Prefs['group_per_letter']:
			dir.add(DirectoryObject(title = firstChar, 
								art = R(ART), 
								thumb = R(ICON), 
								key = Callback(LetterMenuRadio, 
											title = firstChar, 
											serier = serier )))
		
		else:
			for serie in serier:
				dir.add(DirectoryObject(title = serie['title'], 
									tagline = serie['subtitle'], 
									summary = serie['summary'], 
									art = R(ART), 
									thumb = thumb, 
									key = Callback(ProgramMenuRadio, id = serie['id'], title = serie['title'])))
	return dir

def LetterMenuRadio(title, serier):
	dir = ObjectContainer(view_group="List", title1 = "DR NU", title2 = title)
	for serie in serier:
		JSONobj = JSON.ObjectFromURL(APIURL_RADIO % "Programseries/" + serie['id'] + "/videos")
		dir.add(DirectoryObject(title = serie['title'], summary = serie['summary'], art = R(ART), thumb = APIURL_RADIO % "programseries/"+serie['id']+"/images/512x512.jpg", key = Callback(CreateRadioItem, items = JSONobj, title = serie['title'], id = serie['id'])))
	return dir

def NewestMenuRadio(id, title):
        return CreateRadioItem(id=id, title=title, items=JSON.ObjectFromURL(APIURL_RADIO % "videos/newest.json"))

def MostViewedMenuRadio(id, title):
        return CreateRadioItem(id=id, title=title, items=JSON.ObjectFromURL(APIURL_RADIO % "videos/mostviewed.json"))

def SpotMenuRadio(id, title):
        return CreateRadioItem(id=id, title=title, items=JSON.ObjectFromURL(APIURL_RADIO % "videos/spot.json"))

def ProgramMenuRadio(id, title):
	return CreateRadioItem(id=id, title=title, items=JSON.ObjectFromURL(APIURL_RADIO % "programseries/" + id + "/videos"))


		
def CreateRadioItem(id, items, title):
	dir = ObjectContainer(view_group = "List", title1 = "DR NU", title2 = title)

	titles = set()
	for item in items:
		key=APIURL_RADIO % "videos/" + str(item['id'])
		thumb=APIURL_RADIO % "videos/" + str(item['id']) + "/images/512x512.jpg"

		if 'imagePath' in item:
			art="http://dr.dk/nu" + item["imagePath"]
		elif 'programSerieSlug' in item:
			art= APIURL_RADIO % "programseries/" + item['programSerieSlug'] + "/images/1024x768.jpg"
		else:
			art=thumb

			
		if 'spotTitle' in item:
			title=str(item["spotTitle"])
		elif 'name' in item:
			title=str(item["name"])
		else:
			title=str(item["title"])

		if 'isPremiere' in item:
			isPremiere = str(item["isPremiere"])
		elif 'premiere' in item:
			isPremiere = str(item['premiere'])

#		if isPremiere:
#			title = str(title) + str(" *PREMIERE* ")
#			
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
		
		## New video adding
		
		vco = VideoClipObject(title = title, summary = summary, thumb = thumb, key = key)
		if len(content['links'])>0:
			for video in content['links']:
				mo = MediaObject()
				
				if 'bitrateKbps' in video:
					mo.bitrate = video['bitrateKbps']

				if 'height' in video:
					height = video['height']
				else:
					height = None
						
				if 'width' in video:
					width = video['width']
				else:
					width = None 

				if video['fileType'] == "mp4":
					baseClip = video['uri'].rpartition(':')
					clip = "mp4:" + baseClip[2]
					baseUrl = baseClip[0].rpartition('/')[0]+"/"
					po = PartObject(key = RTMPVideoURL(baseUrl, clip = clip, height = height, width = width, live = False))
				elif video['fileType'] == "wma":
					po = PartObject(key = WindowsMediaVideoURL(video['uri'], height = height, width = width))
				else:
					po = PartObject(key = video['uri'])

				mo.add(po)
				vco.add(mo)
		else:
			vco.add(MediaObject(parts = [PartObject(key = JSON.ObjectFromURL(key)["videoManifestUrl"])]))
		dir.add(vco)
	return dir
