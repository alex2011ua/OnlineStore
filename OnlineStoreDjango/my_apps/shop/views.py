from django.http import FileResponse, Http404
from django.shortcuts import render

from .form import gpt_Form
from .llama import LlamaSearch
from .models import Product


def get_foto_product(request, image_path):
    try:
        img = open(f"shop/media/foto/products/{image_path}", "rb")
        response = FileResponse(img)
        return response
    except FileNotFoundError:
        raise Http404(f"file {image_path} not found!")


def get_foto_banner(request, image_path):
    try:
        img = open(f"shop/media/foto/banners/{image_path}", "rb")
        response = FileResponse(img)
        return response
    except FileNotFoundError:
        raise Http404(f"file {image_path} not found!")


def get_foto_category(request, image_path):
    try:
        img = open(f"shop/media/foto/categories/{image_path}", "rb")
        response = FileResponse(img)
        return response
    except FileNotFoundError:
        raise Http404(f"file {image_path} not found!")


def gpt_search(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = gpt_Form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            search_string = form.cleaned_data["search_gpt"]
            search = LlamaSearch()
            answer = search.search_answer(search_string)
            slug = answer.split()[1]
            try:
                product = Product.objects.get(slug=slug)
            except Product.DoesNotExist:
                product = None
            return render(
                request,
                "name.html",
                {"form": form, "answer": answer, "product": product},
            )

    # if a GET (or any other method) we'll create a blank form
    else:
        form = gpt_Form()

    return render(request, "name.html", {"form": form})
