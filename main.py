"""
Main Entry Point - Engineering AI System
Orchestrates all services and initialization
"""

import sys
import argparse
import logging
from pathlib import Path
from logger_config import setup_logger
from config import MAIN_PC_HOST, MAIN_PC_PORT, LAPTOP_HOST, LAPTOP_PORT, GATEWAY_HOST, GATEWAY_PORT

logger = setup_logger('main', 'main.log')

def start_main_pc():
    """Start Main PC Inference Server"""
    logger.info("Starting Main PC Inference Server...")
    try:
        from main_pc_inference_server import app
        logger.info(f"Server running on {MAIN_PC_HOST}:{MAIN_PC_PORT}")
        app.run(host=MAIN_PC_HOST, port=MAIN_PC_PORT, debug=False)
    except Exception as e:
        logger.error(f"Failed to start Main PC: {e}")
        sys.exit(1)

def start_laptop():
    """Start Laptop Tool Server"""
    logger.info("Starting Laptop Tool Server...")
    try:
        from laptop_tool_server import app
        logger.info(f"Server running on {LAPTOP_HOST}:{LAPTOP_PORT}")
        app.run(host=LAPTOP_HOST, port=LAPTOP_PORT, debug=False)
    except Exception as e:
        logger.error(f"Failed to start Laptop: {e}")
        sys.exit(1)

def start_gateway():
    """Start Gateway Web Interface"""
    logger.info("Starting Gateway Web Interface...")
    try:
        from gateway_web_interface import app
        logger.info(f"Server running on {GATEWAY_HOST}:{GATEWAY_PORT}")
        app.run(host=GATEWAY_HOST, port=GATEWAY_PORT, debug=True)
    except Exception as e:
        logger.error(f"Failed to start Gateway: {e}")
        sys.exit(1)

def setup_knowledge_base():
    """Initialize knowledge base"""
    logger.info("Setting up knowledge base...")
    try:
        from knowledge_manager import KnowledgeManager
        km = KnowledgeManager()
        km.save_knowledge_bases()
        logger.info("Knowledge base initialized")
    except Exception as e:
        logger.error(f"Failed to setup knowledge base: {e}")
        sys.exit(1)

def run_tests():
    """Run system tests"""
    logger.info("Running cluster tests...")
    try:
        from test_cluster import main as test_main
        return test_main()
    except Exception as e:
        logger.error(f"Tests failed: {e}")
        return 1

def init_project():
    """Initialize project structure"""
    logger.info("Initializing project structure...")
    from config import DATA_DIR, MODEL_DIR, CACHE_DIR, LOG_DIR
    
    dirs = [DATA_DIR, MODEL_DIR, CACHE_DIR, LOG_DIR]
    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created {dir_path}")
    
    logger.info("Project structure initialized")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Engineering AI System')
    parser.add_argument('--mode', choices=['main-pc', 'laptop', 'gateway', 'test', 'init', 'kb-setup'], 
                       default='gateway', help='Service to run')
    parser.add_argument('--all', action='store_true', help='Run all services (requires separate terminals)')
    
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info("🧠 Engineering AI System - Starting")
    logger.info("=" * 60)
    
    if args.mode == 'init':
        init_project()
        return 0
    
    if args.mode == 'kb-setup':
        setup_knowledge_base()
        return 0
    
    if args.mode == 'test':
        return run_tests()
    
    if args.mode == 'main-pc':
        start_main_pc()
    
    elif args.mode == 'laptop':
        start_laptop()
    
    elif args.mode == 'gateway':
        start_gateway()
    
    elif args.all:
        logger.info("Multi-service mode: run each in separate terminal")
        print("\n📋 Run these commands in separate terminals:\n")
        print("Terminal 1 (Main PC):")
        print("  python main.py --mode main-pc\n")
        print("Terminal 2 (Laptop):")
        print("  python main.py --mode laptop\n")
        print("Terminal 3 (Gateway):")
        print("  python main.py --mode gateway\n")

if __name__ == '__main__':
    main()