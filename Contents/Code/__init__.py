####################################################################################################

VIDEO_PREFIX = "/video/drnu"

APIURL = "http://www.dr.dk/NU/api/%s"

NAME = "DR NU"
ART			  = 'art-default.png'
ICON		  = 'DR.png'

HTTP.CacheTime = 3600

####################################################################################################

def Start():
	Plugin.AddPrefixHandler(VIDEO_PREFIX, VideoMainMenu, NAME, ICON, ART)
	Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
	Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
	MediaContainer.art = R(ART)
	MediaContainer.title1 = NAME
	DirectoryItem.thumb = R(ICON)

def VideoMainMenu():
	dir = MediaContainer(viewGroup="List")
	dir.Append(Function(DirectoryItem(ProgramSerierMenu,"Programmer",subtitle="Alle programserier", summary="",thumb=R(ICON),art=R(ART)),id=None))
	dir.Append(Function(DirectoryItem(NewestMenu,"Nyeste",subtitle="De nyeste videoer", summary="",thumb=R(ICON),art=R(ART)),id=None))
	dir.Append(Function(DirectoryItem(SpotMenu,"Spot",subtitle="Spot light", summary="",thumb=R(ICON),art=R(ART)),id=None))
	dir.Append(Function(DirectoryItem(MostViewedMenu,"Mest Sete",subtitle="Mest Sete", summary="",thumb=R(ICON),art=R(ART)),id=None))
	dir.Append(Function(DirectoryItem(LiveTVMenu, "Live TV", subtitle="Live TV", summary="", thumb=R(ICON), art=R(ART))))
	dir.Append(Function(DirectoryItem(LiveRadioMenu, "Live Radio", subtitle="Live Radio", summary="", thumb=R(ICON), art=R(ART))))
	return dir

def ProgramSerierMenu(sender,id):
	dir=MediaContainer(title1="DR NU", title2="Programserier")
	
	JSONObject=JSON.ObjectFromURL(APIURL % "programseries.json")
	for program in JSONObject:
		slug=program["slug"]
		title=program["title"]
		summary="None"
		summary=program["description"]
		thumb=APIURL % "programseries/" + slug + "/images/600x600.jpg"
		dir.Append(Function(DirectoryItem(ProgramMenu,title=title,subtitle=summary,thumb=thumb,summary=summary),id=slug))
	return dir

def NewestMenu(sender,id):
	dir=MediaContainer(title1="DR NU", title2="Newest")
	JSONObject = JSON.ObjectFromURL(APIURL % "videos/newest.json")
	for item in JSONObject:
		key=APIURL % "videos/" + str(item["id"])
		thumb=APIURL % "videos/" + str(item["id"]) + "/images/600x600.jpg"
		title=item["title"]
		if item["isPremiere"]:
			title = title + " *PREMIERE* "
		summary=item["description"]
		subtitle=item["broadcastChannel"] + ": " + item["formattedBroadcastTime"] 
		video = JSON.ObjectFromURL(key)
		dir.Append(Function(VideoItem(GetVideos, title=title,summary=summary, subtitle=subtitle, thumb=thumb), id=video["videoResourceUrl"]))		
	return dir

def MostViewedMenu(sender,id):
	dir=MediaContainer(title1="DR NU", title2="Mest Sete")
	JSONObject = JSON.ObjectFromURL(APIURL % "videos/mostviewed.json")
	for item in JSONObject:
		key=APIURL % "videos/" + str(item["id"])
		thumb=APIURL % "videos/" + str(item["id"]) + "/images/600x600.jpg"
		title=item["title"]
		if item["premiere"]:
			title = title + " *PREMIERE* "
		summary=item["description"]
		subtitle=item["broadcastChannel"] + ": " + item["formattedBroadcastTime"] + " ["+ item["duration"] + "]"
		video = JSON.ObjectFromURL(key)
		dir.Append(Function(VideoItem(GetVideos, title=title,summary=summary, subtitle=subtitle, thumb=thumb), id=video["videoResourceUrl"]))	
	return dir

def SpotMenu(sender,id):
	dir=MediaContainer(title1="DR NU", title2="Spot")
	JSONObject = JSON.ObjectFromURL(APIURL % "videos/spot.json")
	for item in JSONObject:
		key=APIURL % "videos/" + str(item["id"])
		art="http://dr.dk/nu/" + item["imagePath"]
		title=item["spotTitle"]
		if item["isPremiere"]:
			title = title + " *PREMIERE* "
		subtitle=item["title"]
		summary=item["spotSubTitle"]
		video = JSON.ObjectFromURL(key)
		dir.Append(Function(VideoItem(GetVideos, title=title,subtitle=subtitle, summary=summary, art=art, thumb=art), id=video["videoResourceUrl"]))	
	return dir

def ProgramMenu(sender,id):
	dir=MediaContainer(title1="DR NU", title2="Programserier")
	JSONObject = JSON.ObjectFromURL(APIURL % "programseries/" + id + "/videos")
	for item in JSONObject:
		key=APIURL % "videos/" + str(item["id"])
		thumb=APIURL % "videos/" + str(item["id"]) + "/images/600x600.jpg"
		title=item["title"]
		if item["premiere"]:
			title = title + " *PREMIERE* "
		summary=item["description"]
		subtitle=item["broadcastChannel"] + ": " + item["formattedBroadcastTime"] + " ["+ item["duration"] + "]"
		dir.Append(Function(VideoItem(GetVideos, title=title,summary=summary, subtitle=subtitle, thumb=thumb), id=item["videoResourceUrl"]))
	return dir

