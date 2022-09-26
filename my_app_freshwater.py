# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 14:05:38 2021

@author: watda

my app should be tidied up and inspired by Chris one

path to open 
cd C:\Daten\Transfer\Karriere\nebenjob_conductivity\python_simulation


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
    

    
https://github.com/Vitens/phreeqpython
"""
import os
import flask
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import dash_defer_js_import as dji
import numpy as np

from plotly.subplots import make_subplots

import pandas as pd

#import the package for carbonate system calculation chemistry
import phreeqpython

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

# Server definition

server = flask.Flask(__name__)

app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets,
                external_scripts=external_scripts,
                server=server)

# for Heroku to regognize it
server=app.server

filepath = os.path.split(os.path.realpath(__file__))[0]

narrative_text = open(os.path.join(filepath, "narrative2.md"), "r").read()

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

# read in the bjerrum plot csv file as lines
lines=pd.read_table('bjerrum_plot.csv',sep=',', keep_default_na=False\
                    , na_filter=False, header='infer',engine='python', encoding='utf-8')


# Use the following function when accessing the value of 'my-slider'
# in callbacks to transform the output value to logarithmic
def transform_value(value):
    return 10 ** value



## Interactors
## -----------

#set the ranges for the sliders
T_range=[0,80]
CO2_range=[1,10000] 
alkalinity_range=[1,1e+6]




T_slider=dcc.Slider(id='T_input', min=T_range[0], max=T_range[1], step=0.5, marks={x: str(x)+'°C' for x in range(T_range[0],T_range[1],10)},
        value=20, tooltip={"placement": "bottom", "always_visible": True}, updatemode='drag')

CO2_slider=dcc.Slider(id='CO2_input', min=CO2_range[0], max=CO2_range[1], step=1, marks={x: str(x)+'ppm' for x in range(CO2_range[0],CO2_range[1],1000)},
        value=415, tooltip={"placement": "bottom", "always_visible": True}, updatemode='drag')

alkalinity_slider=dcc.Slider(id='alkalinity_input', min=np.log10(alkalinity_range[0]) ,max=np.log10(alkalinity_range[1]), step=0.01,
        marks={x: '{:.0e}'.format(10**x)+' ueq/L' for x in range(0,6,int(1))},value=np.log10(2500),
        tooltip={"placement": "bottom", "always_visible": True},
        updatemode='drag',drag_value=3)


T_slider2=dcc.Slider(id='T', min=0, max=100, step=0.5, marks={x: str(x)+'°C' for x in range(0,100,10)},
        value=5, tooltip={"placement": "bottom", "always_visible": True}, updatemode='drag')


# APP LAYOUT
# ==========

app.layout = html.Div([
    dbc.Container(children=[
        dcc.Markdown(narrative_text, dangerously_allow_html=True),
        
        #dcc.Graph(id="sir_solution", figure=display_SIR_solution(solve(delta=0.5, R0=2.67, tau=8.5))),
        
        dbc.Row(children=[dbc.Col(children=["water tempearture [°C]:"], className="col-md-4"),
                          dbc.Col(children=[T_slider], className="col-md-8")]),
        html.Br(),
        dbc.Row(children=[dbc.Col(children=["CO2 partial pressure to equilibrate with [ppm]:"], className="col-md-4"),
                          dbc.Col(children=[CO2_slider], className="col-md-8")]),
        html.Br(),
        dbc.Row(children=[dbc.Col(children=["Total Alkalinity [ueq/L] log10(TA) :"], className="col-md-4"),
                          dbc.Col(children=[alkalinity_slider], className="col-md-8")]),
        html.Div(id='slider-output-container'),
        html.Br(),
        html.Br(),
        dcc.Graph(id='indicator-graphic'),
        
        
        
        #stuff for another diagram
# =============================================================================
#         dbc.Row(children=[dbc.Col(children=["Temp [°C]"], className="col-md-4"),
#                           dbc.Col(children=[T_slider2], className="col-md-8")]),
#         dcc.Graph(id='temperature'),
# =============================================================================
        html.Br(),
        html.B('This is the resulting speciation after the system is in Equilibrium with the atmosphere:'),
        html.Br(),
        html.Br(),
        
        html.Table([
        #html.Tr(['species]
        html.Tr([html.Td(['CO2(aq)= ']), html.Td(id='CO2_species'), html.Td("[umol/l]")   ]  ),
        html.Tr([html.Td(['HCO3- = ']), html.Td(id='HCO3_species'), html.Td("[umol/l]") ]),
        html.Tr([html.Td(['CO3-2 = ']), html.Td(id='CO3_species'), html.Td("[umol/l]") ]),
        html.Tr([html.Td(['Na+   = ']), html.Td(id='Na_species'), html.Td("[umol/l]") ]),
        html.Tr([html.Td(['H+    = ']), html.Td(id='H_species'), html.Td("[umol/l]") ]),
        html.Tr([html.Td(['OH-  =   ']), html.Td(id='OH_species'), html.Td("[umol/l]") ]),
        ]),
        html.Br(),
        html.Br(),
        
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
@app.callback(Output('slider-output-container','children'),
              Output("indicator-graphic", "figure"),
              Output("CO2_species","children"),
              Output("HCO3_species","children"),
              Output("CO3_species","children"),
              Output("Na_species","children"),
              Output("H_species","children"),
              Output("OH_species","children"),
              
              [Input("T_input", "value"),
               Input("CO2_input", "value"),
               Input("alkalinity_input", "value")]
              ) 





def update_graph(T,pCO2,alkalinity):
    
    
    # because of the log10 scale of the alkalinity slider
    alk=10**(alkalinity)
    
    #convert umol/L concentartion in mmol/L  
    c=alk*1e-3

    sol=pp.add_solution_simple({'NaHCO3':c},temperature=T) # in Phreeqc default units are mmol/kgw
    
    
    # the pressure default unit is atm so I convert the ppm to atm
    p=pCO2*1e-6
    
    #if pCO2!=0:
    
    #here I have to check what to use for pressure
    CO2=pp.add_gas({'CO2(g)':p}, pressure=p , fixed_pressure=True)


    # reaction with ambient CO2 pressure
    sol.interact(CO2)
    
    

    #plotly command for plots
    # very simple plot that already works 
    #fig= px.line(x=np.linspace(0, 10, 1000),y=T*np.linspace(0, 10, 1000))
    
    #line break in plotly strings <br>
    
    #marker_color defines the different bar colors (it can be also dependent on paramameters, continiuos or distinct)
    # the numbers refer to different colors ( I dont know the exact colors)
    
    fig = make_subplots(rows=1, cols=3, subplot_titles=('Inorganic carbon components <br> in the solution','DIC(T,CO2_atm,pH)',
                                                        "Fractions of <br> DIC(T,CO2_atm,pH)"),column_widths=[0.3, 0.2, 0.5])
    
    # all possible layout settings
    # https://plotly.com/python/reference/layout/
    
    fig.update_layout(
            font_family="Courier New",
            font_size=20,
            font_color="black",
            title_font_family="Courier New",
            title_font_size=29,
            title_font_color="red",
            legend_title_font_color="green",
            height=800, # global plot height
            width=1700,
            title_text="Equilibrium Solution for Freshwater"
            
            )
    

    #
    x_bar=['DIC',r'$HCO_{3_{aq}}^{-1}$','$CO_{3_{aq}}^{-2}$','$CO_{2_{aq}}$']
    
    
    # a=sol.total('HCO3')

    #b=sol.total('CO3')

    #c=sol.total('CO2')

    #get the total dissolved inorganc carbon
    #sol.total_element('C', units='mmol')
    
    
    # print(solution.species['HCO3-'])
    # everything in umol/l
    
    y_bar=[sol.total_element('C', units='mmol')*1000,sol.total('HCO3')*1000,sol.total('CO3')*1000,sol.total('CO2')*1000]
    
    water_type=['freshwater']  # here one can add freshwater etc if it would be interesting in this case
    
    fig.add_trace(go.Bar(name=x_bar[3], x=water_type, y=[y_bar[3]]),row=1, col=1) 
    
    fig.add_trace(go.Bar(name=x_bar[1], x=water_type, y=[y_bar[1]]),row=1, col=1)
    
    fig.add_trace(go.Bar(name=x_bar[2], x=water_type, y=[y_bar[2]]),row=1, col=1)
              
   
    
    # Change the bar mode
    fig.update_layout(barmode='stack')
    
    #to see the very big differences I use a logarithmic scale
    # Update xaxis properties  for just the first plot
    fig.update_yaxes(title_text="concentration [umol/L]", row=1, col=1)
    
    # attention range is in log so 10^0  to 10^6
    
    
    
    
     # DIC 
    fig.add_trace(go.Bar(name=x_bar[0], x=['DIC'], y=[y_bar[0]]),row=1, col=2) 
    fig.update_yaxes(range=[0,10000],row=1, col=2)
   
    
    
   
   # input is the array and then it is defined which columns are x and y
   
    fig.add_trace(go.Scatter(x=lines['pH'],y=lines['CO2_frac'],  mode='lines+markers',name='CO2aq' ),row=1, col=3)
    fig.add_trace(go.Scatter(x=lines['pH'],y=lines['HCO3_frac'], mode='lines+markers',name='HCO3aq' ),row=1, col=3)
    fig.add_trace(go.Scatter(x=lines['pH'],y=lines['CO3_frac'], mode='lines+markers',name='CO3aq'),row=1, col=3)
    fig.add_trace(go.Scatter(x=lines['pH'], y=lines['CO3_frac'], mode='lines+markers', name='CO3aq'), row=1, col=3)
    
    
    fig.update_yaxes(title_text="Fraction in decimal ",title_standoff =4, ticksuffix='', row=1, col=3)
    
    fig.update_xaxes(title_text="pH", row=1, col=3)
    
    #pH of the solution
    pH=sol.pH
    
    # electrical conductivity of the solution
    # SC
	

    # Specific conductance, microsiemens per centimeter. 
    SC=sol.sc
    
    
    
    # Add shapes
    fig.update_layout(
            shapes=[
                    #draw a shape in the third plot   
                    #the reference is the second xref yref
                    dict(type="line", xref="x3", yref='y3',
                              x0=pH, y0=0, x1=pH, y1=1),])
    
    fig.add_annotation(x=12, y=0.7,
            text="pH={:.2f} <br> EC={:.2f} uS/cm".format(pH,SC),
            showarrow=False,
            yshift=1,row=1, col=3)
    
    #get the concentrations of all the  species in the system
    # 
    cCO2=sol.species['CO2']*1e+6
    cHCO3=sol.species['HCO3-']*1e+6
    cCO3=sol.species['CO3-2']*1e+6
    cNa=sol.elements['Na']*1e+6
    cH=sol.species['H+']*1e+6
    cOH=sol.species['OH-']*1e+6
    
    
    #fig.update_layout(height=600, width=800, title_text=r"$\alpha Simulation of Dissolved Carbon Dioxide <br> (assume open system in equilibrium) <br> <br>$")

    #it is not possible to add latex in interactive dash

    #the ouputs are arranged in the way like the app.callback function defines them
    # the order has to be followed strictly
    # here i have added c = alkalinity
    return 'You have selected TA={:.2f} [ueq/L]'.format(alk),fig,"{:.3f}".format(cCO2),"{:.3f}".format(cHCO3),"{:.3f}".format(cCO3),"{:.3f}".format(cNa),"{:.3f}".format(cH),"{:.3f}".format(cOH)

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
