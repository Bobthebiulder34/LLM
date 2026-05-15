"""
Command Line Interface for Engineering AI System
"""

import argparse
import sys
from logger_config import setup_logger
from utils import ClusterManager, format_response, InferenceClient, ToolClient

logger = setup_logger('cli', 'cli.log')

def create_parser():
    """Create argument parser"""
    parser = argparse.ArgumentParser(
        description='Engineering AI System CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py ask "What is trace width?" --domain pcb
  python cli.py tool pcb trace-width --current 5 --copper 1
  python cli.py tool cnc rpm --sfm 400 --diameter 0.5
  python cli.py status
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Ask command
    ask_parser = subparsers.add_parser('ask', help='Ask AI a question')
    ask_parser.add_argument('question', help='Question to ask')
    ask_parser.add_argument('--domain', choices=['pcb', 'cnc', 'cad', 'electronics', 'general'],
                           default='general', help='Domain expertise')
    ask_parser.add_argument('--tokens', type=int, default=512, help='Max tokens')
    
    # Tool command
    tool_parser = subparsers.add_parser('tool', help='Run engineering tools')
    tool_subparsers = tool_parser.add_subparsers(dest='tool_type', help='Tool type')
    
    # PCB tools
    pcb_parser = tool_subparsers.add_parser('pcb', help='PCB tools')
    pcb_subparsers = pcb_parser.add_subparsers(dest='pcb_tool', help='PCB tool')
    
    trace_parser = pcb_subparsers.add_parser('trace-width', help='Calculate trace width')
    trace_parser.add_argument('--current', type=float, required=True, help='Current in amps')
    trace_parser.add_argument('--temp', type=float, default=45, help='Temp rise in C')
    trace_parser.add_argument('--copper', type=float, default=1, help='Copper oz')
    
    # CNC tools
    cnc_parser = tool_subparsers.add_parser('cnc', help='CNC tools')
    cnc_subparsers = cnc_parser.add_subparsers(dest='cnc_tool', help='CNC tool')
    
    rpm_parser = cnc_subparsers.add_parser('rpm', help='Calculate RPM')
    rpm_parser.add_argument('--sfm', type=float, required=True, help='Surface feet per minute')
    rpm_parser.add_argument('--diameter', type=float, required=True, help='Tool diameter')
    
    feed_parser = cnc_subparsers.add_parser('feed', help='Calculate feed rate')
    feed_parser.add_argument('--rpm', type=float, required=True, help='Spindle RPM')
    feed_parser.add_argument('--teeth', type=int, required=True, help='Number of teeth')
    feed_parser.add_argument('--chip-load', type=float, required=True, help='Chip load per tooth')
    
    # Electronics tools
    elec_parser = tool_subparsers.add_parser('electronics', help='Electronics tools')
    elec_subparsers = elec_parser.add_subparsers(dest='elec_tool', help='Electronics tool')
    
    ohms_parser = elec_subparsers.add_parser('ohms', help='Ohm\'s Law calculator')
    ohms_parser.add_argument('--voltage', type=float, help='Voltage in volts')
    ohms_parser.add_argument('--current', type=float, help='Current in amps')
    ohms_parser.add_argument('--resistance', type=float, help='Resistance in ohms')
    
    # Status command
    subparsers.add_parser('status', help='Check cluster status')
    
    # Health command
    subparsers.add_parser('health', help='Run health checks')
    
    return parser

def cmd_ask(args):
    """Handle ask command"""
    manager = ClusterManager()
    result = manager.run_full_workflow(args.question, args.domain)
    print(format_response(result))

def cmd_tool(args):
    """Handle tool command"""
    client = ToolClient()
    
    if args.tool_type == 'pcb':
        if args.pcb_tool == 'trace-width':
            width = client.pcb_trace_width(args.current, args.temp, args.copper)
            print(f"\n✓ Trace Width: {width} mil")
            print(f"  Current: {args.current}A")
            print(f"  Temp Rise: {args.temp}°C")
            print(f"  Copper: {args.copper}oz\n")
    
    elif args.tool_type == 'cnc':
        if args.cnc_tool == 'rpm':
            rpm = client.cnc_rpm(args.sfm, args.diameter)
            print(f"\n✓ RPM: {rpm}")
            print(f"  SFM: {args.sfm}")
            print(f"  Diameter: {args.diameter}in\n")
        
        elif args.cnc_tool == 'feed':
            result = client.post('/api/tool/cnc/feed-rate', {
                'rpm': args.rpm,
                'num_teeth': args.teeth,
                'chip_load_per_tooth': args.chip_load
            })
            if result:
                print(f"\n✓ Feed Rate: {result['feed_rate_ipm']} IPM")
                print(f"  RPM: {args.rpm}")
                print(f"  Teeth: {args.teeth}")
                print(f"  Chip Load: {args.chip_load}\n")
    
    elif args.tool_type == 'electronics':
        if args.elec_tool == 'ohms':
            result = client.post('/api/tool/electronics/ohms-law', {
                'voltage': args.voltage,
                'current': args.current,
                'resistance': args.resistance
            })
            if result:
                print(f"\n✓ Calculation Result:")
                for key, value in result.items():
                    if key != 'parameters':
                        print(f"  {key}: {value}")
                print()

def cmd_status(args):
    """Handle status command"""
    manager = ClusterManager()
    status = manager.check_cluster_status()
    
    print("\n🔍 Cluster Status:")
    print("="*60)
    for service, online in status.items():
        symbol = "✓ ONLINE" if online else "✗ OFFLINE"
        print(f"  {service}: {symbol}")
    print()

def cmd_health(args):
    """Handle health command"""
    from test_cluster import main as test_main
    test_main()

def main():
    """Main CLI entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        if args.command == 'ask':
            cmd_ask(args)
        elif args.command == 'tool':
            cmd_tool(args)
        elif args.command == 'status':
            cmd_status(args)
        elif args.command == 'health':
            cmd_health(args)
    except Exception as e:
        logger.error(f"CLI error: {e}")
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())