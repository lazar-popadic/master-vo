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

RUN sudo apt-get update && \
    sudo apt-get install -y \
    neovim \
    btop \
    ranger \
    && sudo apt-get clean

# X11 and GUI libraries
RUN sudo apt-get update && \
    sudo apt-get install -y \
    x11-apps \
    xauth \
    libx11-6 \
    libxext6 \
    libxrender1 \
    libxtst6 \
    libxi6 \
    libxkbcommon-x11-0 \
    libgl1-mesa-dri \
    libglx-mesa0 \
    mesa-utils \
    dbus-x11 \
    && sudo apt-get clean

# GTK support for GUI apps
RUN sudo apt-get update && \
    sudo apt-get install -y \
    libgtk-3-0 \
    libgtk-3-bin \
    libcanberra-gtk3-module \
    && sudo apt-get clean

# Qt support for GUI apps
RUN sudo apt-get update && \
    sudo apt-get install -y \
    libqt5core5a \
    libqt5gui5 \
    libqt5widgets5 \
    qt5-gtk-platformtheme \
    && sudo apt-get clean

# Python GUI dependencies
RUN sudo apt-get update && \
    sudo apt-get install -y \
    python3-tk \
    python3-pyqt5 \
    && sudo apt-get clean

# SVO specific
RUN sudo apt install -y \
    libboost-all-dev \
    libeigen3-dev 
RUN sudo apt-get update && \
    sudo apt-get install -y \
    python3-opencv \
    libopencv-dev \
    && sudo apt-get clean
RUN sudo apt-get update && \
    sudo apt-get install -y \
    python3-pip \
    python3-dev \
    && sudo apt-get clean && \
    pip3 install opencv-python opencv-contrib-python --break-system-packages
RUN sudo apt-get update && \
    sudo apt-get install -y \
    libopencv-core-dev \
    libopencv-imgproc-dev \
    libopencv-highgui-dev \
    libopencv-calib3d-dev \
    libopencv-features2d-dev \
    libopencv-video-dev \
    libopencv-videoio-dev \
    cmake \
    g++ \
    libsuitesparse-dev \
    qt5-qmake \
    libqglviewer-dev-qt5 \
    python3-venv \
    && sudo apt-get clean

# Set the default command
CMD ["/bin/bash"]
