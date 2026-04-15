FROM python:3.12-slim
WORKDIR /app
# The COPY instruction copies new files or directories from <src> and adds them to the filesystem of the container at the path <dest>.
COPY . .
# RUN runs commands in the container 
RUN pip install -r requirements.txt
# The CMD instruction provides the default command to run when the container starts.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]