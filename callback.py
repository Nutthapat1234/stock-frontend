from datetime import datetime, timedelta
import pandas as pd
import dash_table
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from app import app, cache
import plotly.graph_objs as go
import component.intervalTab
from config import prediction_interval, show_prediction, standard_pattern, focus_range, pattern_name, predict_trend, \
    except_interval, path

from page import realTimePage, predictionPage, backTestPage, stockInfoPage, aboutPage, notFoundPage
from service import Service

TIMEOUT = 60 * 60
stock_stage = None


@app.callback(
    [Output(f"{path[i][1:]}", "active") for i in range(len(path))],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False, False, False
    return [pathname == f"{path[i]}" for i in range(len(path))]


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", path[0]]:
        return realTimePage.component
    elif pathname == path[1]:
        return predictionPage.component
    elif pathname == path[2]:
        return backTestPage.component
    elif pathname == path[3]:
        return stockInfoPage.component
    elif pathname == path[4]:
        return aboutPage.component
    # If the user tries to reach a different page, return a 404 message
    return notFoundPage.generateNotFound(f"The pathname {pathname} was not recognised...")


@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab"),
     Input("stock-variable", "value"),
     Input("chart-variable", "value"), ]
)
def render_real_time_tab_content(active_tab, stock, chartType):
    if stock and chartType:
        if active_tab in except_interval and chartType == "Candlestick":
            return notFoundPage.generateNotFound(f"No avaliable Candle-Stick graph for {active_tab} time interval")
        service = Service.getInstance()
        result = service.getGraph(stock, active_tab, chartType)
        figure = None
        if chartType == "Scatter":
            figure = go.Scatter(x=result["x"], y=result["y"], mode="lines")
        elif chartType == "Candlestick":
            figure = go.Candlestick(x=result["start"],
                                    open=result["open"],
                                    high=result["high"],
                                    low=result["low"],
                                    close=result["close"])

        return dbc.Container(
            [dcc.Graph(
                id="live-graph",
                figure=go.Figure(
                    data=[figure],
                    layout=go.Layout(
                        height=600,
                        xaxis={
                            # 'range': [min(focus[-20:]), max(focus[-20:])],
                            'rangeslider': {'visible': True},
                        },
                    ),
                )),
                dcc.Interval(
                    id='graph-update',
                    interval=60 * 1000
                ), ],
        )
    else:
        return dcc.Graph(figure=go.Figure(
            data=[go.Scatter(x=[], y=[], mode="lines")],
            layout=go.Layout(
                height=600
            )
        ))


@app.callback(Output('live-graph', 'figure'),
              [Input('graph-update', 'n_intervals'),
               Input("tabs", "active_tab"),
               Input("stock-variable", "value"),
               Input("chart-variable", "value"), ],
              [State('live-graph', 'figure')])
def update_graph_scatter(i, interval, stock, chartType, figure):
    if i and interval == "1m":
        x = figure['data'][0]['x']
        y = figure['data'][0]['y']
        result = Service.getInstance().getGraph(stock, interval, chartType)
        if result['x'][-1] == x[-1]:
            print('No change', result['x'][-1])
            return figure
        print(result['x'][-1], result['y'][-1])
        x.append(result['x'][-1])
        y.append(result['y'][-1])
        return go.Figure(
            data=[go.Scatter(x=x, y=y, mode="lines")],
            layout=go.Layout(
                height=600
            )
        )
    return figure


