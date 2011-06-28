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
DR_LIVE_STREAMS ={"DR1": [("livedr01astream3", 1000), ("livedr01bstream3", 1000),("livedr01astream2", 500),("livedr01bstream2", 500),("livedr01astream1", 250), ("livedr01bstream1",250)],
			"DR2": [("livedr02astream3", 1000), ("livedr02bstream3", 1000),("livedr02astream2", 500),("livedr02bstream2", 500), ("livedr02astream1", 250), ("livedr02bstream1",250)],
			"DRU": [("livedr03astream3", 1000), ("livedr03bstream3", 1000),("livedr03astream2", 500),("livedr03bstream2", 500), ("livedr03astream1", 250), ("livedr03bstream1",250)],
			"RAM": [("livedr05astream3", 1000), ("livedr05bstream3", 1000),("livedr05astream2", 500),("livedr05bstream2", 500), ("livedr05astream1", 250), ("livedr05bstream1",250)],
			"DRK": [("livedr04astream3", 1000), ("livedr04bstream3", 1000),("livedr04astream2", 500),("livedr04bstream2", 500), ("livedr04astream1", 250), ("livedr04bstream1",250)]	
			}
DR_LIVE_RADIO_STREAMS = {"P1": ["P1", "P1", [("Channel3_HQ", 192),("Channel3_LQ", 64)]],
					"P2": ["P2", "P2", [("Channel4_HQ", 192),("Channel4_LQ", 64)]],
					"P3": ["P3", "P3", [("Channel5_HQ", 192),("Channel5_LQ", 64)]],
					"P4": [{"KH4": ["P4 København", "KH4", [("Channel8_HQ", 192),("Channel8_LQ", 64)]],
						"NV4": ["P4 Sjælland", "NV4", [("Channel11_HQ", 192),("Channel11_LQ", 64)]],
						"AAR4": ["P4 Østjylland", None, [("Channel14_HQ", 192),("Channel14_LQ", 64)]],
						"AAB4": ["P4 Syd", None, [("Channel12_HQ", 192),("Channel12_LQ", 64)]],
						"OD4": ["P4 Fyn", "OD4", [("Channel7_HQ", 192),("Channel7_LQ", 64)]],
						"AAL4": ["P4 Nordjylland", None, [("Channel10_HQ", 192),("Channel10_LQ", 64)]],
						"HO4": ["P4 Midt & Vest", "HO4", [("Channel9_HQ", 192),("Channel9_LQ", 64)]],
						"TR4": ["P4 Trekanten", "TR4", [("Channel13_HQ", 192),("Channel13_LQ", 64)]],
						"ROE4": ["P4 Bornholm", None, [("Channel6_HQ", 192),("Channel6_LQ", 64)]],
						"ES4": ["P4 Esbjerg", "ES4", [("Channel15_HQ", 192),("Channel15_LQ", 64)]],
						"NS4": ["P4 NordvestSjælland", "NS4", [("Channel11_HQ", 192),("Channel11_LQ", 64)]]
						}],
					"P5": ["DR P5", "P5D", [("Channel25_HQ", 192),("Channel25_LQ", 64)]],
					"P6": ["DR P6 Beat", "P6B", [("Channe29_HQ", 192),("Channe29_LQ", 64)]],
					"P7": ["DR P7 Mix", "P7M", [("Channel21_HQ", 192),("Channel21_LQ", 64)]],
					"RAM": ["DR Ramasjang Radio", "RAM", [("Channel24_HQ", 192),("Channel24_LQ", 64)]],
					"ROB": ["DR R&B", "ROB", [("Channel26_HQ", 192),("Channel26_LQ", 64)]],
					"SK1": ["DR Boogieradio", "SK1", [("Channel18_HQ", 192),("Channel18_LQ", 64)]],
					"DAN": ["DR Dansktop", "DAN", [("Channel19_HQ", 192),("Channel19_LQ", 64)]],
					"JAZ": ["DR Jazz", "JAZ", [("Channel22_HQ", 192),("Channel22_LQ", 64)]],
					"DAB": ["DR Klassisk", "DAB", [("Channe23_HQ", 192),("Channel23_LQ", 64)]],
					"NEWS": ["DR Nyheder", "NEWS", [("Channel2_HQ", 192),("Channel2_LQ", 64)]]
					}
