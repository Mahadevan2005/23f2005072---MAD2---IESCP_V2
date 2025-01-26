# IESCP - Version 2
A web application that enables sponsors to create and manage campaigns, and allows both sponsors and influencers to send and manage ad requests.

## 💻 Built with

### Backend
- **Flask**: A web framework.
- **Flask_SQLAlchemy**: Manages database operations.
- **Flask_RESTful**: Simplifies creating REST APIs.
- **Flask-Caching**: Adds caching support.
- **Celery**: Handles asynchronous tasks.
- **Redis**: Message broker and caching layer.

### Database
- **SQLite**: A lightweight database.

### Frontend
- **HTML**: For structuring web pages.
- **CSS**: Styles web pages.
- **VueJS**: Builds dynamic, reactive user interfaces.
- **Bootstrap**: For responsive and mobile-first design.
- **ChartJS**: Visualizes data through charts.

## ⚙️ Installation Steps

### 1. Clone the Repository
```bash
git clone https://github.com/Mahadevan2005/Influencer_Engagement_and_Sponsorship_Coordination_Platform_Version_2.git
```

### 2. Create & Activate Virtual Environment
- #### Create Virtual Environment
  
```bash
python -m venv venv
```

- #### Activate Virtual Environment
For Linux/macOS:
```
source venv/bin/activate
```
For Windows:
```
venv\\Scripts\\activate
```

### 3. Install Required Backend Package Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Backend
```bash
python run.py
```

### 5. Install Frontend Dependencies
In a new terminal window, install frontend dependencies:
```bash
cd frontend
npm install
```

### 7. Run the Frontend Development Server
```bash
npm run serve
```

### 8. Setup Redis
Make sure Redis is installed and running. You can start Redis using:
```bash
redis-server
```

### 9. Run Celery Worker
In a new terminal window, run the Celery worker:
```bash
celery -A app:celery_app worker -l INFO
```

### 10. Run Celery Beat
In another terminal window, run the Celery Beat scheduler:
```bash
celery -A app:celery_app beat -l INFO
```


### 11. Run MailHog
In another terminal window, run the MailHog to see mail functionality:
```bash
~/go/bin/MailHog
```

🌟 You are all set!
<hr>

## 📸 Screenshots
![Home Page 1](https://github.com/user-attachments/assets/01bd0a37-93d4-40a2-9541-19cb7c9324bb)
![Home Page 2](https://github.com/user-attachments/assets/a863f1bd-6993-41aa-a0e0-0680c276bd54)
![Admin Login](https://github.com/user-attachments/assets/bdee7bc3-3eea-43d3-a6fd-9dfffc414ab2)
![Sponsor Dashboard](https://github.com/user-attachments/assets/f0c502b3-c802-4c76-ace9-d3e702f8d592)
![Sponsor Stats](https://github.com/user-attachments/assets/6023ea1e-9511-4676-ba54-f1a25955539f)
![New Campaign](https://github.com/user-attachments/assets/3aa6fdb0-ae2a-47f1-a93c-36dfc3913292)
![Influencer Dashboard](https://github.com/user-attachments/assets/56e4aa43-4b2c-4590-a601-428e42b6a628)
![Admin Dashboard](https://github.com/user-attachments/assets/5660057d-d09a-4381-bb62-5d525230944a)
![Influencer Requests](https://github.com/user-attachments/assets/7208f334-94a4-4afb-a031-8c05f0b39e6c)
![Campaign Requests](https://github.com/user-attachments/assets/9fd386e9-1f3e-496c-b9c3-75dfe4ee7375)
![Sponsor Requests](https://github.com/user-attachments/assets/a4553849-b6e8-4337-953c-f2360d16e9d6)

<hr>
<h3 align="center">
Thank You ❤️
</h3>
