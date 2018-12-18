from flask import Flask, render_template, redirect, url_for, request, flash, session, make_response
from pymongo import MongoClient
from forms import Studreg, Studlog, Teachlog, Teachreg, tupd, Supd, tcours, sdown, scours, tasses, sansup, tansdo, Labreg, marks, sviewrep
import bcrypt
from gridfs import GridFS
from bson import ObjectId
import json
import socket
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b36e44b9f68e5e32fe9f5d1be56c561e'


client = MongoClient('mongodb://localhost:27017/')
db = client["labman"]

"""
mylist = [
  {"SubjectID": "CSE2004", "Subjname": "Database Management System"},
  {"SubjectID": "CSE1011", "Subjname": "Cryptography Fundamentals"},
  {"SubjectID": "CSE2005", "Subjname": "Operating Systems"},
  {"SubjectID": "MAT2001", "Subjname": "Statistics for Engineers"}
]
x = subj.insert_many(mylist)
"""
grid_fs = GridFS(db)

@app.route('/', methods=['GET','POST'])
def home():
     return render_template('Home.html',title='Welcome to Lab Management System!')



@app.route('/slogin',methods=['GET','POST'])
def slog():
    if 'username' in session:
        regno = session['username']
        return redirect(url_for('studash',regno=regno))
    stdata = db.student_details
    form = Studlog()
    login_user = stdata.find_one({'regno' : form.RegNo.data})
    if request.method =='POST':
        if form.validate_on_submit():
            if login_user is not None:
                if bcrypt.checkpw((form.password.data).encode('utf-8'), (login_user["Password"])):
                    session['username'] = form.RegNo.data
                    return redirect(url_for('studash', regno=session['username']))

            flash('Login Unsuccessful!, Please Try Again!')
    return render_template('slogin.html', title='Student Login', form=form)


@app.route('/tlogin',methods=['GET','POST'])
def tlog():
    if 'username1' in session:
        admin = session['username1']
        return redirect(url_for('teachdash',admin=admin))
    teachdata = db.teacher_details
    form = Teachlog()
    login_user = teachdata.find_one({'FacultyID' : form.admin.data})
    if request.method =='POST':
        if form.validate_on_submit():
            if login_user is not None:
                if bcrypt.checkpw((form.password.data).encode('utf-8'), (login_user["password"])):
                    session['username1'] = form.admin.data
                    return redirect(url_for('teachdash', admin=session['username1']))
            flash('Login Unsuccessful!, Please Try Again')
    return render_template('tlogin.html', title='Teacher Login', form=form)


@app.route('/treg',methods=['GET', 'POST'])
def treg():
    teachdata = db.teacher_details
    form = Teachreg()
    if form.validate_on_submit():
        existing_teach = teachdata.find_one({'FacultyID': form.admin.data})
        if existing_teach is None:
            admin = form.admin.data
            name = form.name.data
            subject = form.subw.data
            hashpass = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt())
            post = {'FacultyID': admin, 'Name': name, 'password': hashpass, 'SubjectID':subject}
            postID = teachdata.insert_one(post).inserted_id
            flash('Teacher Account Created for' + str(form.name.data))
            return redirect(url_for('tlog'))
        flash('This Teacher already exists')
        return redirect(url_for('tlog'))
    return render_template('treg.html',title='Teacher Registration', form=form)


@app.route('/sreg',methods=['GET','POST'])
def sreg():
    stdata = db.student_details
    form = Studreg()
    if form.validate_on_submit():
        existing_stud = stdata.find_one({'regno' : form.RegNo.data})
        if existing_stud is None:
            regno = form.RegNo.data
            name = form.name.data
            sem = form.sem.data
            email = form.email.data
            addr = form.address.data
            ins={}
            if form.dbms.data==True:
                ins['CSE2004'] = 'Database Management System'
                db.dbms1.insert({'Students':regno})
            if form.crypto.data==True:
                ins['CSE1011'] = 'Cryptography Fundamentals'
                db.crypto1.insert({'Students': regno})
            if form.ops.data==True:
                ins['CSE2005'] = 'Operating Systems'
                db.os1.insert({'Students': regno})
            if form.stats.data==True:
                ins['MAT2001'] = 'Statistics for Engineers'
                db.stats1.insert({'Students': regno})
            subas=json.dumps(ins)
            contactno = form.contactno.data
            hashpass = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt())
            post = {'regno':regno, 'name':name,'sem':sem,'email':email,'address':addr,'contactno':contactno,'Subject':subas,'Password':hashpass}
            postID = stdata.insert_one(post).inserted_id
            if form.dbms.data == True:
                c1 = "CSE2004" + " Marks"
                db.student_details.update_one({'regno': form.RegNo.data},
                                              {'$set': {c1: []}})
            if form.crypto.data == True:
                c2 = "CSE1011" + " Marks"
                db.student_details.update_one({'regno': form.RegNo.data},
                                              {'$set': {c2: []}})
            if form.ops.data == True:
                c3 = "CSE2005" + " Marks"
                db.student_details.update_one({'regno': form.RegNo.data},
                                              {'$set': {c3: []}})
            if form.stats.data == True:
                c4 = "MAT2001" + " Marks"
                db.student_details.update_one({'regno': form.RegNo.data},
                                              {'$set': {c4: []}})

            flash('Student Account Created for ' + str(form.name.data))
            return redirect(url_for('slog'))
        flash('This Student Already Exists')

    return render_template('sreg.html', form=form, title='Register')

