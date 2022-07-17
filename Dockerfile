# ARG DJANGO_ALLOWED_HOSTS
# ARG DJANGO_SECRET_KEY
# ARG DJANGO_CORS_ORIGIN_WHITELIST
#
# ENV DJANGO_ALLOWED_HOSTS $DJANGO_ALLOWED_HOSTS
# ENV DJANGO_SECRET_KEY $DJANGO_SECRET_KEY
# ENV DJANGO_CORS_ORIGIN_WHITELIST $DJANGO_CORS_ORIGIN_WHITELIST
#
# RUN mkdir /backend
# WORKDIR /backend
# COPY requirements.txt /backend/
# EXPOSE 8000
# RUN pip install -r requirements.txt
# COPY . /backend/


FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV USER_NAME=app
ENV USER_ID=1001

ENV HOME=/home/$USER_NAME
ENV APP_HOME=/home/$USER_NAME/application
ENV PYTHONPATH="${PYTHONPATH}:$HOME"

# Create user and user's home directory
RUN mkdir -p $APP_HOME
RUN groupadd -g $USER_ID -r $USER_NAME && \
    useradd -u $USER_ID -r -g $USER_NAME -d /home/$USER_NAME -s /sbin/nologin -c "Application user" $USER_NAME

# Assign access rights to user
RUN chown -R $USER_NAME:$USER_NAME $APP_HOME

# Update system
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y gcc python3-dev libpq-dev git

# Install python and required libraries
RUN python3 -m pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy source files
COPY application/ $APP_HOME

# Set working directory
WORKDIR $APP_HOME

# Change current user
USER $USER_NAME

# Show port that applications listens to
EXPOSE 8000

# Run DB migrations
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
COPY create_superuser.sh .
RUN ./create_superuser.sh

# Set command to run when container starts. You can add parameters to the cmd list after the command
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
