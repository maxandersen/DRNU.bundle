####################################################################################################

VIDEO_PREFIX = "/video/drnu"

APIURL = "http://www.dr.dk/NU/api/%s"

NAME  = "DR NU"
ART   = 'art-default.png'
ICON  = 'DR.png'

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
	dir.Append(Function(DirectoryItem(ProgramSerierMenu,"Programmer",subtitle="Alle Programserier", summary="",thumb=R(ICON),art=R(ART)),id=None,title="Programmer"))
	dir.Append(Function(DirectoryItem(NewestMenu,"Nyeste",subtitle="De nyeste videoer", summary="",thumb=R(ICON),art=R(ART)),id=None, title="Nyeste"))
	dir.Append(Function(DirectoryItem(SpotMenu,"Spot",subtitle="Spot light", summary="",thumb=R(ICON),art=R(ART)),id=None, title="Spot"))
	dir.Append(Function(DirectoryItem(MostViewedMenu,"Mest Sete",subtitle="Mest Sete", summary="",thumb=R(ICON),art=R(ART)),id=None, title="Mest Sete"))
	return dir

def ProgramSerierMenu(sender,id,title):
	dir=MediaContainer(title1="DR NU", title2=title)
	
	JSONObject=JSON.ObjectFromURL(APIURL % "programseries.json")
	for program in JSONObject:
		slug=program["slug"]
		title=program["title"]
		if program["videoCount"] > 1:
			title = title + " (" + str(program["videoCount"]) + " afs.)"
		subtitle=", ".join(program["labels"])
		
		summary=program["description"]
		thumb=APIURL % "programseries/" + slug + "/images/600x600.jpg"
                Log("thumb=" + thumb)
		dir.Append(Function(DirectoryItem(ProgramMenu,title=title,subtitle=subtitle,thumb=thumb,summary=summary),id=slug, title=title))
	return dir


def NewestMenu(sender,id, title):
        return CreateVideoItem(sender, id=id, title=title, items=JSON.ObjectFromURL(APIURL % "videos/newest.json"))

def MostViewedMenu(sender,id, title):
        return CreateVideoItem(sender, id=id, title=title, items=JSON.ObjectFromURL(APIURL % "videos/mostviewed.json"))

def SpotMenu(sender,id, title):
        return CreateVideoItem(sender, id=id, title=title, items=JSON.ObjectFromURL(APIURL % "videos/spot.json"))

def ProgramMenu(sender,id, title):
	return CreateVideoItem(sender, id=id, title=title, items=JSON.ObjectFromURL(APIURL % "programseries/" + id + "/videos"))


def CreateVideoItem(sender,id, title, items):
	dir=MediaContainer(title1="DR NU", title2=title)
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
			subtitle=item["broadcastChannel"] + ": " + item["formattedBroadcastTime"]
			if 'duration' in item:
				subtitle = subtitle + " ["+ item["duration"] + "]"

		if 'videoResourceUrl' in item:
			video=item["videoResourceUrl"]
                else:
			video =JSON.ObjectFromURL(key)["videoResourceUrl"]
		
                ## Log("title=" + str(title) + ", subtitle=" + str(subtitle) + ", thumb=" + str(thumb) + ", summary=" + str(summary) + ", id=" + str(video)) 
		dir.Append(Function(VideoItem(GetVideos, title=title,subtitle=subtitle, summary=summary, art=art, thumb=thumb), id=video))     
		##addVideos(sender,video,title,subtitle,summary,art,thumb,dir)
	return dir

def addVideos(sender,id,title,subtitle,summary,art,thumb,dir):
	content = JSON.ObjectFromURL(id)
        for video in content["links"]:
		uri=video["uri"]
		tempclip = uri.split(":")
		Log(uri)
		clip = 'http://vodfiles.dr.dk/' + tempclip[2]	
		dir.Append(Function(VideoItem(GetVideo, title=title + " (" + str(video["bitrateKbps"]) + " bKps)", subtitle=subtitle, summary=summary, art=art, thumb=thumb),clip=clip))
		dir.Append(RTMPVideoItem(tempclip[0] + ":" + tempclip[1], clip=tempclip[2],title=title + " ( RTPM:"+ str(video["bitrateKbps"]) + " bKps)", subtitle=subtitle, summary=summary, art=art, thumb=thumb))

def GetVideo(sender, clip):
       	Log("Showing " + clip)
	return Redirect(clip)
        

def GetVideos(sender,id):
	content = JSON.ObjectFromURL(id)
	
	map = dict()
	for video in content["links"]:
		quality=int(video["bitrateKbps"])
		uri = video["uri"]
		map[quality] = uri
	Log("quality: " + str(map))
	bestUri = map[sorted(map)[0]]
	tempclip = bestUri.split(":")
	clip = 'http://vodfiles.dr.dk/' + tempclip[2]
	Log("Showing " + clip)
	return Redirect(clip)
	
	
	