@app.route('/Labreg',methods=['GET','POST'])
def labreg():
    form = Labreg()
    if form.validate_on_submit():
        existing_lab = db.labs.find_one({'SubjectID': form.subw.data})
        if existing_lab is None:
            staff = form.staff.data
            labid = form.labid.data
            sname = form.sname.data
            subject = form.subw.data
            roomno = form.roomno.data
            post = {'staffid': staff, 'staffname': sname,'SubjectID': subject,'roomno':roomno,'labid':labid}
            postID = db.labs.insert_one(post).inserted_id
            flash('Lab Account Created for' + str(form.sname.data))
            return redirect(url_for('tlog'))
        flash('This lab already exists')
    return render_template("labreg.html",form=form)

@app.route('/labview')
def labview():
    ab = db.teacher_details.find({"FacultyID": session['username1']})
    for s in ab:
        hell = s['SubjectID']
    xz = db.labs.find({"SubjectID": hell})
    return render_template("labview.html",xz=xz)

@app.route('/pcinfo')
def pcinfo():
    hostname = socket.gethostname()
    IP = socket.gethostbyname(hostname)
    x =datetime.datetime.now()
    return render_template('pcinfo.html',IP=IP,x=x)

@app.route('/assignmarks',methods=['GET','POST'])
def assignmarks():
    form =marks()
    if form.validate_on_submit():
        a = db.teacher_details.find({'FacultyID': session['username1']})
        for x in a:
            temp = x['SubjectID']
        cv = temp + " Marks"
        p =db.student_details.find({'regno':form.RegNo.data})
        for x in p:
            gal = x[cv]
        if gal is None:
            db.student_details.update_one({'regno': form.RegNo.data},
                                {'$set': {cv: [{form.asse.data: form.mark.data}]}})
        else:
            gal.append({form.asse.data: form.mark.data})
            newmarklist = gal
            db.student_details.update_one({'regno': form.RegNo.data}, {'$set': {cv:newmarklist}})

        flash("Marks Assigned")
    return render_template('marks.html',form=form)


@app.route('/studash/')
@app.route('/studash/<regno>')
def studash(regno=None):
    stdata = db.student_details
    garuser = stdata.find_one({"regno":regno})
    if regno is None:
        flash('Please Login!')
        return redirect(url_for('home'))
    elif garuser is None:
        flash('Invalid User!, Please Login!')
        return redirect(url_for('home'))
    else:
        try:
            regno == session['username']
            return render_template('studpage.html', regno=regno)
        except KeyError:
            flash('You Have Been not Logged In')
            return redirect(url_for('slog'))

@app.route('/teachdash/')
@app.route('/teachdash/<admin>')
def teachdash(admin=None):
    teachdata = db.teacher_details
    garuser = teachdata.find_one({"FacultyID":admin})
    if admin is None:
        flash('Please Login!')
        return redirect(url_for('home'))
    elif garuser is None:
        flash('Invalid User!, Please Login!')
        return redirect(url_for('home'))
    else:
        try:
            admin == session['username1']
            return render_template('teachdash.html', admin=admin)
        except KeyError:
            flash('You Have Been not Logged In')
            return redirect(url_for('tlog'))

@app.route('/scourse',methods=['GET','POST','PUT'])
def scourse():
    form1 = scours()
    if form1.validate_on_submit():
        a=db.teacher_details.find({"SubjectID":form1.subw.data})
        for std in a:
            fid = std[form1.asse.data]
        return redirect(url_for('download', fileid=fid))

    return render_template('scourse.html', form1=form1)


@app.route('/tcourse', methods=['GET','POST','PUT'])
def tcourse():
    form1 = tcours()
    if form1.validate_on_submit():
        file = request.files[form1.fillet.name]
        a = grid_fs.put(file)
        if grid_fs.find_one(a) is not None:
            flash(file.filename)
            file_id = str(a)
            db.teacher_details.update_one({'FacultyID': session['username1']}, {'$set': {form1.asse.data: file_id}})
            flash('Upload Complete')
        else:
            flash('Error in Saving File')

    return render_template('tcourse.html', form1=form1)


