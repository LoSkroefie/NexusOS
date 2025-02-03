# NexusOS - AI-Powered Operating System

## Overview
NexusOS is a revolutionary AI-powered operating system that combines advanced artificial intelligence with traditional OS capabilities. Built on top of Linux, it features NexusAI - an intelligent system core that can generate and execute commands dynamically.

## Key Features
- 🤖 NexusAI Core - AI-powered system management and automation
- 🖥️ Futuristic GUI Terminal with real-time system monitoring
- 🔧 Dynamic command generation and execution
- 🎯 Voice and text command interface
- 📊 Real-time system monitoring and optimization
- 🔐 AI-powered security and system management

## Components
1. NexusAI Core - The AI-powered system daemon
2. NexusAI Terminal - Futuristic GUI terminal interface
3. NexusAI Shell - AI-enhanced command-line interface
4. System Monitor - Real-time system statistics and optimization

## Linux Distribution

NexusOS is now available as a complete Linux distribution! The distribution is based on Arch Linux and includes:

- Pre-configured AI shell environment
- Ollama AI service
- Optimized system settings
- Beautiful desktop environment
- Voice command support out of the box

### Building the ISO

Requirements:
- Docker
- bash
- git
- At least 10GB of free disk space
- 4GB+ RAM recommended

Steps:

1. Clone the repository:
```bash
git clone https://github.com/yourusername/NexusOS.git
cd NexusOS
```

2. Build the ISO using Docker:
```bash
# Make the build script executable
chmod +x linux/build_scripts/build_iso.sh

# Run the build script in Docker
docker run --rm -it \
  --privileged \
  -v "$(pwd):/nexusos" \
  -v "$(pwd)/output:/output" \
  archlinux:latest \
  /nexusos/linux/build_scripts/build_iso.sh
```

The ISO will be created in the `output` directory.

### Testing the ISO

You can test the ISO using VirtualBox or QEMU:

#### Using VirtualBox
1. Create a new Virtual Machine
2. Select "Other Linux (64-bit)" as the type
3. Allocate at least 4GB RAM
4. Create a virtual hard disk (20GB+ recommended)
5. Mount the ISO and boot
6. Login with:
   - Username: nexusos
   - Password: nexusos

#### Using QEMU
```bash
qemu-system-x86_64 \
  -m 4G \
  -enable-kvm \
  -cdrom output/NexusOS-*.iso \
  -boot d
```

### Default Credentials
- Username: nexusos
- Password: nexusos
- Root password: nexusos

### Features Available After Installation
- NexusAI Terminal (press Ctrl+Alt+T)
- Voice Commands (click microphone icon or press Ctrl+Shift+V)
- System Monitor (click system tray icon)
- Ollama AI Service (pre-configured and running)

### Troubleshooting

If you encounter any issues:

1. Check system requirements
2. Verify SHA256 checksum of the ISO
3. Enable virtualization in BIOS if using VirtualBox/QEMU
4. Check logs in `/var/log/nexusos.log`

For more detailed troubleshooting, see our [Wiki](https://github.com/yourusername/NexusOS/wiki).

## Installation
```bash
# Coming soon
```

## Development Status
- ✅ Core AI System (In Progress)
- ✅ GUI Terminal (In Development)
- ⏳ System Integration (Planned)
- ⏳ Full OS Integration (Planned)

## Requirements
- Python 3.9+
- Ollama (Local AI model)
- PyQt6
- Linux-based system

## Development

### Requirements

- Python 3.8+
- PyQt6
- Ollama AI
- Additional requirements in `requirements.txt`

### Setup Development Environment

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install Ollama:
```bash
# Linux
curl -L https://ollama.ai/download/ollama-linux-amd64 -o ollama
chmod +x ollama
sudo mv ollama /usr/local/bin/

# Start Ollama service
ollama serve
```

3. Run NexusOS:
```bash
python src/main.py
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

NexusOS is licensed under the MIT License. See [LICENSE](LICENSE) for details.
