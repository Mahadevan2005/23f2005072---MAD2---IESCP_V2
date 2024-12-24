# frontend

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

### backend server
python3 app.py

### node modules
npm install

### to create venv in wsl
python3 -m venv env_name

### to activate the venv in wsl
source env_name/bin/activate


### to start the celery worker
celery -A app:celery_app worker -l INFO

### to start the celery beat
celery -A app:celery_app beat -l INFO

### to start the mailhog 
~/go/bin/MailHog

### to restart if any pblm in celery 
sudo service redis-server restart