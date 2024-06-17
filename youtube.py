from datetime import datetime, timedelta

from pytube import Search, YouTube

home_query = 'full audio books'

searchResults: Search | None = None


def home(paginate=False):
    if paginate and searchResults is not None:
        searchResults.get_next_results()
        parse_youtube_search_results(searchResults)
        return

    searchResults = Search(home_query)
    result = parse_youtube_search_results(searchResults)
    return result


def parse_streams(video: YouTube):
    expires = seconds_to_iso(int(video.streaming_data['expiresInSeconds']))
    stream_url = video.streaming_data['formats'][-1]['url']
    return stream_url, expires


def parse_youtube_search_results(results: Search):
    result_list = []
    for video in results.results:
        try:
            video_data = parse_video(video)
            streams = parse_streams(video)
            video_data.update({'streams': streams[0], 'expires': streams[1]})
            result_list.append(video_data)
        except Exception as e:
            print(e)
            continue
    return result_list


def parse_video(video: YouTube):
    return {'title': video.title, 'views': video.views, 'source_url': video.watch_url,
            'release_date': video.publish_date.isoformat(), 'description': video.description,
            'thumbnail_url': video.thumbnail_url, }


def seconds_to_iso(seconds_until_expiry: int):
    # Get the current date and time
    current_time = datetime.now()
    # Calculate the expiration date and time
    expiration_time = current_time + timedelta(seconds=seconds_until_expiry)
    # Convert to ISO 8601 format
    iso_format = expiration_time.isoformat()
    return iso_format
