FROM archlinux:latest

# Update system and install required packages
RUN pacman -Sy --noconfirm archiso git base-devel

# Set working directory
WORKDIR /build

# Copy the build script
COPY linux/build_scripts/build_iso.sh /build/

# Make the script executable
RUN chmod +x /build/build_iso.sh

# Set entrypoint
ENTRYPOINT ["/build/build_iso.sh"]
