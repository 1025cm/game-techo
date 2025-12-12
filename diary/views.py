from django.shortcuts import render, redirect, get_object_or_404
from .models import GameDiary, Profile
from .forms import GameForm, ProfileForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponseForbidden

# 1. トップページ
def index(request):
    diaries = GameDiary.objects.all().order_by('-created_date') # 新しい順に並べる
    return render(request, 'diary/index.html', {'diaries': diaries})

# 2. 新しい日記を書くページ
@login_required
def post_new(request):
    if request.method == "POST":
        # request.POST（文字）だけでなく、request.FILES（画像）も受け取る！
        form = GameForm(request.POST, request.FILES)  # ← ここを変更！
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
    else:
        form = GameForm()
        
    return render(request, 'diary/post_edit.html', {'form': form})
    # 詳細ページを表示する命令
def post_detail(request, pk):
    # pk（背番号）を使って日記を1つ探す。見つからなかったら404エラー（見つかりません）を出す
    post = get_object_or_404(GameDiary, pk=pk)
    return render(request, 'diary/post_detail.html', {'post': post})
    # 編集（リライト）する命令
@login_required
def post_edit(request, pk):
    post = get_object_or_404(GameDiary, pk=pk) # 編集したい日記を探す
    if post.author != request.user:
        return HttpResponseForbidden("この日記の編集権限がありません。")
    if request.method == "POST":
        # 保存ボタンが押されたら、上書き保存する
        form = GameForm(request.POST, request.FILES, instance=post) # instance=post が重要！
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('post_detail', pk=post.pk) # 詳細ページに戻る
    else:
        # まだ何もしてない時は、元々の文字が入った記入用紙を渡す
        form = GameForm(instance=post)
    return render(request, 'diary/post_edit.html', {'form': form})

# 削除する命令
@login_required
def post_delete(request, pk):
    post = get_object_or_404(GameDiary, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden("この日記の削除権限がありません。")
    post.delete() # 削除！
    return redirect('index') # トップページに戻る
    # 会員登録の命令
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() # データベースにユーザーを保存
            login(request, user) # そのまま自動でログインさせる
            return redirect('index') # トップページへ
    else:
        form = UserCreationForm() # 白紙の登録用紙
    return render(request, 'registration/signup.html', {'form': form})
    # いいねボタンが押された時の命令
@login_required
def like_post(request, pk):
    post = get_object_or_404(GameDiary, pk=pk)
    
    # もし、すでにこのユーザーが「いいね」していたら...
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user) # 取り消す（解除）
    else:
        post.likes.add(request.user)    # 追加する（いいね！）
        
    return redirect('post_detail', pk=pk) # 詳細ページに戻る
 # プロフィール画面（見る・編集する兼用）
@login_required
def profile_edit(request):
    # 今ログインしているユーザーのプロフィールを取得（なければ作る！）
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        # 保存ボタンが押されたら
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_edit') # 更新して同じページを表示
    else:
        # 編集ページを開いた時
        form = ProfileForm(instance=profile)

    return render(request, 'registration/profile.html', {'form': form, 'profile': profile})
# コメントを追加する命令
@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(GameDiary, pk=pk) # 日記を探す
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post       # どの日記へのコメントかセット
            comment.author = request.user # 誰が書いたかセット
            comment.save()
            return redirect('post_detail', pk=post.pk) # 詳細ページに戻る
    return redirect('post_detail', pk=post.pk)