from passlib.hash import sha256_crypt
from flask_ini import FlaskIni
from flask import (
        Flask, flash, render_template, redirect, request, url_for)
from flask_login import (
        login_user, logout_user, current_user, LoginManager, login_required)
from forms import FormUser, FormDomain, FormLogin, FormEditUser, FormAdmin
from models import Users, Domain, Administrator, db

app = Flask(__name__)
app.config.from_object('settings')
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.initconfig = FlaskIni()

with app.app_context():
    app.initconfig.read('seloradmin.conf')

home = app.initconfig.get('selor', 'home')
uid = app.initconfig.get('selor', 'uid')
gid = app.initconfig.get('selor', 'gid')
maildir = app.initconfig.get('selor', 'maildir')


@app.teardown_appcontext
def teardown_db(exception):
    db.session.commit()
    db.session.close()


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))


@login_manager.user_loader
def loader_user(id):
    try:
        return Administrator.query.filter_by(id=id).first()
    except Users.DoesNotExist:
        return None


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = FormLogin()

    if request.method == 'GET':
        if not current_user.is_authenticated:
            return render_template('login.html', form=form)
        else:
            return redirect(url_for('usuarios'))

    if request.method == 'POST':
        if form.validate_on_submit():
            form = FormUser(request.form)
            username = form.username.data
            password = form.password.data

            try:
                user = Administrator.query.filter_by(user=username).first()

                dbuser = user.user
                dbpass = user.password

                if username == dbuser and sha256_crypt.verify(
                                                            password, dbpass):
                    login_user(user)
                    return redirect(url_for('usuarios'))
                else:
                    flash(
                        'Usuário ou senha inválida', 'notification is-danger')

            except:
                flash('Usuário ou senha inválida', 'notification is-danger')

        return render_template('login.html', form=form)


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    form = FormAdmin()

    if request.method == 'GET':
        return render_template('admin.html', form=form)

    if request.method == 'POST':
        if form.validate_on_submit():
            form = FormAdmin(request.form)
            atual = form.atual.data
            nova = form.nova.data
            repetir = form.repetir.data

            admin = Administrator.query.first()

            if nova != repetir:
                flash('A nova senha não são iguais', 'notification is-danger')
            elif not sha256_crypt.verify(atual, admin.password):
                flash('A senha atual é inválida', 'notification is-danger')
            else:
                novasenha = sha256_crypt.encrypt(nova)

                admin.password = novasenha

                flash('Senha atualizada', 'notification is-success')
        else:
            flash('Fala ao editar a senha', 'notification is-danger')

        return redirect(url_for('admin'))


@app.route('/', methods=['GET'])
@login_required
def usuarios():
    if request.method == 'GET':
        usuarios = Users.query.all()

        if request.args.get('confirm'):
            email = request.args.get('confirm')

            return render_template(
                                'users.html', usuarios=usuarios, email=email)

        if request.args.get('delete'):
            email = request.args.get('delete')

            query = Users.query.filter_by(mail=email).first()
            db.session.delete(query)

            flash('Email excluído')

            return redirect(url_for('usuarios'))

        return render_template('users.html', usuarios=usuarios)


@app.route('/add-user', methods=['GET', 'POST'])
@login_required
def adduser():
    form = FormUser()

    if request.method == "GET":
        return render_template('adduser.html', form=form)

    if request.method == "POST":

        if form.validate_on_submit():
            form = FormUser(request.form)

            myquota = form.quota.data * 1000 * 1000
            myusername = form.username.data
            mydomain = form.domain.data
            mymail = ("%s@%s" % (myusername, mydomain))
            myhome = ("%s/%s/%s/" % (home, mydomain, myusername))
            mypass = sha256_crypt.encrypt(form.password.data)

            existe = Users.query.filter_by(mail=mymail).first()

            if existe:
                flash('Erro, E-Mail já cadastrado', 'notification is-danger')
            else:
                user = Users(
                    mail=mymail, password=mypass, uid=uid, gid=gid,
                    home=myhome, maildir=maildir, domain=form.domain.data,
                    name=form.name.data, quota=str(myquota), dlocal=myhome
                )
                db.session.add(user)

                flash(
                    'E-Mail cadastrado com sucesso', 'notification is-success')
                return redirect(url_for('adduser'))
        else:
            flash('Fala ao cadastrar o E-Mail', 'notification is-danger')

        return render_template('adduser.html', form=form)


@app.route('/edit-user', methods=['GET', 'POST'])
@login_required
def edituser():
    form = FormEditUser()

    if request.method == 'GET':
        email = request.args.get('email')
        user = Users.query.filter_by(mail=email).first()

        return render_template(
                        'edituser.html', form=form, user=user)

    if request.method == 'POST':
        email = request.args.get('email')
        user = Users.query.filter_by(mail=email).first()

        if form.validate_on_submit():
            form = FormEditUser(request.form)
            name = form.name.data
            quota = int(form.quota.data) * 1000 * 1000

            query = Users.query.filter_by(mail=email).first()
            query.name = name
            query.quota = str(quota)

            if form.password.data:
                password = sha256_crypt.encrypt(form.password.data)
                query.password = password

            flash('E-mail atualizado', 'notification is-success')

            return redirect(url_for('edituser', email=email))

        else:
            flash('Erro ao atualizar o E-Mail', 'notification is-danger')

        return render_template(
                        'edituser.html', form=form, user=user)


@app.route('/domains', methods=['GET'])
@login_required
def domains():
    if request.method == 'GET':
        mydomains = Domain.query.all()

        if request.args.get('confirm'):
            domain = request.args.get('confirm')

            return render_template(
                            'domains.html', mydomains=mydomains, domain=domain)

        if request.args.get('delete'):
            domain = request.args.get('delete')

            query = Domain.query.filter_by(name=domain).first()
            db.session.delete(query)

            flash('Domínio excluído')

            return redirect(url_for('domains'))

        return render_template('domains.html', mydomains=mydomains)


@app.route('/add-domain', methods=['GET', 'POST'])
@login_required
def addomain():
    form = FormDomain()

    if request.method == 'GET':
        return render_template('addomain.html', form=form)

    if request.method == 'POST':
        if form.validate_on_submit():
            form = FormDomain(request.form)
            mycompany = form.company.data
            mydomain = form.domain.data

            dominio = Domain.query.filter_by(name=mydomain).first()

            if dominio:
                flash('Domínio já existe', 'notification is-danger')
            else:
                query = Domain(company=mycompany, name=mydomain)
                db.session.add(query)

                flash("Domínio cadastrado", 'notification is-success')
                return redirect(url_for('addomain'))
        else:
            flash('Fala ao cadastrar o domínio', 'notification is-danger')

        return render_template('addomain.html', form=form)
