from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, "home.html")


def projects(request):
    return render(request, "projects.html")
s

def contact(request):
    return render(request, "contact.html")


import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.http import HttpResponse
from PIL import Image

def mnist(request):
    file = request.FILES.get("file")
    if not file:
        # return HttpResponse("업로드 되지 않았습니다. ")
        return render(request, "mnist.html")
    else:
        file_name = file.name
        file_path = os.path.join(settings.MEDIA_ROOT, "images", file_name)

        with default_storage.open(file_path, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        import numpy as np
        
        # 테스트 이미지 준비
        file_path = "D:/240701 KAIT/LAB/Profile_CLASS/base/media/images/three.png"
        test_image = Image.open(file_path)
        test_image = test_image.resize((28,28))
        test_image = test_image.convert('L')
        test_image = np.asarray(test_image)
        test_image = test_image.reshape(1,28,28,1)

        # 나중에 사용할 때
        from keras.models import load_model
        model = load_model('D:/240701 KAIT/LAB/Profile_CLASS/base/models/mnist_model.h5')
        digit = np.argmax(model.predict(test_image), axis=1)[0]
        probs = model.predict(test_image)[0][digit]
        
        
        probs = 0.9
        
        return render(request, "mnist.html", {"digit": digit, "probs": probs})
        # return HttpResponse("업로드 되었습니다.")