@app.route('/tansdown',methods=['GET','POST'])
def tansdown():
    form1 = tansdo()
    if form1.validate_on_submit():
        b =form1.asse.data +form1.regno.data
        a = db.teacher_details.find({"FacultyID": session['username1']})
        for std in a:
            fid = std[b]
        return redirect(url_for('download', fileid=fid))
    return render_template('tansdown.html', form1=form1)


@app.route('/sanswerupload', methods=['GET', 'POST'])
def ansup():
    form1 = sansup()
    if form1.validate_on_submit():
        file = request.files[form1.fillet.name]
        a = grid_fs.put(file)
        if grid_fs.find_one(a) is not None:
            flash(file.filename)
            file_id = str(a)
            b =form1.asse.data + session['username']
            db.teacher_details.update_one({'SubjectID': form1.subw.data}, {'$set': {b: file_id}})
            flash('Upload Complete')
        else:
            flash('Error in Saving File')
    return render_template('ansup.html',form1=form1)

@app.route('/squestiondownload',methods=['GET','POST'])
def sqdown():
    form1 = sdown()
    if form1.validate_on_submit():
        a = db.teacher_details.find({"SubjectID": form1.subw.data})
        for std in a:
            fid = std[form1.asse.data]
        return redirect(url_for('download', fileid=fid))
    return render_template('squestion.html',form1=form1)


@app.route('/sviewprofile')
def sviewprofile():
    ab=db.student_details.find({"regno":session['username']})
    return render_template('sviewprofile.html', ab=ab)


@app.route('/tviewprofile')
def tviewprofile():
    ab = db.teacher_details.find({"FacultyID": session['username1']})
    return render_template('tviewprofile.html', ab=ab)


@app.route('/supdateprofile', methods=['GET','POST'])
def supdateprofile():
    form = Supd()
    if form.validate_on_submit():
        db.student_details.update_one({'regno': session['username']}, {'$set': {'Name': form.name.data}})
        hashpass = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt())
        db.student_details.update_one({'regno': session['username']}, {'$set': {'sem': form.sem.data}})
        db.student_details.update_one({'regno': session['username']}, {'$set': {'email': form.email.data}})
        db.student_details.update_one({'regno': session['username']}, {'$set': {'address': form.address.data}})
        db.student_details.update_one({'regno': session['username']}, {'$set': {'contactno': form.contactno.data}})
        db.student_details.update_one({'regno': session['username']}, {'$set': {'Password': hashpass}})
        flash('Update Successful!')
    return render_template('supateprof.html', form=form)


@app.route('/viewreports',methods=['GET','POST'])
def strep():
    form=sviewrep()
    if form.validate_on_submit():
        x = form.subw.data + " Marks"
        p = db.student_details.find({"regno":session['username']})
        for q in p:
            temp = q[x]
        x = range(len(temp))
        return render_template('sviewreports.html',temp=temp,form=form,x=x)

    return render_template('sviewreports.html',form=form)

@app.route('/tquesupload',methods=['GET','POST'])
def tquesupload():
    form1 = tasses()
    if form1.validate_on_submit():
        file = request.files[form1.fillet.name]
        a = grid_fs.put(file)
        if grid_fs.find_one(a) is not None:
            flash(file.filename)
            file_id = str(a)
            db.teacher_details.update_one({'FacultyID': session['username1']}, {'$set': {form1.asse.data: file_id}})
            flash('Upload Complete')
        else:
            flash('Error in Saving File')
    return render_template("tquestionupload.html", form1=form1)


@app.route('/tupdate', methods=['GET', 'POST'])
def tupdate():
    form = tupd()
    if form.validate_on_submit():
        db.teacher_details.update_one({'FacultyID':session['username1']}, {'$set':{'Name':form.name.data}})
        hashpass = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt())
        db.teacher_details.update_one({'FacultyID': session['username1']}, {'$set': {'password': hashpass}})
        flash('Update Successful!')
    return render_template('tupdateprof.html', form=form)

@app.route('/download/<fileid>')
def download(fileid):
    oid = ObjectId(fileid)
    grid_fs_file = grid_fs.find_one({'_id': oid})
    response = make_response(grid_fs_file.read())
    a = db.fs.files.find({'_id': oid})
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers["Content-Disposition"] = "attachment; filename={}".format(fileid)
    return response


@app.route('/slogout')
def slogout():
   session.pop('username', None)
   flash('You have been Logged Out!')
   return redirect(url_for('home'))


@app.route('/tlogout')
def tlogout():
   session.pop('username1', None)
   flash('You have been Logged Out!')
   return redirect(url_for('home'))



if __name__=="__main__":
    app.run(debug=True)