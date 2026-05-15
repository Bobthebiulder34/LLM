"""
Quick Start Guide - Interactive Setup
"""

import os
import sys
from pathlib import Path
from config import MAIN_PC_HOST, MAIN_PC_PORT, LAPTOP_HOST, LAPTOP_PORT, GATEWAY_HOST, GATEWAY_PORT
from logger_config import setup_logger
from utils import ClusterManager, format_response

logger = setup_logger('quickstart', 'quickstart.log')

def print_banner():
    """Print welcome banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║       🧠 Engineering AI System - Quick Start Guide        ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_environment():
    """Check system requirements"""
    print("\n📋 Checking environment...")
    
    checks = {
        'Python 3.10+': sys.version_info >= (3, 10),
        'Config loaded': os.path.exists('config.py'),
        'Utils loaded': os.path.exists('utils.py'),
    }
    
    for check, status in checks.items():
        symbol = "✓" if status else "✗"
        print(f"  {symbol} {check}")
    
    return all(checks.values())

def print_network_info():
    """Print network configuration"""
    print("\n🌐 Network Configuration:")
    print(f"  Main PC:   {MAIN_PC_HOST}:{MAIN_PC_PORT}")
    print(f"  Laptop:    {LAPTOP_HOST}:{LAPTOP_PORT}")
    print(f"  Gateway:   {GATEWAY_HOST}:{GATEWAY_PORT}")

def test_cluster():
    """Test cluster connectivity"""
    print("\n🔍 Testing Cluster Connectivity...")
    
    manager = ClusterManager()
    status = manager.check_cluster_status()
    
    for service, online in status.items():
        symbol = "✓ ONLINE" if online else "✗ OFFLINE"
        print(f"  {service}: {symbol}")
    
    return all(status.values())

def interactive_demo():
    """Interactive demo"""
    print("\n💬 Interactive Demo")
    print("="*60)
    print("Try asking engineering questions!")
    print("Example domains: pcb, cnc, cad, electronics")
    print("Type 'quit' to exit\n")
    
    manager = ClusterManager()
    
    while True:
        try:
            domain = input("Domain [pcb/cnc/cad/electronics]: ").strip().lower() or 'general'
            query = input("Question: ").strip()
            
            if query.lower() == 'quit':
                break
            
            if not query:
                continue
            
            print("\n⏳ Processing...")
            result = manager.run_full_workflow(query, domain)
            print(format_response(result))
        
        except KeyboardInterrupt:
            break
        except Exception as e:
            logger.error(f"Demo error: {e}")
            print(f"Error: {e}")

def print_quick_commands():
    """Print quick command reference"""
    print("\n⚡ Quick Commands:")
    print("="*60)
    print("\n1. Initialize project:")
    print("   python main.py --mode init")
    print("\n2. Setup knowledge base:")
    print("   python main.py --mode kb-setup")
    print("\n3. Run tests:")
    print("   python main.py --mode test")
    print("\n4. Start services (separate terminals):")
    print("   Terminal 1: python main.py --mode main-pc")
    print("   Terminal 2: python main.py --mode laptop")
    print("   Terminal 3: python main.py --mode gateway")
    print("\n5. Run this quickstart again:")
    print("   python quickstart.py")

def main():
    """Main quickstart flow"""
    print_banner()
    
    if not check_environment():
        print("\n❌ Environment check failed!")
        sys.exit(1)
    
    print_network_info()
    
    cluster_ok = test_cluster()
    
    if not cluster_ok:
        print("\n⚠️  Some services are offline.")
        print("Make sure all services are running in separate terminals!")
    
    print_quick_commands()
    
    if cluster_ok:
        try:
            response = input("\n🚀 Start interactive demo? (y/n): ").strip().lower()
            if response == 'y':
                interactive_demo()
        except KeyboardInterrupt:
            print("\n\nGoodbye!")

if __name__ == '__main__':
    main()