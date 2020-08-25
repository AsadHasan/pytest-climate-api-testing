"""Tests for World Bank's climate API
"""

import pytest
import requests
from requests.models import Response

from config import BASE_URL


@pytest.mark.parametrize(
    "data_type,gcm,var,start,end,country",
    [
        ("mavg", "bccr_bcm2_0", "pr", 2020, 2039, "gbr"),
        ("annualavg", "cccma_cgcm3_1", "tas", 1980, 1999, "pak"),
        ("manom", "gfdl_cm2_1", "pr", 2060, 2079, "ind"),
        ("annualanom", "mpi_echam5", "tas", 2080, 2099, "usa"),
    ],
)
def test_climate_api(
    data_type: str, gcm: str, var: str, start: int, end: int, country: str
) -> None:
    """Failure of this test implies that API does not
    return correct response for valid parameter permutations
    :rtype: None
    :param data_type: Types such as monthly average (mavg) etc
    :param gcm: Global circulation models
    :param var: Temperature (tas) or precipitation (pr)
    :param start: Start year
    :param end: End year
    :param country: ISO country code
    """
    path: str = f"{data_type}/{gcm}/{var}/{start}/{end}/{country}"
    url: str = f"{BASE_URL}/{path}"
    response: Response = requests.get(url)
    response.raise_for_status()
    json_response: dict = response.json()
    assert json_response != "Invalid request parameters"
    assert len(json_response) > 0
    for item in json_response:
        assert item["gcm"] == gcm
        assert item["variable"] == var
        assert item["fromYear"] == start
        assert item["toYear"] == end
