import os
import pytest
import requests


def test_transform_endpoint():
    url = os.getenv("TRANSFORM_SERVICE_URL", "http://localhost:5000/transform")
    output_epsg = os.getenv("TEST_OUTPUT_EPSG", "3857")
    zip_path = os.getenv("TEST_ZIP_PATH", "samples/RGN_DEC_1921_EW_BGA.zip")

    if not os.path.exists(zip_path):
        raise ValueError(
            "TEST_ZIP_PATH environment variable is not set. Please add and set a zip containing a .shp, .shx, .dbf, and .prj file"
        )

    with open(zip_path, "rb") as zip_file:
        files = {"file": ("RGN_DEC_1921_EW_BGA.zip", zip_file, "application/zip")}
        data = {"output_epsg": output_epsg}
        response = requests.post(url, files=files, data=data)

        # Assert HTTP status code
        assert (
            response.status_code == 200
        ), "Expected status code 200, but got {}".format(response.status_code)

        # Assert response structure
        assert (
            "incoming_epsg" in response.json()
        ), "Response body does not contain 'incoming_epsg'"
        assert (
            "outgoing_epsg" in response.json()
        ), "Response body does not contain 'outgoing_epsg'"
        assert (
            "coordinates" in response.json()
        ), "Response body does not contain 'coordinates'"


if __name__ == "__main__":
    pytest.main()
