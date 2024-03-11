import datetime
import json
import ast
from django.db.models import Avg
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from .models import CatalogItem, Product, Tag, Review, Specification, \
    UserSession, Basket, Order, OrderItem, Delivery, Profile, Image
from .serializer import (
    CatalogItemSerializer, ProductShortSerializer, BasketSerializer,
    TagsFullSerializer, ProductFullSerializer, ReviewsSerializer,
    OrderSerializer, UserSerializer)


class SignInView(APIView):
    def post(self, request: Request) -> Response:
        new_dict = json.loads(request.body.decode('utf-8'))
        username = new_dict["username"]
        password = new_dict["password"]
        user: User = authenticate(username=username, password=password)
        if user is None:
            return Response(status=500)
        else:
            login(request, user)
            return Response(status=200)


class SignOutView(APIView):
    def post(self, request: Request) -> Response:
        logout(request)
        return Response(status=200)


class SignUpView(APIView):
    def post(self, request: Request) -> Response:
        new_dict = json.loads(request.body.decode('utf-8'))
        name = (new_dict["name"]).split(" ")
        first_name = ""
        last_name = ""
        if name[0]:
            first_name = name[0]
        if len(name) > 1:
            last_name = name[1]

        username = new_dict["username"]
        password = new_dict["password"]
        user: User = authenticate(
            first_name=first_name, last_name=last_name, username=username,
            password=password)
        if user is None:
            user = User.objects.create(
                first_name=first_name, last_name=last_name, username=username,
                password=password)
            login(request, user)
            return Response(status=200)
        else:
            return Response(status=500)


class CategoriesView(APIView):
    def get(self, request: Request) -> Response:
        all_categories = CatalogItem.objects.filter(parent=None).all()
        return Response(CatalogItemSerializer(all_categories, many=True).data)


class CatalogView(APIView):
    def get(self, request: Request) -> Response:
        filter_kwargs = dict()
        results = dict()
        results["items"] = []
        if request.query_params.get("filter[name]"):
            filter_names = request.query_params.getlist("filter[name]")
            for filter_name in filter_names:
                if len(filter_name) > 0:
                    filter_kwargs["title__icontains"] = filter_name
                    filter_kwargs["description__icontains"] = filter_name
        if request.query_params.get("filter[minPrice]"):
            filter_kwargs["price__gte"] = int(
                request.query_params.get("filter[minPrice]")
            )
        if request.query_params.get("filter[maxPrice]"):
            filter_kwargs["price__lte"] = int(
                request.query_params.get("filter[maxPrice]")
            )
        if request.query_params.get("filter[freeDelivery]"):
            if ast.literal_eval(
                    (request.query_params.get("filter[freeDelivery]")).capitalize()
            ):
                filter_kwargs["freeDelivery"] = ast.literal_eval(
                    (request.query_params.get("filter[freeDelivery]")).capitalize()
                )
        if request.query_params.get("filter[available]"):
            if ast.literal_eval(
                    (request.query_params.get("filter[available]")).capitalize()
            ):
                filter_kwargs["count__gt"] = 0
        if request.query_params.get("category"):
            category_id = int(request.query_params.get("category"))
            category_ids = list()
            category_ids.append(category_id)
            searched_category = CatalogItem.objects.filter(parent=category_id).all()
            if searched_category:
                for category in searched_category:
                    category_ids.append(category.pk)
            filter_kwargs["category__in"] = category_ids
        if request.query_params.get("tags[]"):
            all_ids = request.query_params.getlist("tags[]")
            for idx in range(len(all_ids)):
                all_ids[idx] = int(all_ids[idx])
            filter_kwargs["tags__in"] = all_ids
        sort = False
        sorting_field = ""
        if request.query_params.get("sort"):
            sort = True
            sorting_field = "-" + request.query_params.get("sort")
            if request.query_params.get("sortType"):
                if request.query_params.get("sortType") == "inc":
                    sorting_field = request.query_params.get("sort")
        if sort:
            products = Product.objects.filter(
                **filter_kwargs
            ).order_by(
                sorting_field
            ).all()
        else:
            products = Product.objects.filter(**filter_kwargs).all()
        currentPage = 1
        if request.query_params.get("currentPage"):
            currentPage = int(request.query_params.get("currentPage"))
        limit = 20
        if request.query_params.get("limit"):
            limit = int(request.query_params.get("limit"))
        num_of_products = 0
        if products:
            num_of_products = products.count()
            if (currentPage - 1) * limit > num_of_products:
                currentPage = 1
            products = products[
                       (currentPage - 1) * limit: currentPage * limit - 1
                       ]
        if num_of_products > 0:
            results["items"] = ProductShortSerializer(
                products,
                many=True
            ).data
        results["currentPage"] = currentPage
        no_of_pages = num_of_products // limit
        if num_of_products % limit > 0:
            no_of_pages += 1
        results["lastPage"] = no_of_pages
        # print("API /catalog response: ", results)
        return Response(data=results, status=200)