DR_LIVE_RADIO_STREAMS_ORDER = ("P1","P2","P3", "P4", "P5","P6","P7","RAM","ROB","SK1","DAN","JAZ","DAB","NEWS")
DR_LIVE_RADIOP4_STREAM_ORDER = ("KH4","NV4","AAR4","AAB4","OD4","AAL4","HO4","TR4","ROE4","ES4","NS4")

DR_TITLE_ICONS = {"DR1": ("DR1", "DR1_icon-default.png"),
				"DR2": ("DR2", "DR2_icon-default.png"),
				"DRU":	("DR K", "DRK_icon-default.png"),
				"RAM":	("DR Ramasjang", "DR_RAMASJANG_icon-default.png"),
				"DRK":	("DR Update", "DR_UPDATE_icon-default.png" )}
DR_LIVE_SORTORDER = ["DR1","DR2","DRU","RAM","DRK"]
LIVE_RADIO_SERVERS = ("rtmp://live.gss.dr.dk/live/", "rtmp://live-rtmpt.gss.dr.dk:80/live/")

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
	dir.add(DirectoryObject(title = "Programmer", summary = "Alle Programserier", art = R(ART), thumb = R(ICON), key = Callback(ProgramSerierMenu,id = None, title = "Programmer")))
	dir.add(DirectoryObject(title = "Nyeste", summary = "De nyeste videos", thumb = R(ICON), art = R(ART), key = Callback(CreateVideoItem, items=JSON.ObjectFromURL(APIURL % "videos/newest.json"), title = "Nyeste")))
	dir.add(DirectoryObject(title = "Spot", summary = "Spot light", thumb = R(ICON), art = R(ART), key = Callback(CreateVideoItem, title="Spot", items=JSON.ObjectFromURL(APIURL % "videos/spot.json"))))
	dir.add(DirectoryObject(title = "Mest sete", summary = "Mest sete", art = R(ART), thumb = R(ICON),key = Callback(CreateVideoItem, title="Mest sete", items=JSON.ObjectFromURL(APIURL % "videos/mostviewed.json"))))
	dir.add(DirectoryObject(title = "Radio", summary = "Lyt til radio", art = R(ART), thumb = R(ICON), key = Callback(MusicMainMenu)))
	dir.add(PrefsObject(title = "Indstillinger...", summary="Indstil DR NU plug-in", thumb = R(ICON), art = R(ART)))
	return dir


def MusicMainMenu():
	dir = ObjectContainer(view_group="List", title1 = "DR NU", title2 = "Radio", art = R(ART))
	dir.add(DirectoryObject(title = "Live Radio", summary = "Lyt til Live Radio", art = R(ART), thumb = R(ICON), key = Callback(LiveRadioMenu)))
	dir.add(DirectoryObject(title = "Programmer" + BETATAG, summary = "Alle Programserier", art = R(ART), thumb = R(ICON), key = Callback(ProgramSerierMenuRadio,id = None, title = "Programmer")))
	dir.add(DirectoryObject(title = "Nyeste" + BETATAG, summary = "De nyeste radioudsendelser", thumb = R(ICON), art = R(ART), key = Callback(CreateRadioItem, items=JSON.ObjectFromURL(APIURL_RADIO % "videos/newest.json"), title = "Nyeste")))
	dir.add(DirectoryObject(title = "Spot" + BETATAG, summary = "Spot light", thumb = R(ICON), art = R(ART), key = Callback(CreateRadioItem, title="Spot", items=JSON.ObjectFromURL(APIURL_RADIO % "videos/spot.json"))))
	dir.add(DirectoryObject(title = "Mest sete" + BETATAG, summary = "Mest sete", art = R(ART), thumb = R(ICON),key = Callback(CreateRadioItem, title="Mest sete", items=JSON.ObjectFromURL(APIURL_RADIO % "videos/mostviewed.json"))))
	dir.add(DirectoryObject(title = "TV", summary = "Se TV", art = R(ART), thumb = R(ICON), key = Callback(VideoMainMenu)))
	dir.add(PrefsObject(title = "Indstillinger...", summary="Indstil DR NU plug-in", thumb = R(ICON), art = R(ART)))
	return dir

