from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime
import os

from models import Bruker, Arrangement, Påmelding
from extensions import db, login_manager
import app_config as config

app = Flask(__name__)

# SQLAlchemy and misc config
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/photos'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Mail Config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587 
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'eventhubconfirmation@gmail.com'
app.config['MAIL_PASSWORD'] = 'hkoe cxks qwsq jvqz'
app.config['MAIL_DEFAULT_SENDER'] = 'eventhubconfirmation@gmail.com'
mail = Mail(app)

# Login Manager
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Du må være logget inn for å få tilgang til denne siden.'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Bruker, int(user_id))


#Uploaded file security
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# -------------------------------
# Register, login, logout
# -------------------------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        navn = request.form['navn']
        epost = request.form['epost']
        passord = request.form['passord']
        bekreft_passord = request.form['bekreft_passord']

        if not navn or not epost or not passord or not bekreft_passord:
            error = 'Alle feltene må fylles ut.'
            return render_template('register.html', error=error)

        if passord != bekreft_passord:
            error = 'Passordene stemmer ikke overens.'
            return render_template('register.html', error=error)

        bruker_eksisterer = Bruker.query.filter_by(epost=epost).first()
        if bruker_eksisterer:
            error = 'Denne e-postadressen er allerede registrert.'
            return render_template('register.html', error=error)

        hashed_passord = generate_password_hash(passord)

        ny_bruker = Bruker(navn=navn, epost=epost, passord=hashed_passord)

        db.session.add(ny_bruker)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        epost = request.form['epost']
        passord = request.form['passord']

        bruker = Bruker.query.filter_by(epost=epost).first()

        if bruker and check_password_hash(bruker.passord, passord):
            login_user(bruker)
            return redirect(url_for('index'))

        error = 'Feil e-post eller passord.'
        return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# -------------------------------
# Home, my events, event details
# -------------------------------

@app.route('/')
def index():
    search_query = request.args.get('search', '').strip()
    filter_date = request.args.get('date', '').strip()

    # Base query
    query = Arrangement.query.filter(Arrangement.dato >= db.func.now())

    # Apply search filter
    if search_query:
        query = query.filter(Arrangement.navn.ilike(f'%{search_query}%'))

    # Apply date filter
    if filter_date:
        try:
            filter_date_obj = datetime.strptime(filter_date, '%Y-%m-%d')
            query = query.filter(db.func.date(Arrangement.dato) == filter_date_obj)
        except ValueError:
            flash('Ugyldig datoformat. Bruk YYYY-MM-DD.', 'warning')

    # Using query
    kommende_arrangementer = query.order_by(Arrangement.dato).all()
    
    # List of joined events - for green checkmark
    påmeldte_arrangementer = []
    if current_user.is_authenticated:
        påmeldte_arrangementer = [
            påmelding.arrangement_id for påmelding in Påmelding.query.filter_by(bruker_id=current_user.id).all()
        ]

    return render_template(
        'index.html',
        arrangementer=kommende_arrangementer,
        search_query=search_query,
        filter_date=filter_date,
        påmeldte_arrangementer=påmeldte_arrangementer
    )

@app.route('/my_events')
@login_required
def my_events():
    
    # Created events
    brukerens_arrangementer = Arrangement.query.filter_by(bruker_id=current_user.id).order_by(Arrangement.dato).all()
    
    # Joined events
    påmeldte_arrangementer = []
    if current_user.is_authenticated:
        påmeldte_arrangementer = [
            påmelding.arrangement_id for påmelding in Påmelding.query.filter_by(bruker_id=current_user.id).all()
        ]
    brukerens_p_arrangementer = Arrangement.query.filter(Arrangement.id.in_(påmeldte_arrangementer)).order_by(Arrangement.dato).all()
    
    return render_template(
        'my_events.html',
        arrangementer=brukerens_arrangementer,
        p_arrangementer = brukerens_p_arrangementer
    )

@app.route('/event/<int:event_id>')
def display_event(event_id):
    arrangement = Arrangement.query.get_or_404(event_id)
    påmeldt = False
    oppretter = Bruker.query.get(arrangement.bruker_id)

    if current_user.is_authenticated:
        påmelding = Påmelding.query.filter_by(bruker_id=current_user.id, arrangement_id=arrangement.id).first()
        if påmelding:
            påmeldt = True
            
    antall_påmeldte = Påmelding.query.filter_by(arrangement_id=arrangement.id).count()
    
    return render_template(
        'event_detail.html',
        arrangement=arrangement,
        påmeldt=påmeldt,
        oppretter=oppretter,
        antall_påmeldte=antall_påmeldte
        
    )

# -------------------------------
# Register, unregister
# -------------------------------

@app.route('/register-for-event/<int:event_id>', methods=['POST'])
@login_required
def join_event(event_id):
    arrangement = Arrangement.query.get_or_404(event_id)

    # Check if user already has signed up
    påmelding_eksisterer = Påmelding.query.filter_by(bruker_id=current_user.id, arrangement_id=arrangement.id).first()
    if påmelding_eksisterer:
        flash('Du er allerede påmeldt dette arrangementet.', 'warning')
        return redirect(url_for('display_event', event_id=event_id))
    
    # New sign-up
    ny_påmelding = Påmelding(bruker_id=current_user.id, arrangement_id=arrangement.id)
    db.session.add(ny_påmelding)
    db.session.commit()
    
    # Send confirmation email
    msg = Message(
        subject=f"Bekreftelse: Påmelding til {arrangement.navn}",
        recipients=[current_user.epost],  # Send til brukerens e-post
        body=f"Hei {current_user.navn},\n\n"
             f"Du er nå påmeldt arrangementet '{arrangement.navn}' som finner sted "
             f"den {arrangement.dato.strftime('%d.%m.%Y %H:%M')} på {arrangement.sted}.\n\n"
             f"Med vennlig hilsen,\nEventHub-teamet"
    )
    mail.send(msg)
    
    flash(f'Du er nå påmeldt arrangementet "{arrangement.navn}".', 'success')
    return redirect(url_for('display_event', event_id=event_id))