class PopularProductsView(APIView):
    def get(self, request: Request) -> Response:
        results = None
        sorting_field = "-avg_rating"
        products = Product.objects.annotate(
            avg_rating=Avg("reviews__rate")
        ).order_by(sorting_field).all()
        if products:
            products = products[0:8]
            results = ProductShortSerializer(products, many=True).data
        return Response(data=results, status=200)


class TagsView(APIView):
    def get(self, request: Request) -> Response:
        if request.query_params.get("category"):
            filter_kwargs = dict()
            category_id = int(request.query_params.get("category"))
            category_ids = []
            category_ids.append(category_id)
            searched_category = CatalogItem.objects.filter(parent=category_id).all()
            if searched_category:
                for category in searched_category:
                    category_ids.append(category.pk)
            filter_kwargs["products__category__pk__in"] = category_ids
            tags = Tag.objects.filter(**filter_kwargs).distinct().all()
        else:
            tags = Tag.objects.all()
        results = None
        if tags:
            results = TagsFullSerializer(tags, many=True).data
        return Response(data=results, status=200)


class LimitedEditionProductsView(APIView):
    def get(self, request: Request) -> Response:
        results = None
        products = Product.objects.filter(limited_edition=True).all()
        if products:
            products = products[0:16]
            results = ProductShortSerializer(products, many=True).data
        return Response(data=results, status=200)


class ProductDetailsView(APIView):

    def get_object(self, id):
        return get_object_or_404(self.get_queryset(), id=id)

    def get(self, request: Request, pk=None, *args, **kwargs) -> Response:
        id = pk or request.query_params.get('id')
        product = Product.objects.get(pk=id)
        results = None
        if product:
            results = ProductFullSerializer(product).data
        return Response(data=results, status=200)


class AddReviewView(APIView):
    def post(self, request: Request, pk=None, *args, **kwargs) -> Response:
        results = None
        new_dict = json.loads(request.body.decode('utf-8'))
        if not request.user.is_authenticated:
            return Response(data="Please login to leave reviews", status=403)
        author = new_dict["author"]
        email = new_dict["email"]
        text = new_dict["text"]
        rate = new_dict["rate"]
        date = datetime.datetime.now()
        review = Review.objects.create(
            author=author,
            email=email,
            text=text,
            rate=rate,
            date=date
        )
        review.save()
        id = pk or request.query_params.get('id')
        product = Product.objects.get(pk=id)
        product.reviews.add(review)
        product.save()
        filter_kwargs = dict()
        filter_kwargs["products__pk"] = id
        reviews = Review.objects.filter(**filter_kwargs).all()
        reviews_serializer = ReviewsSerializer(reviews, many=True)
        results = reviews_serializer.data
        return Response(data=results, status=200)


