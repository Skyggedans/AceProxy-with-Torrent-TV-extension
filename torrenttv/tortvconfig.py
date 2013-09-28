class TorTVConfig:
    # ACE Stream Proxy URL
    aceproxyurl = 'http://192.168.1.1:8000/'
    # Torrent-TV API host
    apihost = 'http://api.torrent-tv.ru/'
    # Authentication URL
    authurl = apihost + 'v2_auth.php?application=tsproxy&typeresult=xml&%s'
    # Playlist URL
    playlisturl = apihost + 'v2_alltranslation.php?type=all&typeresult=xml&%s'
    # Torrent file URL for channel
    channelurl = apihost + 'v2_get_torrent.php?%s'
    # User login in Torrent-TV service
    login = ''
    # User password in Torrent-TV service
    password = ''