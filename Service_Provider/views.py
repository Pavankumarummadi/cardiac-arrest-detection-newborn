from django.db.models import Count, Avg
from django.shortcuts import render, redirect
from django.http import HttpResponse
import xlwt
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

# Create your views here.
from Remote_User.models import ClientRegister_Model, cardiac_arrest_prediction, detection_ratio, detection_accuracy


def serviceproviderlogin(request):
    if request.method  == "POST":
        admin = request.POST.get('username')
        password = request.POST.get('password')
        if admin == "Admin" and password =="Admin":
            detection_accuracy.objects.all().delete()
            return redirect('View_Remote_Users')

    return render(request,'SProvider/serviceproviderlogin.html')

def View_Prediction_Of_Cardiac_Arrest_Type_Ratio(request):
    detection_ratio.objects.all().delete()
    kword = 'No Cardiac Arrest Found'
    obj = cardiac_arrest_prediction.objects.filter(Prediction=kword)
    obj1 = cardiac_arrest_prediction.objects.all()
    count = obj.count()
    count1 = obj1.count()
    
    if count1 > 0:
        ratio = (count / count1) * 100
        if ratio != 0:
            detection_ratio.objects.create(names=kword, ratio=ratio)

    kword1 = 'Cardiac Arrest Found'
    obj1_filtered = cardiac_arrest_prediction.objects.filter(Prediction=kword1)
    obj11 = cardiac_arrest_prediction.objects.all()
    count_filtered = obj1_filtered.count()
    count11 = obj11.count()
    
    if count11 > 0:
        ratio1 = (count_filtered / count11) * 100
        if ratio1 != 0:
            detection_ratio.objects.create(names=kword1, ratio=ratio1)

    obj_results = detection_ratio.objects.all()
    return render(request, 'SProvider/View_Prediction_Of_Cardiac_Arrest_Type_Ratio.html', {'objs': obj_results})

def View_Remote_Users(request):
    obj=ClientRegister_Model.objects.all()
    return render(request,'SProvider/View_Remote_Users.html',{'objects':obj})

def ViewTrendings(request):
    topic = cardiac_arrest_prediction.objects.values('topics').annotate(dcount=Count('topics')).order_by('-dcount')
    return  render(request,'SProvider/ViewTrendings.html',{'objects':topic})

def charts(request,chart_type):
    chart1 = detection_ratio.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request,"SProvider/charts.html", {'form':chart1, 'chart_type':chart_type})

def charts1(request,chart_type):
    chart1 = detection_accuracy.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request,"SProvider/charts1.html", {'form':chart1, 'chart_type':chart_type})

def View_Prediction_Of_Cardiac_Arrest_Type(request):
    obj =cardiac_arrest_prediction.objects.all()
    return render(request, 'SProvider/View_Prediction_Of_Cardiac_Arrest_Type.html', {'list_objects': obj})

def likeschart(request,like_chart):
    charts =detection_accuracy.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request,"SProvider/likeschart.html", {'form':charts, 'like_chart':like_chart})


def Download_Predicted_DataSets(request):

    response = HttpResponse(content_type='application/ms-excel')
    # decide file name
    response['Content-Disposition'] = 'attachment; filename="Predicted_Data.xls"'
    # creating workbook
    wb = xlwt.Workbook(encoding='utf-8')
    # adding sheet
    ws = wb.add_sheet("sheet1")
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    # headers are bold
    font_style.font.bold = True
    # writer = csv.writer(response)
    obj = cardiac_arrest_prediction.objects.all()
    data = obj  # dummy method to fetch data.
    for my_row in data:
        row_num = row_num + 1

        ws.write(row_num, 0, my_row.Fid, font_style)
        ws.write(row_num, 1, my_row.Age_In_Days, font_style)
        ws.write(row_num, 2, my_row.Sex, font_style)
        ws.write(row_num, 3, my_row.ChestPainType, font_style)
        ws.write(row_num, 4, my_row.RestingBP, font_style)
        ws.write(row_num, 5, my_row.RestingECG, font_style)
        ws.write(row_num, 6, my_row.MaxHR, font_style)
        ws.write(row_num, 7, my_row.ExerciseAngina, font_style)
        ws.write(row_num, 8, my_row.Oldpeak, font_style)
        ws.write(row_num, 9, my_row.ST_Slope, font_style)
        ws.write(row_num, 10, my_row.slp, font_style)
        ws.write(row_num, 11, my_row.caa, font_style)
        ws.write(row_num, 12, my_row.thall, font_style)
        ws.write(row_num, 13, my_row.Prediction, font_style)


    wb.save(response)
    return response

def train_model(request):
    detection_accuracy.objects.all().delete()

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

    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.20)

    # Artificial Neural Network (ANN)
    mlpc = MLPClassifier().fit(X_train, y_train)
    y_pred_mlpc = mlpc.predict(X_test)
    detection_accuracy.objects.create(names="Artificial Neural Network (ANN)",
                                      ratio=accuracy_score(y_test, y_pred_mlpc) * 100)

    # SVM Model
    lin_clf = svm.LinearSVC()
    lin_clf.fit(X_train, y_train)
    predict_svm = lin_clf.predict(X_test)
    svm_acc = accuracy_score(y_test, predict_svm) * 100
    detection_accuracy.objects.create(names="SVM", ratio=svm_acc)

    # Logistic Regression
    reg = LogisticRegression(random_state=0, solver='lbfgs').fit(X_train, y_train)
    y_pred_reg = reg.predict(X_test)
    detection_accuracy.objects.create(names="Logistic Regression", ratio=accuracy_score(y_test, y_pred_reg) * 100)

    # Decision Tree Classifier
    dtc = DecisionTreeClassifier()
    dtc.fit(X_train, y_train)
    dtcpredict = dtc.predict(X_test)
    detection_accuracy.objects.create(names="Decision Tree Classifier", ratio=accuracy_score(y_test, dtcpredict) * 100)

    labeled = 'labeled_data.csv'
    data.to_csv(labeled, index=False)

    obj = detection_accuracy.objects.all()
    return render(request, 'SProvider/train_model.html', {'objs': obj})
