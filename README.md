AceProxy: Ace Stream HTTP Proxy
===============================
AceProxy allows you to watch [Ace Stream](http://acestream.org/) live streams or BitTorrent files over HTTP.
It's written in Python + gevent and should work on both Linux and Windows (Mac OS should work too, but was not tested)

Currently it supports Ace Stream Content-ID hashes (PIDs), .acestream files and usual torrent files.

Linux
-----
* Install Python 2 and gevent from your repositories.
* Optionally (if you want multiplexing, and highly recommended overall) install VLC.
* Clone this repository with:

> git clone https://github.com/ValdikSS/aceproxy.git

* Edit aceconfig.py if needed
* Start Ace Stream Engine, VLC and acehttp.py

> acestreamengine --client-console

> vlc -I telnet --sout-keep --demux ffmpeg --clock-jitter=0 --network-caching 500 --sout-mux-caching 500

> python2 acehttp.py

* Run any stream with http://localhost:8000/pid/ace-id-goes-here, http://localhost:8000/torrent/http%3A%2F%2Fsite.com%2Fpath%2Ffile.acelive

Windows
-------
* Install [Python 2](http://python.org/download/), [gevent](https://pypi.python.org/pypi/gevent#downloads) an [greenlet](https://pypi.python.org/pypi/greenlet#downloads)
* Optionally (if you want multiplexing, and highly recommended overall) install [VLC](http://www.videolan.org/vlc/).
* If you have git, clone this repository with:

> git clone https://github.com/ValdikSS/aceproxy.git

or download ZIP of it.

* Edit aceconfig.py if needed
* Start Ace Stream Engine and VLC (with vlc -I telnet --sout-keep --demux ffmpeg --clock-jitter=0 --network-caching 500 --sout-mux-caching 500)
* Start python.exe \path\to\acehttp.py
* Run any stream with http://localhost:8000/pid/ace-id-goes-here, http://localhost:8000/torrent/http%3A%2F%2Fsite.com%2Fpath%2Ffile.acelive

AceProxy with Torrent-TV extension
==================================

This extension contains the functionality, allowing you to interact with Torrent-TV service.
In particular, to retrieve the Torrent-TV playlist in M3U and XML (for NetPlayer SmartTV widget) formats.
Please edit the torrenttv/tortvconfig.py and change the following properties:
* TorTVConfig.aceproxyurl - The URL on which the AceProxy is running
* TorTVConfig.login - Your login in Torrent-TV service
* TorTVConfig.password - Your password in Torrent-TV service

Then you can point your player to the URL of the form http://proxy_host:proxy_port/tortvplaylist/xml or
http://proxy_host:proxy_port/tortvplaylist/m3u depending of the playlist format you want to retrieve.
