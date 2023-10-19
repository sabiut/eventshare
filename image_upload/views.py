from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from .models import UploadedImage


def upload_view(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded image to the UploadedImage model
            image_instance = UploadedImage(image=request.FILES['image'])
            image_instance.save()

            # Redirect to a success page or gallery page
            return redirect('gallery')
    else:
        form = ImageUploadForm()
    return render(request, 'upload.html', {'form': form})


def handle_uploaded_file(f):
    with open('some_file_name.jpg', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def gallery_view(request):
    images = UploadedImage.objects.all().order_by('-upload_date')
    return render(request, 'gallery.html', {'images': images})


def delete_image(request, image_id):
    image = UploadedImage.objects.get(pk=image_id)
    image.delete()
    return redirect('gallery')
