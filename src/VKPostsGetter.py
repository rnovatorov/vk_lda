import vk
import time


class VKPostsGetter(object):
    """
    Used to download posts from VK wall
    """
    def __init__(self, vk_access_token="", wait_time=0.3):
        self.vk_api = self._init_vk_api(vk_access_token)
        self.wait_time = wait_time
        self.MAX_POSTS_PER_REQUEST = 100

    def _init_vk_api(self, vk_access_token):
        session = vk.Session(access_token=vk_access_token)
        api = vk.API(session)
        return api

    def count_posts(self, owner_id, vk_filter):
        response = self.vk_api.wall.get(
            owner_id=owner_id,
            count=1,
            filter=vk_filter
        )
        return response[0]

    def get_posts(self, owner_id, vk_filter, volume):
        """
        Gets all posts from group or user wall

        Requires waiting for some time between requests to get
        everything because of VK API load balancing politics
        """
        if not volume:
            yield []
            raise StopIteration

        downloaded = 0
        offset = 0
        while downloaded != volume:
            if volume - downloaded >= self.MAX_POSTS_PER_REQUEST:
                count = self.MAX_POSTS_PER_REQUEST
            else:
                count = volume - downloaded
            bunch = self.vk_api.wall.get(
                owner_id=owner_id,
                count=count,
                offset=offset,
                filter=vk_filter
            )
            for post in bunch[1:]:  # first elements is count
                downloaded += 1
                yield post
            offset += count
            time.sleep(self.wait_time)

    def get_comments(self, post, need_likes=0):
        """
        Gets all comments from group or user wall

        Requires waiting for some time between requests to get
        everything because of VK API load balancing politics
        """
        owner_id = post["from_id"]
        post_id = post["id"]

        # Checking if comments are accessible
        try:
            time.sleep(self.wait_time)
            response = self.vk_api.wall.getComments(
                owner_id=owner_id,
                post_id=post_id,
                count=1
            )
        except Exception as e:
            print(e)
            return []

        volume = response[0]
        comments = []
        offset = 0
        time.sleep(self.wait_time)
        while len(comments) != volume:
            if volume - len(comments) >= self.MAX_POSTS_PER_REQUEST:
                count = self.MAX_POSTS_PER_REQUEST
            else:
                count = volume - len(comments)
            bunch = self.vk_api.wall.getComments(
                owner_id=owner_id,
                post_id=post_id,
                count=count,
                offset=offset,
                need_likes=need_likes
            )
            comments.extend(bunch[1:])  # first element is count
            offset += count
            time.sleep(self.wait_time)
        return comments
