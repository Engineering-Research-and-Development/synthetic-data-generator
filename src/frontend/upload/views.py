import pandas as pd
import requests
from django.shortcuts import render, redirect
from .forms import CSVUploadForm, ColumnChoice


def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            df = pd.read_csv(csv_file)
            request.session['csv_data'] = df.to_json()
            return redirect('preview_csv')
    else:
        form = CSVUploadForm()
    return render(request, 'upload_csv.html', {'form': form})

def preview_csv(request):
    df_json = request.session.get('csv_data')
    columns = request.session.get('columns')
    if df_json and columns:
        df = pd.read_json(df_json)
        first_10_lines = df.head(10)
        form = ColumnChoice(initial={'columns': columns})
        return render(request, 'preview_csv.html', {'form': form, 'data': first_10_lines.to_html()})
    return redirect('upload_csv')

def send_data(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST)
        if form.is_valid():
            df_json = request.session.get('csv_data')
            columns = form.cleaned_data['columns']
            df = pd.read_json(df_json)
            selected_data = df[columns]
            # Send data to endpoint
            response = requests.post('https://your-endpoint.com/api', json=selected_data.to_dict(orient='records'))
            if response.status_code == 200:
                return render(request, 'success.html')
            else:
                return render(request, 'error.html', {'error': response.text})
    return redirect('upload_csv')