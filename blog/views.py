#-*- coding: utf-8 -*-
from django.views import generic
from .models import *
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.template import RequestContext
from django.core.context_processors import csrf
import lxml.html as LH
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#encoding= utf-8

class Partners(generic.ListView):
    queryset = Entry.objects.published()[:3]
    template_name = "partnerships.html"
    paginate_by = 5

class PageIndex(generic.ListView):
    queryset = Entry.objects.published()[:3]
    template_name = "landing_page.html"
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        entries= Entry.objects.published()[:3]
        i=0
        for e in entries:
            if 'iframe' in e.body:
                root = LH.fromstring(e.body)
                for el in root.iter('iframe'):
                    el.attrib['width'] = '75%'
                    if i==0:
                        el.attrib['height'] ="390"
                    else:
                        el.attrib['height'] = ""
                e.body=LH.tostring(root, pretty_print=True)
            i+=1
        c = {'object_list': entries}
        #print entries[1].body
        print entries[0].images.all()
        return render(request,self.template_name,c)




class BlogIndex(generic.ListView):
    queryset = Entry.objects.published()
    template_name = "blog_index.html"
    paginate_by = 5


    def get(self, request, *args, **kwargs):
        tags = Tag.objects.all()
        entries= Entry.objects.published()
        paginator = Paginator(entries, 5) # Show 5 contacts per page
        page = request.GET.get('page')
        try:
            entries = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            entries = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            entries = paginator.page(paginator.num_pages)
        c = {'object_list': entries,'tags':tags}
        c.update(csrf(request))
        
        return render(request,self.template_name,c)


    def post(self, request, *args, **kwargs):
        tags = Tag.objects.all()
        post_tag = request.POST.get('tag', '')
        post_title = request.POST.get('title','')
        if post_tag=="Todas" or post_tag=="":
            entries= Entry.objects.published()
        else:
            entries = Entry.objects.filter(tags__name=post_tag)
        if post_title!="":
            entries = entries.filter(title__icontains=post_title)

        paginator = Paginator(entries, 5) # Show 5 contacts per page
        page = request.GET.get('page')
        try:
            entries = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            entries = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            entries = paginator.page(paginator.num_pages)
        template="entry_list.html"        
        c = {'object_list': entries,'tags':tags}
        c.update(csrf(request))
        return render(request,template,c)
        """if request.method == "POST":
            #self.tag=get_object_or_404(Tag,slug=self.args[0])
            return Entry.objects.filter(tag__slug__iexact=self.args[0])
        else:
            return Entry.objects.published()"""
    

    """
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BlogIndex, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['tags'] = Tag.objects.all()
        return context"""

class BlogDetail(generic.DetailView):
    model = Entry
    template_name=  "post.html"

    def get(self, request,slug, *args, **kwargs):
        entry= Entry.objects.get(slug=slug)
        try:
            comments= Comment.objects.filter(post=entry)
        except:
            comments={}
        print entry.body
        c = {'object': entry,'slug':slug,'comments':comments}
        c.update(csrf(request))
        
        return render(request,self.template_name,c)

    def post(self, request,slug, *args, **kwargs):
        name = request.POST.get('user', '') 
        text = request.POST.get('text', '')
        entry = Entry.objects.get(slug=slug)
        if name=="":
            name= "Anónimo"
        comments = Comment(name=name,text=text,post=entry)
        comments.save()
        c = {'object': entry,'slug':slug,'comment':comments}
        c.update(csrf(request))
        template_name = "comments.html"
        return render(request,template_name,c)