from django import forms
from .models import GameDiary, Profile, Comment

class GameForm(forms.ModelForm):
    class Meta:
        model = GameDiary
        # ↓ ここに 'image' がないと画面に出ません！
        fields = ('title', 'text', 'image',)
# プロフィール編集用のフォーム
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image', 'bio', 'favorite_game')
        labels = {
            'image': 'アイコン画像',
            'bio': '自己紹介',
            'favorite_game': '推しゲーム',
        }
# コメント記入用フォーム
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'コメントを書く...'}),
        }
        labels = {
            'text': '',
        }