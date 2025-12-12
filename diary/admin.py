from django.contrib import admin
from .models import GameDiary  # さっき作った設計図を読み込む

# 管理画面に登録する
admin.site.register(GameDiary)