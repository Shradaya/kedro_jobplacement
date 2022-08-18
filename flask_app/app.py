import numpy as np
from flask import Flask, request, jsonify
import mlflow
import json

file_name = 'run_id.json'

with open(file_name, 'r', encoding='utf-8') as f:
    run = json.loads(f.read())
    print(run)

logged_model = f"runs:/{run['run_id']}/model"
loaded_model = mlflow.pyfunc.load_model(logged_model)

# # Predict on a Pandas DataFrame.
# import pandas as pd
# loaded_model.predict(pd.DataFrame(data))

app = Flask(__name__)

# model_name = "modelA"
# loaded_model = mlflow.pyfunc.load_model(
#     model_uri=f"models:/{model_name}/latest"
# )

def mapper(value):
    map ={
        0:'Placed',
        1:'Not Placed'
    }
    return map[value]

@app.route('/api',methods=['POST'])
def predict():
    data = request.get_json(force=True)
    to_predict = []
    for input in data.values():
        to_predict.append(int(input))
    result = loaded_model.predict([to_predict])
    prediction = mapper(result[0])
    
    return {
            "data" : data,
            "prediction": prediction
            }
    

# if __name__ == '__main__':
#     app.run(port=5000, debug=True)

