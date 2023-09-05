from flask import Flask, render_template, request, session
from create_table import create_tables
import sqlite3

app = Flask(__name__)
app.secret_key = "ssg@21f2001399"

# Landing page route
@app.route("/")
def homepage():
    return render_template("homepage.html")

# Admin Login route
@app.route("/adminlogin")
def adminlogin():
    return render_template("adminlogin.html")

# User Login page route
@app.route("/login")
def login():
    return render_template("login.html")

# Register page route
@app.route("/register")
def register():
    return render_template("register.html")

#Route to add a new user:
@app.route("/adduser", methods = ['POST', 'GET'])
def adduser():
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']        

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO credentials (name, email, password) VALUES (?,?,?)",(name, email, password))

                con.commit()
                msg = "Record successfully added to database"
        except:
            con.rollback()
            msg = "Error in the INSERT"

        finally:
            con.close()
            return render_template('login.html',msg=msg)
                

#Route to verify a user:
@app.route("/verify", methods = ['POST', 'GET'])
def verify():
    if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']        

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("Select email,password FROM credentials WHERE email=? and password=?", (email, password))

                result = cur.fetchone()
                if email == "Admin1@admin.com" and password == "Admin1":
                    session['email'] = email
                    msg = "Admin Credentials Verified"
                    return render_template('admin.html',msg=msg)
                elif(result):
                    msg = "User Credentials Verified"
                    session['email'] = email
                    return render_template('user.html',msg=msg)
                else:
                    msg = "Wrong Credentials, please check again"  
                    return render_template('error.html',msg=msg)

            con.close()   


@app.route('/logout')
def logout():
    session.clear()
    msg = "You are logged out"
    return render_template('homepage.html',msg = msg) 


# Admin route
@app.route("/admin")
def admin():
    if 'email' in session:
        return render_template('admin.html', email=session['email'])
    else:
        msg = "Error in the starting session, please try logging in again"  
        return render_template('error.html',msg=msg)    

# Admin Categories
@app.route("/admincategories")
def admincategories():
    if 'email' in session:
       con = sqlite3.connect("database.db")
       con.row_factory = sqlite3.Row

       cur = con.cursor()
       cur.execute("SELECT rowid, * FROM category")

       rows = cur.fetchall()
       con.close()
       return render_template('admincategories.html', rows=rows)
    else:
        msg = "Error in the starting session, please try logging in again"  
        return render_template('error.html',msg=msg) 


# Admin Create Category
@app.route("/newcategory")
def newcategory():
    return render_template('newcategory.html')



# Add new category
@app.route("/addcategory", methods = ['POST', 'GET'])
def addcategory():
    if request.method == 'POST':
        try:
            cname = request.form['cname']
            cename = request.form['cename']
            cquantity = request.form['cquantity'] 
            unit = request.form['unit']   
            rate = request.form['rate']
            orignalquantity = request.form['cquantity']
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO category (cname, cename, cquantity, unit, rate, incart, orignalquantity) VALUES (?,?,?,?,?,0,?)",(cname, cename, cquantity, unit, rate, orignalquantity))
                
                con.commit()
                msg = "Record successfully added to database"
        except:
            con.rollback()
            msg = "Error in the INSERT"

        finally:
            con.close()
            return render_template('admin.html',msg=msg)
        

# Edit Route
@app.route("/edit", methods=['POST','GET'])
def edit():
    if request.method == 'POST':
        try:
            id = request.form['id']
            con = sqlite3.connect("database.db")
            con.row_factory = sqlite3.Row

            cur = con.cursor()
            cur.execute("SELECT rowid, * FROM category WHERE rowid = " + id)

            rows = cur.fetchall()
        except:
            id=None
        finally:
            con.close()
            return render_template("edit.html",rows=rows)
        

# Route used to execute the UPDATE statement on a specific record in the database
@app.route("/editrec", methods=['POST','GET'])
def editrec():
    if request.method == 'POST':
        try:
            rowid = request.form['rowid']
            cname = request.form['cname']
            cename = request.form['cename'] 
            unit = request.form['unit']   
            rate = request.form['rate'] 
            cquantity = request.form['cquantity'] 
            orignalquantity = request.form['cquantity']
            

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("UPDATE category SET cname=' "+cname+" ', cename=' "+cename+"', unit=' "+unit+"', rate=' "+rate+"', cquantity=' "+cquantity+"', orignalquantity=' "+orignalquantity+" ' WHERE rowid="+rowid)

                con.commit()
                msg = "Record successfully edited in the database"
        except:
            con.rollback()
            msg = "Error in the Edit: UPDATE scategory SET  cename=' "+cename+"', cquantity=' "+cquantity+"' WHERE rowid="+rowid

        finally:
            con.close()
            return render_template('admin.html',msg=msg)
        

