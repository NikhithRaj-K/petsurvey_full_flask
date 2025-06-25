from flask import Flask, render_template, request, url_for, redirect, flash, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from functools import wraps
from dotenv import load_dotenv
from os import environ
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
from flask_migrate import Migrate


load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = environ.get('APP_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(UserDetails, user_id)


class UserDetails(UserMixin, db.Model): # user table schema
    userid:   Mapped[str] = mapped_column(String(30), primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(100))
    email:    Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    phone:    Mapped[str] = mapped_column(String(15), unique=True, nullable=False)

    def get_id(self):
        return self.userid

class UserResponses(db.Model):  # user_response table schema
    id:        Mapped[int] = mapped_column(Integer, primary_key=True)
    userid:    Mapped[str] = mapped_column(String(50), ForeignKey("user_details.userid"), nullable=False)
    useremail: Mapped[str] = mapped_column(String(50))
    question1: Mapped[str] = mapped_column(String(50))
    question2: Mapped[str] = mapped_column(String(500))
    question3: Mapped[str] = mapped_column(String(50))
    question4: Mapped[str] = mapped_column(String(50))
    question5: Mapped[str] = mapped_column(String(500))
    question6: Mapped[str] = mapped_column(String(500))
    question7: Mapped[str] = mapped_column(String(500))
    question8: Mapped[str] = mapped_column(String(500))
    question9: Mapped[str] = mapped_column(String(500))
    question10: Mapped[str] = mapped_column(String(500))
    question11: Mapped[str] = mapped_column(String(500))

    def to_dict(self):
        return {
            "id": self.id,
            "userid": self.userid,
            "useremail": self.useremail,
            "question1": self.question1,
            "question2": self.question2,
            "question3": self.question3,
            "question4": self.question4,
            "question5": self.question5,
            "question6": self.question6,
            "question7": self.question7,
            "question8": self.question8,
            "question9": self.question9,
            "question10": self.question10,
            "question11": self.question11,
        }


class AdminDetails(UserMixin, db.Model):
    id       : Mapped[int] = mapped_column(Integer, primary_key=True)
    email    : Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password : Mapped[str] = mapped_column(String(100), nullable=False)


with app.app_context():
    db.create_all()


def nocache(view): #browser cache settings
    @wraps(view)
    def no_cache_view(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Cache-Control'] = 'no-store, no-cache,must-revalidate, private, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    return no_cache_view

@app.route('/signup', methods=["GET", "POST"])
@nocache
def signup():
    if request.method == "POST":

        email = request.form.get('email')
        result = db.session.execute(db.select(UserDetails).where(UserDetails.email == email))
        latest_user = db.session.execute(db.select(UserDetails).order_by(UserDetails.userid.desc())).scalars().first()
        user = result.scalar()

        if user: # if user exists...
            flash("You've already signed up with that email, sign in instead!")
            return redirect(url_for('signin'))

        if latest_user:
            latest_uid_num = int(latest_user.userid.replace("UID", ""))
            next_uid = f"UID{latest_uid_num + 1:03d}"

        else:
            next_uid = "UID001"

        hash_and_salted_password = generate_password_hash(request.form.get('password'),
                                                          method='pbkdf2:sha256',
                                                          salt_length=8)

        new_user = UserDetails(userid=next_uid,
                        username=request.form.get('username'),
                        email=request.form.get('email'),
                        password=hash_and_salted_password,
                        phone=request.form.get('phone'),
                        )
        db.session.add(new_user)
        db.session.commit()
        flash('Signup successful! Please login.', 'success')

        return redirect(url_for("signin"))
    return render_template("signup.html", logged_in=current_user.is_authenticated)

@app.route('/', methods=["GET", "POST"])
@nocache
def signin():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        result = db.session.execute(db.select(UserDetails).where(UserDetails.email == email))
        user = result.scalar()

        # Email doesn't exist or password incorrect.
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('signin'))
        elif not check_password_hash(user.password, password):
            flash("Password is incorrect, please try again.")
            return redirect(url_for('signin'))
        else:
            login_user(user)
            return redirect(url_for('home'))

    return render_template("signin.html")

@app.route('/home', methods=["GET", "POST"])
@nocache
@login_required
def home():
    if request.method == "POST":
        current_user_email = current_user.email
        current_user_uid = current_user.userid

        question1 = request.form.get('answer1')
        question2 = ', '.join(request.form.getlist('answer2')) # multi select with others
        other_q2  = request.form.get('other_q2')
        question3 = request.form.get('answer3')
        question4 = request.form.get('answer4') # toggle option with others
        other_q4 = request.form.get('other_q4')
        question5 = ', '.join(request.form.getlist('answer5')) # multi select with others
        other_q5  = request.form.get('other_q5')
        question6 = request.form.get('answer6') # toggle option with others
        other_q6  = request.form.get('other_q6')
        question7 = request.form.get('answer7') # toggle option with others
        other_q7  = request.form.get('other_q7')
        question8 = request.form.get('answer8')
        question9 = request.form.get('answer9')
        question10 =', '.join(request.form.getlist('answer10')) # multi select
        question11 = request.form.get('answer11')
        other_q11 = request.form.get('other_q11')

        if "Others" in question2 and other_q2:
            question2 += f", {other_q2}"

        if "Others" in question4 and other_q4:
            question4 += f", {other_q4}"

        if "Others" in question5 and other_q5:
            question5 += f", {other_q5}"

        if "Others" in question6 and other_q6:
            question6 += f", {other_q6}"

        if "Others" in question7 and other_q7:
            question7 += f", {other_q7}"

        if "Others" in question11 and other_q11:
            question11 += f", {other_q11}"

        user_responses = UserResponses(
            userid     =current_user_uid,
            useremail=current_user_email,
            question1=question1,
            question2=question2,
            question3=question3,
            question4=question4,
            question5=question5,
            question6=question6,
            question7=question7,
            question8=question8,
            question9=question9,
            question10=question10,
            question11=question11,
        )

        try:
            db.session.add(user_responses)
            db.session.commit()
            flash("Survey submitted successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while submitting the survey.", "danger")
            print(f"[DB ERROR] {e}")
        return redirect(url_for('home'))

    try:
        return render_template("home.html", name=current_user.username, logged_in=True)
    except Exception as e:
        print(f"[ERROR] Failed to render home: {e}")
        return abort(403, description="Unauthorized Access")

@app.route('/admin', methods=["GET", "POST"])
@nocache
def adminsignin():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        result = db.session.execute(db.select(AdminDetails).where(AdminDetails.email == email))
        adminuser = result.scalar()

        # Email doesn't exist or password incorrect.
        if not adminuser:
            flash("That email does not exist, please try again.")
            return redirect(url_for('adminsignin'))
        elif adminuser.password != password:#not check_password_hash(adminuser.password, password):
            flash("Password is incorrect, please try again.")
            return redirect(url_for('adminsignin'))
        else:
            login_user(adminuser)
            return redirect(url_for('admin_dashboard'))

    return render_template("adminsignin.html")


@login_manager.user_loader
def load_user(user_id):
    user = db.session.get(UserDetails, user_id)
    if user:
        return user
    return db.get_or_404(AdminDetails, str(user_id))

def admin_required(function): # decorator function to check if user is admin or not to get to admin dashboard
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not isinstance(current_user._get_current_object(), AdminDetails):
            abort(403)
        return function(*args, **kwargs)
    return decorated_function


@app.route('/admin/dashboard')
@nocache
@admin_required
def admin_dashboard():

    responses = UserResponses.query.all()

    df = pd.DataFrame([r.to_dict() for r in UserResponses.query.all()])

    # QUESTION 1 ANALYSIS ######################################################################################
    q1_responses = df['question1'].value_counts()
    q1_total_responses = q1_responses.sum()
    fig1 = px.pie(q1_responses, values=q1_responses.values, names=q1_responses.index)
    # fig1.update_layout(width=1300, height=600)
    fig1.update_layout(title={'text': f"How long have you owned pets?<br><sup>{q1_total_responses} responses</sup>"})
    fig1_html = pio.to_html(fig1, full_html=False)

    # QUESTION 2 ANALYSIS ######################################################################################
    q2_responses_df = df['question2']
    q2_total_responses = q2_responses_df.count()

    list2 = []
    for response in q2_responses_df:
        list2.extend(response.split(', '))

    list2_df = pd.DataFrame(list2, columns=['response'])
    q2_responses_valid_df = list2_df['response'].value_counts().reset_index()
    q2_responses_valid_df.columns = ['response', 'count']
    # custom_order = ['Dog', 'Cat', 'Bird', 'Fish', 'Reptile', 'Others']
    # q2_responses_valid_df['response'] = pd.Categorical(q2_responses_valid_df['response'], categories=custom_order, ordered=True)
    # q2_responses_valid_df = q2_responses_valid_df.sort_values('response')
    total2 = q2_responses_valid_df['count'].sum()
    q2_responses_valid_df['percentage'] = (q2_responses_valid_df['count'] / total2 * 100).round(1)
    q2_responses_valid_df['label'] = q2_responses_valid_df['count'].astype(str) + ' (' + q2_responses_valid_df[
        'percentage'].astype(str) + '%)'
    q2_responses_valid_df = q2_responses_valid_df[q2_responses_valid_df['response'] != 'Others']
    q2_responses_valid_df.reset_index(drop=True, inplace=True)
    fig2 = px.bar(q2_responses_valid_df, x='count', y='response', orientation='h',
                  title=f"What types of pets do you currently own?<br><sup>{q2_total_responses} responses</sup>",
                  text='label')
    fig2.update_layout(width=1300, height=600)
    fig2.update_layout(xaxis_title="Count", yaxis_title="Pet Type")  # title_x=0.5)
    fig2.update_layout(yaxis={'categoryorder': 'total ascending'})

    fig2.update_traces(textposition='outside')
    fig2.update_layout(showlegend=False)
    fig2_html = pio.to_html(fig2, full_html=False)

    # QUESTION 3 ANALYSIS ######################################################################################
    q3_responses = df['question3'].value_counts()
    q3_total_responses = q3_responses.sum()
    fig3 = px.pie(q3_responses, values=q3_responses.values, names=q3_responses.index)
    # fig3.update_layout(width=1300, height=600)
    fig3.update_layout(title={
        'text': f"How often do you use social media to engage with other pet owners?<br><sup>{q3_total_responses} responses</sup>"})
    fig3_html = pio.to_html(fig3, full_html=False)

    # QUESTION 4 ANALYSIS ######################################################################################
    q4_responses_df = df['question4']
    list4 = []
    for response in q4_responses_df:
        list4.extend(response.split(', '))

    list4_df = pd.DataFrame(list4, columns=['response'])
    q4_responses_valid_df = list4_df['response'].value_counts().reset_index()
    q4_responses_valid_df.columns = ['response', 'count']
    q4_responses_valid_df = q4_responses_valid_df[q4_responses_valid_df['response'] != 'Others']
    q4_responses_valid_df.reset_index(drop=True, inplace=True)
    q4_total_responses = q4_responses_df.count()
    fig4 = px.pie(q4_responses_valid_df, values='count', names='response')
    # fig4.update_layout(width=1300, height=600)
    fig4.update_layout(title={
        'text': f"Do you follow any pet-related accounts on social media?(If yes, please specify which platform you use most often)<br><sup>{q4_total_responses} responses</sup>"})
    fig4_html = pio.to_html(fig4, full_html=False)

    # QUESTION 5 ANALYSIS ######################################################################################
    q5_responses_df = df['question5']
    q5_total_responses = q5_responses_df.count()
    list5 = []
    for response in q5_responses_df:
        list5.extend(response.split(', '))

    list5_df = pd.DataFrame(list5, columns=['response'])
    q5_responses_valid_df = list5_df['response'].value_counts().reset_index()
    q5_responses_valid_df.columns = ['response', 'count']
    total5 = q5_responses_valid_df['count'].sum()
    q5_responses_valid_df['percentage'] = (q5_responses_valid_df['count'] / total5 * 100).round(1)
    q5_responses_valid_df['label'] = q5_responses_valid_df['count'].astype(str) + ' (' + q5_responses_valid_df[
        'percentage'].astype(str) + '%)'
    q5_responses_valid_df = q5_responses_valid_df[q5_responses_valid_df['response'] != 'Others']
    q5_responses_valid_df.reset_index(drop=True, inplace=True)
    fig5 = px.bar(q5_responses_valid_df, x='count', y='response', orientation='h',
                  title=f"What challenges do you face when looking for pet care information online?(Select all that apply)<br><sup>{q5_total_responses} responses</sup>",
                  text='label')
    fig5.update_layout(width=1300, height=600)
    fig5.update_layout(xaxis_title="Count", yaxis_title="Challenge Type")  # title_x=0.5)
    fig5.update_layout(yaxis={'categoryorder': 'total ascending'})
    fig5.update_traces(textposition='outside')
    fig5.update_layout(showlegend=False)
    fig5_html = pio.to_html(fig5, full_html=False)

    # QUESTION 6 ANALYSIS ######################################################################################
    q6_responses_df = df['question6']
    q6_total_responses = q6_responses_df.count()

    list6 = []
    for response in q6_responses_df:
        list6.extend(response.split(', '))

    list6_df = pd.DataFrame(list6, columns=['response'])
    q6_responses_valid_df = list6_df['response'].value_counts().reset_index()
    q6_responses_valid_df.columns = ['response', 'count']
    q6_responses_valid_df = q6_responses_valid_df[q6_responses_valid_df['response'] != 'Others']
    q6_responses_valid_df.reset_index(drop=True, inplace=True)
    fig6 = px.pie(q6_responses_valid_df, values='count', names='response')
    # fig6.update_layout(width=1300, height=600)
    fig6.update_layout(title={
        'text': f"How do you currently find local services for your pets(e.g., vet clinics, groomers, pet-friendly cafes)?<br><sup>{q6_total_responses} responses</sup>"})
    fig6_html = pio.to_html(fig6, full_html=False)

    # QUESTION 7 ANALYSIS ######################################################################################
    q7_responses_df = df['question7']
    q7_total_responses = q7_responses_df.count()
    list7 = []
    for response in q7_responses_df:
        list7.extend(response.split(', '))

    list7_df = pd.DataFrame(list7, columns=['response'])
    q7_responses_valid_df = list7_df['response'].value_counts().reset_index()
    q7_responses_valid_df.columns = ['response', 'count']
    q7_responses_valid_df = q7_responses_valid_df[q7_responses_valid_df['response'] != 'Others']
    q7_responses_valid_df.reset_index(drop=True, inplace=True)
    fig7 = px.pie(q7_responses_valid_df, values='count', names='response',
                  title=f"How do you currently find other pet owners for socializing or playdates? ({q7_total_responses} responses)")
    #fig7.update_layout(width=1300, height=600)
    fig7.update_layout(title={
        'text': f"How do you currently find other pet owners for socializing or playdates?<br><sup>{q7_total_responses} responses</sup>"})
    fig7_html = pio.to_html(fig7, full_html=False)

    # QUESTION 8 ANALYSIS ######################################################################################
    q8_responses_df = df['question8']
    q8_total_responses = q8_responses_df.count()
    list8 = []
    for response in q8_responses_df:
        list8.extend(response.split(', '))

    list8_df = pd.DataFrame(list8, columns=['response'])
    list8_df['response'] = list8_df['response'].str.lower()  # converts responses strings to lower case
    q8_responses_valid_df = list8_df['response'].value_counts().reset_index()
    q8_responses_valid_df.columns = ['response', 'count']
    total8 = q8_responses_valid_df['count'].sum()
    q8_responses_valid_df['percentage'] = (q8_responses_valid_df['count'] / total8 * 100).round(1)
    q8_responses_valid_df['label'] = q8_responses_valid_df['count'].astype(str) + ' (' + q8_responses_valid_df[
        'percentage'].astype(str) + '%)'
    fig8 = px.bar(q8_responses_valid_df, x='response', y='count',
                  title=f"Have you ever experienced difficulty in adopting a pet or finding trustworthy adoption listings? What was the biggest barrier?<br><sup>{q8_total_responses} responses</sup>",
                  text='label')
    fig8.update_layout(xaxis_title="Responses", yaxis_title="Count")  # title_x=0.5)
    fig8.update_layout(width=1300, height=600)
    fig8.update_traces(textposition='outside')
    fig8.update_layout(showlegend=False)
    fig8_html = pio.to_html(fig8, full_html=False)

    # QUESTION 9 ANALYSIS ######################################################################################
    q9_responses_df = df['question9']
    q9_total_responses = q9_responses_df.count()
    list9 = []
    for response in q9_responses_df:
        list9.extend(response.split(', '))

    list9_df = pd.DataFrame(list9, columns=['response'])
    list9_df['response'] = list9_df['response'].str.lower()  # converts responses strings to lower case
    q9_responses_valid_df = list9_df['response'].value_counts().reset_index()
    q9_responses_valid_df.columns = ['response', 'count']
    total9 = q9_responses_valid_df['count'].sum()
    q9_responses_valid_df['percentage'] = (q9_responses_valid_df['count'] / total9 * 100).round(1)
    q9_responses_valid_df['label'] = q9_responses_valid_df['count'].astype(str) + ' (' + q9_responses_valid_df[
        'percentage'].astype(str) + '%)'

    fig9 = px.bar(q9_responses_valid_df, x='response', y='count',
                  title=f"Have you ever experienced difficulty in adopting a pet or finding trustworthy adoption listings? What was the biggest barrier?<br><sup>{q9_total_responses} responses</sup>",
                  text='label')
    fig9.update_layout(width=1300, height=600)
    fig9.update_layout(xaxis_title="Responses", yaxis_title="Count")  # title_x=0.5)
    fig9.update_traces(textposition='outside')
    fig9.update_layout(showlegend=False)
    fig9_html = pio.to_html(fig9, full_html=False)

    # QUESTION 10 ANALYSIS ######################################################################################
    q10_responses_df = df['question10']
    q10_total_responses = q10_responses_df.count()

    list10 = []
    for response in q10_responses_df:
        list10.extend(response.split(', '))

    list10_df = pd.DataFrame(list10, columns=['response'])
    q10_responses_valid_df = list10_df['response'].value_counts().reset_index()
    q10_responses_valid_df.columns = ['response', 'count']
    total10 = q10_responses_valid_df['count'].sum()
    q10_responses_valid_df['percentage'] = (q10_responses_valid_df['count'] / total10 * 100).round(1)
    q10_responses_valid_df['label'] = q10_responses_valid_df['count'].astype(str) + ' (' + q10_responses_valid_df[
        'percentage'].astype(str) + '%)'
    q10_responses_valid_df = q10_responses_valid_df[q10_responses_valid_df['response'] != 'Others']
    q10_responses_valid_df.reset_index(drop=True, inplace=True)
    fig10 = px.bar(q10_responses_valid_df, x='count', y='response', orientation='h',
                  title=f"What features would you want most in a platform dedicated to pets? (Select top 3)<br><sup>{q10_total_responses} responses</sup>",
                  text='label')
    #fig10.update_layout(width=1300, height=600)
    fig10.update_layout(xaxis_title="Count", yaxis_title="Response")  # title_x=0.5)
    fig10.update_layout(yaxis={'categoryorder': 'total ascending'})

    fig10.update_traces(textposition='outside')
    fig10.update_layout(showlegend=False)
    fig10_html = pio.to_html(fig10, full_html=False)

    # QUESTION 11 ANALYSIS ######################################################################################
    q11_responses_df = df['question11']
    list11 = []
    for response in q11_responses_df:
        list11.extend(response.split(', '))

    list11_df = pd.DataFrame(list11, columns=['response'])
    q11_responses_valid_df = list11_df['response'].value_counts().reset_index()
    q11_responses_valid_df.columns = ['response', 'count']
    q11_responses_valid_df = q11_responses_valid_df[q11_responses_valid_df['response'] != 'Others']
    q11_responses_valid_df.reset_index(drop=True, inplace=True)
    q11_total_responses = q11_responses_df.count()
    fig11 = px.pie(q11_responses_valid_df, values='count', names='response')
    # fig11.update_layout(width=1300, height=600)
    fig11.update_layout(title={
        'text': f"Would you be willing to pay for premium features on a pet social platform?<br><sup>{q11_total_responses} responses</sup>"})
    fig11_html = pio.to_html(fig11, full_html=False)


    return render_template("admindashboard.html", user_responses_table=responses, admin_email=current_user.email, fig1=fig1_html, fig2=fig2_html, fig3=fig3_html, fig4=fig4_html, fig5=fig5_html, fig6=fig6_html, fig7=fig7_html, fig8=fig8_html, fig9=fig9_html, fig10=fig10_html, fig11=fig11_html)


@app.route('/logout')
@nocache
@login_required
def logout():
    logout_user()
    return redirect(url_for('signin'))

@app.route('/adminlogout')
@nocache
@login_required
def adminlogout():
    logout_user()
    return redirect(url_for('adminsignin'))


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8000)
