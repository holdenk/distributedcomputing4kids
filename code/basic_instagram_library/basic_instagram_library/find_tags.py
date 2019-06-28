#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import sys

def find_tags(username):
    """Find the tags for a specific username. Re-uses scraper if present"""
    # Save and restore stderr/stdout
    oldstderr = sys.stderr
    oldstdout = sys.stdout
    tags = []
    try:
        scraper_singleton = ScraperSingleton()
        scraper = scraper_singleton.get_scraper()
        scraper.quit = False
        user_data = scraper.get_shared_data(username)

        if user_data is None:
            raise Exception("Nothing for user %s" % username)

        media = scraper.deep_get(user_data, 'entry_data.ProfilePage[0].graphql.user.edge_owner_to_timeline_media.edges')
        for entry in media:
            edges = entry['node']['edge_media_to_caption']['edges'] or []
        for node in edges:
            caption = node['node']['text'] or None
            if caption is not None:
                tags += caption.split(' ')
    finally:
        sys.stderr = oldstderr
        sys.stdout = oldstdout
    return tags

# We use a singleton here for performance reasons with map so we
# don't have to introduce mapPartitions yet
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class ScraperBaseClass(object):
    _scraper = None

    def get_scraper(self):
        if self._scraper is None:
            from instagram_scraper.app import InstagramScraper
            scraper = InstagramScraper()
            scraper.quit = False
            scraper.authenticate_as_guest()
            self._scraper = scraper
        return self._scraper

    
class ScraperSingleton(ScraperBaseClass, metaclass=Singleton):
    pass

