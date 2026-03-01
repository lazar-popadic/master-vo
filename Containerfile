FROM docker.io/ubuntu:24.04

# Set environment variables to avoid interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Update package lists and install basic utilities
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y \
    curl \
    wget \
    git \
    vim \
    nano \
    htop \
    net-tools \
    iputils-ping \
    build-essential \
    software-properties-common \
    apt-utils \
    sudo \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Give ubuntu user passwordless sudo
RUN echo "ubuntu ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/ubuntu && \
    chmod 0440 /etc/sudoers.d/ubuntu

# Create mount point for workspace and set proper ownership
RUN mkdir -p /workspace && \
    chown -R ubuntu:ubuntu /workspace

# Set working directory
WORKDIR /workspace

# Switch to ubuntu user
USER ubuntu

# Set locale
RUN sudo apt-get update && \
    sudo apt-get install -y locales && \
    sudo locale-gen en_US.UTF-8 && \
    sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8

# Set the default command
CMD ["/bin/bash"]
