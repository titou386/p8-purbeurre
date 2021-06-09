#!/usr/bin/env bash

REPO="p8-purbeurre"
REPO_URL="https://github.com/titou386/${REPO}.git"
WORK_DIR=$PWD
APP_NAME="purbeurre"

if groups $USER | grep -q ${USER}; then
    GROUP=$USER
else
    GROUP="nogroup"
fi

DB_HOST=""
DB_PORT=""
DB_NAME=""
DB_USER=""
DB_PASSWORD=""
SECRET_KEY=""
VIRT_ENV=""


os_check() {
    detected_os=$(grep "\bID\b" /etc/os-release | cut -d '=' -f2 | tr -d '"')
    if [ ! "${detected_os}" = "ubuntu" ]; then
        echo "Ce script a été testé que sur une distribution Ubuntu"
        echo
        exit 1
    fi
}

install_error() {
    echo "Echec de l'installation ..."
    exit 1
}

os_check

# NO ROOT to install
if [[ "${EUID}" -eq 0 ]]; then
    echo "Vous ne devez pas être en administrateur."
    install_error
fi

input=""
until [[ -n $input ]]; do
    echo "ATTENTION : Si une configuration est déjà présente, elle sera écrasée !"
    echo -n "Voulez-vous continuer ? (y/N) "
    read input
    if [[ -z ${input} ]] || [[ ${input} == 'n' ]] || [[ ${input} == 'N' ]]; then
        exit 0
    elif [[ ${input} == 'Y' ]] || [[ ${input} == 'y' ]]; then
        :
    else
        input=""
    fi
done
unset ${input}

sudo apt-get update
sudo apt-get install -y python3-pip nginx virtualenv supervisor git

#####################################################################################
echo "Vous devez définir quelques paramètres ..."
input=""
until [[ -n $input ]]; do
    echo -n "Vouler-vous installer & configurer Postgresql sur ce serveur ? (y/N) "
    read input
    if [[ -z ${input} ]] || [[ ${input} == 'n' ]] || [[ ${input} == 'N' ]]; then
        POSTGRESQL_LOCAL="NO"
    elif [[ ${input} == 'Y' ]] || [[ ${input} == 'y' ]]; then
        POSTGRESQL_LOCAL="YES"
        DB_HOST="localhost"
        sudo apt-get install -y postgresql
    else
    input=""
    fi
done

#####################################################################################
until [[ -n $DB_HOST ]]; do
    echo -n "Adresse de la base données ?"
    read DB_HOST
done
#####################################################################################    
until [[ -n $DB_PORT ]]; do
    echo -n "Port de la base de données ? (5432) "
    read input
    if [[ $input =~ ^-?[0-9]+$ ]]; then
        DB_PORT=${input}
        unset ${input}
    elif [[ -n input ]]; then
        DB_PORT="5432"
    fi
done    
#####################################################################################
until [[ -n $DB_NAME ]]; do
    echo -n "Nom de la base de données : "
    read DB_NAME
done
#####################################################################################
until [[ -n $DB_USER ]]; do
    echo -n "Nom d'utilisateur la base de données : "
    read DB_USER
done
#####################################################################################
until [[ -n $DB_PASSWORD ]]; do
    echo -n "Mot de passe de la base de données : "
    read DB_PASSWORD
done
#####################################################################################
until [[ -n $VIRT_ENV ]]; do
    echo -n "Nom de votre environnement virtuel python : "
    read VIRT_ENV
done
#####################################################################################

if [[ ${POSTGRESQL_LOCAL} == 'YES' ]]; then
    echo "Creation de la base de données ..."
    sudo -u postgres -H -- psql <<EOF
    CREATE DATABASE ${DB_NAME};
    CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASSWORD}';
    ALTER ROLE ${DB_USER} SET client_encoding TO 'utf8';
    ALTER ROLE ${DB_USER} SET default_transaction_isolation TO 'read committed';
    ALTER ROLE ${DB_USER} SET timezone TO 'Europe/Paris';
    GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_USER}; 
EOF
fi
######################################################################################
if [[ -d $REPO ]]; then
    echo "Mise à jour ..."
    cd $REPO
    git pull
    retVal=$?
    cd ..
else
    echo "Clone du repo ..."
    git clone ${REPO_URL}
    retVal=$?
fi
if [ $retVal -ne 0 ]; then
    echo "Erreur..."
    exit $retVal
fi

