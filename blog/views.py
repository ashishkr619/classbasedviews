from django.shortcuts import render
from django.views.generic import View,ListView,DetailView,CreateView,UpdateView,DeleteView,FormView
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import get_object_or_404,redirect,reverse
from django.urls import reverse_lazy
import requests
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from blog.models import Post,Comment,Category
from blog.forms import PostForm,CommentForm


#our custom mixin
class PageContentMixin(object):
    page_title=None

    def get_context_data(self,**kwargs):
        context=super().get_context_data()
        context['page_title'] =self.page_title
        return context


class PostList(PageContentMixin,ListView):
    model =Post
    template_name ='blog/home.html'
    context_object_name='posts'
    ordering ='-pub_date'
    paginate_by =3
    page_title='Goldie\'s Home'


# class PostDisplay(DetailView):
#     #main mixin :SingleObjectMixin 
#     model = Post
#     context_object_name='post'
#     pk_url_kwarg='pk'
#     template_name ='blog/post_detail.html'

#     #Returns the object the view is displaying. 
#     def get_object(self):
#         post = super().get_object() #the current post
#         post.view_count = post.view_count +1 
#         post.save()
#         return post

#     def get_context_data(self,*args,**kwargs):
#         """Insert the single object into the context dict."""
#         context = super().get_context_data(**kwargs)#the current context
#         context['comments'] =Comment.objects.filter(post= self.get_object())#get the current post
#         context['form']=CommentForm
#         return context

class PostDisplay(SingleObjectMixin,View):

    model = Post

    def get(self,request,*args,**kwargs):
        self.object = self.get_object()
        self.object.view_count = self.object.view_count +1 
        self.object.save()
        post = self.get_context_data(object=self.object)
        return render(request,'blog/post_detail.html',post)

    def get_context_data(self,*args,**kwargs):
        """Insert the single object into the context dict."""
        context = super().get_context_data(**kwargs)#the current context
        context['comments'] =Comment.objects.filter(post= self.get_object())#get the current post
        context['form']=CommentForm
        return context
      
            
class PostComment(FormView):
    form_class = CommentForm
    template_name='blog/post_detail.html'

    def form_valid(self,form):
        form.instance.author = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk'])
        form.instance.post= post
        form.save()
        return super(PostComment,self).form_valid(form)

    def get_success_url(self):
        return reverse('blog:detail',kwargs={'pk':self.kwargs['pk']})    


class PostDetail(PageContentMixin,View):
    page_title='detail'
    def get(self,request,*args,**kwargs):
        view = PostDisplay.as_view()
        return view(request,*args,**kwargs) 

    def post(self,request,*args,**kwargs):
        view = PostComment.as_view()
        return view(request,*args,**kwargs) 


class PostCreate(PageContentMixin,CreateView):
    #ModelFormMixin is the main one
    model = Post
    fields = ['title','category','content']
    page_title='Create new post'

    def form_valid(self,form):
        """If the form is valid, save the associated model."""
        form.instance.author =self.request.user
        form.save()
        return super(PostCreate,self).form_valid(form)


class PostUpdate(PageContentMixin,UpdateView):
    model =Post
    fields =['title','category','content']
    page_title='update'

class PostDelete(PageContentMixin,DeleteView):
    model =Post
    success_url= reverse_lazy('blog:home')#wait till url is available ,since only after deletion we want to redirect
    context_object_name='post'
    template_name='blog/post_confirm_delete.html'
    page_title='delete post'



#inheriting a class and overriding its properties
@method_decorator(login_required,name='dispatch')#lookout for get,put,post,delete
class Dashboard(PageContentMixin,View):
    page_title='dashboard'
    def get(self, request,*args,**kwargs):
        view = PostList.as_view(
            template_name='blog/admin_page.html',
            paginate_by=4 
            )
        return view(request,*args,**kwargs)       


class PostCategory(PageContentMixin,ListView):
    model =Post
    template_name='blog/post_category.html'
    context_object_name='posts'
    paginate_by =3
    page_title='category'

    def get_queryset(self):
        self.category = get_object_or_404(Category,pk=self.kwargs['pk'])
        return Post.objects.filter(category=self.category)

    def get_context_data(self,**kwargs):
        context = super().get_context_data()
        context['category'] = self.category
        return context     




