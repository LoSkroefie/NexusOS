#!/bin/bash

# Prepare build environment for NexusOS

# Create necessary directories
mkdir -p /build/iso
mkdir -p /build/work
mkdir -p /build/out

# Install additional required packages
pacman -Sy --noconfirm \
    arch-install-scripts \
    squashfs-tools \
    libisoburn \
    dosfstools \
    lynx \
    archiso

# Copy NexusOS files
mkdir -p /build/nexusos
cp -r /nexusos/* /build/nexusos/

# Create custom pacman.conf
cat > /build/pacman.conf << EOF
[options]
HoldPkg     = pacman glibc
Architecture = auto
CheckSpace
SigLevel    = Required DatabaseOptional
LocalFileSigLevel = Optional

[core]
Include = /etc/pacman.d/mirrorlist

[extra]
Include = /etc/pacman.d/mirrorlist

[community]
Include = /etc/pacman.d/mirrorlist
EOF

echo "Build environment prepared successfully!"
