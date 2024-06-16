from youtube import YoutubeExtension
from youtube import YouTube

if __name__ == '__main__':
    po = YouTube('https://www.youtube.com/watch?v=2lAe1cqCOXo')

    print(po.streams.get_audio_only())

    yt = YoutubeExtension()
    print(yt.home())
