import datetime
import re
import math
from django.utils.html import strip_tags

def count_words(html_string):
    """ This method id to get the total length of the words"""
    word_string = strip_tags(html_string)
    match_words = re.findall('r\w+', word_string)
    count       = len(match_words)
    return count


def get_read_time(html_string):
    """this method is to convert the words to time"""
    count           =   count_words(html_string)
    read_time_min   =   math.ceil((count/200.0)) # assuming 200wpm in reading
    #read_time_sec   =   read_time_min * 60
    #read_time       =   str(datetime.timedelta(seconds = read_time_sec))
    return read_time_min