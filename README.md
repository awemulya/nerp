
### 1. Install
```
wget https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.4.1.noarch.rpm # download elasticsearch
sudo yum localinstall elasticsearch-*.rpm # install elasticsearch
sudo service elasticsearch start # start elasticsearch service
sudo chkconfig elasticsearch on # enable elasticsearch service on system startup
virtualenv env # create a virtual environment
source env/bin/activate # Enter the virtual environment
git clone git@github.com:awecode/nerp.git app # git clone the repo
cd app # cd to project dir
export DJANGO_SETTINGS_MODULE=app.settings
pip install -r requirements/development.txt # install Python packages required for development
cp app/local_settings.sample.py app/local_settings.py # create local settings file from sample file
vi app/local_settings.py # configure your settings here, database, static & media paths and urls
./manage.py migrate # synchronize database and run migrations
./manage.py loaddata groups # install default groups
./manage.py loaddata users # install admin user
./manage.py collectstatic # collect static files
```

### 2. Run
```
./manage.py runserver
```

### 3. Rejoice!