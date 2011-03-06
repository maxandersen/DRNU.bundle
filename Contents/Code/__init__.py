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
		title=item["title"] + ": " + item["formattedBroadcastTime"]
		subtitle=item["description"]
		dir.Append(Function(VideoItem(GetVideos, title=title,subtitle=subtitle, thumb=thumb), id=item["videoResourceUrl"]))
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
	
	
