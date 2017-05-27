import os
import sys


PYTHON_VERSION = sys.version_info.major

WAIT_TIME = 0.3
VK_ACCESS_TOKEN = os.getenv("VK_TOKEN", "")  # Put your token here if needed to access private posts
VK_FILTER_OWNER = "owner"
VK_FILTER_OTHERS = "others"
