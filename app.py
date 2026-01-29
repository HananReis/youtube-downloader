from flask import Flask, render_template, abort

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/page/<name>')
def page(name):
    mapping = {
        'index': 'index.html',
        'modelos': 'paginas/modelos.html',
        'informacoes': 'paginas/informacoes.html',
        'contato': 'paginas/contanto.html'
    }
    template = mapping.get(name)
    if not template:
        abort(404)
    # Renderizar template (que estende base.html) mas extrair apenas o conteúdo
    html = render_template(template)
    # Extrair conteúdo do <main>
    from html.parser import HTMLParser
    class MainExtractor(HTMLParser):
        def __init__(self):
            super().__init__()
            self.in_main = False
            self.content = []
            self.main_found = False
        
        def handle_starttag(self, tag, attrs):
            if tag == 'main':
                self.in_main = True
                self.main_found = True
        
        def handle_endtag(self, tag):
            if tag == 'main':
                self.in_main = False
        
        def handle_data(self, data):
            if self.in_main:
                self.content.append(data)
    
    extractor = MainExtractor()
    extractor.feed(html)
    
    if extractor.main_found and extractor.content:
        return ''.join(extractor.content)
    return html

if __name__ == "__main__":
    app.run(debug=True)