def LiveRadioMenu():
	dir = ObjectContainer(view_group = "List", title1 = "DR NU", title2 = "Live Radio", art = R(ART))
	if Prefs['quality'] == 'low':
		qIndex = 1
	elif Prefs['quality'] == 'medium':
		qIndex = 1
	else:
		qIndex = 0
	for channel in DR_LIVE_RADIO_STREAMS_ORDER:
		if channel is not "P4":
			vco = VideoClipObject(title = DR_LIVE_RADIO_STREAMS[channel][0], key = "http://www.dr.dk/#" + channel, summary = getRadioMetadata(channel), art = R(ART), thumb = R(ICON))
			if Prefs['quality'] is "auto":
				for links in DR_LIVE_RADIO_STREAMS[channel][2]:
					for server in LIVE_RADIO_SERVERS:
						vco.add(MediaObject(bitrate = links[1], parts = [PartObject(key=RTMPVideoURL(server, clip = links[0], height = None, width = None, live = True))]))
				dir.add(vco)
			else:
				for server in LIVE_RADIO_SERVERS:
					vco.add(MediaObject(bitrate = DR_LIVE_RADIO_STREAMS[channel][2][qIndex][1], parts = [PartObject(key = RTMPVideoURL(server, clip = DR_LIVE_RADIO_STREAMS[channel][2][qIndex][0], height = None, width = None, live = True))]))
				dir.add(vco)	
		else:
			dir.add(DirectoryObject(title = "P4", summary = "Vælg din regionale P4", art = R(ART),thumb=R(ICON), key = Callback(LiveRadioP4Menu)))				
	return dir

def LiveRadioP4Menu():
	dir = ObjectContainer(view_group="List",title1 = "DR NU", title2 = "P4", art = R(ART))
	if Prefs['quality'] == 'low':
		qIndex = 1
	elif Prefs['quality'] == 'medium':
		qIndex = 1
	else:
		qIndex = 0
	for channel in DR_LIVE_RADIOP4_STREAM_ORDER:
		vco = VideoClipObject(title = DR_LIVE_RADIO_STREAMS["P4"][0][channel][0], key = "http://www.dr.dk/" + channel, summary = getRadioMetadata(channel), art = R(ART), thumb = R(ICON))	
		if Prefs['quality'] is "auto":
			for links in DR_LIVE_RADIO_STREAMS["P4"][0][channel][2]:
				for server in LIVE_RADIO_SERVERS:
						vco.add(MediaObject(bitrate = links[1], parts = [PartObject(key=RTMPVideoURL(server, clip = links[0], height = None, width = None, live = True))]))
		else:
			for server in LIVE_RADIO_SERVERS:
				vco.add(MediaObject(bitrate = DR_LIVE_RADIO_STREAMS["P4"][0][channel][2][qIndex][1], parts = [PartObject(key = RTMPVideoURL(server, clip = DR_LIVE_RADIO_STREAMS["P4"][0][channel][2][qIndex][0], height = None, width = None, live = True))]))
		dir.add(vco)
	return dir

