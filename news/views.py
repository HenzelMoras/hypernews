import json
import datetime

from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings


class ComingSoonPageView(View):
    def get(self, request, *args, **kwargs):
        return redirect('/news/')  # render(request, 'news/news.html')

    def post(self, request, *args, **kwargs):
        pass


class MainPageView(View):
    def get(self, request, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH, 'r') as json_file:
            raw = json.load(json_file)
            dates = sorted({item['created'].split()[0] for item in raw}, reverse=True)  # get and sort all the dates
            sorted_news = {}
            for date in dates:
                date_news = [item for item in raw if item['created'].split()[0] == date
                             and request.GET.get('q', '') in item['title']]
                if date_news:
                    sorted_news[date] = date_news

        return render(request, 'news/main.html',
                      context={'sorted_news': sorted_news, 'search': request.GET.get('q', '')})

    def post(self, request, *args, **kwargs):
        pass


class NewsView(View):
    def get(self, request, *args, **kwargs):
        news = {'created': '', 'text': '', 'title': 'Oops... there is no news', 'link': ''}
        link = request.get_full_path().replace('/news/', '').strip('/')
        with open(settings.NEWS_JSON_PATH, 'r') as json_file:
            raw = json.load(json_file)
            for _news in raw:
                if _news['link'] == int(link):
                    news = _news
                    break
        return render(request, 'news/news.html', context={'news': news})

    def post(self, request, *args, **kwargs):
        pass


class CreateNewsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'news/create.html')

    def post(self, request, *args, **kwargs):
        self.add(request.POST.get('news_text', 'Oops... there is something wrong'), request.POST.get('title', 'Error'))
        return HttpResponseRedirect('/news/')

    def add(self, text, title):
        """Adds news to the file according to the passed parameters."""
        raw = self.get_all()
        with open(settings.NEWS_JSON_PATH, 'w') as json_file:
            now = datetime.datetime.now()
            created = now.strftime('%Y-%m-%d %H:%M:%S')
            link = now.strftime('%Y%m%d%H%M%S')  # %f
            raw.append({'created': created, 'text': text, 'title': title, 'link': int(link)})
            json.dump(raw, json_file)

    def get_all(self):
        """Returns the entire news list from a file. Each news item is a list item in the form of a dictionary."""
        with open(settings.NEWS_JSON_PATH, 'r') as json_file:
            return json.load(json_file)
