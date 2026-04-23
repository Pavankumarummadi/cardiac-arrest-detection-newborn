from django.shortcuts import render, redirect
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import VotingClassifier

# Create your views here.
from Remote_User.models import ClientRegister_Model, cardiac_arrest_prediction

def login(request):
    if request.method == "POST" and 'submit1' in request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            enter = ClientRegister_Model.objects.get(username=username, password=password)
            request.session["userid"] = enter.id
            return redirect('ViewYourProfile')
        except ClientRegister_Model.DoesNotExist:
            pass

    return render(request, 'RUser/login.html')

def Add_DataSet_Details(request):
    return render(request, 'RUser/Add_DataSet_Details.html', {"excel_data": ''})

def Register1(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phoneno = request.POST.get('phoneno')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        ClientRegister_Model.objects.create(username=username, email=email, password=password, phoneno=phoneno,
                                            country=country, state=state, city=city)
        return render(request, 'RUser/Register1.html')
    else:
        return render(request, 'RUser/Register1.html')

def ViewYourProfile(request):
    userid = request.session['userid']
    obj = ClientRegister_Model.objects.get(id=userid)
    return render(request, 'RUser/ViewYourProfile.html', {'object': obj})

def Predict_Cardiac_Arrest_Type(request):
    if request.method == "POST":
        Fid = request.POST.get('Fid')
        Age_In_Days = request.POST.get('Age_In_Days')
        Sex = request.POST.get('Sex')
        ChestPainType = request.POST.get('ChestPainType')
        RestingBP = request.POST.get('RestingBP')
        RestingECG = request.POST.get('RestingECG')
        MaxHR = request.POST.get('MaxHR')
        ExerciseAngina = request.POST.get('ExerciseAngina')
        Oldpeak = request.POST.get('Oldpeak')
        ST_Slope = request.POST.get('ST_Slope')
        slp = request.POST.get('slp')
        caa = request.POST.get('caa')
        thall = request.POST.get('thall')

        data = pd.read_csv("Datasets.csv", encoding='latin-1')

        def apply_results(status):
            if status == 0:
                return 0  # No Cardiac Arrest Found
            elif status == 1:
                return 1  # Cardiac Arrest Found
            return status

        data['Results'] = data['HeartDisease'].apply(apply_results)

        x = data['Fid']
        y = data['Results']

        cv = CountVectorizer()
        x = cv.fit_transform(x)

        models = []
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.20)

        # Artificial Neural Network (ANN)
        mlpc = MLPClassifier().fit(X_train, y_train)
        models.append(('MLPClassifier', mlpc))

        # SVM Model
        lin_clf = svm.LinearSVC()
        lin_clf.fit(X_train, y_train)
        models.append(('svm', lin_clf))

        # Logistic Regression
        reg = LogisticRegression(random_state=0, solver='lbfgs').fit(X_train, y_train)
        models.append(('logistic', reg))


        classifier = VotingClassifier(estimators=models)
        classifier.fit(X_train, y_train)

        vector1 = cv.transform([Fid]).toarray()
        predict_text = classifier.predict(vector1)

        prediction = int(predict_text[0])

        if prediction == 0:
            val = 'No Cardiac Arrest Found'
        elif prediction == 1:
            val = 'Cardiac Arrest Found'
        else:
            val = 'Unknown'

        cardiac_arrest_prediction.objects.create(
            Fid=Fid,
            Age_In_Days=Age_In_Days,
            Sex=Sex,
            ChestPainType=ChestPainType,
            RestingBP=RestingBP,
            RestingECG=RestingECG,
            MaxHR=MaxHR,
            ExerciseAngina=ExerciseAngina,
            Oldpeak=Oldpeak,
            ST_Slope=ST_Slope,
            slp=slp,
            caa=caa,
            thall=thall,
            Prediction=val
        )

        return render(request, 'RUser/Predict_Cardiac_Arrest_Type.html', {'objs': val})
    return render(request, 'RUser/Predict_Cardiac_Arrest_Type.html')