@app.callback(
    Output("prediction-graph", "children"),
    [Input("stock-prediction-variable", "value")]
)
def render_prediction_graph(stock):
    global stock_stage
    stock = stock or stock_stage

    @cache.memoize(timeout=TIMEOUT)
    def compute_graph(stock):
        if stock:
            container = []
            for interval in prediction_interval:
                result = Service.getInstance().getGraph(stock, interval, "Scatter")
                x = result["x"]
                y = result["y"]

                all_point = go.Scatter(x=x, y=y, mode="lines", showlegend=False)
                last_ten = go.Scatter(x=x[-10:], y=y[-10:], mode=result["mode"], name="last 10 point")
                container.append(html.H3("Prediction " + stock + " for " + interval))

                buttons = []
                data = []
                number = 0
                active = 0
                active_name = ""
                active_value = None
                active_color = None
                # for example
                output = Service.getInstance().getPrediction("stock", y[-10:])
                possible_value = max(output)
                for index in range(13):
                    show = False
                    if index == 0:
                        name = "original"
                        button_name = "original"
                        data = [all_point, last_ten]
                    else:
                        name = "pattern " + str(index) + " " + pattern_name[index] + " " + str(
                            round(output[number])) + "%"
                        button_name = "pattern " + str(index) + " " + str(round(output[number])) + "%"
                        if number < len(output) and output[number] == possible_value:
                            active_name = name
                            active = number + 1
                            if round(output[number]) > 90:
                                if active_name in predict_trend["up"]:
                                    active_value = "This stock tend to be up"
                                    active_color = "success"
                                else:
                                    active_value = "This stock tend to be down"
                                    active_color = "danger"
                            else:
                                active_value = "The similarity of pattern is less than 90%, this stock is currently in unknown trend"
                                active_color = "dark"
                            show = True
                        label_name = "pattern " + str(index)
                        normalized_value = normalize(max(y[-10:]), min(y[-10:]), standard_pattern[number])
                        data.append(
                            go.Scatter(x=x[-10:], y=normalized_value, mode="lines+markers",
                                       name=label_name,
                                       visible=show,
                                       )
                        )
                        number += 1
                    buttons.append(dict(
                        label=button_name,
                        method="update",
                        args=[
                            {"visible": show_prediction[index],
                             "title": name,
                             "annotations": []}]), )

                fig = go.Figure(
                    data=data,
                    layout=go.Layout(
                        title=active_name,
                        height=600,
                        width=1050,
                        yaxis={
                            'range': [min(y[-20:]) - 5, max(y[-20:]) + 5]
                        },
                        xaxis={
                            'range': [datetime.fromisoformat(min(x[-15:])[:-1]) - timedelta(days=focus_range[interval]),
                                      datetime.fromisoformat(max(x[-15:])[:-1]) + timedelta(days=focus_range[interval])

                                      ],
                        },
                    ),
                )
                fig.update_layout(
                    updatemenus=[
                        dict(
                            type="buttons",
                            direction="down",
                            active=active,
                            x=1.4,
                            y=1.1,
                            buttons=list(buttons),
                        )
                    ])
                container.append(
                    dbc.Row(
                        [
                            dbc.Alert(id="alert",
                                      children="From the most percentage of similar pattern: " + active_value,
                                      color=active_color,
                                      style={"width": "100%"})
                        ]
                    )
                )
                container.append(
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dcc.Graph(figure=fig)
                                ]
                            ),
                        ],
                    ),
                )
            return container, stock

    if stock:
        container, stock_stage = compute_graph(stock)
        print(stock_stage)
        return container


@app.callback(Output("callback-temp", "children"), [Input('prediction-cache', 'n_intervals')])
def delete_cache(n):
    if n == 0:
        return
    cache.clear()


@app.callback(
    Output("backTest-graph", "children"),
    [Input("stock-backTest-variable", "value")]
)
def render_backTest_graph(stock):
    global stock_stage
    stock = stock or stock_stage

    @cache.memoize(timeout=TIMEOUT)
    def compute_graph(stock):
        if stock:
            result = Service.getInstance().getBackTest(stock)
            x_value = result["x"]
            y_value = result["y"]
            data_set = {}
            graphs = []
            for element in result["label"]:
                if element["pattern"] not in data_set:
                    data_set[element["pattern"]] = {"x_value": [], "y_value": [], "pattern": element["pattern"]}
                index = element["index"]
                start_index = -index - 9
                end_index = -index + 1
                if end_index == 0:
                    end_index = len(y_value)
                data_set[element["pattern"]]["x_value"] += x_value[start_index:end_index]
                data_set[element["pattern"]]["x_value"] += [None]
                data_set[element["pattern"]]["y_value"] += y_value[start_index:end_index]
                data_set[element["pattern"]]["y_value"] += [None]

            for pattern in sorted(data_set):
                pattern = data_set[pattern]
                if pattern["pattern"] in predict_trend["up"]:
                    value = "This stock tend to be up"
                    color = "success"
                else:
                    value = "This stock tend to be down"
                    color = "danger"

                data = [go.Scatter(x=x_value, y=y_value, mode="lines", name=stock),
                        go.Scatter(x=pattern["x_value"], y=pattern["y_value"], mode="lines+markers",
                                   name="Pattern " + str(pattern["pattern"]))]
                fig = go.Figure(data=data)
                graphs.append(
                    html.H3(
                        stock + " Pattern " + str(pattern["pattern"]) + " (" + pattern_name[pattern["pattern"]] + ")"))
                graphs.append(dbc.Alert(
                    children="From the principle in pattern " + str(pattern["pattern"]) + " :" + value,
                    color=color,
                    style={"width": "100%"}))
                graphs.append(dcc.Graph(figure=fig))
                graphs.append(html.Br())

            return graphs, stock

    if stock:
        graphs, stock_stage = compute_graph(stock)
        return graphs


