from django.db.models.signals import post_delete
import os

from .models import Post


def deleteConverImage(sender, instance=None, **kwargs):
    """Delete cover image from directory when a post is deleted"""
    imgPath = instance.coverImage.path
    os.remove(imgPath)

    print(f"{instance} and all its related files are deleted successfully")


post_delete.connect(deleteConverImage, sender=Post)
