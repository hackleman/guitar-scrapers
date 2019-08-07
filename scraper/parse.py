# import sys
# import json
# import requests
# import json
# import re
# from bs4 import BeautifulSoup
# from .tab import UltimateTab, UltimateTabInfo
# from flask import request, jsonify
# from urllib.parse import urlparse

# def parseurl(url):
#     html = requests.get(url).content

#     # Parse url and find pre tag with tablature
#     soup = BeautifulSoup(html, "html.parser")
#     tabs_html_content = soup.find_all('pre')
#     formatted_tab_string = ''.join(map(str, tabs_html_content[1].contents))

#     # Parse each line of the string into json
#     tab = UltimateTab ()
#     for tab_line in formatted_tab_string.split('\n'):
#         re_span_tag = re.compile(r'<span[^>]*>|<\/span[^>]*>')

#         if not tab_line: # Line is blank
#             tab.append_blank_line()
#         elif re_span_tag.search(tab_line): # Line contains chords
#             sanitized_tab_line = re_span_tag.sub(r' ', tab_line)
#             tab.append_chord_line(sanitized_tab_line)
#         else: # Line contains lyrics/string
#             tab.append_lyric_line(tab_line)

#     # Construct full json object
#     json = {}

#     json['lines'] = tab.as_json_dictionary()['lines']

#     # Return constructed json under a single tag
#     return json