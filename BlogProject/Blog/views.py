#__author:  Administrator
#date:   2018/12/31
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from datetime import date
from .models import Post, Category, Tag
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from comments.forms import CommentForm, CommentFormSet
from django.db.models import Q
import markdown
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
from django.forms import formset_factory
#日历模块 可以查看一个月有多少天： calendar.monthrange(year, month) 返回值为元组：(这个月第一天星期几， 这个月最大天数)
import calendar

class IndexView(ListView):
    model = Post
    template_name = 'Blog/index.html'
    context_object_name = 'post_list'
    #每页显示多少篇文章，ListView已经帮我们实现了简单的分页功能
    paginate_by = 15

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        """
        使用此方法以获取传入模板的字典，
        把自己写的分页方法更新到字典用，方便前端调用
        """
        #从父类中获取传给模板的字典
        context = super(IndexView, self).get_context_data(**kwargs)
        #获取需要的参数传入自己写的方法中
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        #调用自己写的分页方法
        pagination_data = self.pagination_data(paginator, page, is_paginated)
        #将自己的分页方法更新到context中
        context.update(pagination_data)

        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            #没有分页，返回空，不用显示分页
            return {}
        #当前页左边需要显示的连续页码
        left = []
        #当前页右边需要显示的连续页码
        right = []
        #左边是否需要显示省略号
        left_has_more = False
        #右边是否需要显示省略号
        right_has_more = False

        #是否显示第一页，如果left包含了第一页就不需要显示了
        first = False
        #是否显示最后一页，如果right包含了最后一页就不需要显示了
        last = False

        #当前页码号
        page_number = page.number
        #总页码
        total_pages = paginator.num_pages
        #获取整个分页页码列表，如总共4页，则 [1,2,3,4]
        page_range = paginator.page_range

        if page_number == 1:
            #当前为第一页，即左边没有页码
            #获取当前页右边连续两个页码, 当前页索引为0， 页码为1，
            #所以直接用当前页码为索引表示当前页的后一页,
            # 切片超出最大索引默认为空
            right = page_range[page_number:page_number + 2]
            if right[-1] < total_pages - 1:
                #right 列表比 总页数的前一页还要小，
                # 说明最后一页前面至少还有一页没在right中，即需要显示省略号
                right_has_more = True
            if right[-1] < total_pages:
                #比最后一页小，说明没有包含最后一页，需要另外显示
                last = True

        elif page_number == total_pages:
            #当前页是最后一页
            left = page_range[(page_number-3) if (page_number - 3) > 0 else 0:page_number-1]
            #如果最左边的页码比第二页好要大，则需要用省略号 省略其他页码
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        else:
            #当前页不是第一页， 也不是最后一页
            left = page_range[(page_number-3) if (page_number-3) > 0 else 0:page_number-1]
            right = page_range[page_number:page_number + 2]
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        data = {'left': left,
                'right': right,
                'left_has_more': left_has_more,
                'right_has_more': right_has_more,
                'first': first,
                'last': last
                }
        return data

class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get("pk"))
        return super(CategoryView, self).get_queryset().filter(category=cate)

class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)

class ArchivesView(IndexView):
    def get_queryset(self):
        created_year = self.kwargs.get('year')
        created_month = self.kwargs.get('month')
        monthrange = calendar.monthrange(created_year, created_month)
        return super(ArchivesView, self).get_queryset().filter(created_time__range=(date(created_year, created_month, 1),
                                                               date(created_year, created_month, monthrange[1])))

class PostDetailView(DetailView):
    model = Post
    template_name = 'Blog/detail.html'
    context_object_name = 'post'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        #覆写这个方法是为了对post的body进行渲染
        post = super(PostDetailView, self).get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])
        post.body = md.convert(post.body)
        post.toc = md.toc
        return post

    def get_context_data(self, **kwargs):
        #如果要获取其他额外的数据（除了get_queryset获取的数据，还需要其他的数据），
        # 就需要重写此方法来获取，并添加到原来的context中
        context = super(PostDetailView, self).get_context_data(**kwargs)
        # print(self.request.user.username, self.request.user.email)
        formset = CommentFormSet()
        comment_list = self.object.comment_set.all()
        context.update({
            'formset': formset,
            'comment_list': comment_list
        })
        return context
@login_required
def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = '请输入关键词'
        return render(request, 'Blog/index.html',{'error_msg': error_msg})

    post_list = Post.objects.filter(Q(title__icontains=q)|Q(body__icontains=q))
    return render(request, 'Blog/index.html', {'error_msg': error_msg,
                                               'post_list': post_list})

