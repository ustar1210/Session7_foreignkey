from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog, Comment, Tag
from django.utils import timezone

def detail(request, id):
    blog = get_object_or_404(Blog, pk = id)
    if request.method == 'GET':
        # filter에 post 객체 그대로 넣어주기
        comments = Comment.objects.filter(blog=blog)
        return render(request, 'main/detail.html',{
            'blog':blog,
            'comments':comments,
            })
    elif request.method == "POST":
        new_comment = Comment()
        # foreignkey > blog 객체 직접 넣어주기
        new_comment.blog = blog
        # foreignkey > request.user 객체 직접 넣어주기
        new_comment.writer = request.user
        new_comment.content = request.POST['content']
        new_comment.pub_date = timezone.now()
        new_comment.save()
        return redirect('main:detail', id)

def mainpage(request):
    blogs = Blog.objects.all()
    return render(request, 'main/mainpage.html', {'blogs':blogs})

def secondpage(request):
    return render(request, 'main/secondpage.html')

def create(request):
    if request.user.is_authenticated:
        new_blog = Blog()
        new_blog.title = request.POST['title']
        new_blog.writer = request.user
        new_blog.pub_date = timezone.now()
        new_blog.body = request.POST['body']
        new_blog.image = request.FILES.get('image')
        new_blog.save()
        # 본문의 내용을 띄어쓰기로 잘라낸다
        words = new_blog.body.split(' ')
        # 만약 단어가 #로 시작하면, #를 뗀 후 tag_list에 모아둔다.
        tag_list = []
        for w in words:
            if w[0]=='#':
                tag_list.append(w[1:])
        # 해시태그가 들어있는 tag_list를 하나씩 돌면서
        for t in tag_list:
            # 기존에 존재하는 태그면 get, 없으면 create
            tag, boolean = Tag.objects.get_or_create(name=t)
            # 이후 태그 필드에 추가
            new_blog.tags.add(tag.id)
        return redirect('main:detail', new_blog.id)
    else :
        return redirect('accounts:login')

def new(request):
    return render(request, 'main/new.html')

# 수정 화면으로 가는 코드 구현
def edit(request, id):
    edit_blog = Blog.objects.get(id=id)
    return render(request, 'main/edit.html', {'blog' : edit_blog})

# update(수정) 기능 구현
def update(request, id):
    if request.user.is_authenticated:
        update_blog = Blog.objects.get(id=id)
        if request.user == update_blog.writer:
            update_blog.title = request.POST['title']
            update_blog.pub_date = timezone.now()
            update_blog.body = request.POST['body']
            update_blog.save()
            return redirect('main:detail', update_blog.id)
    return redirect('accounts:login')


# delete(삭제) 기능 구현
def delete(request, id):
    delete_blog = Blog.objects.get(id=id)
    delete_blog.delete()
    return redirect('main:mainpage')

# 모든 tag 리스트를 볼 수 있는 페이지 구현
def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'main/tag_list.html', {
        'tags':tags,
    })

# 태그 선택 시 해당 태그가 포함된 게시물 보는 기능 구현
def tag_blogs(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    blogs = tag.blogs.all()
    return render(request, 'main/tag_blogs.html',{
        'tag':tag,
        'blogs':blogs,
    })