@app.callback(
    Output('image', 'src'),
    [Input('stock_dropdown', 'value')])
def update_image_src(value):
    global stock_stage
    value = value or stock_stage
    stock_stage = value
    if value == 'AAPL':
        return "assets/APPL.png"
    elif value == 'FB':
        return "assets/FACEBOOK.png"
    elif value == 'GOOGL':
        return "assets/GOOGAL.jpg"
    elif value == 'SBUX':
        return "assets/SBUX.png"
    elif value == 'TRUE_BK':
        return "assets/TRUE.png"
    elif value == 'BDMS_BK':
        return "assets/BDMS.png"
    elif value == 'CPALL_BK':
        return "assets/CP.jpg"
    elif value == 'LPN_BK':
        return "assets/LPN.jpg"
    elif value == 'WHA_BK':
        return "assets/WHA.png"
    elif value == 'MSFT':
        return "assets/MSFT.png"


@app.callback(
    Output('dd-output-container', 'children'),
    [Input('stock_dropdown', 'value')])
def update_output(value):
    global stock_stage
    value = value or stock_stage
    stock_stage =value
    if value == 'AAPL':
        return "Apple Inc. is engaged in designing, manufacturing and marketing mobile communication and media devices, personal computers, and portable digital music players. The Company's products and services include iPhone, iPad, Mac, iPod, Apple TV, a portfolio of consumer and professional software applications, the iOS and Mac OS X operating systems, iCloud, and a range of accessory, service and support offerings. It sells its products worldwide through its online stores, its retail stores, its direct sales force, third-party wholesalers, and resellers. Apple Inc. is headquartered in Cupertino, California."
    elif value == 'FB':
        return "Facebook Inc. operates a social networking website worldwide. The Company's products for users are free of charge and available on the Web, mobile Web, and mobile platforms, such as Android and iOS. Its website enables users to connect, share, discover, and communicate with each other. The Facebook Platform is a set of tools and application programming interfaces that developers can use to build social apps on Facebook or to integrate their Websites with Facebook. It offers products that enable advertisers and marketers to engage with its users. Facebook Inc. is headquartered in Menlo Park, California."
    elif value == 'GOOGL':
        return "Alphabet Inc. is engaged in technology business. The Company provides web-based search, advertisements, maps, software applications, mobile operating systems, consumer content, enterprise solutions, commerce and hardware products through its subsidiaries. Alphabet Inc., formerly known as Google Inc., is headquartered in Mountain View, California."
    elif value == 'SBUX':
        return "Starbucks Corporation, together with its subsidiaries, operates as a roaster, marketer, and retailer of specialty coffee worldwide. The company operates in three segments: Americas; International; and Channel Development. Its stores offer coffee and tea beverages, roasted whole bean and ground coffees, single-serve and ready-to-drink beverages, and iced tea; and various food products, such as pastries, breakfast sandwiches, and lunch items. The company also licenses its trademarks through licensed stores, and grocery and foodservice accounts. It offers its products under the Starbucks, Teavana, Seattle's Best Coffee, Evolution Fresh, Ethos, Starbucks Reserve, and Princi brand names. As of October 30, 2019, the company operated approximately 31,000 stores. Starbucks Corporation was founded in 1971 and is based in Seattle, Washington."
    elif value == 'TRUE_BK':
        return "True Corporation Public Company Limited, together with its subsidiaries, engages in the telecommunications and diversified communications industries in Thailand. The company operates through TrueMove H, TrueOnline, and TrueVisions segments. It offers telephone, mobile, broadband Internet, Wi-Fi, and television and digital platforms. The company is also involved in entertainment, mobile equipment lessor, program production, non-government telecommunication, artist management and related, and marketing management activities. In addition, it operates news channel; and provides business solutions, online digital media services on website and telecommunication devices, distribution center services, consultancy and management services related to logistics, advertising sale and agency services, wireless telecommunication services, football club and related activities management services. Further, the company operates as a content provider; produces and distributes movie films; designs, develops, produces, and sells software products; and offers hospitality technology, as well as business process outsourcing services in technical service, marketing, and customer relations. The company was formerly known as TelecomAsia Corporation Public Company Limited and changed its name to True Corporation Public Company Limited in April 2004. True Corporation Public Company Limited was founded in 1990 and is headquartered in Bangkok, Thailand"
    elif value == 'BDMS_BK':
        return "Bangkok Dusit Medical Services Public Company Limited, together with its subsidiaries, operates hospitals in Thailand and internationally. The company owns and manages hospital groups, including Bangkok Hospital, Samitivej Hospital, BNH Hospital, Phyathai Hospital, Paolo Memorial Hospital, and Royal Hospital. It operates regenerative and preventive wellness clinics. In addition, it operates hotels; distributes cosmetic goods; provides accounting, health insurance, laboratory services, investment, information technology, training, insurance brokerage, air transportation, and property management services, as well as asset management services; and manufactures, distributes, and retails medicine and pharmaceutical products. The company has 47 hospitals in Thailand and Cambodia. Bangkok Dusit Medical Services Public Company Limited was founded in 1969 and is based in Bangkok, Thailand."
    elif value == 'CPALL_BK':
        return "CP ALL Public Company Limited, together with its subsidiaries, operates and franchises convenience stores under the 7-Eleven name to other retailers primarily in Thailand. It operates through three segments: Convenience Stores, Cash and Carry, and Other. The company is involved in the manufacture and sale of convenience and frozen foods, and bakery products; sale and maintenance of retail equipment; information technology, as well as marketing and advertising activities; provision of research and development services; and cash and carry and e-commerce business, as well as operates as a life and accident insurance broker. It also distributes commercial cards and tickets, catalog merchandises, and equipment for retailing and software development; and offers bill payment collection, information technology, logistics, smart purse cards, investment, educational institution, human resources development, and training and business seminar services, as well as healthcare and medical specialist's consultation services. As of December 31, 2019, CP ALL Public Company Limited operated 11,712 stores. The company was formerly known as C.P. Seven Eleven Public Company Limited and changed its name to CP ALL Public Company Limited in 2007. CP ALL Public Company Limited was founded in 1988 and is headquartered in Bangkok, Thailand."
    elif value == 'LPN_BK':
        return "L.P.N. Development Public Company Limited and its affiliated companies carry on the business of real estate development aiming to sell and rent the developed projects, as offices and residential condominiums located in the Central Business District (CBD) of Bangkok and neighbouring provinces. These offices and residential condominiums initially developed are dominated by high-rise and huge buildings."
    elif value == 'WHA_BK':
        return "WHA Corporation Public Company Limited, together with its subsidiaries, develops, rents, and leases lands, buildings, factories, warehouses, and other properties in Thailand and internationally. The company operates through Domestic Real Estate Business, Power Business, Water Business, Other Domestic Business, and Overseas Real Estate Business segments. It develops and manages properties in industrial estates and industrial zones. The company also provides raw water, portable water, and clarifies water; wastewater treatment services; and maintenance services to industrial estate customers, such as power plants, steel mills, and automotive and petrochemical industries. In addition, the company operates power projects; and provides digital services, data center, Internet connection, and other IT services. WHA Corporation Public Company Limited was founded in 2003 and is headquartered in Muang Samut Prakan, Thailand."
    elif value == 'MSFT':
        return "Microsoft Corporation develops, licenses, and supports software, services, devices, and solutions worldwide. Its Productivity and Business Processes segment offers Office, Exchange, SharePoint, Microsoft Teams, Office 365 Security and Compliance, and Skype for Business, as well as related Client Access Licenses (CAL); Skype, Outlook.com, and OneDrive; LinkedIn that includes Talent and marketing solutions, and subscriptions; and Dynamics 365, a set of cloud-based and on-premises business solutions for small and medium businesses, large organizations, and divisions of enterprises. Its Intelligent Cloud segment licenses SQL and Windows Servers, Visual Studio, System Center, and related CALs; GitHub that provides a collaboration platform and code hosting service for developers; and Azure, a cloud platform. It also provides support services and Microsoft consulting services to assist customers in developing, deploying, and managing Microsoft server and desktop solutions; and training and certification to developers and IT professionals on various Microsoft products. Its More Personal Computing segment offers Windows OEM licensing and other non-volume licensing of the Windows operating system; Windows Commercial, such as volume licensing of the Windows operating system, Windows cloud services, and other Windows commercial offerings; patent licensing; Windows Internet of Things; and MSN advertising. It also provides Microsoft Surface, PC accessories, and other intelligent devices; Gaming, including Xbox hardware, and Xbox software and services; video games and third-party video game royalties; and Search, including Bing and Microsoft advertising. It sells its products through distributors and resellers; and directly through digital marketplaces, online stores, and retail stores. It has strategic partnerships with Humana Inc., Nokia, Telkomsel, Swiss Re, Kubota Corporation, and FedEx Corp. The company was founded in 1975 and is headquartered in Redmond, Washington."


