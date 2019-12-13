from django.shortcuts import render
# Create your views here.
from django.http                    import HttpResponse
from django.http                    import JsonResponse
from django.views.decorators.csrf   import csrf_exempt
from rest_framework.renderers       import JSONRenderer
from rest_framework.parsers         import JSONParser
from prediction.models              import House
from prediction.serializers         import HouseSerializer
@csrf_exempt
def predict(request):
    """
    Renvoie une house avec la MEDV completee
    (Attend une MEDV innexistante)
    """
    if request.method == 'GET':
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'POST':
        data        = JSONParser().parse(request)
        serializer  = HouseSerializer(data=data)
        if serializer.is_valid():
            data["MEDV"]        = predict_medv(data)
            serializer          = HouseSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data  , status=201)
        return     JsonResponse(serializer.errors, status=400)

def predict_medv(unscaled_data):
    from sklearn.externals import joblib
    colonnes        = ["CRIM", "ZN", "INDUS", "CHAS", "NOX", "RM",
                        "AGE", "DIS", "RAD", "TAX", "PTRATIO", "B",
                        "LSTAT"]
    path_to_model   = "./prediction/modele_pour_boston_dataset.pkl"
    # on remet les data dans l'ordre des colonnes de la base d'apprentissage
    unscaled_data   = [unscaled_data[colonne] for colonne in colonnes]
    import numpy as np
    unscaled_data = np.array(unscaled_data).reshape(1,-1)
    print(unscaled_data)
    # on load le modèle appris préalablement
    model           = joblib.load(path_to_model)
    # on prédit
    medv            = model.predict(unscaled_data)
    # on renvoie la prédiction
    return medv

@csrf_exempt
def house_list(request):
    if request.method == 'GET':
        houses      = House.objects.all()
        serializer  = HouseSerializer(houses, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data        = JSONParser().parse(request)
        serializer  = HouseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data  , status=201)
        return     JsonResponse(serializer.errors, status=400)
@csrf_exempt
def house_detail(request, pk):
    print("house_detail")
    try:
        house = House.objects.get(pk=pk)
    except House.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = HouseSerializer(house)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        data       = JSONParser().parse(request)
        serializer = HouseSerializer(house, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        house.delete()
        return HttpResponse(status=204)
    return HttpResponse(status=204)
