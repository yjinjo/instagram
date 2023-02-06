import re

from django.conf import settings
from django.db import models
from django.urls import reverse


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="insta/posts/%Y/%m/%d")
    caption = models.CharField(max_length=500)
    tag_set = models.ManyToManyField("Tag", blank=True)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.caption

    def extract_tag_list(self):
        # 알파벳 부터 한글까지 1회이상 반복되는 것만 쓰겠다는 뜻입니다.
        tag_name_list = re.findall(r"#([a-zA-Z\dㄱ-힣]+)", self.caption)
        tag_list = []
        for tag_name in tag_name_list:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            tag_list.append(tag)
        return tag_list


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
