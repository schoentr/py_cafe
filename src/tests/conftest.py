from src.models import db as _db
from src.models import Manager, Customer, Employee, Order, OrderItems, Item, Reservation
from src import app as _app
import pytest
import os


@pytest.fixture()
def app(request):
    """ Session-wide testable Flask app """
    _app.config.from_mapping(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI=os.getenv('TEST_DATABASE_URL'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        WTF_CSRF_ENABLED=False
    )
    ctx = _app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return _app


@pytest.fixture()
def db(app, request):
    """ Session-wide test DB """

    _db.app = app
    _db.create_all()

    def teardown():
        _db.drop_all()
    request.addfinalizer(teardown)
    return _db


@pytest.fixture()
def session(db, request):
    """ Create new DB session for testing """
    connection = db.engine.connect()
    transaction = connection.begin()
    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)
    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()
    request.addfinalizer(teardown)

    return session


@pytest.fixture()
def client(app, db, session):
    """ Create test client """
    client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield client
    ctx.pop()


@pytest.fixture()
def customer(session):
    """ Create test user with customer role """
    customer = Customer(
        name='Milo',
        email='milo@test.com',
        password='12345',
        phone='123-456-7890'
    )
    session.add(customer)
    session.commit()
    return customer


@pytest.fixture()
def auth_customer(client, customer):
    client.post(
        '/login',
        data={'email': customer.email, 'password': '12345'},
        follow_redirects=True
    )
    return client


@pytest.fixture()
def manager(session):
    """ Create test user with manager role """
    manager = Manager(
        name='Tim',
        email='tim@test.com',
        password='12345'
    )
    session.add(manager)
    session.commit()
    return manager


@pytest.fixture()
def auth_manager(client, manager):
    client.post(
        '/login',
        data={'email': manager.email, 'password': '12345'},
        follow_redirects=True
    )
    return client


@pytest.fixture()
def employee(session):
    """ Create test employee """
    employee = Employee(
        name='Dan',
        email='dan@test.com',
        password='54321',
        pay_rate=10.50
    )
    session.add(employee)
    session.commit()
    return employee

@pytest.fixture()
def reservation(session):
    """ create test reservation """
    reservation = Reservation(
        date = '3/24/2019',
        time = '11:00 PM',
        party = 3
    )
    return reservation

@pytest.fixture()
def auth_employee(client, employee):
    client.post(
        '/login',
        data={'email': employee.email, 'password': '54321'},
        follow_redirects=True
    )
    return client


@pytest.fixture()
def items(session):
    """ Create test items """
    item2 = Item(
        name='Cheeseburger',
        price=8.50,
        cog=5.00,
        inventory_count=22
    )
    session.add(item2)
    item1 = Item(
        name='Biscuits and Gravy',
        price=9.50,
        cog=6.00,
        inventory_count=12
    )
    session.add(item1)
    session.commit()
    return [item1, item2]


@pytest.fixture()
def order(session, customer, employee, items):
    """ Create test order """
    order = Order(
        customer=customer,
        employee=employee,
        items=items,
    
    )
    session.add(order)
    session.commit()
    return order
