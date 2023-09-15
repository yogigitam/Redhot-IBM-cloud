from flask import Flask, request,render_template,session
import ibm_db


app = Flask(__name__)
 
app.secret_key="_ab+d=5"
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=fbd88901-ebdb-4a4f-a32e-9822b9fb237b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PWD=Iwt9vNbYJxxLXBPu;PORT=32731;UID=kmv72920;SECURITY=SSL;SSLCERTIFICATE=DigiCertGlobalRootCA.crt",'','')
print(conn)
print(ibm_db.active(conn))
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        global uname
        uname = request.form['username']
        pword = request.form['password']
        print(uname, pword)
        sql = "SELECT * FROM REGR WHERE UNAME = ? AND PASSWD = ?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt, 1, uname)
        ibm_db.bind_param(stmt,2,pword)
        ibm_db.execute(stmt)
        out = ibm_db.fetch_assoc(stmt)
        print(out)
        if out != False:
            session['UNAME'] = uname
            session['MAIL'] = out['MAIL']
            
            if out['ROLE'] == "Admin":
                return render_template("Adminprofile.html",adName = uname, adEmail = out['MAIL'] )
            elif out['ROLE'] == "Stude":
                return render_template("Studentprofile.html",stName = uname, stEmail = out['MAIL'])
            else: 
                return render_template("Facultyprofile.html",faName = uname, faEmail = out['MAIL'])
        else: 
            msg = "Invalid Credentials"
            return render_template("login.html",message1= msg)
    return render_template("login.html")


@app.route("/register", methods=['GET', 'POST'])
def regsiter():
    if request.method == "POST":
        name = request.form['NAME']
        email = request.form['MAIL']
        uname = request.form['UNAME']
        pword = request.form['PASSWD']
        role = request.form['ROLE']
        print(uname,email,pword,role,name)
        sql = "SELECT * FROM REGR WHERE UNAME=?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt, 1, uname)
        ibm_db.execute(stmt)
        out = ibm_db.fetch_assoc(stmt)
        print(out)
        if out != False:
            msg = "Already Registered"
            return render_template("registration1.html",message2 = msg)
        else:
            sql = "INSERT INTO REGR VALUES(?,?,?,?,?)"
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt, 1, name)
            ibm_db.bind_param(stmt, 2,email)
            ibm_db.bind_param(stmt, 3, pword)
            ibm_db.bind_param(stmt, 4, uname)
            ibm_db.bind_param(stmt, 5, role)
            ibm_db.execute(stmt)
            msg = "Registered"
            return render_template("registration1.html", message2 =msg)

    return render_template("registration1.html")






if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)
