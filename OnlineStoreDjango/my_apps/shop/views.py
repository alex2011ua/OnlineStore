from django.http import FileResponse


def get_foto_product(request, image_path):
    img = open(f"shop/media/foto/products/{image_path}", "rb")
    response = FileResponse(img)
    return response

def get_foto_banner(request, image_path):
    img = open(f"shop/media/foto/banners/{image_path}", "rb")
    response = FileResponse(img)
    return response
