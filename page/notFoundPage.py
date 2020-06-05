import dash_html_components as html
import dash_dangerously_set_inner_html


def generateNotFound(text):
    return dash_dangerously_set_inner_html.DangerouslySetInnerHTML(f'''
        <div class="error-page">
            <div>
                <h1 data-h1="404">404</h1>
                <p data-p="NOT FOUND">{text}</p>
            </div>
        </div>
''')
