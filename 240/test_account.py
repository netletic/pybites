import pytest

from account import Account


@pytest.fixture
def jarno():
    return Account(owner="jarno")


@pytest.fixture
def rebecca():
    return Account(owner="rebecca", amount=10)


def test_balance(jarno):
    jarno.add_transaction(20)
    assert jarno.balance == 20


def test_exception(jarno):
    with pytest.raises(ValueError) as exc:
        jarno.add_transaction("string")
    assert str(exc.value) == "please use int for amount"


def test_str(jarno, rebecca):
    assert str(jarno) == "Account of jarno with starting amount: 0"
    assert str(rebecca) == "Account of rebecca with starting amount: 10"


def test_repr(jarno, rebecca):
    assert repr(jarno) == "Account('jarno', 0)"
    assert repr(rebecca) == "Account('rebecca', 10)"


def test_transactions(jarno):
    jarno.add_transaction(20)
    jarno.add_transaction(-10)
    jarno.add_transaction(50)
    jarno.add_transaction(-20)
    jarno.add_transaction(30)
    assert jarno.balance == 70


def test_len_and_getitem(jarno):
    jarno.add_transaction(-20)
    jarno.add_transaction(30)
    jarno.add_transaction(40)
    assert len(jarno) == 3
    assert jarno[1] == 30
    assert jarno[-1] == 40


def test_comparison(jarno, rebecca):
    assert rebecca > jarno
    assert jarno < rebecca
    jarno.add_transaction(30)
    assert rebecca < jarno
    assert rebecca <= jarno
    assert jarno > rebecca
    assert jarno >= rebecca


def test_equality(jarno, rebecca):
    assert jarno != rebecca
    jarno.add_transaction(10)
    assert jarno == rebecca
    assert not jarno > rebecca
    assert not rebecca > jarno
    assert not jarno < rebecca
    assert not rebecca < jarno


def test_merge_account(jarno, rebecca):
    jarno.add_transaction(10)
    joint_acc = jarno + rebecca
    assert joint_acc.owner == "jarno&rebecca"
    assert joint_acc.balance == 20
    rebecca.add_transaction(10)
    joint_acc2 = rebecca + jarno
    assert joint_acc2.owner == "rebecca&jarno"
    assert joint_acc2.balance == 30