def LiveTV():
	dir = ObjectContainer(view_group="List", title1 = "DR NU", title2 = "Live TV", art = R(ART) )
	drRTMP = "rtmp://rtmplive.dr.dk/live"
	for channelID in DR_LIVE_SORTORDER: 
	
		channelObj = MovieObject(url = "http://www.dr.dk/nu/live#%s" % channelID,
								title = DR_TITLE_ICONS[channelID][0],
								thumb = R(DR_TITLE_ICONS[channelID][1]),
								art = R(ART),
								summary = getTVLiveMetadata(channelID)
								)
		if Prefs['quality'] == "auto":
			for channel in DR_LIVE_STREAMS[channelID]:
				medObj = MediaObject(protocols = Protocol.RTMP,
									bitrate = channel[1],
									audio_channels = 2)
				po = PartObject(key = RTMPVideoURL(drRTMP, clip = channel[0], live=True, height=467, width=830))
				medObj.add(po)
				channelObj.add(medObj)
		else:
			channel = DR_LIVE_STREAMS[channelID]
			if Prefs['quality'] == "high":
				singleBandwidth = 1000
				clip1 = channel[0][0]
				clip2 = channel[1][0]
			if Prefs['quality'] == "medium":
				singleBandwidth = 500
				clip1 = channel[2][0]
				clip2 = channel[3][0]
			if Prefs['quality'] == "low":
				clip1 = channel[4][0]
				clip2 = channel[5][0]
				singleBandwidth = 250
			medObj1 = MediaObject(protocols = Protocol.RTMP,
								bitrate = singleBandwidth,
								audio_channels = 2,
								
								)
			medObj2 = MediaObject(protocols = Protocol.RTMP,
								bitrate = singleBandwidth,
								audio_channels = 2
								)
			po1 = PartObject(key = RTMPVideoURL(drRTMP, clip = clip1, live = True, height = 467, width = 830))
			po2 = PartObject(key = RTMPVideoURL(drRTMP, clip = clip2, live = True, height = 467, width = 830))
			medObj1.add(po1)
			medObj2.add(po2)
			channelObj.add(medObj1)
			channelObj.add(medObj2)
		dir.add(channelObj)
		#dir.add(LiveTVChannel(channel))
	return dir



def ProgramSerierMenu(id,title):
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
								key = Callback(LetterMenu, 
											title = firstChar, 
											serier = serier )))
		
		else:
			for serie in serier:
				dir.add(DirectoryObject(title = serie['title'], 
									tagline = serie['subtitle'], 
									summary = serie['summary'], 
									art = R(ART), 
									thumb = thumb, 
									key = Callback(CreateVideoItem, 
												items = JSON.ObjectFromURL(APIURL % "programseries/"+serie['id'] + "/videos"),
												title = serie['title'])))
			
	return dir

def LetterMenu(title, serier):
	dir = ObjectContainer(view_group="List", title1 = "DR NU", title2 = title)
	for serie in serier:
		JSONobj = JSON.ObjectFromURL(APIURL % "Programseries/" + serie['id'] + "/videos")
		dir.add(DirectoryObject(title = serie['title'], summary = serie['summary'], art = R(ART), thumb = APIURL % "programseries/"+serie['id']+"/images/512x512.jpg", key = Callback(CreateVideoItem, items = JSONobj, title = serie['title'])))
	return dir

		
