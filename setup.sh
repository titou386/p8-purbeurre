#!/usr/bin/env bash

PKG_MANAGER="sudo apt-get"
PKG_INSTALL=("${PKG_MANAGER}" install -y)
REPO_URL=https://github.com/titou386/${REPO}.git
REPO=p8-purbeurre
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
VIRTUAL_ENV=""


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

# NO ROOT to install
if [[ "${EUID}" -eq 0 ]]; then
    echo "Vous ne devez pas être en administrateur."
    install_error

input=""
until [[ $input ]]; do
    echo "ATTENTION : Si une configuration est déjà présente, elle sera écrasée !"
    echo -n "Voulez-vous continuer ? (y/N) "

done

os_check

PKG_MANAGER update
PKG_INSTALL python3-pip nginx virtualenv supervisor clone

#####################################################################################
echo "Vous devez définir quelques paramètres ..."
until [[ $DB_HOST ]]; do
    echo -n "Vouler-vous installer & configurer Postgresql sur ce serveur ? (y/N) "
    read POSTGRESQL_LOCAL
    
    if [[ -z ${POSTGRESQL_LOCAL} ]] || [[ "$POSTGRESQL_LOCAL" == "n" ]] || [[ "$POSTGRESQL_LOCAL" == "N" ]]; then
        POSTGRESQL_LOCAL = "NO"
    elif [[ "$POSTGRESQL_LOCAL" == "y" ]] || [[ "$POSTGRESQL_LOCAL" == "Y" ]]; then
        POSTGRESQL_LOCAL = "YES"
        DB_HOST = "localhost"
        apt-get install -y postgresql
    fi
done

#####################################################################################
until [[ $DB_HOST ]]; do
    echo -n "Adresse de la base données ?"
    READ DB_HOST
done
#####################################################################################    
until [[ $DB_PORT ]]; do
    echo -n "Port de la base de données ? (5432) "
    read input
    if [[ $input =~ ^-?[0-9]+$ ]]; then
        DB_PORT=${input}
        unset ${input}
    elif [[ -z input ]]; then
        DB_PORT="5432"
    fi
done    
#####################################################################################
until [[ $DB_NAME ]]; do
    echo -n "Nom de la base de données : "
    read DB_NAME
done
#####################################################################################
until [[ $DB_USER ]]; do
    echo -n "Nom d'utilisateur la base de données : "
    read DB_USER
done
#####################################################################################
until [[ $DB_PASSWORD ]]; do
    echo -n "Mot de passe de la base de données : "
    read DB_PASSWORD
done
#####################################################################################
until [[ $VIRTUAL_ENV ]]; do
    echo -n "Nom de votre environnement virtuel python : "
    read VIRTUAL_ENV
done
#####################################################################################

if [[ $POSTGRESQL_LOCAL == 'YES' ]]; then
    echo "Creation de la base de données ..."
    sudo -u postgres -H -- psql << EOF >/dev/null 2>&1
    CREATE DATABASE ${DB_NAME};
    CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASSWORD}';
    ALTER ROLE ${DB_USER} SET client_encoding TO 'utf8';
    ALTER ROLE ${DB_USER} SET default_transaction_isolation TO 'read committed';
    ALTER ROLE ${DB_USER} SET timezone TO 'Europe/Paris';
    GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_USER}; 
EOF
fi
######################################################################################
echo "Clone du repo ..."
git clone 
######################################################################################
echo "Configuration de l'environnement de travail ..."
pip install virtualenv
virtualenv -p python3 ${VIRTUAL_ENV}
source ${VIRTUAL_ENV}/bin/activate
pip install -r ${REPO}/requirements.txt

if [[ -z ${SECRET_KEY} ]]; then
    SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; \
            print(get_random_secret_key())')

echo -e "DB_HOST=${DB_HOST}
DB_PORT=${DB_PORT}
DB_USER=${DB_USER}
DB_PASSWORD=${DB_PASSWORD}
DB_NAME=${DB_NAME}
SECRET_KEY=${SECRET_KEY}
ALLOWED_HOSTS='ec2-*.amazonaws.com'" > .${VIRTUAL_ENV}

echo -e "#!/usr/bin/bash

NAME=${APP_NAME}
DJANGODIR=${WORK_DIR}/${REPO}
SOCKFILE=${WORK_DIR}/${APP_NAME}_gunicorn.sock
USER=${USER}
GROUP=${GROUP}
NUM_WORKERS=3
DJANGO_SETTINGS_MODULE=${APP_NAME}.settings
DJANGO_WSGI_MODULE=${APP_NAME}.wsgi

echo \"Starting $NAME as `whoami`\"

# Activate the virtual environment
export $(cat ${WORK_DIR}/.${VIRTUAL_ENV} | xargs)
source ${WORK_DIR}/${VIRTUAL_ENV}/bin/activate
cd ${WORK_DIR}/${REPO}

export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH


# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec ../${VIRTUAL_ENV}/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
--name $NAME \
--workers $NUM_WORKERS \
--user=$USER --group=$GROUP \
--bind=unix:$SOCKFILE \
--log-level=debug \
--log-file=-
" > ${WORK_DIR}/${VIRTUAL_ENV}/bin/gunicorn_start
chmod +x ${WORK_DIR}/${VIRTUAL_ENV}/bin/gunicorn_start

sudo -i

echo -e "[program:${APP_NAME}]
command = ${WORK_DIR}/${VIRTUAL_ENV}/bin/gunicorn_start
user = ${USER} 
stdout_logfile = /var/log/supervisor/${APP_NAME}.log
redirect_stderr = true
environment=LANG=en_US.UTF-8,LC_ALL=en_US.UTF-8
autostart = true
autorestart = true" > /etc/supervisor/conf.d/${APP_NAME}.conf

echo -e "upstream ${APP_NAME}_server {
    server unix:${WORK_DIR}/${APP_NAME}_gunicorn.sock fail_timeout=0;
}

server {

    listen   80;

    access_log /var/log/nginx/${APP_NAME}/nginx-access.log;
    error_log /var/log/nginx/$APP_NAME}/nginx-error.log;

    location /static/ {
         alias   ${WORK_DIR}/${REPO}/static/;
    }

    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;

        if (!-f $request_filename) {
            proxy_pass http://${APP_NAME}_server;
            break;
        }
    }
}
" > /etc/nginx/sites-available/${APP_NAME}

ln -s /etc/nginx/sites-available/${APP_NAME} /etc/nginx/sites-enabled
rm -fr /etc/nginx/sites-enabled/default

NGNIX_LOGDIR=/var/log/nginx/${APP_NAME}
test -d $NGNIX_LOGDIR || mkdir -p $NGNIX_LOGDIR

service supervisor restart
sleep 5
service nginx restart
logout

echo "Configuration terminée."
exit 0
