from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.core.exceptions import ValidationError
from .models import Product
from .models import Photo


# Página de inicio
class HomePageView(TemplateView):
    template_name = "pages/home.html"


# Página "Acerca de"
class AboutPageView(TemplateView):
    template_name = "pages/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "title": "About us - Online Store",
                "description": "My first page ever",
                "author": "DCH",
            }
        )
        return context


# Página de contacto
class ContactPageView(TemplateView):
    template_name = "pages/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "title": "Contact Us - Online Store",
                "email": "dch@gmail.com",
                "address": "popular, Medellin, Colombia",
                "phone": "11235813",
            }
        )
        return context


# Vista para listar productos desde la base de datos
class ProductIndexView(View):
    template_name = "products/index.html"

    def get(self, request):
        viewData = {
            "title": "Products - Online Store",
            "subtitle": "List of products",
            "products": Product.objects.all(),
        }
        return render(request, self.template_name, viewData)


# Vista para mostrar detalles de un producto
class ProductShowView(View):
    template_name = "products/show.html"

    def get(self, request, id):
        try:
            product_id = int(id)
            if product_id < 1:
                raise ValueError("Product ID must be 1 or greater")
            product = get_object_or_404(Product, pk=product_id)
        except (ValueError, IndexError):
            return HttpResponseRedirect(reverse("home"))

        viewData = {
            "title": f"{product.name} - Online Store",
            "subtitle": f"{product.name} - Product information",
            "product": product,
        }
        return render(request, self.template_name, viewData)


# ✅ Formulario basado en Modelo
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price"]

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is not None and price <= 0:
            raise ValidationError("Price must be greater than zero.")
        return price


# ✅ Vista para crear producto usando ModelForm
class ProductCreateView(View):
    template_name = "products/create.html"

    def get(self, request):
        form = ProductForm()
        viewData = {"title": "Create product", "form": form}
        return render(request, self.template_name, viewData)

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("success")  # Asegúrate de que esta ruta exista
        viewData = {"title": "Create product", "form": form}
        return render(request, self.template_name, viewData)


# Página de éxito al crear producto
class SuccessView(TemplateView):
    template_name = "pages/success.html"


# --- CART SYSTEM ---

from django.views import View
from django.shortcuts import render, redirect


class CartView(View):
    template_name = "cart/index.html"

    def get(self, request):
        # Base de datos simulada de productos
        products = {
            121: {"name": "Tv samsung", "price": "1000"},
            11: {"name": "Iphone", "price": "2000"},
        }

        # Productos en carrito desde la sesión
        cart_products = {}
        cart_product_data = request.session.get("cart_product_data", {})

        for key, product in products.items():
            if str(key) in cart_product_data.keys():
                cart_products[key] = product

        # Datos para la plantilla
        view_data = {
            "title": "Cart - Online Store",
            "subtitle": "Shopping Cart",
            "products": products,
            "cart_products": cart_products,
        }

        return render(request, self.template_name, view_data)

    def post(self, request, product_id):
        cart_product_data = request.session.get("cart_product_data", {})
        cart_product_data[product_id] = product_id
        request.session["cart_product_data"] = cart_product_data
        return redirect("cart_index")


class CartRemoveAllView(View):
    def post(self, request):
        if "cart_product_data" in request.session:
            del request.session["cart_product_data"]
        return redirect("cart_index")


def photo_list(request):
    photos = Photo.objects.all()
    return render(request, "pages/photo_list.html", {"photos": photos})


from django.shortcuts import render, redirect
from django.views import View


def ImageViewFactory(image_storage):
    class ImageView(View):
        template_name = "images/index.html"

        def get(self, request):
            image_url = request.session.get("image_url", "")
            return render(request, self.template_name, {"image_url": image_url})

        def post(self, request):
            image_url = image_storage.store(request)
            request.session["image_url"] = image_url
            return redirect("image_index")

    return ImageView
