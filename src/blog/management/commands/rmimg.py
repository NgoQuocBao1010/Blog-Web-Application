from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from blog.models import Post

import re
import os


class Command(BaseCommand):
    help = "Remove un used image from database"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        posts = Post.objects.all()
        contentImgs = []

        for post in posts:
            urls = re.findall(
                r"http?://\S+?/\S+?\.(?:jpg|jpeg|gif|png)",
                post.content,
            )

            for url in urls:
                imgName = url.split("contents/")[1]
                contentImgs.append(imgName)

        contetnFolderPath = os.path.join(settings.MEDIA_ROOT, "contents")
        allHistoryContentImgs = os.listdir(contetnFolderPath)

        for imgFile in allHistoryContentImgs:
            if imgFile not in contentImgs:
                imgPath = os.path.join(contetnFolderPath, imgFile)
                os.remove(imgPath)
