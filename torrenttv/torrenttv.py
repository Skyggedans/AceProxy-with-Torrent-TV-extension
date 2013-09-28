import urllib, urllib2, logging
import xml.dom.minidom as minidom
from tortvconfig import TorTVConfig

class TorrentTV:
    logger = logging.getLogger('http_TorTVExtension')
    session = None
    
    @staticmethod
    def auth():
        try:
            TorrentTV.session == None

            url = TorTVConfig.authurl % (urllib.urlencode({'username': TorTVConfig.login,
                'password': TorTVConfig.password}),)

            TorrentTV.logger.debug('Attempting to authenticate using ' + url)

            response = urllib2.urlopen(url)
            
            result = minidom.parseString(response.read())
            success = int(result.getElementsByTagName('success')[0].firstChild.nodeValue)
            if success == 1:
                TorrentTV.session = result.getElementsByTagName('session')[0].firstChild.nodeValue
                TorrentTV.logger.debug('Authentication succeeded')
            else:
                TorrentTV.logger.error('Authentication failed!')

        except urllib2.URLError as e:
            TorrentTV.logger.error("urllib2 exception: " + str(e))
    
    @staticmethod
    def getPlaylist(type = 'xml'):
        if TorrentTV.session == None:
            TorrentTV.auth()

        try:
            url = TorTVConfig.playlisturl % (urllib.urlencode({'session': TorrentTV.session}),)

            TorrentTV.logger.debug('Attempting to retrieve the playlist from ' + url)

            response = urllib2.urlopen(url)
            result = minidom.parseString(response.read())
            success = int(result.getElementsByTagName('success')[0].firstChild.nodeValue)
            if success == 1:
                if type == 'xml':
                    playlist = TorrentTV.generateXMLPlaylist(result.getElementsByTagName('channel'))
                elif type == 'm3u':
                    playlist = TorrentTV.generateM3UPlaylist(result.getElementsByTagName('channel'))
                TorrentTV.logger.debug('Playlist retrieval succeeded')
                return playlist
            else:
                TorrentTV.logger.error('Playlist retrieval failed!')
                return None

        except urllib2.URLError as e:
            TorrentTV.logger.error("urllib2 exception: " + str(e))
            return None

    @staticmethod
    def generateXMLPlaylist(channels):
        playlist = minidom.Document()
        rss_elem = playlist.createElement("rss")
        rss_elem.setAttribute("version", "2.0")
        playlist.appendChild(rss_elem)
        channel_elem = playlist.createElement("channel")
        rss_elem.appendChild(channel_elem)

        def processChannel(channel):
            channel_id = int(channel.attributes.get('id').value)
            channel_name = channel.attributes.get('name').value

            item_elem = playlist.createElement("item")
            title_elem = playlist.createElement("title")
            title_elem.appendChild(playlist.createTextNode(channel_name))
            item_elem.appendChild(title_elem)

            enclosure_elem = playlist.createElement("enclosure")
            channel_url = TorTVConfig.aceproxyurl + 'torrent/';
            channel_url += urllib2.quote(TorTVConfig.channelurl %
                (urllib.urlencode({'session': TorrentTV.session,
                    'channel_id': channel_id}),)).replace('/', '%2F')
            enclosure_elem.setAttribute("url", channel_url)
            enclosure_elem.setAttribute("type", "video/mpeg")
            item_elem.appendChild(enclosure_elem)
            channel_elem.appendChild(item_elem)

        map(processChannel, channels)

        return playlist.toxml('utf8')

    @staticmethod
    def generateM3UPlaylist(channels):
        playlist = ['#EXTM3U']

        def processChannel(channel):
            channel_id = int(channel.attributes.get('id').value)
            channel_name = channel.attributes.get('name').value.encode('utf8')
            playlist.append('#EXTINF:-1, %s' % (channel_name,))
            channel_url = TorTVConfig.aceproxyurl + 'torrent/';
            channel_url += urllib2.quote(TorTVConfig.channelurl %
                (urllib.urlencode({'session': TorrentTV.session,
                    'channel_id': channel_id}),)).replace('/', '%2F')
            playlist.append(channel_url)

        map(processChannel, channels)

        return '\n'.join(playlist)