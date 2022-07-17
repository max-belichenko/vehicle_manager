FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV USER_NAME=app
ENV USER_ID=1001

ENV HOME=/home/$USER_NAME
ENV APP_HOME=/home/$USER_NAME/application
ENV PYTHONPATH="${PYTHONPATH}:$HOME"

# Update system
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y gcc python3-dev libpq-dev git build-essential

# Set up virtual environment
WORKDIR $HOME

RUN python3 -m venv venv
RUN . ./venv/bin/activate
RUN python3 -m pip install --upgrade pip

# Install uWSGI application server
RUN pip install uwsgi

# Install required application libs
COPY ./requirements.txt $HOME
RUN pip install -r requirements.txt

# Copy application files
RUN mkdir -p $APP_HOME
COPY application/ $APP_HOME
# !!! NEXT LINE IS FOR DEMONSTRATION PURPOSE ONLY! REMOVE IN PRODUCTION !!!
COPY .env $APP_HOME

# Make database migrations
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate

# Create superuser (REMOVE IN PRODUCTION)
# !!! NEXT LINE IS FOR DEMONSTRATION PURPOSE ONLY! REMOVE IN PRODUCTION !!!
COPY create_superuser.sh .
# !!! NEXT LINE IS FOR DEMONSTRATION PURPOSE ONLY! REMOVE IN PRODUCTION !!!
RUN sed -i -e 's/\r$//' create_superuser.sh
# !!! NEXT LINE IS FOR DEMONSTRATION PURPOSE ONLY! REMOVE IN PRODUCTION !!!
RUN ./create_superuser.sh

# Add `app` system user to use in Docker container
RUN groupadd -g $USER_ID -r $USER_NAME && \
    useradd -u $USER_ID -r -g $USER_NAME -d $HOME -s /sbin/nologin -c "Application user" $USER_NAME
RUN chown -R $USER_NAME:$USER_NAME $HOME

# Set container state before launch application
USER $USER_NAME
WORKDIR $APP_HOME
EXPOSE 8000

# Set command to run when container starts
CMD ["uwsgi", "--http", ":8000", "--module", "vehicle_manager.wsgi"]
