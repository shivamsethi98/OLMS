from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField,IntegerField,SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileField

class Studreg(FlaskForm):
    RegNo = StringField('RegistrationNo', validators=[DataRequired('A RegNo is required'), Length(min=9, max=9,message='RegNo must be of 9 Characters')])
    name = StringField('Name', validators=[DataRequired('A name is required')])
    sem = SelectField('Semester', choices=[('Semester-I','Semester-I'),('Semester-II','Semester-II'),('Semester-III','Semester-III'),('Semester-IV','Semester-IV'),('Semester-V','Semester-V'),('Semester-VI','Semester-VI'),('Semester-VII','Semester-VII'),('Semester-VIII','Semester-VIII')], validators=[DataRequired('Select One Subject')])
    email = StringField('Email', validators=[DataRequired('Please enter email!'),Email(message='Enter in correct format')])
    address = StringField('Address', validators=[DataRequired('Please enter address')])
    dbms=BooleanField('Database Management System',default='checked')
    crypto = BooleanField('Cryptography Fundamentals', default='checked')
    ops = BooleanField('Operating Systems', default='checked')
    stats = BooleanField('Statistics for Engineers', default='checked')
    contactno = StringField('Contactno', validators=[DataRequired('Enter in Correct Format'),Length(min=10,max=10,message='Contact No must be of 10 digits!.')])
    password = PasswordField('Password', validators=[DataRequired('Please Enter a Password!')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired('Please validate password!'), EqualTo('password',message='Password Does not match!')])
    submit = SubmitField('Register')

class Studlog(FlaskForm):
    RegNo = StringField('RegistrationNo', validators=[DataRequired('A RegNo is required'),Length(min=9, max=9, message='RegNo must be of 9 Characters')])
    password = PasswordField('Password',validators=[DataRequired('Enter Password!')])
    Submit = SubmitField('Log In')

class Teachlog(FlaskForm):
    admin = StringField('Faculty ID',validators=[DataRequired('A Faculty Id is required'),Length(min=5,max =5, message='A Faculty Id must consist of 5 characters!')])
    password = PasswordField('Password', validators=[DataRequired('Enter Password!')])
    Submit = SubmitField('Log In')

class Teachreg(FlaskForm):
    admin = StringField('Faculty ID', validators=[DataRequired('A Faculty Id is required'), Length(min=5, max=5,message='A Faculty Id must consist of 5 characters!')])
    subw = SelectField('Subject', choices=[('CSE2004', 'CSE2004-Database Management System'), ('CSE1011', 'CSE1011-Cryptography Fundamentals'), ('CSE2005', 'CSE2005-Operating Systems'), ('MAT2001', 'MAT2001-Statistics for Engineers')], validators=[DataRequired('Select One Subject')])
    name = StringField('Name', validators=[DataRequired('A name is required')])
    password = PasswordField('Password', validators=[DataRequired('Enter Password!')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired('Please validate password!'),EqualTo('password',message='Password Does not match!')])
    submit = SubmitField('Register')

class tupd(FlaskForm):
    name = StringField('Name', validators=[DataRequired('A name is required')])
    password = PasswordField('Password', validators=[DataRequired('Enter Password!')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired('Please validate password!'), EqualTo('password',message='Password Does not match!')])
    submit = SubmitField('Update')

class Supd(FlaskForm):
    #RegNo = StringField('RegistrationNo', validators=[DataRequired('A RegNo is required'),
     #                                                 Length(min=9, max=9, message='RegNo must be of 9 Characters')])
    name = StringField('Name', validators=[DataRequired('A name is required')])
    sem = SelectField('Semester', choices=[('Semester-I', 'Semester-I'), ('Semester-II', 'Semester-II'),
                                           ('Semester-III', 'Semester-III'), ('Semester-IV', 'Semester-IV'),
                                           ('Semester-V', 'Semester-V'), ('Semester-VI', 'Semester-VI'),
                                           ('Semester-VII', 'Semester-VII'), ('Semester-VIII', 'Semester-VIII')],
                      validators=[DataRequired('Select One Subject')])
    email = StringField('Email', validators=[DataRequired('Please enter email!'),Email(message='Enter in correct format')])
    address = StringField('Address', validators=[DataRequired('Please enter address')])
    contactno = StringField('Contactno', validators=[DataRequired('Enter in Correct Format'),Length(min=10,max=10,message='Contact No must be of 10 digits!.')])
    password = PasswordField('Password', validators=[DataRequired('Please Enter a Password!')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired('Please validate password!'), EqualTo('password',message='Password Does not match!')])
    submit = SubmitField('Update')

