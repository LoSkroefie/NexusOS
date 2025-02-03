#!/bin/bash

# NexusOS Linux Distribution Build Script
set -e

# Configuration
WORK_DIR="/build/nexusos_build"
ISO_NAME="NexusOS-$(date +%Y%m%d).iso"
PROFILE_DIR="${WORK_DIR}/profile"

# Create working directory
mkdir -p "${WORK_DIR}"
cd "${WORK_DIR}"

echo "Creating profile directory..."
# Create profile directory
cp -r /usr/share/archiso/configs/releng "${PROFILE_DIR}"

echo "Customizing packages..."
# Create custom package list with only essential packages
cat > "${PROFILE_DIR}/packages.x86_64" << EOF
# Base system
base
linux
linux-firmware
grub
efibootmgr
networkmanager
sudo
syslinux
memtest86+
memtest86+-efi
edk2-shell

# Desktop environment
xorg-server
xorg-xinit
openbox
alacritty

# Audio
pulseaudio
pulseaudio-alsa

# Development tools
python
python-pip
git
wget
curl
python-virtualenv

# Additional utilities
vim
nano
htop
neofetch
docker
ollama
EOF

echo "Adding NexusOS files..."
# Add NexusOS files
mkdir -p "${PROFILE_DIR}/airootfs/opt/nexusos"
if [ -d "/nexusos/src" ]; then
    cp -r /nexusos/src "${PROFILE_DIR}/airootfs/opt/nexusos/"
    cp -r /nexusos/requirements.txt "${PROFILE_DIR}/airootfs/opt/nexusos/"
else
    echo "Warning: NexusOS source directory not found"
fi

echo "Creating pip requirements file..."
# Create pip requirements file
mkdir -p "${PROFILE_DIR}/airootfs/opt/nexusos/venv"

echo "Configuring system services..."
# Configure system
mkdir -p "${PROFILE_DIR}/airootfs/etc/systemd/system"

# Create Ollama service
cat > "${PROFILE_DIR}/airootfs/etc/systemd/system/ollama.service" << EOF
[Unit]
Description=Ollama AI Service
After=network.target

[Service]
ExecStart=/usr/bin/ollama serve
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOF

# Create NexusOS service
cat > "${PROFILE_DIR}/airootfs/etc/systemd/system/nexusos.service" << EOF
[Unit]
Description=NexusOS AI Shell
After=ollama.service
Requires=ollama.service

[Service]
ExecStart=/opt/nexusos/venv/bin/python /opt/nexusos/src/main.py
Environment=DISPLAY=:0
Environment=PYTHONPATH=/opt/nexusos/src
Environment=OLLAMA_HOST=localhost:11434
Restart=always
User=nexusos

[Install]
WantedBy=multi-user.target
EOF

# Create user setup script
cat > "${PROFILE_DIR}/airootfs/root/setup.sh" << EOF
#!/bin/bash
set -e

# Create nexusos user
useradd -m -G wheel -s /bin/bash nexusos
echo "nexusos:nexusos" | chpasswd
echo "nexusos ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers.d/nexusos

# Set up Python virtual environment
cd /opt/nexusos
python -m venv venv
source venv/bin/activate
pip install --no-cache-dir -r requirements.txt

# Enable services
systemctl enable NetworkManager
systemctl enable ollama
systemctl enable nexusos

# Set up auto-login
mkdir -p /etc/systemd/system/getty@tty1.service.d/
cat > /etc/systemd/system/getty@tty1.service.d/override.conf << EOL
[Service]
ExecStart=
ExecStart=-/usr/bin/agetty --autologin nexusos --noclear %I \$TERM
EOL

# Configure .xinitrc for the nexusos user
cat > /home/nexusos/.xinitrc << EOL
#!/bin/sh
exec openbox-session
EOL

chown nexusos:nexusos /home/nexusos/.xinitrc
chmod +x /home/nexusos/.xinitrc
EOF

chmod +x "${PROFILE_DIR}/airootfs/root/setup.sh"

echo "Building ISO..."
# Build the ISO
mkdir -p "${WORK_DIR}/out"
mkarchiso -v -w "${WORK_DIR}/work" -o "${WORK_DIR}/out" "${PROFILE_DIR}"

echo "ISO build complete! Output available at: ${WORK_DIR}/out/${ISO_NAME}"
