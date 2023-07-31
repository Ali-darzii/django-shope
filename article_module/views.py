from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.list import ListView
from django.urls import reverse

from .forms import CommentForm
from .models import Article, ArticleCategory, Comment
from django.views.generic import DetailView
from jalali_date import datetime2jalali, date2jalali
from django.core.paginator import Paginator


# Create your views here.


# class ArticlesView(View):  # we could use ListView or TemplateView (ListView has pagined_by that is so good)
#     def get(self, request):
#         article: Article = Article.objects.filter(is_active=True)
#         context = {
#             'articles': article
#         }
#         return render(request, 'article_module/articles_page.html', context)


# class ArticlesListView(TemplateView):
#     template_name = 'article_module/articles_page.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         article: Article = Article.objects.filter(is_active=True)
#         paginator = Paginator(article, 3)
#         context['article'] = article
#         context['date'] = datetime2jalali(self.request.user.date_joined).strftime('%y/%m/%d _ %H:%M:%S')
#         return context

class ArticlesListView(ListView):
    template_name = 'article_module/articles_page.html'
    model = Article
    paginate_by = 3
    context_object_name = 'article'

    def get_queryset(self):
        query = super(ArticlesListView, self).get_queryset()
        query = query.filter(is_active=True)
        category_name = self.kwargs.get('category')  # from url it's get the <str:category>
        if category_name is not None:
            query = query.filter(selected_categories__url_title__iexact=category_name)
            # from selected category we go in ArticleCategory with (__) and we will filter it
        return query


def article_categories_component(request: HttpRequest):
    article_main_category = ArticleCategory.objects.prefetch_related('articlecategory_set').filter(is_active=True, parent_id=None)
    # when parent_id is None means --> we selected the parents
    context = {
        'main_categories': article_main_category
    }
    return render(request, 'article_module/components/article_categories_component.html', context)


class ArticlesDetialView(DetailView):
    model = Article
    template_name = 'article_module/article_detail.html'

    def get_queryset(self):
        query = super(ArticlesDetialView, self).get_queryset()
        query = query.filter(is_active=True)
        return query

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        connected_comments = Comment.objects.filter(CommentPost=self.get_object())
        number_of_comments = connected_comments.count()
        data['comments'] = connected_comments
        data['no_of_comments'] = number_of_comments
        data['comment_form'] = CommentForm()
        return data

    def post(self, request, *args, **kwargs):
        if self.request.method == 'POST':
            comment_form = CommentForm(self.request.POST)
            if comment_form.is_valid():
                content = comment_form.cleaned_data['content']
                try:
                    parent = comment_form.cleaned_data['parent']
                except:
                    parent = None

            new_comment = Comment(content=content, author=self.request.user, CommentPost=self.get_object(),
                                  parent=parent)
            new_comment.save()
            return redirect(self.request.path_info)


def add_article_comment(request: HttpRequest):
    print(request.GET)
    return HttpResponse('hello')
