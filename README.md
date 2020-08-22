# ytify
🎧 Small utility to export YouTube playlist to Spotify – built with [odesli.co](https://odesli.co).
- Obtain the wanted playlist using [youtube-dl](https://github.com/ytdl-org/youtube-dl/)
```bash
youtube-dl -j --flat-playlist "https://www.youtube.com/playlist?list=$ID" | jq -r '.id' | sed 's_^_https://youtu.be/_' > youtube.txt
```
In case you want to export your liked songs, consider [this workaround](https://www.reddit.com/r/YoutubeMusic/comments/fdv784/i_succeed_to_transfer_all_my_liked_songs_in_a_new/) – use [Chromium extension](https://chrome.google.com/webstore/detail/youtube-for-tv/gmmbpchnelmlmndfnckechknbohhjpge/related) if you don't have TV with YouTube.
- Run the script
```bash
pip install -r requirements.txt  # it's recommended to use virtual environment
python ytify.py
```
- Paste the contents of spotify.txt to [Spotify desktop app](http://www.spotify.com/download)
- Download and save somewhere anything which is not available on Spotify:
```bash
youtube-dl --extract-audio --audio-format mp3 -a youtube.err
```