# Route used to DELETE a specific record in the database    
@app.route("/delete", methods=['POST','GET'])
def delete():
    if request.method == 'POST':
        try:
            rowid = request.form['id']
            with sqlite3.connect('database.db') as con:
                    cur = con.cursor()
                    cur.execute("DELETE FROM category WHERE rowid="+rowid)

                    con.commit()
                    msg = "Record successfully deleted from the database"
        except:
            con.rollback()
            msg = "Error in the DELETE"

        finally:
            con.close()
            return render_template('admin.html',msg=msg)
        

# Route for summary:
@app.route("/summary")
def summary():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT rowid, * FROM category")

    rows = cur.fetchall()
    con.close()
    return render_template('summary.html', rows=rows)


# Route for User:
@app.route("/user")
def user():
    return render_template('user.html')


# Route for exploring categories:
@app.route("/explore")
def explore():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT rowid, * FROM category")

    rows = cur.fetchall()
    con.close()
    return render_template('explore.html', rows=rows)


#filter in cart:
@app.route("/filter", methods=['POST','GET'])
def filter():
    cfilter = request.form['cfilter']
    pfilter = request.form['pfilter']
    
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT rowid, cname, cename, unit, rate, cquantity, incart FROM category WHERE rate = ? AND cname = ?", (pfilter,cfilter))

    rows = cur.fetchall()
    return render_template('filter.html', rows=rows)
        
        


# Adding in Cart:
@app.route("/add", methods=['POST','GET'])
def add():
    if request.method == 'POST':
        try:
            rowid = request.form['id']
            cquantity = request.form['cquantity'] 
            incart = request.form['incart']  
            orignalquantity = request.form['orignalquantity']   

            
            con = sqlite3.connect('database.db')
            cur = con.cursor()
            cur.execute("UPDATE category SET cquantity=cquantity - 1, incart=incart + 1 WHERE rowid="+rowid)
            msg = "Record successfully edited in the database" 
            con.commit()
            con.close()
            return render_template('explore.html',msg=msg)           
            

        except:
            msg = "You can't add this, it's not available" 
            return render_template('explore.html',msg=msg) 
           
              
# Deleting in Cart:
@app.route("/deleteitem", methods=['POST','GET'])
def deleteitem():
    if request.method == 'POST':
        try:
            rowid = request.form['id']  
            cquantity = request.form['cquantity'] 
            incart = request.form['incart'] 
            orignalquantity = request.form['orignalquantity']   

            if(orignalquantity == cquantity):
                msg = "You can't delete if you haven't selected anything!!!"       
                return render_template('explore.html',msg=msg)                    

            else:
                con = sqlite3.connect('database.db')
                cur = con.cursor()
                cur.execute("UPDATE category SET cquantity=cquantity + 1, incart=incart - 1 WHERE rowid="+rowid)
                msg = "Record successfully edited in the database" 
                con.commit()
                con.close()
                return render_template('explore.html',msg=msg)
                            
    
        except:
            msg = "Error in the Edit: UPDATE category" 
            return render_template('explore.html',msg=msg)               

# Route for cart:
@app.route("/cart")
def cart():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT rowid, cname, cename, unit, rate, incart FROM category WHERE incart >= 1")

    rows = cur.fetchall()
    total_cost = sum(row["rate"] * row["incart"] for row in rows)
    con.close()
    return render_template('cart.html', rows=rows, total_cost=total_cost)


# Route for checkout:
@app.route("/checkout", methods=['POST','GET'])
def checkout():
    if request.method == 'POST':
        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("UPDATE category SET  incart=incart - incart  WHERE incart >= 1")
                msg = "Thankyou for Shopping !!!"                

                con.commit()
                
        except:
            con.rollback()
            msg = "Error in the Edit:"

        finally:
            con.close()
            return render_template('user.html', msg = msg)
        

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
        
  