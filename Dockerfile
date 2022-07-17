FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV USER_NAME=app
ENV USER_ID=1001

ENV HOME=/home/$USER_NAME
ENV APP_HOME=/home/$USER_NAME/application
ENV PYTHONPATH="${PYTHONPATH}:$HOME"

# Create `app` user and user's home directory
RUN mkdir -p $APP_HOME
RUN groupadd -g $USER_ID -r $USER_NAME && \
    useradd -u $USER_ID -r -g $USER_NAME -d $HOME -s /sbin/nologin -c "Application user" $USER_NAME
RUN chown -R $USER_NAME:$USER_NAME $HOME

# Update system
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y gcc python3-dev libpq-dev git

# Install Python, WSGI and required libraries
WORKDIR $HOME

RUN python3 -m pip install --upgrade pip
RUN python3 -m venv venv
RUN . ./venv/bin/activate

RUN pip install uwsgi

COPY ./requirements.txt $HOME
RUN pip install -r requirements.txt

# Copy application source files
COPY application/ $APP_HOME

# !!! FOR DEMONSTRATION PURPOSE ONLY! REMOVE IN PRODUCTION !!!
COPY .env $APP_HOME
# !!! FOR DEMONSTRATION PURPOSE ONLY! REMOVE IN PRODUCTION !!!

# Run DB migrations and create superuser
WORKDIR $APP_HOME

RUN python3 manage.py makemigrations
RUN python3 manage.py migrate

# !!! FOR DEMONSTRATION PURPOSE ONLY! REMOVE IN PRODUCTION !!!
COPY create_superuser.sh .
RUN chmod +x create_superuser.sh
RUN ./create_superuser.sh
# !!! FOR DEMONSTRATION PURPOSE ONLY! REMOVE IN PRODUCTION !!!

# Change user to `app`
USER $USER_NAME

# Show port that applications listens to
EXPOSE 8000

# Set command to run when container starts
# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["uwsgi", "--http", ":8000", "--module", "vehicle_manager.wsgi"]
