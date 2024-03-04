# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 14:05:38 2021

@author: watda

the framework used for this python app is Flask

Developers can develop the Python backend framework any way they need, however, it was designed for applications that are open-ended.
Flask has been used by big companies, which include LinkedIn and Pinterest.
Compared to Django, Flask is best suited for small and easy projects.
Thus, you can expect a web server development, support for Google App Engine as well as in-built unit testing.

my app should be tidied up and inspired by Chris one

path to open 


then run it from the console anaconde prompt

python my_app_freshwater.py

how to make it online available:
https://www.youtube.com/watch?v=b-M2KQ6_bM4


1. Open Heroku website and add application   (the name of the app will be part of the url)
2. Open Pycharm Community Verion
3. Create new project in Pycharm Community Verion  choose virtual environment (Virtualenv)
4. copy the files for the app in the folder of the new project 

5. Manually install all necessary packages  to run the python code in the virtual env
    important package used indirectly alwas has to be installed
    + pip install gunicorn    

6.create a requiremnets text file with all the pip install package + version

7. create .gitignore file  (or just copy it from the other projects)
 the gitignore file   is a simple text file with following content:
     venv
     *.pyc
     .env
     .DS_Store
8. create a procfile  with the content 
    web : guincorn  appname_without.py:server
    
9. create a requirements file  (command in the Pycharm terminal)
    this tells heroku which packages are necessary to run the app
    pip freeze > requirements.txt
    
    
10. log in  command in Pycharm
    heroku login

update to generate a simple requirements.txt file that just contains what was used in the given project

menue -> tools -> Synch Python requirements

In the procfile the python file with the real app that should be used need to be specified.
    

    
https://github.com/Vitens/phreeqpython
"""

"""
lukas 04.03.2024

improved version allowing for more input variables (more water parameters)

put a table as input


