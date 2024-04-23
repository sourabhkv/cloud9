# Use the official Python 3.11 image on Ubuntu as a base image  
FROM python:3.11  
  
# Set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1  
ENV PYTHONUNBUFFERED 1  
  
# Create and set the working directory  
WORKDIR /drive  
  
# Copy the current directory contents into the container at /drive  
COPY ./drive /drive/  
  
# Install yt-dlp by downloading the binary and making it executable  
RUN curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp \  
    && chmod a+rx /usr/local/bin/yt-dlp  
  
# Install ffmpeg using the package manager  
RUN apt-get update \  
    && apt-get install -y ffmpeg \  
    && rm -rf /var/lib/apt/lists/*  
  
# Copy the requirements file into the container at /drive  
# Install any needed packages specified in requirements.txt  
RUN pip install --no-cache-dir -r requirements.txt  
  
# Expose the port the app runs on  
EXPOSE 80  
  
# Run django development server  
CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]  