class tcours(FlaskForm):
    asse = SelectField('Course Materials', choices=[('Course-I', 'Course-I'), ('Course-II', 'Course-II'),
                                                    ('Course-III', 'Course-III'), ('Course-IV', 'Course-IV'),
                                                    ('Course-V', 'Course-V'), ('Course-VI', 'Course-VI'),
                                                    ('Course-VII', 'Course-VII'),
                                                    ('Course-VIII', 'Course-VIII')],
                       validators=[DataRequired('Select One Option')])
    fillet = FileField()
    submit = SubmitField('Submit')

class tasses(FlaskForm):
    asse = SelectField('Semester', choices=[('Assessment-I', 'Assessment-I'), ('Assessment-II', 'Assessment-II'),
                                           ('Assessment-III', 'Assessment-III'), ('Assessment-IV', 'Assessment-IV'),
                                           ('Assessment-V', 'Assessment-V'), ('Assessment-VI', 'Assessment-VI'),
                                           ('Assessment-VII', 'Assessment-VII'), ('Assessment-VIII', 'Assessment-VIII')],
                      validators=[DataRequired('Select One Subject')])
    fillet = FileField()
    submit = SubmitField('Submit')

class sdown(FlaskForm):
    asse = SelectField('Semester', choices=[('Assessment-I', 'Assessment-I'), ('Assessment-II', 'Assessment-II'),
                                            ('Assessment-III', 'Assessment-III'), ('Assessment-IV', 'Assessment-IV'),
                                            ('Assessment-V', 'Assessment-V'), ('Assessment-VI', 'Assessment-VI'),
                                            ('Assessment-VII', 'Assessment-VII'),
                                            ('Assessment-VIII', 'Assessment-VIII')],
                       validators=[DataRequired('Select One Subject')])

    subw = SelectField('Subject', choices=[('CSE2004', 'CSE2004-Database Management System'),
                                           ('CSE1011', 'CSE1011-Cryptography Fundamentals'),
                                           ('CSE2005', 'CSE2005-Operating Systems'),
                                           ('MAT2001', 'MAT2001-Statistics for Engineers')],
                       validators=[DataRequired('Select One Subject')])
    submit = SubmitField('Submit')

class marks(FlaskForm):
    def validate_marks(form, field):
        if int(field.data) > 50 or int(field.data) < 0:
            raise ValidationError('Marks must be in in 0 to 50!')
    asse = SelectField('Semester', choices=[('Assessment-I', 'Assessment-I'), ('Assessment-II', 'Assessment-II'),
                                            ('Assessment-III', 'Assessment-III'), ('Assessment-IV', 'Assessment-IV'),
                                            ('Assessment-V', 'Assessment-V'), ('Assessment-VI', 'Assessment-VI'),
                                            ('Assessment-VII', 'Assessment-VII'),
                                            ('Assessment-VIII', 'Assessment-VIII')],
                       validators=[DataRequired('Select One Subject')])
    RegNo = StringField('RegistrationNo', validators=[DataRequired('A RegNo is required'),
                                                      Length(min=9, max=9, message='RegNo must be of 9 Characters')])
    mark = StringField('Marks', validators=[DataRequired('Marks are required'), validate_marks])
    submit = SubmitField('Submit')

