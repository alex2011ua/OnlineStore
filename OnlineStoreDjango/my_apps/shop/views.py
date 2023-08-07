from django.http import FileResponse


def get_foto(request, image_path):
    img = open(f"shop/media/products/{image_path}", "rb")
    response = FileResponse(img)
    return response