@app.route('/unregister-from-event/<int:event_id>', methods=['POST'])
@login_required
def leave_event(event_id):
    arrangement = Arrangement.query.get_or_404(event_id)

    påmelding = Påmelding.query.filter_by(bruker_id=current_user.id, arrangement_id=arrangement.id).first()
    if påmelding:
        db.session.delete(påmelding)
        db.session.commit()
        flash(f'Du er nå avmeldt arrangementet "{arrangement.navn}".', 'info')
    else:
        flash('Du er ikke påmeldt dette arrangementet.', 'warning')

    return redirect(url_for('display_event', event_id=event_id))

# -------------------------------
# Create, delete, edit event
# -------------------------------

@app.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    if request.method == 'POST':
        navn = request.form['navn']
        beskrivelse = request.form['beskrivelse']
        dato_str = request.form['dato']
        sted = request.form['sted']
        bilde = request.files['bilde']

        if not navn or not beskrivelse or not dato_str or not sted:
            flash('Alle feltene må fylles ut.', 'warning')
            return render_template('create_event.html')

        try:
            dato = datetime.strptime(dato_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash('Ugyldig dato- og tidspunktformat.', 'danger')
            return render_template('create_event.html')
        
        bilde = None
        if bilde and allowed_file(bilde.filename):
            filnavn = secure_filename(bilde.filename)
            bilde.save(os.path.join(app.config['UPLOAD_FOLDER'], filnavn))
            bilde = filnavn

        nytt_arrangement = Arrangement(
            navn=navn,
            beskrivelse=beskrivelse,
            dato=dato,
            sted=sted,
            bruker_id=current_user.id,
            bilde=bilde
        )

        db.session.add(nytt_arrangement)
        db.session.commit()
        flash(f'Arrangementet "{navn}" er opprettet.', 'success')
        return redirect(url_for('index')) 

    return render_template('create_event.html')

@app.route('/delete_event/<int:event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    arrangement = Arrangement.query.get_or_404(event_id)
    
    if arrangement.bruker_id != current_user.id:
        abort(403)

    db.session.delete(arrangement)
    db.session.commit()
    flash(f'Arrangementet "{arrangement.navn}" er slettet.', 'success')
    return redirect(url_for('my_events'))

@app.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    arrangement = Arrangement.query.get_or_404(event_id)

    if arrangement.bruker_id != current_user.id:
        abort(403)
    if request.method == 'POST':
        navn = request.form['navn']
        beskrivelse = request.form['beskrivelse']
        dato_str = request.form['dato']
        sted = request.form['sted']
        bilde = request.files['bilde']

        if not navn or not beskrivelse or not dato_str or not sted:
            flash('Alle feltene må fylles ut.', 'warning')
            return render_template('edit_event.html', arrangement=arrangement)

        try:
            dato = datetime.strptime(dato_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash('Ugyldig dato- og tidspunktformat.', 'danger')
            return render_template('edit_event.html', arrangement=arrangement)
        
        if bilde and allowed_file(bilde.filename):
                filnavn = secure_filename(bilde.filename)
                bilde.save(os.path.join(app.config['UPLOAD_FOLDER'], filnavn))
                arrangement.bilde = filnavn

        arrangement.navn = navn
        arrangement.beskrivelse = beskrivelse
        arrangement.dato = dato
        arrangement.sted = sted

        db.session.commit()
        flash(f'Arrangementet "{navn}" er oppdatert.', 'success')
        return redirect(url_for('my_events'))
    
    arrangement.dato_str = arrangement.dato.strftime('%Y-%m-%dT%H:%M')
    return render_template('edit_event.html', arrangement=arrangement)

# -------------------------------
# Forgotten Password Functionality
# -------------------------------

serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

def generate_reset_token(email):
    return serializer.dumps(email, salt='password-reset-salt')

def verify_reset_token(token, expiration=3600):
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=expiration)
    except:
        return None
    return email

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = Bruker.query.filter_by(epost=email).first()
        if user:            
            token = generate_reset_token(email)
            reset_url = url_for('reset_password', token=token, _external=True)
            
            msg = Message(
                subject="Tilbakestilling av passord",
                recipients=[email],
                body=f"Klikk på denne linken for å lage et nytt passord: {reset_url}"
            )
            mail.send(msg)

        flash('En link for å lage nytt passord er sendt på mail dersom din mailadresse er registrert.', 'info')
        return redirect(url_for('login'))
    return render_template('forgot_password.html')

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    email = verify_reset_token(token)
    if not email:
        flash('Resetlinken er utgått eller ugyldig.', 'danger')
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        new_password = request.form['password']
        confirm_password = request.form['confirm_password']
        if new_password != confirm_password:
            flash('Passordene du har skrevet inn er ikke like.', 'warning')
            return render_template('reset_password.html', token=token)

        user = Bruker.query.filter_by(epost=email).first()
        user.passord = generate_password_hash(new_password)
        db.session.commit()

        flash('Passordet ditt er endret. Du kan nå logge inn.', 'success')
        return redirect(url_for('login'))

    return render_template('reset_password.html', token=token)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)