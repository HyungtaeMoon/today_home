from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.views.generic import ListView, UpdateView, TemplateView

from product.forms import CommentCreateForm, CommentUpdateForm
from .models import Product, CartItem, Category, Comment

User = get_user_model()


# def main_total_list(request):
#     products = Product.objects.all()
#     categories = Category.objects.all()
#     context = {
#         'products': products,
#         'categories': categories,
#     }
#     return render(request, 'product/home.html', context)


class Home(TemplateView):
    """
    FBV 로 2개의 multiple 한 쿼리셋을 context 에 담아 해당 템플릿으로 렌더링하는 것을
    TemplateView 로 리팩토링하여 재구현
    """
    template_name = 'product/home.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['products'] = Product.objects.all()
        context_data['categories'] = Category.objects.all()
        return context_data


home = Home.as_view()


class CategoryList(TemplateView):
    """
    스토어 > 상품 리스트의 메인 페이지

    body 페이지에는 등록된 모든 상품,
    왼쪽 사이드 바 페이지에는 모든 카테고리를 보여줌
    """
    template_name = 'product/category-list.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['product_list'] = Product.objects.all()
        context_data['category_list'] = Category.objects.all()
        return context_data


category_list = CategoryList.as_view()

# def category_list(request):
#     category_list = Category.objects.all()
#     product_list = Product.objects.all()
#     context = {
#         'category_list': category_list,
#         'product_list': product_list,
#     }
#     return render(request, 'product/category-list.html', context)


def category_detail(request, category_pk):
    category_list = Category.objects.all()
    category_detail = Category.objects.get(id=category_pk)
    product_list = Product.objects.filter(category__id=category_detail.id)
    context = {
        'category_list': category_list,
        'category_detail': category_detail,
        'product_list': product_list,
    }
    return render(request, 'product/category-detail.html', context)


def product_detail(request, product_pk):
    product = Product.objects.get(pk=product_pk)
    comment_list = Comment.objects.filter(product__id=product.id)
    context = {
        'product': product,
        'comment_list': comment_list,
    }
    return render(request, 'product/product-detail.html', context)


@login_required
def my_cart(request):
    cart_item = CartItem.objects.filter(user__id=request.user.pk)
    # 장바구니에 담긴 상품의 총 합계 가격
    total_price = 0
    for each_total in cart_item:
        total_price += each_total.product.price
    if cart_item is not None:
        context = {
            'cart_item': cart_item,
            'total_price': total_price,
        }
        return render(request, 'cart/cart-list.html', context)
    return redirect('product:my-cart')


@login_required
def add_cart(request, product_pk):
    product = Product.objects.get(pk=product_pk)

    try:
        cart = CartItem.objects.get(product__id=product.pk, user__id=request.user.pk)
        print(cart)
        if cart:
            if cart.product.name == product.name:
                cart.quantity += 1
                cart.save()
                cart_item = CartItem.objects.filter(user__id=request.user.pk)
                print(cart_item)
                print(request.user.pk)
    except CartItem.DoesNotExist:
        user = User.objects.get(pk=request.user.pk)
        cart = CartItem(
            user=user,
            product=product,
            quantity=1,
        )
        cart.save()
        cart_item = CartItem.objects.filter(user__id=request.user.pk)
        print(f'{cart_item} 은 생성되었습니다.')
    # return render(request, 'cart/cart-list.html', {'cart_item': cart_item})
    return redirect('product:my-cart')


def comment_create(request, product_pk):
    if request.method == 'POST':
        product = Product.objects.get(pk=product_pk)
        form = CommentCreateForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.content = form.cleaned_data['content']
            comment.rating = form.cleaned_data['rating']
            comment.image = form.cleaned_data['image']
            comment.product = product
            form.save()
            messages.success(request, '댓글이 생성되었습니다.')
            return redirect('product:product-detail', product.pk)

    form = CommentCreateForm()
    context = {
        'form': form,
    }
    return render(request, 'product/comment-create.html', context)


class CommentUpdateView(UpdateView):
    model = Comment
    fields = ['rating', 'content', 'image']

    def get_success_url(self):
        # Product 모델에서 get_absolute_url 로 reverse 경로를 지정해야
        # get_success_url 함수가 동작
        return resolve_url(self.object.product)


comment_edit = CommentUpdateView.as_view()

# @login_required
# def comment_update(request, comment_pk):
#     """상품 디테일 페이지에서 해당하는 댓글 내용을 수정하는 기능"""
#     if request.method == 'POST':
#         # product = Product.objects.get(pk=product_pk)
#         comment = Comment.objects.get(comment_pk=comment_pk)
#         product = Product.objects.get(comment_pk=comment.pk)
#
#         form = CommentUpdateForm(request.POST, request.FILES)
#
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.rating = form.cleaned_data['rating']
#             comment.content = form.cleaned_data['content']
#             comment.image = form.cleaned_data['image']
#             comment.save()
#             return redirect('product:product-detail', product.pk)
#
#     form = CommentUpdateForm()
#     context = {
#         'form': form,
#     }
#     return render(request, 'product/comment.html', context)


@login_required
def comment_delete(request, comment_id, product_id):
    product = Product.objects.get(pk=product_id)
    comment = Comment.objects.get(pk=comment_id)

    if comment.user.pk == request.user.pk:
        comment.delete()
    return redirect('product:product-detail', product.pk)


class SearchListView(ListView):
    model = Product
    queryset = Product.objects.all()
    template_name = 'product/category-list.html'

    def get_queryset(self):
        self.q = self.request.GET.get('q', '')

        qs = super().get_queryset()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
            print(qs)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.q
        return context
