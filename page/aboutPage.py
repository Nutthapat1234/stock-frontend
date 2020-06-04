import dash_html_components as html
import dash_bootstrap_components as dbc

component = dbc.Container(
    [
       
        html.Div([
        html.H1("Elliot Wave"),
        html.Br(),

        html.Div([
        html.P("Elliott wave is the pattern that provides clues about what will happen next in the market. "
            "The Elliot wave pattern consists of an impulse wave and correction wave, the impulse wave then "
            "are subdivided into 5 waves labeled as wave 1, wave 2, wave 3, wave 4, and wave 5. Three of the waves"
            " move in the impulse direction and another two move in the retracements direction of the impulse wave, there are three rules for motive wave that must be satisfied:"),
        html.P("1.) Wave 2 always retrace less than 100% of wave 1.", style = {'text-indent': '50px'}),
        html.P("2.) Wave 4 always retrace less than 100% of wave 3.", style = {'text-indent': '50px'}),
        html.P("3.) Wave 3 always travels beyond the end of wave 1 and never be the shortest wave.", style = {'text-indent': '50px'}),
        html.P("The corrective waves are subdivided into 3 structures mostly labeled as wave A, wave B, and wave C. Which two of them (A, C) are moving in impulse direction and one of them (B) move in retracement direction. There is only one rule for corrective waves to be satisfied."),
        html.P("1.) Wave B ends noticeably lower than where wave A starts.", style = {'text-indent': '50px'}),
        html.P("The Elliott wave is complete with the combination of Impulse wave and Corrective wave.")
        ,
        html.Img(src="assets/Wave.png", style={'height':'20%', 'width':'50%','textAlign': 'center', 'margin-left': 'auto','margin-right': 'auto', 'display': 'block'})
        
    ]),
  
])
    
   ,html.Div([
    html.Br(),
    html.H1("12 Pattern of Elliot Wave"),
    html.Div( html.Img(src="assets/Pattern1.png", style={'width':'33%','display': 'table','float':'left','padding':'5px'})), 
    html.Div( html.Img(src="assets/Pattern2.png", style={'width':'33%','display': 'table','float':'left','padding':'5px'})),
    html.Div( html.Img(src="assets/Pattern3.png", style={'width':'33%','display': 'table','float':'left','padding':'5px'})), 
    html.Div( html.Img(src="assets/Pattern4.jpg", style={'width':'33%','display': 'table','float':'left','padding':'5px'})), 
    html.Div( html.Img(src="assets/Pattern5.png", style={'width':'33%','display': 'table','float':'left','padding':'5px'})), 
    html.Div( html.Img(src="assets/Pattern6.png", style={'width':'33%','display': 'table','float':'left','padding':'5px'})),
    html.Div( html.Img(src="assets/Pattern7.png", style={'width':'33%','display': 'table','float':'left','padding':'5px'})), 
    html.Div( html.Img(src="assets/Pattern8.png", style={'width':'33%','display': 'table','float':'left','padding':'5px'})), 
    html.Div( html.Img(src="assets/Pattern9.png", style={'width':'33%','display': 'table','float':'left','padding':'5px'})), 
    html.Div( html.Img(src="assets/Pattern10.png", style={'width':'33%','display': 'table','float':'left','padding':'5px'})),
    html.Div( html.Img(src="assets/Pattern11.png", style={'width':'33%','display': 'table','float':'left','padding':'5px'})), 
    html.Div( html.Img(src="assets/Pattern12.png", style={'width':'33%','display': 'table','float':'left','padding':'5px'})), 

])

          
    ]
)
