from datetime import date, datetime

import dash
import numpy as np
import pandas as pd
import pymongo
from dash import dcc, html
from dash.dependencies import Input, Output


m=[['Здравоохранение',  'Спорт и события'],
['Здравоохранение', 'Права человека'],
['Здравоохранение', 'ЧС'],
['Дети и молодежь'],
['Старшее поколение', 'Ветераны и Историческая память'],
['Старшее поколение', 'Интеллектуальная помощь'],
['Природа','Урбанистика'],
['Природа', 'Поиск пропавших'],
['Культура и искусство',  'Образование'],
['Культура и искусство', 'Наука']]


m = pd.DataFrame(m)
m[-1]='main'
m=m.sort_index(axis=1)
m.columns=np.arange(m.shape[1])



hours=[{'label': str(i), 'value': str(i)} if i>9 else {'label': '0'+str(i), 'value': '0'+str(i)}
    for i in range(0,24)]

minutes=[{'label': str(i), 'value': str(i)} if i>5 else {'label': '0'+str(i), 'value': '0'+str(i)}
    for i in np.arange(0,60,5)]


butt=[]

def get_tab(md,i):
    global butt
    c='-'.join(list(md)[:-1] + [i])
    x=[i[1] for i in mdse if i[0]==c ]
    if len(x)==0:
        x = [html.Button('далее', id='next '+ c, n_clicks=0)]
        butt+=['next '+ c]
    else:
        x=x[0]
    return x


a = m.shape[1]-1
mdse=[]

while a>0:
    md=m.groupby(list(np.arange(a)))[a].apply(lambda x: list(np.unique(x))
                               if list(x)[0]!=None else False)
    mds=md[md!=False].reset_index()
    mdse = [['-'.join(list(md)[:-1])]+[[dcc.Tabs(
                id='-'.join(list(md)[:-1]),
                value=list(md)[-1][0],
                children=[dcc.Tab(label=i, value='-'.join(list(md)[:-1] + [i]),
                    children = get_tab(md,i)
                      )
            for i in list(md)[-1]]
    )]] for md in np.array(mds)]
    a-=1

mdse=mdse[0][1][0]

app = dash.Dash(__name__)

app.title = "Выбор заявки"


app.config.suppress_callback_exceptions = True

app.layout= html.Div([
            html.Div(id='page-content', className='content')
            ,  dcc.Location(id='url', refresh=False)
        ])


success = html.Div([dcc.Location(id='url_start_new', refresh=True)
            ,html.Div(className="row", children=[
                html.Div('Имя Фамилия',style=dict(width='10%')),
                dcc.Textarea(
                id='textarea'
                ,value=''
                ,style={'height': 15},#'width': '100%',
            )], style=dict(display='flex')),
            html.Br(),
            html.Div(
                className="row", children=[
            html.Div('Дата', style=dict(width='5%')),
            dcc.DatePickerSingle(
                id='my-date-picker-single',
                min_date_allowed=datetime.now().date(),
                max_date_allowed=date(2023, 1, 1),
                initial_visible_month=datetime.now().date(),
                date=datetime.now().date()
            ),
            html.Div('  ', style=dict(width='1%')),
            html.Div('Время', style=dict(width='5%')),
            html.Div(className='six columns', children=[
                dcc.Dropdown(
                    id='demo-dropdown',
                    options=hours,
                    value='12', clearable=False,searchable=False
                )], style={'width':'5%'})
            , html.Div(className='six columns', children=[
            dcc.Dropdown(
                id='demo-dropdown1',
                options=minutes,
                value='00', clearable=False,searchable=False
            )], style={'width':'5%'})
        ], style=dict(display='flex')),
        html.H2('''Выбрать категорию''', id='h1')
            , mdse, html.Div(id='result'),
        html.Br(),html.Br(),
        html.Div(id='textarea-example-output', style={'whiteSpace': 'pre-line'})
])

time=[]

@app.callback(
    Output('textarea-example-output', 'children'),
    [Input('my-date-picker-single', 'date'),
     Input('demo-dropdown', 'value'),
     Input('demo-dropdown1', 'value'),
     Input('textarea', 'value')])
def update_output(date_value,value,value1,value2):
    global time
    if date_value + value + value1 + value2:
        date_object = date.fromisoformat(date_value)
        date_string = date_object.strftime('%B %d, %Y')
        time=[date_string, value, value1,value2]
        return f'''Вы выбрали: \nдата: {date_string}\nвремя: {' '.join([value, value1])}\nКомментарий: {value2}'''



inp_butt=[Input(i, 'n_clicks') for i in butt]
men_choice=''


@app.callback(
    Output('result', 'children')
    , inp_butt)
def logout_dashboard(*n_clicks):
    global men_choice, time

    for k, i in enumerate(n_clicks):
        if i > 0:
            men_choice = butt[k]
            print('  dddd  ', k,  men_choice , time)

    if sum(n_clicks) > 0:
        return '/data'









@app.callback(
    Output('page-content', 'children')
    , [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return success
    elif pathname =='/data':
        return one
    else:
        return '404'



app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

if __name__ == '__main__':
    import platform
    if platform.system() == 'Windows':
        app.run_server(debug=True)
    else:
        app.run_server(host='0.0.0.0', port=7777)