@app.callback(
    Output(component_id='income_table', component_property='children'),
    [Input(component_id='stock_dropdown', component_property='value')]
)
def update_table(stock_dropdown):
    global stock_stage
    stock_dropdown = stock_dropdown or stock_stage
    stock_stage = stock_dropdown
    if stock_dropdown:
        if stock_dropdown == 'AAPL':
            df = pd.read_csv('./assets/APPLEINC1.csv')
        elif stock_dropdown == 'FB':
            df = pd.read_csv('./assets/FB1.csv')
        elif stock_dropdown == 'GOOGL':
            df = pd.read_csv('./assets/GOOG1.csv')
        elif stock_dropdown == 'SBUX':
            df = pd.read_csv('./assets/SBUX1.csv')
        elif stock_dropdown == 'TRUE_BK':
            df = pd.read_csv('./assets/TRUE1.csv')
        elif stock_dropdown == 'BDMS_BK':
            df = pd.read_csv('./assets/BDMS1.csv')
        elif stock_dropdown == 'CPALL_BK':
            df = pd.read_csv('./assets/CP1.csv')
        elif stock_dropdown == 'LPN_BK':
            df = pd.read_csv('./assets/LPN1.csv')
        elif stock_dropdown == 'WHA_BK':
            df = pd.read_csv('./assets/WHA1.csv')
        elif stock_dropdown == 'MSFT':
            df = pd.read_csv('./assets/MSFT1.csv')

        return dash_table.DataTable(
            data=df.to_dict('records')
            , columns=[{"name": i, "id": i} for i in df.columns]
            , style_table={
                'height': '600px',
                'width': '1090px'
            },
            style_cell={
                'fontFamily': 'Open Sans',
                'textAlign': 'center',
                'height': '30px',
                'padding': '0px 5px',
                'whiteSpace': 'inherit',

            }

        )


