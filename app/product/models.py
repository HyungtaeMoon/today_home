from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Company(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    image = models.ImageField(upload_to='company', blank=True)

    class Meta:
        verbose_name = '회사명'
        verbose_name_plural = '회사 리스트'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    image = models.ImageField(upload_to='category', blank=True)

    class Meta:
        verbose_name = '카테고리'
        verbose_name_plural = '모든 상품 카테고리'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    image = models.ImageField(upload_to='products', blank=True)
    # 가격은 양수만 취급하기 때문에 PositiveIntegerField
    price = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '판매 상품'
        verbose_name_plural = '상품 리스트'

    def __str__(self):
        return self.name


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '장바구니'
        verbose_name_plural = '장바구니 리스트'

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=250)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='comment-img')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = '댓글 리스트'

    def __str__(self):
        return self.product
