from app.models import Occurrences
from sqlalchemy import extract, func
from datetime import datetime
from app.models import Occurrences, OccurrencesSchema
from app import db
import locale

def add_occurrence(form,location):

        tipos_manifestacao = {
            "denuncia": "",
            "contaminacao": form.data["valorcontaminacao"],
            "visita": form.data["valorvisita"]
        }

        valtipomanifest = tipos_manifestacao[form.data["tipomanifest"]]

        nova_ocorrencia = Occurrences(
        name=form.data["nome"],
        create_date= datetime.now(),
        email=form.data["email"],
        tel=form.data["tel"],
        tipomanifest=form.data["tipomanifest"],
        valortipomanifest=valtipomanifest,
        cep=form.data["cep"],
        rua=location["rua"],
        numero=form.data["numero"],
        bairro=location["bairro"],
        lat=location["lat"],
        long=location["long"]
)
        db.session.add(nova_ocorrencia)
        db.session.commit()

def filter_occurrences_data(query, bairro=None):

    q_contaminados = query.filter(Occurrences.tipomanifest == "contaminacao")
    q_denuncias = query.filter(Occurrences.tipomanifest == "denuncia")
    q_visitas = query.filter(Occurrences.tipomanifest == "visita")

    def count_occurrences(query, filter_value):
        return query.filter(Occurrences.valortipomanifest == filter_value).count()
    

    def get_bairros(query):
        bairros = []
        
        results = query.with_entities(Occurrences.bairro).distinct().all()

        for result in results:
            bairros.append(result[0])

        return bairros

    def bairros_com_mais_denuncias(query,qtdbairros):
        bairros = {}

        results = query.with_entities(Occurrences.bairro, func.count(Occurrences.bairro)).group_by(Occurrences.bairro).order_by(func.count(Occurrences.bairro).desc()).limit(qtdbairros).all()

        for result in results:
            bairros[result[0]] = result[1]

        return bairros
    
    def ruas_com_mais_denuncias(query,qtdruas):
        ruas = {}

        results = query.with_entities(Occurrences.rua, func.count(Occurrences.rua)).group_by(Occurrences.rua).order_by(func.count(Occurrences.rua).desc()).limit(qtdruas).all()

        for result in results:
            ruas[result[0]] = result[1]

        return ruas
    
    def get_total_occurrences_by_month(query, year=None, filter_value=None):
        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
        current_year = datetime.now().year

        if filter_value:
            query = query.filter(Occurrences.valortipomanifest == filter_value)

        if year:
            current_month = 12
        else:
            current_month = datetime.today().month

        q_occurrences_current_year = query.filter(extract('year', Occurrences.create_date) == current_year)

        occurrences_by_month = {}

        for month in range(1, current_month+1):
            occurrences = q_occurrences_current_year.filter(extract('month', Occurrences.create_date) == month).count()

            month_name = datetime.strptime(str(month), '%m').strftime('%b')

            occurrences_by_month[month_name] = occurrences

        return occurrences_by_month

    bairroOrRua = {}
    if bairro == None:
        bairroOrRua["bairros"] = bairros_com_mais_denuncias(q_denuncias, 5)
    else:
        bairroOrRua["ruas"] = ruas_com_mais_denuncias(q_denuncias, 5)

    return {
        "ocorrencias": {
            "total": query.count(),
            "meses": get_total_occurrences_by_month(query),
        },
        "bairros": get_bairros(query),
        "contaminados": {
            "total": q_contaminados.count(),
            "dengue": {
                "total": count_occurrences(q_contaminados, "dengue"),
                "meses": get_total_occurrences_by_month(q_contaminados, filter_value="dengue"),
            },
            "zika": {
                "total": count_occurrences(q_contaminados, "zika"),
                "meses": get_total_occurrences_by_month(q_contaminados, filter_value="zika"),
            },
            "chikungunya": {
                "total": count_occurrences(q_contaminados, "chikungunya"),
                "meses": get_total_occurrences_by_month(q_contaminados, filter_value="chikungunya"),
            },
            "febreamarela": {
                "total": count_occurrences(q_contaminados, "febreamarela"),
                "meses": get_total_occurrences_by_month(q_contaminados, filter_value="febreamarela"),
            },
        },
        "visitas": {
            "total": q_visitas.count(),
            "tarde": count_occurrences(q_visitas, "tarde"),
            "manha": count_occurrences(q_visitas, "manha"),
        },
        "denuncias": {
            "total": q_denuncias.count(),
            **bairroOrRua,
        },
    }

def get_occurrences_bairros():
    return Occurrences.query.with_entities(Occurrences.bairro).distinct().all()

def get_occurrences_data(tipomanifest=None, bairro=None):
    occurrences_schema = OccurrencesSchema(many=True)
    
    query = Occurrences.query
    query = query.filter(Occurrences.tipomanifest == tipomanifest) if tipomanifest else query
    query = query.filter(Occurrences.bairro.ilike(f'%{bairro}%')) if bairro else query
    
    occurrences = query.all()

    occurrences_dict = occurrences_schema.dump(occurrences)
    occurrences_info = filter_occurrences_data(query, bairro)

    data = {
        "data"  : occurrences_dict,
        "occurrences_info"  : occurrences_info
    }

    return data