@app.callback(
    Output(component_id='stakeholder_table', component_property='children'),
    [Input(component_id='stock_dropdown', component_property='value')]
)
def update_table2(stock_dropdown):
    global stock_stage
    stock_dropdown = stock_dropdown or stock_stage
    stock_stage = stock_dropdown
    if stock_dropdown:
        if stock_dropdown == 'AAPL':
            df = pd.read_csv('./assets/APPLEINC2.csv')
        elif stock_dropdown == 'FB':
            df = pd.read_csv('./assets/FB2.csv')
        elif stock_dropdown == 'GOOGL':
            df = pd.read_csv('./assets/GOOG2.csv')
        elif stock_dropdown == 'SBUX':
            df = pd.read_csv('./assets/SBUX2.csv')
        elif stock_dropdown == 'TRUE_BK':
            df = pd.read_csv('./assets/TRUE2.csv')
        elif stock_dropdown == 'BDMS_BK':
            df = pd.read_csv('./assets/BDMS2.csv')
        elif stock_dropdown == 'CPALL_BK':
            df = pd.read_csv('./assets/CP2.csv')
        elif stock_dropdown == 'LPN_BK':
            df = pd.read_csv('./assets/LPN2.csv')
        elif stock_dropdown == 'WHA_BK':
            df = pd.read_csv('./assets/WHA2.csv')
        elif stock_dropdown == 'MSFT':
            df = pd.read_csv('./assets/MSFT2.csv')

        return dash_table.DataTable(
            data=df.to_dict('records')
            , columns=[{"name": i, "id": i} for i in df.columns]
            , style_table={
                'height': '600px',
                'width': '1090px'
            },
            style_cell={
                'fontFamily': 'Open Sans',
                'textAlign': 'center',
                'height': '30px',
                'padding': '0px 5px',
                'whiteSpace': 'inherit',

            }

        )


def normalize(max_scale, min_scale, data):
    max_scale = max_scale
    min_scale = min_scale
    max_value = max(data)
    min_value = min(data)
    output = []
    for element in data:
        output.append(min_scale + ((element - min_value) * (max_scale - min_scale)) / (max_value - min_value))

    return output
