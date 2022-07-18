from django.contrib import admin

# Register your models here.
from mptt.admin import DraggableMPTTAdmin

from product.models import Category, Product, Images, Comment, Images1


class ProductImageInline(admin.TabularInline):
    model = Images
    readonly_fields = ('id',)
    extra = 5


class CommentImageInline(admin.TabularInline):
    model = Images1
    readonly_fields = ('id',)
    extra = 5


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent', 'status']
    list_filter = ['status']


class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Product,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Product,
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


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status','image_tag']
    list_filter = ['category']
    readonly_fields = ('image_tag',)
    inlines = [ProductImageInline]
    prepopulated_fields = {'slug': ('title',)}


class CommentyAdmin(admin.ModelAdmin):
    list_display = ['subject', 'comment', 'rate', 'create_at']
    list_filter = ['status']
    readonly_fields = ('image_tag',)
    inlines = [CommentImageInline]
    list_filter = ('subject', 'comment', 'ip', 'user', 'product', 'rate')


class Images1Admin(admin.ModelAdmin):
    readonly_fields = ('image_tag',)


admin.site.register(Category, CategoryAdmin2)
admin.site.register(Product,ProductAdmin)
admin.site.register(Images)
admin.site.register(Comment, CommentyAdmin)
admin.site.register(Images1,Images1Admin)