class scours(FlaskForm):
    asse = SelectField('Course Materials', choices=[('Course-I', 'Course-I'), ('Course-II', 'Course-II'),
                                            ('Course-III', 'Course-III'), ('Course-IV', 'Course-IV'),
                                            ('Course-V', 'Course-V'), ('Course-VI', 'Course-VI'),
                                            ('Course-VII', 'Course-VII'),
                                            ('Course-VIII', 'Course-VIII')],
                       validators=[DataRequired('Select One Option')])

    subw = SelectField('Subject', choices=[('CSE2004', 'CSE2004-Database Management System'),
                                           ('CSE1011', 'CSE1011-Cryptography Fundamentals'),
                                           ('CSE2005', 'CSE2005-Operating Systems'),
                                           ('MAT2001', 'MAT2001-Statistics for Engineers')],
                       validators=[DataRequired('Select One Subject')])
    submit = SubmitField('Submit')

class sansup(FlaskForm):
    asse = SelectField('Semester', choices=[('Assessment-I', 'Assessment-I'), ('Assessment-II', 'Assessment-II'),
                                           ('Assessment-III', 'Assessment-III'), ('Assessment-IV', 'Assessment-IV'),
                                           ('Assessment-V', 'Assessment-V'), ('Assessment-VI', 'Assessment-VI'),
                                           ('Assessment-VII', 'Assessment-VII'), ('Assessment-VIII', 'Assessment-VIII')],
                      validators=[DataRequired('Select One Subject')])
    subw = SelectField('Subject', choices=[('CSE2004', 'CSE2004-Database Management System'),
                                           ('CSE1011', 'CSE1011-Cryptography Fundamentals'),
                                           ('CSE2005', 'CSE2005-Operating Systems'),
                                           ('MAT2001', 'MAT2001-Statistics for Engineers')],
                       validators=[DataRequired('Select One Subject')])
    fillet = FileField()
    submit = SubmitField('Submit')

class tansdo(FlaskForm):
    regno = StringField('RegistrationNo', validators=[DataRequired('A RegNo is required'),
                                                      Length(min=9, max=9, message='RegNo must be of 9 Characters')])
    asse = SelectField('Semester', choices=[('Assessment-I', 'Assessment-I'), ('Assessment-II', 'Assessment-II'),
                                            ('Assessment-III', 'Assessment-III'), ('Assessment-IV', 'Assessment-IV'),
                                            ('Assessment-V', 'Assessment-V'), ('Assessment-VI', 'Assessment-VI'),
                                            ('Assessment-VII', 'Assessment-VII'),
                                            ('Assessment-VIII', 'Assessment-VIII')],
                       validators=[DataRequired('Select One Subject')])
    submit = SubmitField('Submit')

class Labreg(FlaskForm):
    staff=StringField('Staff ID', validators=[DataRequired('A Staff Id is required')])
    labid=StringField('Lab ID',validators=[DataRequired('A Labid needed'), Length(min=6,max =6, message='A lab Id must consist of 6 characters!')])
    sname=StringField('Staff Name', validators=[DataRequired('A Staff name is required')])
    subw = SelectField('Subject', choices=[('CSE2004', 'CSE2004-Database Management System'), ('CSE1011', 'CSE1011-Cryptography Fundamentals'), ('CSE2005', 'CSE2005-Operating Systems'), ('MAT2001', 'MAT2001-Statistics for Engineers')], validators=[DataRequired('Select One Subject')])
    roomno = StringField('Room no,', validators=[DataRequired('A Room no. is required')])
    submit = SubmitField('Submit')

class sviewrep(FlaskForm):
    subw = SelectField('Subject', choices=[('CSE2004', 'CSE2004-Database Management System'),
                                           ('CSE1011', 'CSE1011-Cryptography Fundamentals'),
                                           ('CSE2005', 'CSE2005-Operating Systems'),
                                           ('MAT2001', 'MAT2001-Statistics for Engineers')],
                       validators=[DataRequired('Select One Subject')])

    submit = SubmitField('Submit')