from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
from .models import PredResults
import requests
import json

def predict(request):
    return render(request, 'predict.html')


def predict_chances(request):

    if request.POST.get('action') == 'post':

        input1 = (request.POST.get('input1'))
        input2 = (request.POST.get('input2'))
        input3 = (request.POST.get('input3'))

        aqi_data_updated = pd.read_csv('AQI_Data_Updated.csv')

        #result = aqi_data_updated[(aqi_data_updated.State == input1) & (aqi_data_updated.City == input2) & (aqi_data_updated.StationName == input3)].iloc[:, 3:-1].values

        base_url = "https://api.waqi.info"

        token = open('waqitoken.txt').read()

        name = input3
        r = requests.get(base_url + f"/feed/{name}/?token={token}")
        pollutants = ['pm25', 'pm10', 'o3']
        val = []
        for i in pollutants:
            val.append(r.json()['data']['forecast']['daily'][i][0]['avg'])
        # print(val)

        # pollutants_add = [10.063455, 31.214742, 0.862796]

        result = val
        model = pd.read_pickle('new_model_realtime.pickle')

        obs_val = [[], [], []]

        for index, j in enumerate(pollutants):
            for i in range(7):
                avg, date, max, min = (r.json()['data']['forecast']['daily'][j][i]['avg'],
                                       r.json()['data']['forecast']['daily'][j][i]['day'],
                                       r.json()['data']['forecast']['daily'][j][i]['max'],
                                       r.json()['data']['forecast']['daily'][j][i]['min'])
                obs_val[index].append([avg, max, min, date])

        temp_l = [[], [], [], [], [], [], []]
        for k in range(7):
            temp_l[k].append(obs_val[0][k][3])
            for m in range(0, 3):

                l = []
                for n in range(0, 3):
                    l.append(obs_val[n][k][m])
                calculate_aqi = model.predict([l])
                temp_l[k].append(round(calculate_aqi[0], 2))

        weekly_data = {'avg_val': [], 'Max': [], 'Min': [], 'Date_val': []}

        for i in temp_l:
            weekly_data['Date_val'].append(str(i[0]))
            weekly_data['avg_val'].append(str(i[1]))
            weekly_data['Max'].append(str(i[2]))
            weekly_data['Min'].append(str(i[3]))

        json_string = json.dumps(weekly_data)


        # Make prediction
        result1 = model.predict([result])

        classification = round(result1[0], 2)

        PredResults.objects.create(input1=input1, input2=input2, input3=input3,
                                   classification=classification)

        return JsonResponse({'result': classification, 'input1': input1,
                             'input2': input2, 'input3': input3, 'result1': classification, 'json_string': json_string },
                            safe=False)


def view_results(request):
    # Submit prediction and show all
    data = {"dataset": PredResults.objects.all()}
    return render(request, "results.html", data)

