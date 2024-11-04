import json
import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models import db
from models.account import Account

ACCOUNT_DATA = {}

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Configura la base de datos antes y después de todas las pruebas"""
    # Se ejecuta antes de todas las pruebas
    db.create_all()
    yield
    # Se ejecuta después de todas las pruebas
    db.session.close()

class TestAccountModel:
    """Modelo de Pruebas de Cuenta"""

    @classmethod
    def setup_class(cls):
        """Conectar y cargar los datos necesarios para las pruebas"""
        global ACCOUNT_DATA
        with open('tests/fixtures/account_data.json') as json_data:
            ACCOUNT_DATA = json.load(json_data)
        print(f"ACCOUNT_DATA cargado: {ACCOUNT_DATA}")

    @classmethod
    def teardown_class(cls):
        """Desconectar de la base de datos"""
        pass  # Agrega cualquier acción de limpieza si es necesario

    def setup_method(self):
        """Truncar las tablas antes de cada prueba"""
        db.session.query(Account).delete()
        db.session.commit()

    def teardown_method(self):
        """Eliminar la sesión después de cada prueba"""
        db.session.remove()

    ######################################################################
    #  C A S O S   D E   P R U E B A
    ######################################################################

    def test_create_an_account(self):
        """Probar la creación de una sola cuenta"""
        data = ACCOUNT_DATA[0]  # obtener la primera cuenta
        account = Account(**data)
        account.create()
        assert len(Account.all()) == 1

    def test_create_all_accounts(self):
        """Probar la creación de múltiples cuentas"""
        for data in ACCOUNT_DATA:
            account = Account(**data)
            account.create()
        assert len(Account.all()) == len(ACCOUNT_DATA)
    
    def test_repr(self):
        # Arrange
        account = Account()
        # Act
        account.name = "Jared"
        # Assert
        assert str(account) == "<Account 'Jared'>"

    def test_to_dict(self):
        # Arrange
        account_data = ACCOUNT_DATA[0]
        account = Account(**account_data)
        result = account.to_dict()
        assert result["id"] == account.id
        assert result["name"] == account.name 
        assert result["email"] == account.email
        assert account.phone_number == result["phone_number"]
        assert account.disabled == result["disabled"]
        assert account.date_joined == result["date_joined"]

    def test_update(self):
        # Arrange
        account_data = ACCOUNT_DATA[1]
        account = Account(**account_data)
        account.create()
        assert account.id is not None
        account.name = "Pepito"
        account.update()
        updated_account = Account.find(account.id)
        assert updated_account.name == account.name