def CreateVideoItem(items, title):
	dir = ObjectContainer(view_group = "List", title1 = "DR NU", title2 = title)

	titles = set()
	for item in items:
		key=APIURL % "videos/" + str(item["id"])
		thumb=APIURL % "videos/" + str(item["id"]) + "/images/512x512.jpg"

		if 'imagePath' in item:
			art="http://dr.dk/nu" + item["imagePath"]
		elif 'programSerieSlug' in item:
			art= APIURL % "programseries/" + item['programSerieSlug'] + "/images/1024x768.jpg"
		else:
			art=thumb

			
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
		
		if Prefs['quality'] == "low":
			throtle = 500
		elif Prefs['quality'] == "medium":
			throtle = 1000
		else:
			throtle = 20000
		
		
		vco = VideoClipObject(title = title, summary = summary, thumb = thumb, key = key)
		if len(content['links'])>0:
			for video in content['links']:
				mo = MediaObject()
				
				if 'bitrateKbps' in video:
					mo.bitrate = video['bitrateKbps']
				if mo.bitrate < throtle:
					if 'height' in video:
						height = video['height']
					else:
						height = None
						
					if 'width' in video:
						width = video['width']
					else:
						width = None 
	
					if video['fileType'] == "mp4":
						baseUrl = "rtmp://vod.dr.dk/cms/"
						clip = "mp4:" + video["uri"].split(":")[2]
						po = PartObject(key = RTMPVideoURL(baseUrl, clip = clip, height = height, width = width, live = False))
						#Log.Debug("Adding WM PO - key: " + po.key)
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
			description_now = "\n" + String.StripTags(JSONobj['currentProgram']['description']).replace("'","\'")
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
		
	return strNowNext

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

def ProgramSerierMenuRadio(id,title):
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
									key = Callback(CreateRadioItem, 
												items = JSON.ObjectFromURL(APIURL_RADIO % "programseries/"+serie['id'] + "/videos"),
												title = serie['title'])))
			
	return dir

def LetterMenuRadio(title, serier):
	dir = ObjectContainer(view_group="List", title1 = "DR NU", title2 = title)
	for serie in serier:
		JSONobj = JSON.ObjectFromURL(APIURL_RADIO % "Programseries/" + serie['id'] + "/videos")
		dir.add(DirectoryObject(title = serie['title'], summary = serie['summary'], art = R(ART), thumb = APIURL_RADIO % "programseries/"+serie['id']+"/images/512x512.jpg", key = Callback(CreateRadioItem, items = JSONobj, title = serie['title'])))
	return dir

		
def CreateRadioItem(items, title):
	dir = ObjectContainer(view_group = "List", title1 = "DR NU", title2 = title)

	titles = set()
	for item in items:
		key=APIURL_RADIO % "videos/" + str(item["id"])
		thumb=APIURL_RADIO % "videos/" + str(item["id"]) + "/images/512x512.jpg"

		if 'imagePath' in item:
			art="http://dr.dk/nu" + item["imagePath"]
		elif 'programSerieSlug' in item:
			art= APIURL_RADIO % "programseries/" + item['programSerieSlug'] + "/images/1024x768.jpg"
		else:
			art=thumb

			
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
		
		if Prefs['quality'] == "low":
			throtle = 500
		elif Prefs['quality'] == "medium":
			throtle = 1000
		else:
			throtle = 20000
		
		
		vco = VideoClipObject(title = title, summary = summary, thumb = thumb, key = key)
		if len(content['links'])>0:
			for video in content['links']:
				mo = MediaObject()
				
				if 'bitrateKbps' in video:
					mo.bitrate = video['bitrateKbps']
				if mo.bitrate < throtle:
					if 'height' in video:
						height = video['height']
					else:
						height = None
						
					if 'width' in video:
						width = video['width']
					else:
						width = None 
	
#					if video['fileType'] == "mp4":
#						baseUrl = "rtmp://vod.dr.dk/cms/"
#						clip = "mp4:" + video["uri"].split(":")[2]
#						po = PartObject(key = RTMPVideoURL(baseUrl, clip = clip, height = height, width = width, live = False))
						#Log.Debug("Adding WM PO - key: " + po.key)
					if video['fileType'] == "wma":
						po = PartObject(key = WindowsMediaVideoURL(video['uri'], height = height, width = width))
					else:
						po = PartObject(key = video['uri'])
					mo.add(po)
					vco.add(mo)
		else:
			vco.add(MediaObject(parts = [PartObject(key = JSON.ObjectFromURL(key)["videoManifestUrl"])]))
		dir.add(vco)
	return dir