import pytest

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected", [
    (8, 3, 11),
    (10, 3, 13),
    (2, 2, 4)

])


def test_add(num1, num2, expected):
    print('testing add function')
    summ = num1 + num2
    assert summ == expected  

class InsufficientFunds(Exception):
    pass

class BankAccount:
    def __init__(self, starting_balance=0):
        self.balance = starting_balance

    def deposit(self, amount):
        self.balance += amount
    
    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFunds('Insufficient Funds')
        self.balance -= amount
    
    def interest(self, amount):
        self.balance *= 1.1

def test_bank_account_initial_amount(bank_account):
    assert bank_account.balance == 50

def test_initial_bank_value(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_deposit(bank_account):
    bank_account.deposit(30)
    assert bank_account.balance == 80

@pytest.mark.parametrize("deposited, withdrawn, expected", [
    (200, 100, 100),
    (400, 200, 200),
    (500, 100, 400)
])

def test_bank_transation(zero_bank_account, deposited, withdrawn, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrawn)
    zero_bank_account.balance == expected

def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)