def GetVideos(sender,id):
	content = JSON.ObjectFromURL(id)
	map = dict()
	for video in content["links"]:
		quality=int(video["qualityId"])
		uri = video["uri"]
		map[quality] = uri
	bestUri = map[sorted(map)[0]]
	tempclip = bestUri.split(":")
	clip = 'http://vodfiles.dr.dk/' + tempclip[2]
	Log("Showing " + clip)
	return Redirect(clip)
	
def LiveTVMenu(sender):
	drRTMP = "rtmp://rtmplive.dr.dk/live"
	dir = MediaContainer(title1="DR NU - Live TV", title2="Live TV")	
	dir.Append(RTMPVideoItem(drRTMP, clip="livedr01astream3", width=830, height=467, live=True, title="DR1", summary="DR1 Live", thumb=R(ICON) ) )
	dir.Append(RTMPVideoItem(drRTMP, clip="livedr02astream3", width=830, height=467, live=True, title="DR2", summary="DR2 Live", thumb=R(ICON) ) )
	dir.Append(RTMPVideoItem(drRTMP, clip="livedr03astream3", width=830, height=467, live=True, title="DR Update", summary="DR1 Update", thumb=R(ICON) ) )
	dir.Append(RTMPVideoItem(drRTMP, clip="livedr04astream3", width=830, height=467, live=True, title="DR K", summary="DR1 K Live", thumb=R(ICON) ) )
	dir.Append(RTMPVideoItem(drRTMP, clip="livedr05astream3", width=830, height=467, live=True, title="DR Ramsjang", summary="DR1 Ramasjang Live", thumb=R(ICON) ) )
	return dir


def LiveRadioMenu(sender):
	drRTMP = "rtmp://live.gss.dr.dk/live/"
	dir=MediaContainer(title1="DR NU - Live Radio", title2="Live Radio")
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel3_HQ", width=0, height=0, live=True, title="P1", summary="P1 Live", thumb=R(ICON)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel4_HQ", width=0, height=0, live=True, title="P2", summary="P2 Live", thumb=R(ICON)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel15_HQ", width=0, height=0, live=True, title="P3", summary="P3 Live", thumb=R(ICON)))
	dir.Append(Function(DirectoryItem(LiveRadioP4Menu,"P4",subtitle="P4", summary="",thumb=R(ICON),art=R(ART))))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel25_HQ", width=0, height=0, live=True, title="DR P5", summary="DR P5 Live", thumb=R(ICON)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel29_HQ", width=0, height=0, live=True, title="DR P6 Beat", summary="DR P6 Beat Live", thumb=R(ICON)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel21_HQ", width=0, height=0, live=True, title="DR P7 Mix", summary="DR P7 Mix Live", thumb=R(ICON)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel24_HQ", width=0, height=0, live=True, title="DR Ramasjang Radio", summary="DR Ramasjang Radio Live", thumb=R(ICON)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel21_HQ", width=0, height=0, live=True, title="DR Hit", summary="DR Hit Live", thumb=R(ICON)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel18_HQ", width=0, height=0, live=True, title="DR Boogieradio", summary="DR Boogieradio Live", thumb=R(ICON)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel27_HQ", width=0, height=0, live=True, title="DR Rock", summary="DR Rock Live", thumb=R(ICON)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel10_HQ", width=0, height=0, live=True, title="DR Dansktop", summary="DR Dansktop Live", thumb=R(ICON)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel19_HQ", width=0, height=0, live=True, title="DR Jazz", summary="DR Jazz Live", thumb=R(ICON)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel23_HQ", width=0, height=0, live=True, title="DR Klassisk", summary="DR Klassisk Live", thumb=R(ICON)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel2_HQ", width=0, height=0, live=True, title="DR Nyheder", summary="DR Nyheder Live", thumb=R(ICON)))	
	return dir

def LiveRadioP4Menu(sender):
	drRTMP = "rtmp://live.gss.dr.dk/live/"
	dir=MediaContainer(title1="DR NU - P4", title2="P4")
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel18_HQ", width=0, height=0, live=True, title="P4 København", summary="P4 København Live", thumb=R(ICON)))	
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel11_HQ", width=0, height=0, live=True, title="P4 Sjælland", summary="P4 Sjælland Live", thumb=R(ICON)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel14_HQ", width=0, height=0, live=True, title="P4 Østjylland", summary="P4 Østjylland Live", thumb=R(ICON)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel12_HQ", width=0, height=0, live=True, title="P4 Syd", summary="P4 Syd Live", thumb=R(ICON)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel17_HQ", width=0, height=0, live=True, title="P4 Fyn", summary="P4 Fyn Live", thumb=R(ICON)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel10_HQ", width=0, height=0, live=True, title="P4 Nordjylland", summary="P4 Nordjylland Live", thumb=R(ICON)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel9HQ", width=0, height=0, live=True, title="P4 Midt & Vest", summary="P4 Midt & Vest Live", thumb=R(ICON)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel13_HQ", width=0, height=0, live=True, title="P4 Trekanten", summary="P4 Trekanten Live", thumb=R(ICON)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel6_HQ", width=0, height=0, live=True, title="P4 Bornholm", summary="P4 Bornholm Live", thumb=R(ICON)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel15_HQ", width=0, height=0, live=True, title="P4 Esbjerg", summary="P4 Esbjerg Live", thumb=R(ICON)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel11_HQ", width=0, height=0, live=True, title="P4 NordvestSjælland", summary="P4 NordvestSjælland Live", thumb=R(ICON)))
	return dir	
	
