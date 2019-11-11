from flask import Flask,request
from flask_restful import Resource,Api
from sklearn.externals import joblib
import pandas as pd

app=Flask(__name__)
api=Api(app)

class Test_index(Resource):
    def post(self):
        loaded_model = joblib.load('./model/test_model')
        test_data=request.get_json()
        input_df=pd.DataFrame([test_data])
        input_df.rename(columns={"input_lstat":'LSTAT',"input_rm":'RM'},inplace=True)
        print(input_df)
        y_train_predict = loaded_model.predict(input_df)
        test_output=pd.DataFrame(y_train_predict,columns={'output'})
        output=test_output.to_dict(orient="list")
        return output

api.add_resource(Test_index,"/test")
if __name__=='__main__':
    app.run(debug=True)
