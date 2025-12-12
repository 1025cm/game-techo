from django.db import models
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# これが「ゲーム日記」の設計図です
class GameDiary(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    # ↓ これを追加！（upload_to='images/' は imagesフォルダに入れるという意味）
    # blank=True は「写真なしでもOK」という意味です
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)

    def __str__(self):
        return self.title
    def total_likes(self):
        return self.likes.count()
        # プロフィール（ユーザーの追加情報）
class Profile(models.Model):
    # ユーザーと1対1で紐付ける（Aさんのプロフィールはこれ！と決める）
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # 自己紹介（空っぽでもOK）
    bio = models.TextField(max_length=500, blank=True)
    
    # アイコン画像
    image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    
    # 好きなゲーム
    favorite_game = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username
# 魔法：ユーザーが新しく作られたら、自動でプロフィールも作る！
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# 魔法：ユーザーが保存されたら、プロフィールも保存する！
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
# コメントの設計図
class Comment(models.Model):
    # どの日記へのコメントか（日記が消えたらコメントも消す）
    post = models.ForeignKey('diary.GameDiary', on_delete=models.CASCADE, related_name='comments')
    
    # 誰が書いたか
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # コメントの中身
    text = models.TextField()
    
    # 日付
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text