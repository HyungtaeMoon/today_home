from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import ListView

from product.forms import CommentCreateForm
from .models import Product, CartItem, Category, Comment

User = get_user_model()


def main_total_list(request):
    """메인 페이지로 추후 product-list 외에 다른 모델도 추가 예정"""
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'product/total-list.html', context)


def category_list(request):
    category_list = Category.objects.all()
    product_list = Product.objects.all()
    context = {
        'category_list': category_list,
        'product_list': product_list,
    }
    return render(request, 'product/category-list.html', context)


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
    cart_item = CartItem.objects.filter(user_id=request.user.pk)
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
        cart = CartItem.objects.get(product__id=product.pk, user_id=request.user.pk)
        print(cart)
        if cart:
            if cart.product.name == product.name:
                cart.quantity += 1
                cart.save()
                cart_item = CartItem.objects.filter(user_id=request.user.pk)
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
        cart_item = CartItem.objects.filter(user_id=request.user.pk)
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
            return redirect('product:product-detail', product.pk)
    else:
        form = CommentCreateForm()
        context = {
            'form': form,
        }
    return render(request, 'product/comment-create.html', context)


@login_required()
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
