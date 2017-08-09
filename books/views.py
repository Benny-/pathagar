from io import StringIO
import urllib
import datetime
import ciso8601
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy

from .opds import Catalog, AcquisitionFeed, NavigationFeed, RootNavigationFeed
from . import fimfic

epoch = datetime.datetime.utcfromtimestamp(0)

catalog = Catalog('fimfiction:full-catalog',
                    'Fimfiction',
                    'Ebooks from fimfiction.net',
                    reverse_lazy('fimfic_opds_root'),
                    reverse_lazy('fimfic_opds_search'),
                    icon=settings.STATIC_URL+'images/elements_of_harmony_dictionary_icon_by_xtux345-d4myvo7.png')

# Transforms a image url to a 3th party transform image url (3th party image converter). See https://images.weserv.nl/
# This is done to guarantee we always have a consistent format.
def imgUrlToOTFTransformUrl(url, format):
    format = format.lower()
    if format not in ['jpg', 'png', 'gif', 'webp']:
        raise NotImplementedError("Format not supported")
    parsed = urllib.parse.urlparse(url)
    return 'https://images.weserv.nl/?output='+format+'&url=' + urllib.parse.quote('ssl:' + parsed.netloc + parsed.path + ('?' if len(parsed.query)>0 else '') + parsed.query)

def acquisitionFeed(request, sort, cursor=None):
    api_response = fimfic.getBooks(sort, cursor)
    next = None
    prev = None
    if 'prev' in api_response.content.links:
        pass
    if 'next' in api_response.content.links:
        pass
    acquisitionFeed = AcquisitionFeed(catalog, prev=prev, next=next)
    for book in api_response.data:
    
        thumbnail = None
        image = None
        
        if 'cover_image' in book.attributes:
            if 'full' in book.attributes['cover_image']:
                thumbnail = book.attributes['cover_image']['full']
                
            if 'large' in book.attributes['cover_image']:
                thumbnail = book.attributes['cover_image']['large']
                
            if 'medium' in book.attributes['cover_image']:
                thumbnail = book.attributes['cover_image']['medium']
                
            if 'thumbnail' in book.attributes['cover_image']:
                thumbnail = book.attributes['cover_image']['thumbnail']
        
        
            if 'thumbnail' in book.attributes['cover_image']:
                image = book.attributes['cover_image']['full']
                
            if 'medium' in book.attributes['cover_image']:
                image = book.attributes['cover_image']['full']
                
            if 'large' in book.attributes['cover_image']:
                image = book.attributes['cover_image']['full']
                
            if 'full' in book.attributes['cover_image']:
                image = book.attributes['cover_image']['full']
        
        if thumbnail is not None:
            thumbnail = imgUrlToOTFTransformUrl(thumbnail, 'png')
            thumbnail = {'url':thumbnail, 'type':'image/png'}
        
        if image is not None:
            image = imgUrlToOTFTransformUrl(image, 'png')
            image = {'url':image, 'type':'image/png'}
        
        published = None
        if book.attributes['date_published'] is None:
            published = epoch # Some data published are Null. That is why we have to do something like this.
        else:
            ciso8601.parse_datetime(book.attributes['date_published'])
        
        acquisitionFeed.addBookEntry(
                'urn:fimfiction:' + book.id,
                book.attributes['title'].strip(),
                published,
                book.attributes['short_description'].strip(),
                book.attributes['description_html'],
                thumbnail=thumbnail,
                image=image,
                opds_url='http://fimfiction.djazz.se/story/{}/download/fimfic_{}.epub'.format(book.id, book.id),
                html_url='https://www.fimfiction.net/story/'+book.id+'/'+urllib.parse.quote(book.attributes['title'].strip())
            )
    
    sio = StringIO()
    acquisitionFeed.write(sio, 'UTF-8')
    return HttpResponse(sio.getvalue(), content_type='application/atom+xml')

def cursor():
    return HttpResponse('TODO: acquisitionFeedCursor is not yet implemented', content_type='text/plain', status=501)

def search(request):
    return HttpResponse('TODO: Search is not yet implemented', content_type='text/plain', status=501)

def fimfic_opds_root(request):
    navFeed = RootNavigationFeed(catalog)
    
    navFeed.addAquisitionEntry('published', 'Latest published', reverse('fimfic_opds_by_published'))
    navFeed.addAquisitionEntry('hotness', 'Hottest', reverse('fimfic_opds_by_hotness'))
    navFeed.addAquisitionEntry('updated', 'Latest updated', reverse('fimfic_opds_by_update'))
    navFeed.addAquisitionEntry('ratings', 'Highest rating', reverse('fimfic_opds_by_rating'))
    navFeed.addAquisitionEntry('words', 'Most words', reverse('fimfic_opds_by_words'))
    navFeed.addAquisitionEntry('views', 'Most views', reverse('fimfic_opds_by_views'))
    navFeed.addAquisitionEntry('comments', 'Most comments', reverse('fimfic_opds_by_comments'))
    navFeed.addAquisitionEntry('likes', 'Most likes', reverse('fimfic_opds_by_likes'))
    navFeed.addAquisitionEntry('dislikes', 'Most dislikes', reverse('fimfic_opds_by_dislikes'))
    
    sio = StringIO()
    navFeed.write(sio, 'UTF-8')
    return HttpResponse(sio.getvalue(), content_type='application/atom+xml')

