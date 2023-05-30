import os
import pytest
import requests

def test_transform_endpoint():
    url = os.getenv('TRANSFORM_SERVICE_URL', 'http://localhost:5000/transform')
    output_epsg = 3857  # or any EPSG code you want

    # Define the path of your zip file
    zip_path = 'samples/RGN_DEC_1921_EW_BGA.zip'

    with open(zip_path, 'rb') as zip_file:
        files = {'file': ('RGN_DEC_1921_EW_BGA.zip', zip_file, 'application/zip')}
        data = {'output_epsg': output_epsg}
        response = requests.post(url, files=files, data=data)

        # Assert HTTP status code
        assert response.status_code == 200, "Expected status code 200, but got {}".format(response.status_code)

        # Assert response structure
        assert 'incoming_epsg' in response.json(), "Response body does not contain 'incoming_epsg'"
        assert 'outgoing_epsg' in response.json(), "Response body does not contain 'outgoing_epsg'"
        assert 'coordinates' in response.json(), "Response body does not contain 'coordinates'"

if __name__ == "__main__":
    pytest.main()
