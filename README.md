dr.dk/nu Plex Plugin
====================

Provides access to the content available from dr.dk/nu.

Most content is freely available, but some of the content might not be
viewable outside of Denmark.

Installation
============

With Git (Recommended):
cd ~/Library/Application Support/Plex Media Server/Plug-ins/
git clone git://github.com/maxandersen/DRNU.bundle.git

With Zip (Only if Git scares you): 
Download https://github.com/maxandersen/DRNU.bundle/zipball/master
Unzip content into ~/Library/Application Support/Plex Media Server/Plug-ins/

Now Plex should see the DRNU plugin.

Changes
=======
Based on plugin posted at
(http://forums.plexapp.com/index.php/topic/6283-dr-and-tv2-plugins-denmark/page__view__findpost__p__150323)
by Plex forum user MTI.

07/03/2011: 
	    Added support for Newest, Most Viewed & Spotlight.
	    Started making better usage of summary/subtitles.

14/06/2011
		Added support for live TV and radio
		
15/06/2001
		Added Logos for Live TV
		Added Fanart
		Bugfix: DR Hit (Obsolete) is now DR R&B
		
16/06/2011
	If available, the information for now / next will be 
	shown in live radio menu.
	Currently showing Live TV is shown in Live TV Menu
	Live Radio moved to music plugins
	Added background art til Live TV and Live Radio
	
18/06/2011
	Solved problem with on-demand clips buffering, and clips 
	looking bad
	Bugfix. Some data did not supply braodcast channel and 
	broadcast time, which prevented the plugin from playing 
	the file