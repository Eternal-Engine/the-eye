# Pull official base image
FROM python:3.10.1-slim-buster

# Set working directory
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV VIRTUAL_ENV=/opt/venv

# Start venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Point the server port
EXPOSE 8000

# Install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc postgresql \
  && apt-get clean

# Install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Add app
COPY . .

# Add entrypoint.sh
COPY ./entrypoint.sh .
RUN chmod +x /usr/src/app/entrypoint.sh

# Run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

# Execute alembic and start up the server
CMD alembic upgrade head \
  && uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8000
