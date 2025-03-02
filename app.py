from flask import Flask, request, jsonify
import pandas as pd
from io import StringIO

app = Flask(__name__)


@app.route('/upload-csv', methods=['POST'])
def upload_csv():
    # Get the file from the request
    file = request.files['file']

    # Read the CSV data into a pandas DataFrame
    csv_data = file.read().decode('utf-8')
    df = pd.read_csv(StringIO(csv_data))

    # Process the dataframe (your custom logic here)
    # For now, just returning the CSV as JSON
    table = df.to_dict(orient='split')  # This is just an example to return as JSON

    return jsonify(table)


if __name__ == '__main__':
    app.run(debug=True)
