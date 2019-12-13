def predict_medv(unscaled_data):
    from sklearn.externals import joblib
    colonnes        = ["CRIM", "ZN", "INDUS", "CHAS", "NOX", "RM",
                        "AGE", "DIS", "RAD", "TAX", "PTRATIO", "B",
                        "LSTAT"]
    path_to_model   = "./ipynb/model_svr.pkl"
    path_for_scaler = "./ipynb/scaler.pkl"
    unscaled_data   = [unscaled_data[colonne] for colonne in colonnes]
    model           = joblib.load(path_to_model)
    scaler          = joblib.load(path_for_scaler)
    donnees_scalees = scaler.transform(unscaled_data)
    medv            = model.predict(donnees_scalees)
    return medv


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
