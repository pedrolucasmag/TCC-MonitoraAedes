from app import create_app
from app.models import User, Occurrences, db
from datetime import datetime

app = create_app()

def test_user_class():
    # Verifica se os atributos da classe User foram definidos corretamente
    from app.models import User
    assert hasattr(User, '__tablename__')
    assert hasattr(User, 'id')
    assert hasattr(User, 'name')
    assert hasattr(User, 'email')
    assert hasattr(User, 'password')
    assert callable(getattr(User, '__str__'))
    assert callable(getattr(User, 'toJSON'))

def test_user_creation():
    with app.app_context():
        db.session.query(User).filter_by(email="teste456@teste.com").delete()
        user = User(name="Fulano da Silva", email="teste456@teste.com", password="teste123")
        db.session.add(user)
        db.session.commit()
        assert user.id is not None
        assert user.name == "Fulano da Silva"
        assert user.email == "teste456@teste.com"
        assert user.password == "teste123"

# Verifica se os atributos da classe Occurences foram definidos corretamente
def test_occurrences_class():
    from app.models import Occurrences
    assert hasattr(Occurrences, '__tablename__')
    assert hasattr(Occurrences, 'id')
    assert hasattr(Occurrences, 'create_date')
    assert hasattr(Occurrences, 'name')
    assert hasattr(Occurrences, 'email')
    assert hasattr(Occurrences, 'tel')
    assert hasattr(Occurrences, 'tipomanifest')
    assert hasattr(Occurrences, 'valortipomanifest')
    assert hasattr(Occurrences, 'rua')
    assert hasattr(Occurrences, 'numero')
    assert hasattr(Occurrences, 'bairro')
    assert hasattr(Occurrences, 'cep')
    assert hasattr(Occurrences, 'lat')
    assert hasattr(Occurrences, 'long')
    assert callable(getattr(Occurrences, '__str__'))


def test_occurrence_creation():

    with app.app_context():
        occurrence = Occurrences(
            create_date=datetime.now(),
            name="Fulano da Silva",
            email="teste@example.com",
            tel="555-1234",
            tipomanifest="visita",
            valortipomanifest="tarde",
            rua="Rua A",
            numero=123,
            bairro="Bairro A",
            cep=12345,
            lat=-23.55,
            long=-46.64
        )
        db.session.add(occurrence)
        db.session.commit()

        # Verificar se a ocorrência foi criada corretamente
        assert occurrence.id is not None
        assert occurrence.create_date is not None
        assert occurrence.name == "Fulano da Silva"
        assert occurrence.email == "teste@example.com"
        assert occurrence.tel == "555-1234"
        assert occurrence.tipomanifest == "visita"
        assert occurrence.valortipomanifest == "tarde"
        assert occurrence.rua == "Rua A"
        assert occurrence.numero == 123
        assert occurrence.bairro == "Bairro A"
        assert occurrence.cep == 12345
        assert occurrence.lat == -23.55
        assert occurrence.long == -46.64