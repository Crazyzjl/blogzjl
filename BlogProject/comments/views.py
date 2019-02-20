from django.shortcuts import render, get_object_or_404, redirect
from Blog.models import Post
from django.contrib.auth.decorators import login_required

from .models import Comment
from .forms import CommentForm, CommentFormSet
# Create your views here.
@login_required
def post_comment(request, pk):
    # 先获取被评论的文章，因为后面需要把评论和被评论的文章关联起来。
    #这个函数的作用是当获取的文章（Post）存在时，则获取；否则返回 404 页面给用户。
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        # 用户提交的数据存在 request.POST 中，这是一个类字典对象。
        # 我们利用这些数据构造了 CommentForm 的实例，这样 Django 的表单就生成了
        data = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '1',
            # 'form-MAX_NUM_FORMS': '',
            'form-0-name': request.user.username,
            'form-0-email': request.user.email,
            'form-0-text': request.POST.get('form-0-text'),
            # 'form-0-ORDER': '1',
        }
        # print(request.POST.get('form-0-text'))
        formset = CommentFormSet(data=data)
        if formset.is_valid():
            # 检查到数据是合法的，调用表单的 save 方法保存数据到数据库，
            #formset 时一个集合 用for循环出第一组表单
            for form in formset:
                # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。

                comment = form.save(commit=False)

                # 将评论和被评论的文章关联起来。
                comment.post = post
                # 最终将评论数据保存进数据库，调用模型实例的 save 方法
                comment.save()
            # 重定向到 post 的详情页，实际上当 redirect 函数接收一个模型的实例时，它会调用这个模型实例的 get_absolute_url 方法，
            # 然后重定向到 get_absolute_url 方法返回的 URL。
            return redirect(post)

        else:
            # 检查到数据不合法，重新渲染详情页，并且渲染表单的错误。
            # 因此我们传了三个模板变量给 detail.html，
            # 一个是文章（Post），一个是评论列表，一个是表单 form
            # 注意这里我们用到了 post.comment_set.all() 方法，
            # 这个用法有点类似于 Post.objects.all()
            # 其作用是获取这篇 post 下的的全部评论，
            # 因为 Post 和 Comment 是 ForeignKey 关联的，
            # 因此使用 post.comment_set.all() 反向查询全部评论。
            # 具体请看下面的讲解。
            comment_list = post.comment_set.all()
            context = {'post': post,
                       'formset': formset,
                       'comment_list': comment_list
                       }

            return render(request, 'Blog/detail.html', context=context)
    # redirect既可以接收一个URL作为参数，也可以接收一个模型的实例作为参数（例如这里的
    # post）。如果接收一个模型的实例，那么这个实例必须实现了get_absolute_url
    # 方法，这样redirect会根据get_absolute_url方法返回的URL值进行重定向
    # 不是 post 请求，说明用户没有提交数据，重定向到文章详情页。
    return redirect(post)

