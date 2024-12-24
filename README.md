## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

### To start backend server
python3 app.py

### To install node modules
npm install

### To create venv in wsl
python3 -m venv env_name

### To activate the venv in wsl
source env_name/bin/activate


### To start the celery worker
celery -A app:celery_app worker -l INFO

### To start the celery beat
celery -A app:celery_app beat -l INFO

### To start the mailhog 
~/go/bin/MailHog

### To restart if any problem with celery 
sudo service redis-server restart
