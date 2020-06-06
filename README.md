# StartupMatch API

This is a repository containing the Backedn PR's for Founders' StartupMatch website. StartupMatch is a Job Board application determined to find good student-company fits for startups that are hiring at UIUC.

The backend is written using the Django REST Framework, using Google's CloudSQL backend to store data and being consumed by a React frontend. To see more of the frontend, go to [this fork](https://github.com/SirajChokshi/startup-job-board/tree/frontend-backend/backend/frontend).

## Getting Started

To run the API locally, make sure you have authentication credentials with our Google Cloud project. Also make sure you have the Google Cloud Proxy installed as well as the Google Cloud SDK. For running without accessing the Google server, make sure you have Python3 installed and the latest version of Django.

### Prerequisites

Install requirements using the following

```
pip install -r requirements.txt
```

### Installing

Once you have the dependencies installed, clone or fork the repository. Start the google cloud proxy before continuing. If not using the google database and instead using a local MySQL db, update the `settings.py` file to point to that sql backend instead of the Google CloudSQL backend.

Start the server by running:
```
python manage.py runserver
```

And navigate to localhost:8000 to see if it worked!

Official API Documentation can be found in the `backend/` folder's README.

## Deployment

Deployment is still in progress with this particular API, but a hosting service like Heroku or DigitalOcean is preferred. In the Dockerfile be sure to specify that the Cloud SQL Proxy should be started (and gcloud auth should be set) before starting the server.

## Built With

* [Django](https://www.djangoproject.com/) - The API Framework used
* [Python 3.7](https://www.python.org/downloads/release/python-370/) - Dependency Management
* [Google Cloud Platform](https://cloud.google.com/sql) - Cloud Database Hosting

## Contributing

This project is not yet available for contributing, nor are we currently accepting PR's from outside the organization.

## Authors

* **Davis Keene** - *Backend* - [Website](https://daviskeene.com)
* **Siraj Chokshi** - *Frontend* - [Website](https://sirajchokshi.com)

See also the list of [contributors](https://github.com/Illinois-Founders/startup-job-board/contributors) who participated in this project.

## License

No applicable license yet.

## Acknowledgments

Thank you to [Jordan Campbell](https://www.linkedin.com/in/jordan-campbell-733621102) for pioneering this project.