######################################################################################
echo "Configuration de l'environnement de travail ..."

pip3 install virtualenv
virtualenv -p python3 ${VIRT_ENV}
source ${VIRT_ENV}/bin/activate
pip3 install -r ${REPO}/requirements.txt

if [[ ! $SECRET_KEY ]]; then
    cd $REPO
    SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; \
            print(get_random_secret_key())')
    export SECRET_KEY
    cd ..
fi

cat > .${VIRT_ENV} <<EOF
DB_HOST=${DB_HOST}
DB_PORT=${DB_PORT}
DB_USER=${DB_USER}
DB_PASSWORD=${DB_PASSWORD}
DB_NAME=${DB_NAME}
SECRET_KEY=${SECRET_KEY}
ALLOWED_HOSTS='ec2-*.amazonaws.com'
EOF

export $(cat .${VIRT_ENV} | xargs)

cd $REPO
python3 manage.py collectstatic
python3 manage.py migrate
cd ..
deactivate

cat > ${WORK_DIR}/${VIRT_ENV}/bin/gunicorn_start <<EOF
#!/usr/bin/env bash

NAME=${APP_NAME}
DJANGODIR=${WORK_DIR}/${REPO}
SOCKFILE=${WORK_DIR}/${APP_NAME}_gunicorn.sock
USER=${USER}
GROUP=${GROUP}
NUM_WORKERS=3
DJANGO_SETTINGS_MODULE=${APP_NAME}.settings
DJANGO_WSGI_MODULE=${APP_NAME}.wsgi

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
export \$(cat ${WORK_DIR}/.${VIRT_ENV} | xargs)
source ${WORK_DIR}/${VIRT_ENV}/bin/activate
cd \$DJANGODIR

export DJANGO_SETTINGS_MODULE=\$DJANGO_SETTINGS_MODULE
export PYTHONPATH=\$DJANGODIR:\$PYTHONPATH


# Create the run directory if it doesn't exist
RUNDIR=\$(dirname \$SOCKFILE)
test -d \$RUNDIR || mkdir -p \$RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec ${WORK_DIR}/${VIRT_ENV}/bin/gunicorn \${DJANGO_WSGI_MODULE}:application \
--name \$NAME \
--workers \$NUM_WORKERS \
--user=\$USER --group=\$GROUP \
--bind=unix:\$SOCKFILE \
--log-level=debug \
--log-file=-

EOF

chmod +x ${WORK_DIR}/${VIRT_ENV}/bin/gunicorn_start

sudo bash -c "cat > /etc/supervisor/conf.d/${APP_NAME}.conf <<EOF
[program:${APP_NAME}]
command = ${WORK_DIR}/${VIRT_ENV}/bin/gunicorn_start
user = ${USER}
stdout_logfile = /var/log/supervisor/${APP_NAME}.log
redirect_stderr = true
environment=LANG=en_US.UTF-8,LC_ALL=en_US.UTF-8
autostart = true
autorestart = true
EOF"

cat > ${APP_NAME} <<EOF
upstream ${APP_NAME}_server {
    server unix:${WORK_DIR}/${APP_NAME}_gunicorn.sock fail_timeout=0;
}

server {

    listen   80;

    access_log /var/log/nginx/${APP_NAME}/nginx-access.log;
    error_log /var/log/nginx/${APP_NAME}/nginx-error.log;

    location /static/ {
         alias   ${WORK_DIR}/${REPO}/${APP_NAME}/static/;
    }

    location / {
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header Host \$http_host;
        proxy_redirect off;

        if (!-f \$request_filename) {
            proxy_pass http://${APP_NAME}_server;
            break;
        }
    }
}
EOF

sudo chown root:root ${APP_NAME}
sudo mv -f ${APP_NAME} /etc/nginx/sites-available

if [[ ! -L /etc/nginx/sites-enabled/${APP_NAME} ]]; then
    sudo ln -s /etc/nginx/sites-available/${APP_NAME} /etc/nginx/sites-enabled
fi

if [[ -L /etc/nginx/sites-enabled/default ]]; then
    sudo rm -fr /etc/nginx/sites-enabled/default
fi

NGNIX_LOGDIR=/var/log/nginx/${APP_NAME}
sudo sh -c "test -d $NGNIX_LOGDIR || sudo mkdir -p $NGNIX_LOGDIR"

sudo service supervisor restart
sleep 5
sudo service nginx restart

echo "Configuration terminée."
exit 0

