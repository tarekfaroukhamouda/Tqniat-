from flask import Flask,render_template,request,Response
import pandas
import requests
import json
from sklearn.impute import SimpleImputer
import numpy 
app=Flask(__name__)

@app.route("/")
def index():
    single_hotel={}
    all_hotel=[]
    #request for data from thetwo providers
    providerARequest = requests.get("http://www.mocky.io/v2/5e400f423300005500b04d0c")
    providerBRequest= requests.get("http://www.mocky.io/v2/5e4010ad3300004200b04d15")
    providerAdata=pandas.read_json(providerARequest.content)
    providerBdata=pandas.read_json(providerBRequest.content)
    #change the headersfrom provider A to  headerof Provider B so All be the same headers
    providerAdata = providerAdata.rename(columns={'Fare': 'Price', 'Hotel': 'hotelName','roomAmenities':'amenities'})
    #change the typepf rate from  ****  to number
    providerBdata['Rate']=providerBdata['Rate'].apply(lambda x:len(x))
    #combine the two dataframs
    frames = [providerAdata, providerBdata]
    result = pandas.concat(frames)
    #sorting the record accordint to Rate
    result=result.sort_values(by=['Rate'],ascending=False)
    #changing the discount value from Nan to no dicount 
    imputer = SimpleImputer(missing_values=numpy.nan, strategy='constant',fill_value="No Discount")
    imputer.fit(result.iloc[:, 1:5])
    result.iloc[:, 1:5] = imputer.transform(result.iloc[:, 1:5])
    #filling the dic from dataframe
    for hotelname,rate,price,amentities,discount in zip(result.iloc[:,0],result.iloc[:,1],result.iloc[:,2],result.iloc[:,3],result.iloc[:,4]):
        single_hotel['hotelname']=hotelname
        single_hotel['Rate']=rate
        #split the string value of amentities to array so all data to be array when send it so we check if its string or array
        if isinstance(amentities, str):
           
            single_hotel['amentities']=amentities.split()
        else:
            single_hotel['amentities']=amentities
        single_hotel['Price']=price
        single_hotel['discount']=discount
        all_hotel.append(single_hotel)
        single_hotel={}
    
    return Response(json.dumps(all_hotel))
if __name__=="__main__":
    app.debug=True
    app.run()

#just trying to understand github
