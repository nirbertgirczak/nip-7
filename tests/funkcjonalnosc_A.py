import pytest
from src.manager import Manager
from src.models import Parameters

default_parameters = Parameters(
    apartments_json_path='data/apartments.json',
    tenants_json_path='data/tenants.json',
    transfers_json_path='data/transfers.json',
    bills_json_path='data/bills.json'
)


def test_powinno_zwalidowac_poprawna_kwote_przelewu():
    manager = Manager(parameters=default_parameters)
    wynik = manager.validate_transfer_amount(amount=500, min_value=10, max_value=10000)
    assert wynik is True, "Prawidłowa kwota powinna zostać zaakceptowana."

def test_powinno_rzucic_value_error_gdy_kwota_zbyt_niska():
    manager = Manager(parameters=default_parameters)
    with pytest.raises(ValueError) as exc_info:
        manager.validate_transfer_amount(amount=5, min_value=10, max_value=10000)
    assert "zbyt niska" in str(exc_info.value).lower(), "Błąd powinien informować o zbyt niskiej kwocie."


def test_powinno_rzucic_value_error_gdy_kwota_zbyt_wysoka():
    manager = Manager(parameters=default_parameters)
    with pytest.raises(ValueError) as exc_info:
        manager.validate_transfer_amount(amount=15000, min_value=10, max_value=10000)
    assert "limit" in str(exc_info.value).lower() or "zbyt wysoka" in str(exc_info.value).lower()

@pytest.mark.parametrize("bledna_kwota", [0. -50, -0.01])
def test_powinno_rzucic_value_error_dla_ujemnych_i_zera(bledna_kwota):
    manager = Manager(parameters=default_parameters)
    with pytest.raises(ValueError):
        manager.validate_transfer_amount(amount=bledna_kwota, min_value=10, max_value=10000)
        
