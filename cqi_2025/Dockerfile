# Use the official Python image from the Docker Hub
FROM python:3.10-slim

RUN pip install requests flask Pillow numpy


# Copy the current directory contents into the container at /app
COPY . .

# Run app.py when the container launches
CMD ["python", "app.py"]