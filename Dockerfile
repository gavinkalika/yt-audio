# Use the official Python image as the base
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /var

# Install dependencies including FFmpeg
RUN apt-get update && apt-get install -y \
    ffmpeg \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container
COPY . /var

COPY .bashrc /root/.bashrc

# Verify FFmpeg installation
RUN ffmpeg -version && ffprobe -version

# Install Python dependencies from requirements.txt
RUN pip install -r requirements.txt

# Set the default command to start a bash shell
CMD ["bash"]
