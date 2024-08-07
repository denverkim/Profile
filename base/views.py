from keras.models import load_model
import numpy as np
from PIL import Image
from django.conf import settings
import os
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.http import HttpResponse, HttpResponseBadRequest


def home(request):
    return render(request, "home.html")


def projects(request):
    return render(request, "projects.html")


def contact(request):
    return render(request, "contact.html")


def mnist_copy(request):
    return render(request, "mnist_copy.html")


def mnist(request):
    file = request.FILES.get("image")
    if not file:
        return render(request, "mnist.html")
        # # Process the image
        # return HttpResponse("Image uploaded successfully!")
    else:
        file_name = file.name
        file_path = os.path.join(settings.MEDIA_ROOT, "images", file_name)

        # Save the uploaded file
        with default_storage.open(file_path, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # 테스트 데이터 준비
        test_data = Image.open(file_path)
        test_data = test_data.resize((28, 28))
        test_data = test_data.convert("L")
        test_data = np.asarray(test_data)
        test_data = test_data.reshape(1, 28, 28, 1)

        # 글자와 확률을 예측
        model = load_model("base/models/mnist_model.h5")
        pred = model.predict(test_data)
        letter = np.argmax(pred, axis=1)[0]
        probs = pred[0][int(letter)]
        return render(request, "mnist.html", {"letter": letter, "probs": probs})


def fashion_mnist(request):
    file = request.FILES.get("image")
    if not file:
        return render(request, "fashion_mnist.html")
        # # Process the image
        # return HttpResponse("Image uploaded successfully!")
    else:
        file_name = file.name
        file_path = os.path.join(settings.MEDIA_ROOT, "images", file_name)

        # Save the uploaded file
        with default_storage.open(file_path, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # 테스트 데이터 준비
        test_data = Image.open(file_path)
        # test_data = Image.open(
        #     "D:/240701 KAIT/LAB/profile/Profile/base/media/images/ankleboot.jpg"
        # )

        test_data = test_data.resize((28, 28))
        test_data = test_data.convert("L")
        test_data = np.array(test_data)
        test_data = 255 - test_data
        test_data = test_data / 255.0
        test_data = test_data.reshape(1, 28, 28, 1)

        # 글자와 확률을 예측
        model = load_model(
            "D:/240701 KAIT/LAB/profile/Profile/base/models/fashion_mnist_model.h5"
        )
        pred = model.predict(test_data)

        # 라벨이름 저장
        label_names = [
            "T-shirt/top",
            "Trouser",
            "Pullover",
            "Dress",
            "Coat",
            "Sandal",
            "Shirt",
            "Sneaker",
            "Bag",
            "Ankle boot",
        ]

        clothing_num = np.argmax(pred, axis=1)[0]
        clothing = label_names[clothing_num]
        probs = pred[0][int(clothing_num)]

        return render(
            request, "fashion_mnist.html", {"clothing": clothing, "probs": probs}
        )


import tensorflow as tf
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.applications.resnet50 import decode_predictions
import numpy as np
from keras.applications.resnet50 import ResNet50


def cifar10(request):
    file = request.FILES.get("image")
    if not file:
        return render(request, "cifar10.html")
        # # Process the image
        # return HttpResponse("Image uploaded successfully!")
    else:
        file_name = file.name
        file_path = os.path.join(settings.MEDIA_ROOT, "images", file_name)

        # Save the uploaded file
        with default_storage.open(file_path, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # 테스트 데이터 준비
        from keras.preprocessing import image
        import numpy as np
        from keras.preprocessing.image import load_img, img_to_array
        from keras.models import load_model

        test_image = image.load_img(file_path, target_size=(32, 32))
        test_image = img_to_array(test_image) / 255.0
        test_image = np.expand_dims(test_image, axis=0)

        # 사전학습 모델 가져오기
        model = load_model(
            "D:/240701 KAIT/LAB/profile/Profile/base/models/vgg4_model.keras"
        )

        # 라벨이름 저장
        label_names = [
            "airplane",
            "automobile",
            "bird",
            "cat",
            "deer",
            "dog",
            "frog",
            "horse",
            "ship",
            "truck",
        ]
        pred = model.predict(test_image)
        objs_num = np.argmax(pred, axis=1)[0]
        objs = label_names[objs_num]
        probs = pred[0][int(objs_num)]

        # pred = decode_predictions(model.predict(x), top=1)
        # objs = pred[0][0][1]
        # probs = pred[0][0][2]

        return render(request, "cifar10.html", {"objs": objs, "probs": probs})


def ocr(request):
    return render(request, "ocr.html")
