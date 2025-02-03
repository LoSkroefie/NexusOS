# NexusOS - AI-Powered Operating System

## Overview
NexusOS is a revolutionary AI-powered operating system that combines advanced artificial intelligence with traditional OS capabilities. Built on top of Arch Linux, it features NexusAI - an intelligent system core that can generate and execute commands dynamically.

## Version
Current Version: 0.1.0 (2025-02-03)
- First bootable ISO release
- Complete AI integration with Ollama
- Full desktop environment support
- Voice command capabilities

## Key Features
- 🤖 NexusAI Core - AI-powered system management and automation
- 🖥️ Futuristic GUI Terminal with real-time system monitoring
- 🔧 Dynamic command generation and execution
- 🎯 Voice and text command interface
- 📊 Real-time system monitoring and optimization
- 🔐 AI-powered security and system management

## System Requirements
- x86_64 architecture
- 4GB RAM minimum (8GB recommended)
- 20GB disk space
- UEFI or BIOS boot support
- Internet connection for AI features

## Quick Start

### Option 1: Download ISO
1. Download the latest ISO from our releases page
2. Create a bootable USB or DVD
3. Boot from the installation media
4. Login with default credentials:
   - Username: nexusos
   - Password: nexusos

### Option 2: Build from Source
Requirements:
- Docker
- bash
- git
- 10GB+ free disk space
- 4GB+ RAM

```bash
# Clone the repository
git clone https://github.com/LoSkroefie/NexusOS.git
cd NexusOS

# Build using Docker
docker run --rm -it \
  --privileged \
  -v "$(pwd):/nexusos" \
  -v "$(pwd)/output:/output" \
  archlinux:latest \
  /nexusos/linux/build_scripts/build_iso.sh
```

The ISO will be created in the `output` directory.

## Components
1. NexusAI Core - The AI-powered system daemon
2. NexusAI Terminal - Futuristic GUI terminal interface
3. NexusAI Shell - AI-enhanced command-line interface
4. System Monitor - Real-time system statistics and optimization

## Development

### Repository Structure
```
nexusos/
├── src/                    # Source code
│   ├── nexus_core/        # AI and system core
│   └── nexus_terminal/    # GUI terminal
├── linux/                  # Build scripts and configs
├── docs/                   # Documentation
└── tests/                 # Test suites
```

### Building and Testing
```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Build documentation
cd docs && make html
```

## Contributing
1. Fork the repository on GitHub
2. Create your feature branch
3. Commit your changes
4. Push to your branch
5. Create a Pull Request

## License
NexusOS is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Support
- [Issue Tracker](https://github.com/LoSkroefie/NexusOS/issues)
- [Documentation](https://github.com/LoSkroefie/NexusOS/wiki)
- [Wiki](https://github.com/LoSkroefie/NexusOS/wiki)

## Acknowledgments
- Built on Arch Linux
- Uses Ollama for AI capabilities
- OpenBox for desktop environment
- PyQt6 for GUI components
