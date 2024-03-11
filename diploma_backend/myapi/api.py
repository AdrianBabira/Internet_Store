# from rest_framework.generics import ListAPIView
# from . import serializer
# from . import models
#
#
# class CatalogItemListAPIView(ListAPIView):
#     serializer_class = serializer.CatalogItemSerializer
#
#     def get_queryset(self):
#         return models.CatalogItem.objects.all()
#
#
# class SubcategoriesListAPIView(ListAPIView):
#     serializer_class = serializer.SubcategoriesSerializer
#
#     def get_queryset(self):
#         return models.Subcategory.objects.all()
