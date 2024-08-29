from flask import Flask , render_template,request,url_for,redirect
import joblib
import sqlite3


model=joblib.load("./models/linear_model.lb")

app=Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/feedback', methods=['GET'])
def feedback():
    return render_template('feedback.html')

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    name = request.form['name']
    email = request.form['email']
    feedback = request.form['feedback']
    
    # Process the feedback (e.g., save to database or send email)
    # Here, we'll just print it to the console
    print(f"Feedback received from {name} ({email}): {feedback}")
    
    return redirect(url_for('feedback'))


@app.route('/predict',methods=['GET','POST'])
def predict():
    if request.method=='POST':
        brand_name=int(request.form['brand_name'])
        Kms_Driven=int(request.form['Kms_Driven'])
        owner=int(request.form['owner'])
        age=int(request.form['age'])
        power=int(request.form['power'])
        
        brand_dict = {'Bajaj': 1,'Royal Enfield': 2,'Hero': 3,'Honda': 4,'Yamaha': 5,'TVS': 6,
                        'KTM': 7,'Suzuki': 8,'Harley-Davidson': 9,'Kawasaki': 10,'Hyosung': 11,
                        'Mahindra': 12,'Benelli': 13,'Triumph': 14,'Ducati': 15,'BMW': 16}

        brand_dict2={value:key for key,value in brand_dict.items()}
        print(brand_dict2)
        UNSEEN_DATA= [[Kms_Driven,owner,age,	power,brand_name]]

        PREDICTION=model.predict(UNSEEN_DATA)[0][0]
        # return str(round(PREDICTION))
        
        # post data into database
        query_to_insert="""
        Insert into BikeDetails values(?,?,?,?,?,?)
        """
        conn=sqlite3.connect('bikedata.db')
        cur=conn.cursor()
        data=(owner,brand_dict2[brand_name],Kms_Driven,power,age,int(round(PREDICTION,2)))
        cur.execute(query_to_insert,data)
        conn.commit()
        print("Your record has been stored in database")
        cur.close()
        conn.close()

        # return render_template('result.html',UNSEEN_DATA,prediction_text=str(round(PREDICTION,2)))
        return render_template('result.html', 
                           prediction_text=str(round(PREDICTION, 2)),
                           brand_name=brand_name,
                           Kms_Driven=Kms_Driven,
                           owner=owner,
                           age=age,
                           power=power)


if __name__=='__main__':
    app.run(debug=True)


