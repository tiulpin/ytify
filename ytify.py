import logging
from pathlib import Path
from urllib.parse import quote

from ratelimit import limits, sleep_and_retry
from requests import get
from tqdm import tqdm

YT_PLAYLIST_PATH = Path("youtube.txt")
ER_PLAYLIST_PATH = Path("youtube.err")
SY_PLAYLIST_PATH = Path("spotify.txt")

ODESLI_RATE_LIMIT = 9
MINUTE = 60


@sleep_and_retry
@limits(calls=ODESLI_RATE_LIMIT, period=MINUTE)
def get_odesli(song_url: str) -> dict:
    """
    Gets response from Odesli server.
    :param song_url:
    :return:
    """
    response = get(f"https://api.song.link/v1-alpha.1/links?url={quote(song_url)}")

    if response.status_code != 200:
        raise Exception(response.text)

    return response.json()


def get_spotify_url(odesli_response: dict) -> str:
    """
    Returns Spotify URL according to the Odesli API schema.
    :param odesli_response: successful response from Odesli server
    :return: Spotify URL to song (if found)
    """
    return odesli_response["linksByPlatform"]["spotify"]["url"]


def load_playlist(path: Path) -> list:
    """
    Loads playlist from the given file (without https://).
    :param path: path to the playlist file with separated by \n URLs to songs
    :return: playlist – list of song URLs
    """
    with open(path) as f:
        playlist = [line.rstrip().lstrip("https://") for line in f]

    return playlist


def save_playlist(playlist: list, path: Path) -> None:
    """
    Saves the given playlist (list of urls) to the given path.
    :param playlist: list of song URLs
    :param path: path to save the playlist
    """
    with open(path, "w") as f:
        for line in playlist:
            f.write(line + "\n")


def ytify() -> None:
    """
    Main script. Don't forget to run youtube-dl to get youtube.txt file before the launch:
    youtube-dl -j --flat-playlist "https://www.youtube.com/playlist?list=$ID" | jq -r '.id' | sed 's_^_https://youtu.be/_' > youtube.txt
    """
    log = logging.getLogger(__name__)

    yts, sps, failed = load_playlist(YT_PLAYLIST_PATH), [], []

    for yt in tqdm(yts):
        try:
            sps.append(get_spotify_url(get_odesli(yt)))
        except Exception as ex:
            log.debug(str(ex))
            failed.append(yt)
            continue

    log.info(f"{len(sps)} songs saved, {len(failed)} failed.")
    save_playlist(failed, ER_PLAYLIST_PATH)
    save_playlist(sps, SY_PLAYLIST_PATH)


if __name__ == "__main__":
    ytify()

