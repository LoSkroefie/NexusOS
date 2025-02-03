# Use Arch Linux as base
FROM archlinux:latest

# Install required packages for building
RUN pacman -Sy --noconfirm \
    base-devel \
    archiso \
    git \
    python \
    python-pip \
    grub \
    xorriso \
    mtools \
    dosfstools \
    arch-install-scripts \
    squashfs-tools \
    wget \
    curl \
    efibootmgr \
    && rm -rf /var/cache/pacman/pkg/*

# Set working directory
WORKDIR /build

# Copy build scripts
COPY build_scripts /build/scripts
RUN chmod +x /build/scripts/build_iso.sh

# Create output directory
RUN mkdir -p /output

# Set entrypoint
ENTRYPOINT ["/build/scripts/build_iso.sh"]
