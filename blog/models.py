from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse
# Create your models here.
from django.utils.safestring import mark_safe
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category_blog(MPTTModel):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    parent = TreeForeignKey('self', blank=True, null=True , related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    # keywords = models.CharField(max_length=255)
    description = models.TextField(max_length=505)
    image=models.ImageField(blank=True, default='default1.png', upload_to='images/')
    status=models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    def __str__(self):  # __str__ method elaborated later in
        full_path = [self.title]  # post.  use __unicode__ in place of
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])


class Blog_Home(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )

    category = models.ForeignKey(Category_blog, on_delete=models.CASCADE) #many to one relation with Category
    title = models.CharField(max_length=950)
    short = RichTextUploadingField(null=True)
    image = models.ImageField(default='default1.png', upload_to='images/',null=False)
    detail = RichTextUploadingField()
    slug = models.SlugField(null=False, unique=True, allow_unicode=True)
    status = models.CharField(max_length=10,choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""

    def get_absolute_url(self):
        return reverse('category_blog_detail', kwargs={'slug': self.slug})

    @property
    def get_products(self):
        return Blog_Home.objects.filter(categories__title=self.title)