"""





import os

import dash
import dash_bootstrap_components as dbc
import dash_defer_js_import as dji
import flask
import pandas as pd
# import the package for carbonate system calculation chemistry
import phreeqpython
import plotly.graph_objects as go
from dash import dcc, dash_table
from dash import html
from dash.dependencies import Input, Output
from numpy import log10
from plotly.subplots import make_subplots

import numpy as np

#database which should be used for the calculations
# PhreeqPython comes standard with phreeqc.dat, pitzer.dat and vitens.dat
pp = phreeqpython.PhreeqPython(database='vitens.dat')



#from components import solve

external_stylesheets = ['https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css',
                        'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.18.1/styles/monokai-sublime.min.css']

#external_stylesheets=[dbc.themes.CYBORG]


external_scripts = ['https://code.jquery.com/jquery-3.2.1.slim.min.js',
                    'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js',
                    'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js']

# no clue what these external scripts do
#external_scripts=[dbc.]
# Server definition

server = flask.Flask(__name__)

# layout options
# https://dash-bootstrap-components.opensource.faculty.ai/docs/components/layout/

app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets,
                external_scripts=external_scripts,
                server=server,
                meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}])

# title taht will be visible in the browser tab
app.title = 'Open Carbonate System Alkalinity Calculations'

# for Heroku to regognize it
server=app.server

filepath = os.path.split(os.path.realpath(__file__))[0]

narrative_text = open(os.path.join(filepath, "narrative2_improved.md"), "r").read()
refs_text = open(os.path.join(filepath, "references2.md"), "r").read()
some_text = open(os.path.join(filepath, "sometext.md"), "r").read()

mathjax_script = dji.Import(src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/latest.js?config=TeX-AMS-MML_SVG")


app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            <script type="text/x-mathjax-config">
            MathJax.Hub.Config({
                tex2jax: {
                inlineMath: [ ['$','$'],],
                processEscapes: true
                }
            });
            </script>
            {%renderer%}
        </footer>
    </body>
</html>
'''

# COMPONENTS
# ==========

## Interactors
## -----------

#set some constants

M_C=12.011 #g/mol
M_CH4=16.04 #g/mol
M_CO2=44.01 #g/mol
M_CO3=60.01 #g/mol
M_H=1.00784 #g/mol
M_H2=M_H*2 # g/mol
M_H2O=18.01528 #g/mol
M_HCO3=61.0168 # g/mol
M_Na=22.98976928 # g/mol
M_NaCO3=M_CO3+M_Na # g/mol
M_NaHCO3=M_HCO3+M_Na # g/mol
M_OH=17.008 # g/mol
M_NaOH=M_Na+M_OH # g/mol
M_O=15.999 # g/mol
M_O2=M_O*2 # g/mol



M_Mg=24.305 # g/mol
M_Ca=40.078  # g/mol
M_CaCO3=M_Ca+M_C+3*M_O
M_MgCO3=M_Mg+M_C+3*M_O
M_MgHCO3=M_Mg+M_HCO3
M_CaHCO3=M_Ca+M_HCO3

M_CaOH=M_Ca+M_OH

M_MgOH=M_Mg+M_OH

#create the converfrsion dict
conv={'CH4': M_CH4, 'CO2': M_CO2,
      'CO3-2': M_CO3, 'H+': M_H,
      'H2': M_H2,'H2O': M_H2O,
      'HCO3-': M_HCO3, 'Na+':M_Na,
      'NaCO3-': M_NaCO3, 'NaHCO3': M_NaHCO3,
      'NaOH': M_NaOH, 'O2': M_O2, 'OH-':M_OH,
      'Ca+2':M_Ca,'CaCO3':M_CaCO3,
      'Mg+2':M_Mg,'MgCO3':M_MgCO3,
      'MgHCO3+':M_MgHCO3,'MgOH+':M_MgOH,
      'CaHCO3+':M_CaHCO3,'CaOH+':M_CaOH}


#put a whole table here for the input



#variables for the data table

params = [
    'TA [ueq/kgw]', 'water T [°C]', 'air pCO2 [ppm]', 'Na+',
    'Mg+2', 'Ca+2', ''
]

# APP LAYOUT
# ==========

app.layout = html.Div([
    dbc.Container(children=[
        dcc.Markdown(narrative_text, dangerously_allow_html=True),

        #input whole editable data table

        dash_table.DataTable(
                id='table-editing-simple',
                columns=(
                    [{'id': 'Model', 'name': 'Model'}] +
                    [{'id': p, 'name': p} for p in params]
                ),
                data=[
                    dict(Model=i, **{param: 0 for param in params})
                    for i in range(1, 2)
                ],
                editable=True
            ),


        html.Br(),
        html.B('This is the resulting speciation after the water is in equilibrium with the atmosphere:'),
        html.Br(),
        html.Br(),
        
        #html.Table([
        #html.Tr(['species]
        #html.Tr([html.Td(['CO2(aq)= ']), html.Td(id='CO2_species'), html.Td("[umol/l]")   ]  ),
        #html.Tr([html.Td(['HCO3- = ']), html.Td(id='HCO3_species'), html.Td("[umol/l]") ]),
        #html.Tr([html.Td(['CO3-2 = ']), html.Td(id='CO3_species'), html.Td("[umol/l]") ]),
        #html.Tr([html.Td(['Na+   = ']), html.Td(id='Na_species'), html.Td("[umol/l]") ]),
        #html.Tr([html.Td(['H+    = ']), html.Td(id='H_species'), html.Td("[umol/l]") ]),
        #html.Tr([html.Td(['OH-  =   ']), html.Td(id='OH_species'), html.Td("[umol/l]") ]),
        #html.Tr([html.Td(['NaCO3- =   ']), html.Td(id='NaCO3_species'), html.Td("[umol/l]") ]),
        #]),

        html.Div(id="table1", style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'middle'}),
        html.Br(),
        html.Br(),
        html.B('Those are the satutrration index of minerals that can precipitate:'),
        html.Br(),
        html.Br(),
        html.Div(id="table2", style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'middle'}),
        html.Br(),
        html.Br(),
        html.B('Bulk parameters:'),
        html.Br(),
        html.Br(),
        html.Div(id="table3", style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'middle'}),
        dcc.Markdown(some_text, dangerously_allow_html=True),
        
        
        
        dcc.Markdown(refs_text, dangerously_allow_html=True),
        html.Br(),
        html.Br(),
        html.Br(),
         
        
        
    ]),
    mathjax_script
])
    
"""  
# added stuff could be dagerous
html.H6("Change the value in the text box to see callbacks in action!"),
html.Div([
"Input: ",
dcc.Input(id='my-input', value='initial value', type='text'), 
        
]),
html.Br(),
html.Div(id='my-output'),
"""  


# INTERACTION
# ===========
# here inputs and outputs of the application are defined

# change here
@app.callback(Output("table1","children"),
                    Output("table2","children"),
                    Output("table3","children"),

              # new output plot include here 18.10.2022

              #this number of inputs need to match with the  update function
              [Input('table-editing-simple', 'data'),
               Input('table-editing-simple', 'columns'),]
              ) 



# input for the function that is called to generate all the output


def update_graph(rows, columns):



    # getting all the data from the input table
    df = pd.DataFrame(rows, columns=[c['name'] for c in columns])

    #make whole dataframe to float
    df = df.apply(pd.to_numeric, errors='coerce')

    #define output table

    #df_out=

    #solution function can just take single numbers so we use a for loop

    #when all input is zero it is fine

    for k in df.index:

        sol = pp.add_solution({'units': 'umol/kgw',
                               #'pH': pH,
                               'density': 1.000,
                               'temp': df.loc[k,'water T [°C]'],
                               # include the cations
                               #'Li': np.nan_to_num(cat[('IC_Ca', '[umol_l]')]),
                               'Na': np.nan_to_num(df.loc[k,'Na+']),
                               #'N(-3)': np.nan_to_num(cat[('IC_NH4', '[umol_l]')]),  # N(-3) stands for NH4
                               #'K': np.nan_to_num(cat[('IC_K', '[umol_l]')]),
                               'Ca': np.nan_to_num(df.loc[k,'Ca+2']),
                               'Mg': np.nan_to_num(df.loc[k,'Mg+2']),
                               # include the anions
                               #'F': np.nan_to_num(an[('IC_F', '[umol_l]')]),
                               #'Cl': np.nan_to_num(an[('IC_Cl', '[umol_l]')]),
                               #'N(3)': np.nan_to_num(an[('IC_NO2', '[umol_l]')]),  # N(-3) stands for NO2-

                               # enter total inorganic carbon (C or C(4))
                               # include CO2 as carbon (IV) oxide  (CO2) all C in the configuration
                               # 'C(4)':DIC,
                               # test different notation
                               #'C(4)': DIC,
                               #enter the alklainity (as CO3)
                               'Alkalinity':np.nan_to_num(df.loc[k,'TA [ueq/kgw]']),
                               })

        #closed system case no CO2 interaction
        if np.nan_to_num(df.loc[k,'air pCO2 [ppm]'])<=0.0:
            # pH of the solution
            pH = sol.pH

            # Specific conductance, microsiemens per centimeter.
            SC = sol.sc

            # DIC of the solution
            DIC = (sol.total('CO2', units='mol') + sol.total('HCO3', units='mol') + sol.total('CO3',
                                                                                              units='mol'))  # convert it to mol


        else:
            # the pressure default unit is atm so I convert the ppm to atm
            p=df.loc[k,'air pCO2 [ppm]']*1e-6

            # the function equilizie needs the phreeqc input the partial pressure in negative log10 scale

            input_pCO2=log10(p)


            # new function from phreeqc package used this time
            # reaction with ambient CO2 pressure
            sol.equalize(['CO2(g)'], [input_pCO2])

            # pH of the solution
            pH = sol.pH

            # Specific conductance, microsiemens per centimeter.
            SC = sol.sc

            # DIC of the solution
            DIC = (sol.total('CO2', units='mol') + sol.total('HCO3', units='mol') + sol.total('CO3',units='mol'))  # convert it to mol

    #after reaction generate the output

    #get concentration of all species
    df=pd.DataFrame.from_dict(sol.species, orient='index', columns=['concentration [mol/L]'])

    df = df.rename_axis(['species']).reset_index()


    # dict comprehension {k: prices[k]*stock[k] for k in prices}

    df['concentration [mg/L]']={key: 1000*value*conv[key] for key,value in sol.species.items()}.values()

    df['concentration [ppm]'] = {key: 1000 * value * conv[key] for key, value in sol.species.items()}.values()
    #format = Format(precision=4, scheme=Scheme.fixed)


    #dash table object

    tbl1=dash_table.DataTable(
        id="format_table",
        columns=[
            {
                "name": i,
                "id": i,
                "type": "numeric",  # Required!
                'format': dash_table.Format.Format(precision=4, scheme=dash_table.Format.Scheme.exponent)
            }
            for i in df.columns
        ],
        data=df.to_dict("records"),
        editable=True,
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
            'minWidth': '100%'},
    )

    #output the saturation index table

    df_phases=pd.DataFrame.from_dict(sol.phases, orient='index', columns=['saturation index'])

    df_phases = df_phases.rename_axis(['mineral']).reset_index()
    # get SI of the phases


    tbl2 = dash_table.DataTable(
        id="format_table",
        columns=[
            {
                "name": i,
                "id": i,
                "type": "numeric",  # Required!
                'format': dash_table.Format.Format(precision=4, scheme=dash_table.Format.Scheme.exponent)
            }
            for i in df_phases.columns
        ],
        data=df_phases.to_dict("records"),
        editable=True,
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
            'minWidth': '100%'},
        style_data_conditional=[

            {
                'if': {
                    'filter_query': '{saturation index} >0',
                    'column_id': 'saturation index'
                },
                'backgroundColor': 'tomato',
                'color': 'white'
            },



        ]
    )




    # calculate DIC


    d={'Dissolved inorganic carbon [mol/kgw]':[DIC],'pH':[pH],'EC [uS/cm]':[SC]}

    df_extra=pd.DataFrame.from_dict(d,orient='index',columns=['number'])

    df_extra = df_extra.rename_axis(['variable']).reset_index()


    tbl3 = dash_table.DataTable(
        id="format_table",
        columns=[
            {
                "name": i,
                "id": i,
                "type": "numeric",  # Required!
                'format': dash_table.Format.Format(precision=4, scheme=dash_table.Format.Scheme.exponent)
            }
            for i in df_extra.columns
        ],
        data=df_extra.to_dict("records"),
        editable=True,
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
            'minWidth': '100%'},

    )




    return tbl1, tbl2,tbl3

# here comes the speciation
    
'''

@app.callback(Output("numbers",'children'),
              Input("x","value"))

def update_result(x, y):
    return "The muver of moles of HCO§ is: {}".format(x)

'''


# another app callback for the next plot therefore I will use a single temprerature slider
'''
@app.callback(Output("temperature", "figure"),
              Input("T", "value"),
              )
def third_callback(T):
    
    x = np.arange(10)

    fig = go.Figure(data=go.Scatter(x=x, y=T*x**2))
    
    return fig

'''


if __name__ == '__main__':
    app.run_server(debug=True)