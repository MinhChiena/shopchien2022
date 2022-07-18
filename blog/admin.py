from django.contrib import admin

# Register your models here.
from mptt.admin import DraggableMPTTAdmin

from blog.models import Category_blog, Blog_Home
from product.admin import ProductImageInline


class Category_blogAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category_blog.objects.add_related_count(
                qs,
                Blog_Home,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category_blog.objects.add_related_count(qs,
                 Blog_Home,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'


class Blog_HomeAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status','image_tag']
    list_filter = ['category']
    readonly_fields = ('image_tag',)
    prepopulated_fields = {'slug': ('title',)}



admin.site.register(Category_blog, Category_blogAdmin2)
admin.site.register(Blog_Home,Blog_HomeAdmin)