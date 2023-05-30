from flask import Flask, request, jsonify
import pyogrio

app = Flask(__name__)


@app.route("/transform", methods=["POST"])
def transform():
    """
    Endpoint for transforming geographic data from an input spatial reference
    system (EPSG) to an output EPSG specified in the form data.

    This function processes a .zip file containing the geographic data (.shp, .shx, .dbf,
    .prj, .cpg files) passed as an uploaded file. It leverages a recent feature in PyOGRIO
    that supports reading geographic data directly from an in-memory zip file. This
    eliminates the need to save the zip file to a temporary location before reading.

    The geographic data is read into a GeoDataFrame and then converted to the specified EPSG.

    The function returns a JSON object containing the EPSG of the input data, the EPSG
    of the transformed data, and the coordinates of the transformed polygon in GeoJSON format.

    Request Parameters:
    - 'file': a .zip file containing the geographic data.
    - 'output_epsg': the EPSG code for the desired output spatial reference system.

    Returns:
    - JSON object with:
        'incoming_epsg': EPSG code of the input spatial reference system,
        'outgoing_epsg': EPSG code of the transformed data,
        'coordinates': GeoJSON representation of the transformed polygon.

    Raises:
    - ValueError: if the required form parameters are missing or invalid.
    """

    # Ensure a file was uploaded
    if "file" not in request.files:
        raise ValueError("No file part in the request.")

    uploaded_file = request.files["file"]

    # Ensure a file was selected for upload
    if uploaded_file.filename == "":
        raise ValueError("No selected file.")

    # Load geographic data from uploaded file into GeoDataFrame
    try:
        geo_df = pyogrio.read_dataframe(uploaded_file)
    except Exception as e:
        raise ValueError(f"Failed to read data: {e}")

    # Retrieve EPSG of the input data
    input_epsg = geo_df.crs.to_epsg()

    # Retrieve desired output EPSG from form data
    if "output_epsg" not in request.form:
        raise ValueError("Missing 'output_epsg' in form data.")

    output_epsg = request.form["output_epsg"]

    # Transform the geographic data to the desired EPSG
    try:
        transformed_geo_df = geo_df.to_crs(epsg=output_epsg)
    except Exception as e:
        raise ValueError(f"Failed to transform EPSG: {e}")

    # Construct and return the JSON response
    response = {
        "incoming_epsg": input_epsg,
        "outgoing_epsg": output_epsg,
        "coordinates": transformed_geo_df.geometry.to_json(),
    }

    return jsonify(response)


@app.route("/status", methods=["GET"])
def status():
    """
    Endpoint for checking the liveness of the application.

    Returns:
    - A simple JSON object indicating that the application is running.
    """
    return jsonify({"status": "The application is running."})


if __name__ == "__main__":
    app.run(debug=True)
