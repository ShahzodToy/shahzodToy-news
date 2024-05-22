from django.shortcuts import render
from .models import Post,Comment,Category
from django.views import View
from django.shortcuts import get_object_or_404
from taggit.models import Tag
from django.db.models import Count
from .forms import CommentForm
from django.shortcuts import redirect 
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger

class HomeView(View):
    def get(self,request,tag_slug=None):
        posts = Post.published.all()[:2]

        all_posts = Post.published.order_by('-publish')
        paginator = Paginator(all_posts,5)
        page_number = request.GET.get('page')
        try:
            all_posts = paginator.page(page_number)
        except PageNotAnInteger:
 # If page_number is not an integer deliver the first page
            all_posts = paginator.page(1)
        except EmptyPage:

 # If page_number is out of range deliver last page of results
            
            all_posts = paginator.page(paginator.num_pages)


        tag = None
        if tag_slug:
            tag  = get_object_or_404(Tag,slug=tag_slug)
            posts = posts.filter(tags__in=[tag])
        context = {
            'posts':posts,
            'tag':tag,
            'all_posts':all_posts
        }
        return render(request,'tech-index.html',context)

class ReviewPage(View):
    def get(self,request):
        comments = Comment.objects.all()
        context = {
            'comments':comments
        }
        return render(request,'tech-review.html',context)


class CategoryList(View):
    def get(self,request,tag_slug=None):
        
        posts = Post.published.all()
        tag = None
        if tag_slug:
            tag = get_object_or_404(Tag,slug=tag_slug)
            posts = posts.filter(tags__in=[tag])
        context = {
            'posts':posts,
            'tag':tag,
        }
        return render(request,'tech-category-01.html',context)

class DetailPage(View):
    def get(self,request,post):
        post = get_object_or_404(Post,slug = post,status = Post.Status.PUBLISHED)
        #List of similar posts
        post_tags_ids = post.tags.values_list('id',flat=True)
        similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
        similar_posts=similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
        comments = post.comments.all()
    
        form  = CommentForm()
        context = {
            'post':post,
            'similar_posts':similar_posts,
            'form':form,
            'comments':comments,
        
        }
        return render(request,'tech-single.html',context)
    
class PostComment(View):
    def post(self,request,post):

        post = get_object_or_404(Post,slug=post,status = Post.Status.PUBLISHED)

        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)

            comment.post = post
            comment.save()
            return redirect(reverse('detail_page',kwargs = {'post':post.slug}))

        context = {
            'post':post,
            'form':comment
        }
            
        
        return render(request,'tech-single.html',context)
        
class ContactPage(View):
    def get(self,request):
        context = {}
        return render(request,'tech-contact.html',context)




