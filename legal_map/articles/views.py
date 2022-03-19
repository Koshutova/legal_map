from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.views.generic import TemplateView

from legal_map import settings
from legal_map.articles.forms import ArticleForm, ContactUsForm
from legal_map.articles.models import Article
from legal_map.core.decorators import any_group_required


class IndexView(TemplateView):
    template_name = 'index.html'


def contact_us(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_mail = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_mail, [settings.EMAIL_HOST_USER])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            messages.success(request, "Your message has been submitted successfully")

    form = ContactUsForm()
    return render(request, 'contact_us.html', {'form': form, })


def list_all_articles(request):
    all_articles = Article.objects.all()

    context = {
        'articles': all_articles,
    }

    return render(request, 'articles/list_all_articles.html', context)


@any_group_required(groups=['Author'])
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('list all articles')
    else:
        form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'articles/article_create.html', context)


def article_details(request, pk):
    article = Article.objects.get(pk=pk)
    is_creator = article.user == request.user

    context = {
        'article': article,
        'is_creator': is_creator,
    }

    return render(request, 'articles/article_detail.html', context)


@any_group_required(groups=['Author'])
def edit_article(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('list all articles')
    else:
        form = ArticleForm(instance=article)

    context = {
        'form': form,
        'article': article
    }

    return render(request, 'articles/article_edit.html', context)


@any_group_required(groups=['Author'])
def delete_article(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == 'POST':
        article.delete()
        return redirect('list all articles')
    else:
        context = {
            'article': article,
        }
        return render(request, 'articles/article_delete.html', context)


@any_group_required(groups=['Author'])
def list_my_articles(request):
    all_articles = Article.objects.all()
    my_articles = all_articles.filter(user_id=request.user.id)
    has_articles = my_articles.exists()

    context = {
        'all_articles': all_articles,
        'my_articles': my_articles,
        'has_articles': has_articles,
    }
    return render(request, 'articles/list_my_articles.html', context)

