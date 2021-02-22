from operator import itemgetter
from collections import namedtuple
import os
import pickle
import urllib.request
import re
import isodate

# prework
# download pickle file and store it in a tmp file
pkl_file = "pycon_videos.pkl"
data = f"https://bites-data.s3.us-east-2.amazonaws.com/{pkl_file}"
tmp = os.getenv("TMP", "/tmp")
pycon_videos = os.path.join(tmp, pkl_file)
urllib.request.urlretrieve(data, pycon_videos)

# the pkl contains a list of Video namedtuples
Video = namedtuple("Video", "id title duration metrics")


# def _add_duration_in_minutes(videos):
#     for video in videos:
#         m = re.match(r"PT(\d*H)*(\d*M)*\d*S*", video.duration)
#         h = int(m.group(1).rstrip("H")) if m.group(1) else 0
#         m = int(m.group(2).rstrip("M")) if m.group(2) else 0
#         video.metrics["runtime"] = h * 60 + m
#     return videos


def _add_duration_in_minutes(videos):
    for video in videos:
        duration = isodate.parse_duration(video.duration).total_seconds()
        video.metrics["runtime"] = duration / 60
    return videos


def load_pycon_data(pycon_videos=pycon_videos):
    """Load the pickle file (pycon_videos) and return the data structure
    it holds"""
    with open(pycon_videos, "rb") as fp:
        videos = pickle.load(fp)
        return _add_duration_in_minutes(videos)


def get_most_popular_talks_by_views(videos):
    """Return the pycon video list sorted by viewCount"""
    return sorted(
        videos, key=lambda video: int(video.metrics["viewCount"]), reverse=True
    )


def get_most_popular_talks_by_like_ratio(videos):
    """Return the pycon video list sorted by most likes relative to
    number of views, so 10 likes on 175 views ranks higher than
    12 likes on 300 views. Discount the dislikeCount from the likeCount.
    Return the filtered list"""

    def like_ratio(video):
        likes = int(video.metrics["likeCount"])
        dislikes = int(video.metrics["dislikeCount"])
        views = int(video.metrics["viewCount"])
        return (likes - dislikes) / views

    return sorted(videos, key=like_ratio, reverse=True)


def get_talks_gt_one_hour(videos):
    """Filter the videos list down to videos of > 1 hour"""
    return [video for video in videos if video.metrics["runtime"] > 60]


def get_talks_lt_twentyfour_min(videos):
    """Filter videos list down to videos that have a duration of less than
    24 minutes"""
    return [video for video in videos if video.metrics["runtime"] < 24]
