from django.db import models
# Create your models here.
#---------------------------------------------------------
from datetime import datetime
#---------------------------------------------------------
from django.contrib.auth.models import User
#---------------------------------------------------------
class Author(models.Model):
    rating = models.IntegerField(default=0)
    user   = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,)

    def update_rating(self, post, comment):
        author = self.pk
        articles = post.objects.filter(kind='ART')
        com_all  = comment.objects.all()
        com_art  = comment.objects.filter(post_id__kind='ART')
        
        rating_article = 0
        for x in articles:
           author_id = x.author_id
           if author==author_id:
              rating_article += x.post_rating
        rating_article = rating_article * 3
        rating_com_all = 0
        for x in com_all:
           user_id = x.user_id
           if author==user_id:
              rating_com_all += x.com_rating
        rating_com_art = 0
        for x in com_art:
           user_id = x.user_id
           if author==user_id:
              rating_com_art += x.com_rating

        self.rating = rating_article + rating_com_all + rating_com_art      
        self.save()
        return self.rating    
#---------------------------------------------------------
class Category(models.Model):
    name  = models.CharField(max_length = 255, unique=True)
#---------------------------------------------------------
class Post(models.Model):
    article   = 'ART'
    news      = 'NEW'   
    POSITIONS = [
        (article, 'Статья'),
        (news,    'Новости')]
    kind    = models.CharField(max_length = 3, choices=POSITIONS,)
    time_in = models.DateTimeField(auto_now_add = True) 
    title   = models.CharField(max_length = 255)
    text    = models.TextField()
    post_rating = models.IntegerField(default=0)
    
    author  = models.ForeignKey(Author, on_delete = models.CASCADE)
    posts   = models.ManyToManyField(Category, through = 'PostCategory')
    
    def preview(self):
        if self.kind != 'ART':
            return 'Метод не применим к новостям'
        else:
            self.preview = self.text[:124] + '...'
            return self.preview

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    @staticmethod
    def best_article():
        best = Post.objects.filter(kind='ART').order_by('-post_rating').first()
        best_article = best.__dict__
        print()
        print('Лучшая статья (на на основе лайков/дислайков к ней)')        
        time = best_article['time_in']
        time = datetime.strftime(time, '%Y-%m-%d %H:%M:%S')
        print('Дата добавления:', time)
        user_pk = best_article['author_id']
        username = User.objects.get(pk=user_pk).username
        print('username автора:', username)
        best_rating = best_article['post_rating']
        print('рейтинг статьи :', best_rating)
        best_title = best_article['title']
        print('заголовок :', best_title)
        best_text = best_article['text']
        print('превью    :', best_text[:124] + '...')
        print()
        return best          
#---------------------------------------------------------    
class PostCategory(models.Model):
    post     = models.ForeignKey(Post,     on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
#---------------------------------------------------------  
class Comment(models.Model):
    text       = models.TextField()
    time_in    = models.DateTimeField(auto_now_add = True)
    com_rating = models.IntegerField(default = 0)
    
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    
    def like(self):
        self.com_rating += 1
        self.save()
        
    def dislike(self):
        self.com_rating -= 1
        self.save()
 
    @staticmethod
    def show_comments(best_article):
        q = Comment.objects.filter(post_id=best_article).values('id')
        print()
        print('Комментарии к статье:')
        print(best_article.text[:124] + ' ...')
        for i, x in enumerate(q):
            com_id = x['id']
            com = Comment.objects.get(pk=com_id)
            time = com.time_in
            print('-------------------------------------------')
            print('Комментарий №', com_id)
            print('Дата:', datetime.strftime(time, '%Y-%m-%d %H:%M:%S'))
            user = com.user_id
            print('Пользователь:', User.objects.get(pk=user).username)
            rating = com.com_rating
            print('Рейтинг комментария:', rating)
            text = com.text
            print('Текст комментария:', text)
        print()