class BasketView(APIView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        session_id = request.session.session_key
        new_dict = json.loads(request.body.decode('utf-8'))
        product_pk = new_dict["id"]
        user_session, created = UserSession.objects.get_or_create(sessionID=session_id)
        product = Product.objects.get(pk=product_pk)
        already_added, created = Basket.objects.get_or_create(session=user_session, product=product)
        already_added.count += new_dict["count"]
        already_added.save()
        products = Basket.objects.filter(session=user_session.pk).all()
        results = BasketSerializer(products, many=True).data
        return Response(data=results, status=200)

    def get(self, request: Request) -> Response:
        session_id = request.session.session_key
        user_session, created = UserSession.objects.get_or_create(sessionID=session_id)
        products = Basket.objects.filter(session=user_session.pk).all()
        results = BasketSerializer(products, many=True).data
        return Response(data=results, status=200)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        results = None
        session_id = request.session.session_key
        user_session = UserSession.objects.get(sessionID=session_id)
        new_dict = json.loads(request.body.decode('utf-8'))
        product_pk = new_dict["id"]
        product = Product.objects.get(pk=product_pk)

        basket_item = Basket.objects.get(session=user_session, product=product)
        if basket_item:
            if basket_item.count == new_dict["count"]:
                basket_item.delete()
            else:
                basket_item.count -= new_dict["count"]
                basket_item.save()
            products = Basket.objects.filter(session=user_session.pk).all()
            results = BasketSerializer(products, many=True).data
        return Response(data=results, status=200)


class BannerView(APIView):
    def get(self, request: Request) -> Response:
        filter_kwargs = dict()
        filter_kwargs["count__gt"] = 0
        products = Product.objects.filter(**filter_kwargs).order_by("?").all()[0:3]
        results = ProductShortSerializer(products, many=True).data
        return Response(data=results, status=200)


class OrderView(APIView):
    def post(self, request: Request, pk=None, *args, **kwargs) -> Response:
        if not request.user.is_authenticated:
            return Response(data="Please login to create order!", status=403)
        id = pk or request.query_params.get('id')
        results = dict()
        if id is None:
            # Order is created and filled with current Basket contents
            basket_items = json.loads(request.body.decode('utf-8'))
            delivery_type = Delivery.objects.get(name="ordinary")
            if len(basket_items) > 0:
                order = Order.objects.create(user=request.user, delivery_type=delivery_type)
                results["orderId"] = order.pk
                for basket_item in basket_items:
                    basket_product = Product.objects.get(pk=basket_item["id"])
                    OrderItem.objects.create(order=order, product=basket_product, count=basket_item["count"])
                session_id = request.session.session_key
                user_session = UserSession.objects.get(sessionID=session_id)
                basket_items = Basket.objects.filter(session=user_session).all()
                if basket_items:
                    for basket_item in basket_items:
                        basket_item.delete()
                user_session.delete()
            return Response(data=results, status=200)
        else:
            new_dict = json.loads(request.body.decode('utf-8'))
            name = (new_dict["fullName"]).split(" ")
            first_name = ""
            last_name = ""
            if name[0]:
                first_name = name[0]
            if len(name) > 1:
                last_name = name[1]
            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.email = new_dict["email"]
            request.user.save()
            request.user.profile.phone = new_dict["phone"]
            request.user.profile.save()
            order = Order.objects.get(pk=id)
            order.status = new_dict["status"]
            order.city = new_dict["city"]
            order.address = new_dict["address"]
            delivery = Delivery.objects.get(name=new_dict["deliveryType"])
            order.delivery_type = delivery
            order.payment_type = new_dict["paymentType"]
            order.save()
            results["orderId"] = order.pk
            return Response(data=results, status=200)

    def get(self, request: Request, pk=None, *args, **kwargs) -> Response:
        id = pk or request.query_params.get('id')
        results = None
        if id is None:
            orders = Order.objects.filter(user=request.user).all()
            results = OrderSerializer(orders, many=True).data
        else:
            order = Order.objects.get(pk=id)
            results = OrderSerializer(order, many=False).data
        return Response(data=results, status=200)


class PaymentView(APIView):
    def post(self, request: Request, pk=None, *args, **kwargs) -> Response:
        if not request.user.is_authenticated:
            return Response(data="Please login to create order!", status=403)
        id = pk or request.query_params.get('id')
        new_dict = json.loads(request.body.decode('utf-8'))
        number_string = new_dict["number"]
        number = int(number_string)
        if (number % 2 == 0) and (len(number_string) == 8):

            order = Order.objects.get(pk=id)
            if order.status == "created":
                items = OrderItem.objects.filter(order=order).all()
                enough_goods = True
                for item in items:
                    if item.count > item.product.count:
                        enough_goods = False
                if enough_goods:
                    for item in items:
                        item.product.count -= item.count
                        item.product.save()
                    order.status = "paid"
                    order.save()
                    return Response(status=200)
        return Response(status=400)


class ProfileView(APIView):
    def get(self, request: Request, *args, **kwargs) -> Response:
        Profile.objects.get_or_create(user=request.user)
        results = UserSerializer(request.user, many=False).data
        return Response(data=results, status=200)

    def post(self, request: Request, *args, **kwargs) -> Response:
        new_dict = json.loads(request.body.decode('utf-8'))
        name = (new_dict["fullName"]).split(" ")
        first_name = ""
        last_name = ""
        if name[0]:
            first_name = name[0]
        if len(name) > 1:
            last_name = name[1]
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.email = new_dict["email"]
        request.user.save()
        request.user.profile.phone = new_dict["phone"]
        request.user.profile.save()
        results = UserSerializer(request.user, many=False).data
        return Response(data=results, status=200)


class ProfilePasswordView(APIView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        new_dict = json.loads(request.body.decode('utf-8'))
        new_password = new_dict["newPassword"]
        password = new_dict["currentPassword"]
        user: User = authenticate(username=request.user.username, password=password)
        if user is None:
            return Response(status=500)
        else:
            user.password = new_password
            user.save()
            return Response(status=200)


class ProfileAvatarView(APIView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        Profile.objects.get_or_create(user=request.user)
        file = request.FILES["avatar"]
        image = Image.objects.create(src=file, alt="Profile avatar")
        request.user.profile.avatar = image
        request.user.profile.save()
        return Response(status=200)
