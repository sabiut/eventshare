from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from .models import UploadedImage
import boto3
from io import BytesIO
from PIL import Image
from django.conf import settings


def upload_view(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the image first
            processed_image = process_image(request.FILES['image'])

            # Dynamic file path based on the original filename
            file_path = f'uploaded_images/{request.FILES["image"].name}'

            # Save the processed image to Linode Object Storage
            s3_client = boto3.client('s3',
                                     region_name='ap-south-1',
                                     endpoint_url='https://phptogallery.ap-south-1.linodeobjects.com',
                                     aws_access_key_id=settings.AWS_ACCESS_KEY,
                                     aws_secret_access_key=settings.AWS_SECRET_KEY)

            try:
                s3_client.upload_fileobj(
                    processed_image, 'phptogallery', file_path)
            except Exception as e:
                print(f"An error occurred: {e}")
                # Render an error message to the user
                return render(request, 'upload.html', {'form': form, 'error': 'Failed to upload the image. Please try again.'})

            # Save the reference to the model
            image_instance = UploadedImage(image=file_path)
            image_instance.save()

            # Redirect to the gallery or another page
            return redirect('gallery')
    else:
        form = ImageUploadForm()
    return render(request, 'upload.html', {'form': form})


def process_image(uploaded_image):
    """
    Process the uploaded image. 
    For now, we'll simply return the uploaded image without any processing.
    """
    image = Image.open(uploaded_image)

    # Convert the image to RGB mode if it's not already
    if image.mode != 'RGB':
        image = image.convert('RGB')

    output = BytesIO()
    image.save(output, format='JPEG')
    output.seek(0)
    return output


def gallery_view(request):
    images = UploadedImage.objects.all().order_by('-upload_date')
    image_urls = []
    base_url = 'https://phptogallery.ap-south-1.linodeobjects.com/phptogallery/'

    for image in images:
        image_url = base_url + image.image.name
        image_urls.append(image_url)
    print(image_url)

    return render(request, 'gallery.html', {'image_urls': image_urls})


# def upload_view(request):
#     if request.method == 'POST':
#         form = ImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Save the uploaded image to the UploadedImage model
#             image_instance = UploadedImage(image=request.FILES['image'])
#             image_instance.save()

#             # Redirect to a success page or gallery page
#             return redirect('gallery')
#     else:
#         form = ImageUploadForm()
#     return render(request, 'upload.html', {'form': form})
