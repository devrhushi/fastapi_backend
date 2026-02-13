FROM python:3.14-slim

WORKDIR /usr/src/app

# ./ tells where to copy ./ is usr/sr/app without ./ u have to speccify whole path
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#we have to write two times copy so if no change in requiremnet that step can be skipped because it takes time and it will be cached

# to run the app following command
# This tells Docker to run migrations first, then start the server
CMD sh -c "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"
