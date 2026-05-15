# Engineering AI System - Quick Start

## 🚀 Quick Start (3 Steps)

### 1. Initialize Project
```bash
python main.py --mode init
```

### 2. Setup Knowledge Base
```bash
python main.py --mode kb-setup
```

### 3. Run Services
Open 3 terminals:

**Terminal 1 - Main PC (Inference)**
```bash
python main.py --mode main-pc
```

**Terminal 2 - Laptop (Tools)**
```bash
python main.py --mode laptop
```

**Terminal 3 - Gateway (Web UI)**
```bash
python main.py --mode gateway
```

Then visit: `http://localhost:5000`

## 💻 Command Line Usage

### Ask Questions
```bash
# Simple question
python cli.py ask "What is PCB trace width?"

# With domain expertise
python cli.py ask "Trace sizing for 5A current" --domain pcb

# Custom token limit
python cli.py ask "Explain G-code" --domain cnc --tokens 1024
```

### Engineering Tools

**PCB Design**
```bash
python cli.py tool pcb trace-width --current 5 --temp 45 --copper 1
```

**CNC Machining**
```bash
python cli.py tool cnc rpm --sfm 400 --diameter 0.5
python cli.py tool cnc feed --rpm 1500 --teeth 4 --chip-load 0.008
```

**Electronics**
```bash
python cli.py tool electronics ohms --voltage 12 --resistance 1000
```

### Check Status
```bash
python cli.py status
```

## 🎯 Interactive Demo

```bash
python quickstart.py
```

This will:
- ✓ Check your environment
- ✓ Show network config
- ✓ Test cluster connectivity
- ✓ Launch interactive demo

## 📁 Project Structure

```
LLM/
├── main.py                      # Main entry point
├── config.py                    # Configuration
├── utils.py                     # Utility functions
├── cli.py                       # Command line interface
├── quickstart.py                # Interactive setup
├── main_pc_inference_server.py  # Inference service
├── laptop_tool_server.py        # Tools service
├── laptop_data_prep.py          # Data preparation
├── gateway_web_interface.py     # Web interface
├── rag_system.py                # RAG implementation
├── engineering_tools.py         # Engineering calculations
├── knowledge_manager.py         # Knowledge base management
├── logger_config.py             # Logging setup
├── test_cluster.py              # System tests
├── templates/
│   └── dashboard.html           # Web UI
├── data/                        # Data storage
├── models/                      # Model storage
├── logs/                        # Log files
└── requirements.txt             # Dependencies
```

## 🔧 Configuration

Edit `.env` file to customize:
```
MAIN_PC_HOST=192.168.1.100
MAIN_PC_PORT=5001
LAPTOP_HOST=192.168.1.200
LAPTOP_PORT=5000
GATEWAY_HOST=192.168.1.50
GATEWAY_PORT=5000
```

## 🧪 Testing

```bash
# Run all tests
python main.py --mode test

# Run health checks
python cli.py health
```

## 📊 Supported Domains

- **PCB**: Trace width, via sizing, impedance, layer stackup
- **CNC**: RPM, feed rate, tool recommendations
- **CAD**: DFM principles, tolerance, assembly
- **Electronics**: Ohm's Law, power, RC circuits, component selection

## 🔗 Endpoints

| Service | Port | Endpoint |
|---------|------|----------|
| Main PC | 5001 | /api/inference |
| Laptop  | 5000 | /api/tool/* |
| Gateway | 5000 | / (web), /api/chat |

## 📝 Troubleshooting

**Services offline?**
- Check IPs in `.env` match your network
- Firewall rules allow ports 5000-5001
- All services in separate terminals

**Slow inference?**
- CPU inference is normal (5-10 tokens/sec)
- For GPU, modify config.py DEVICE='cuda'

**No response?**
- Check logs: `logs/*.log`
- Verify model downloaded: `models/`
- Run `python cli.py status`

## 📚 Learn More

- **Architecture**: See `ARCHITECTURE.md`
- **API Docs**: See `gateway_web_interface.py`
- **Setup**: See `SETUP.md`
- **Contributing**: See `CONTRIBUTING.md`