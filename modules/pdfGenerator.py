import jinja2
import pdfkit
import os
from dotenv import load_dotenv

# crea un archivo .env para almacenar rutas de variables que puedan comprometer 
# nuestras privacidad
load_dotenv()

WKHTMLTOPDF_ROUTE = os.getenv('WKHTMLTOPDF_ROUTE')
PDF_ROUTE= os.getenv('PDF_ROUTE')
ROUTE_TEMPLATE= os.getenv('ROUTE_TEMPLATE')
ROUTE_CSS= os.getenv('ROUTE_CSS')

class ImportPDF:
    def create_pdf( info ):
        ruta_template = ROUTE_TEMPLATE
        rutacss = ROUTE_CSS
        nombre_template = ruta_template.split('/')[-1]
        ruta_template = ruta_template.replace(nombre_template, '')
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(ruta_template))
        template =  env.get_template(nombre_template)
        html = template.render(info)

        options = {
            'page-size' : 'Letter',
            'margin-top' : '0.05in',
            'margin-right': '0.05in',
            'margin-bottom' : '0.05in',
            'margin-left' : '0.05in',
            'encoding' : 'UFT-8'
        }

        # la ruta de variables cambia en que sistema operativo estas usando y donde hayas guardado el ejecutable para la extension
        config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_ROUTE)
        ruta_salida = PDF_ROUTE 
        pdfkit.from_string(html, ruta_salida, css=rutacss, options=options, configuration=config)

    # def initPDF(self, info):
    #     self.ruta_template = ROUTE_TEMPLATE
    #     self.rutacss = ROUTE_CSS
    #     self.__create_pdf(self.ruta_template, info, self.rutacss)