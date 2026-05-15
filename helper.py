"""
Utility functions and helpers
"""

import os
import json
import requests
from typing import Dict, List, Any, Optional
from config import MAIN_PC_URL, LAPTOP_URL, GATEWAY_URL, INFERENCE_TIMEOUT, TOOL_TIMEOUT
from logger_config import setup_logger

logger = setup_logger('utils', 'utils.log')

class ServiceClient:
    """Client for communicating with cluster services"""
    
    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url
        self.timeout = timeout
    
    def health_check(self) -> bool:
        """Check if service is online"""
        try:
            response = requests.get(f'{self.base_url}/health', timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def post(self, endpoint: str, data: Dict) -> Optional[Dict]:
        """Send POST request to service"""
        try:
            url = f'{self.base_url}{endpoint}'
            response = requests.post(url, json=data, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"POST {endpoint} error: {e}")
            return None
    
    def get(self, endpoint: str) -> Optional[Dict]:
        """Send GET request to service"""
        try:
            url = f'{self.base_url}{endpoint}'
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"GET {endpoint} error: {e}")
            return None

class InferenceClient(ServiceClient):
    """Client for Main PC inference"""
    
    def __init__(self):
        super().__init__(MAIN_PC_URL, INFERENCE_TIMEOUT)
    
    def infer(self, prompt: str, context: str = '', max_tokens: int = 512) -> Optional[str]:
        """Run inference"""
        data = {
            'prompt': prompt,
            'context': context,
            'max_tokens': max_tokens
        }
        result = self.post('/api/inference', data)
        return result['response'] if result else None

class ToolClient(ServiceClient):
    """Client for Laptop tool calculations"""
    
    def __init__(self):
        super().__init__(LAPTOP_URL, TOOL_TIMEOUT)
    
    def pcb_trace_width(self, current_amps: float, temp_rise_c: float = 45, copper_oz: float = 1) -> Optional[float]:
        """Calculate PCB trace width"""
        data = {'current_amps': current_amps, 'temp_rise_c': temp_rise_c, 'copper_oz': copper_oz}
        result = self.post('/api/tool/pcb/trace-width', data)
        return result['trace_width_mil'] if result else None
    
    def cnc_rpm(self, sfm: float, diameter: float) -> Optional[int]:
        """Calculate CNC RPM"""
        data = {'surface_feet_per_min': sfm, 'tool_diameter_inches': diameter}
        result = self.post('/api/tool/cnc/rpm', data)
        return result['rpm'] if result else None
    
    def ohms_law(self, voltage: Optional[float] = None, current: Optional[float] = None, resistance: Optional[float] = None) -> Optional[Dict]:
        """Calculate using Ohm's Law"""
        data = {}
        if voltage is not None:
            data['voltage'] = voltage
        if current is not None:
            data['current'] = current
        if resistance is not None:
            data['resistance'] = resistance
        
        return self.post('/api/tool/electronics/ohms-law', data)

class ClusterManager:
    """Manage cluster operations"""
    
    def __init__(self):
        self.inference_client = InferenceClient()
        self.tool_client = ToolClient()
        self.logger = logger
    
    def check_cluster_status(self) -> Dict[str, bool]:
        """Check status of all services"""
        return {
            'main_pc': self.inference_client.health_check(),
            'laptop': self.tool_client.health_check(),
            'gateway': self._check_gateway()
        }
    
    def _check_gateway(self) -> bool:
        """Check gateway status"""
        try:
            response = requests.get(f'{GATEWAY_URL}/api/status', timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def run_full_workflow(self, query: str, domain: str = 'general') -> Dict[str, Any]:
        """Run complete workflow"""
        self.logger.info(f"Processing query: {query}")
        
        # Build domain context
        contexts = {
            'pcb': "You are an expert PCB designer.",
            'cnc': "You are an expert CNC machinist.",
            'cad': "You are an expert CAD/CAM engineer.",
            'electronics': "You are an expert electronics engineer."
        }
        context = contexts.get(domain, "You are a helpful engineering assistant.")
        
        # Run inference
        response = self.inference_client.infer(query, context)
        
        return {
            'query': query,
            'domain': domain,
            'response': response,
            'status': 'success' if response else 'failed'
        }

def format_response(response: Dict[str, Any]) -> str:
    """Format response for display"""
    output = f"\n{'='*60}\n"
    output += f"Domain: {response.get('domain', 'N/A')}\n"
    output += f"Query: {response.get('query', 'N/A')}\n"
    output += f"Status: {response.get('status', 'N/A')}\n"
    output += f"{'='*60}\n"
    output += f"{response.get('response', 'No response')}\n"
    return output

def save_config(config: Dict, filepath: str = '.env'):
    """Save configuration to .env file"""
    with open(filepath, 'w') as f:
        for key, value in config.items():
            f.write(f"{key}={value}\n")
    logger.info(f"Config saved to {filepath}")

def load_config(filepath: str = '.env') -> Dict:
    """Load configuration from .env file"""
    config = {}
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    config[key] = value
    return config