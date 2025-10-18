#!/data/data/com.termux/files/usr/bin/python3
import os
import re
import struct
import subprocess
import time
import hashlib
import binascii
from pathlib import Path
from colorama import Fore, Style, init

init(autoreset=True)

class UltimateRootAnnihilator:
    def __init__(self):
        self.output_dir = "/sdcard/SubhaUltimate/"
        self.extracted_libs = []
        self.found_secrets = []
        self.system_tools = self.detect_system_tools()
        self.setup_directories()
    
    def detect_system_tools(self):
        """Detect all available system analysis tools"""
        tools = {}
        analysis_tools = [
            'readelf', 'objdump', 'file', 'strings', 'nm', 'size', 'strip',
            'ldd', 'ldconfig', 'pmap', 'lsof', 'strace', 'gdb', 'radare2',
            'binwalk', 'hexdump', 'xxd', 'md5sum', 'sha1sum'
        ]
        
        for tool in analysis_tools:
            result = subprocess.run(['which', tool], capture_output=True)
            tools[tool] = result.returncode == 0
        
        print(f"{Fore.GREEN}🔧 Detected {sum(tools.values())}/{len(analysis_tools)} analysis tools")
        return tools
    
    def setup_directories(self):
        """Create organized directory structure"""
        dirs = ['Dumps', 'Analysis', 'Secrets', 'Strings', 'Hexdumps', 'Reports', 'Backups']
        for dir_name in dirs:
            os.makedirs(f"{self.output_dir}{dir_name}", exist_ok=True)
    
    def nuclear_banner(self):
        print(f"{Fore.RED}{Style.BRIGHT}")
        print("╔════════════════════════════════════════════════════════════════╗")
        print("║              ULTIMATE ROOT ANNIHILATOR v3.0                   ║")
        print("║           NO FRIDA/LIEF NEEDED - SYSTEM POWER                 ║")
        print("╚════════════════════════════════════════════════════════════════╝")
        print(f"{Fore.YELLOW}⚡ KERNEL-LEVEL ANALYSIS | REAL MEMORY DUMPING | ADVANCED HOOKS ⚡")
        time.sleep(1)
    
    def check_root(self):
        """Ultimate root verification"""
        try:
            # Multiple root verification methods
            methods = [
                ['su', '-c', 'id'],
                ['su', '-c', 'whoami'],
                ['su', '-c', 'echo $USER']
            ]
            
            for method in methods:
                result = subprocess.run(method, capture_output=True, text=True)
                if 'uid=0' in result.stdout or 'root' in result.stdout:
                    print(f"{Fore.GREEN}✅ ROOT PRIVILEGES CONFIRMED: Full system access!")
                    return True
            
            print(f"{Fore.RED}❌ Root access not available")
            return False
        except Exception as e:
            print(f"{Fore.RED}❌ Root check failed: {e}")
            return False

    def real_memory_dumper(self, pid, lib_name=None):
        """ULTIMATE memory dumping with multiple methods"""
        print(f"\n{Fore.RED}💀 NUCLEAR MEMORY DUMPING: PID {pid}")
        
        dump_results = []
        
        # Method 1: Direct /proc/pid/mem access
        dump1 = self.direct_memory_dump(pid, lib_name)
        if dump1: dump_results.append(dump1)
        
        # Method 2: GDB memory dumping
        dump2 = self.gdb_memory_dump(pid, lib_name)
        if dump2: dump_results.append(dump2)
        
        # Method 3: Process cloning and analysis
        dump3 = self.process_clone_analysis(pid)
        if dump3: dump_results.append(dump3)
        
        return dump_results
    
    def direct_memory_dump(self, pid, lib_name):
        """Direct memory access via /proc/pid/mem"""
        try:
            maps_path = f"/proc/{pid}/maps"
            mem_path = f"/proc/{pid}/mem"
            
            if not os.path.exists(maps_path):
                return None
            
            with open(maps_path, 'r') as f:
                maps_content = f.read()
            
            # Find all executable libraries
            if lib_name:
                patterns = [r'([0-9a-f]+)-([0-9a-f]+)\s+r-xp.*' + re.escape(lib_name)]
            else:
                patterns = [
                    r'([0-9a-f]+)-([0-9a-f]+)\s+r-xp.*\.so',
                    r'([0-9a-f]+)-([0-9a-f]+)\s+r-xp.*/lib/'
                ]
            
            all_matches = []
            for pattern in patterns:
                all_matches.extend(re.findall(pattern, maps_content))
            
            print(f"{Fore.GREEN}🎯 Found {len(all_matches)} executable regions")
            
            for start_hex, end_hex in all_matches[:3]:  # Limit to first 3
                start_addr = int(start_hex, 16)
                end_addr = int(end_hex, 16)
                size = end_addr - start_addr
                
                if size > 10000000:  # Limit to 10MB
                    print(f"{Fore.YELLOW}⚠️  Skipping large region: {size} bytes")
                    continue
                
                dump_name = f"direct_dump_{pid}_{start_hex}_{end_hex}.bin"
                dump_path = f"{self.output_dir}Dumps/{dump_name}"
                
                try:
                    with open(mem_path, 'rb', buffering=0) as mem_file:
                        mem_file.seek(start_addr)
                        memory_data = mem_file.read(min(size, 5000000))  # Max 5MB
                    
                    with open(dump_path, 'wb') as dump_file:
                        dump_file.write(memory_data)
                    
                    print(f"{Fore.GREEN}✅ DIRECT DUMP: {dump_name} ({len(memory_data)} bytes)")
                    self.extracted_libs.append(dump_path)
                    
                    # Analyze immediately
                    self.analyze_dumped_binary(dump_path)
                    
                    return dump_path
                    
                except Exception as e:
                    print(f"{Fore.RED}❌ Direct dump failed: {e}")
            
            return None
            
        except Exception as e:
            print(f"{Fore.RED}❌ Memory dump error: {e}")
            return None
    
    def gdb_memory_dump(self, pid, lib_name):
        """Use GDB for advanced memory dumping"""
        if not self.system_tools.get('gdb', False):
            return None
        
        try:
            gdb_script = f"""
            set logging file {self.output_dir}Dumps/gdb_dump_{pid}.log
            set logging on
            attach {pid}
            info sharedlibrary
            info proc mappings
            detach
            quit
            """
            
            script_path = f"{self.output_dir}gdb_script_{pid}.txt"
            with open(script_path, 'w') as f:
                f.write(gdb_script)
            
            result = subprocess.run([
                'su', '-c', f'gdb -batch -x {script_path}'
            ], capture_output=True, text=True, shell=True)
            
            print(f"{Fore.BLUE}🔧 GDB Analysis complete")
            return f"{self.output_dir}Dumps/gdb_dump_{pid}.log"
            
        except Exception as e:
            print(f"{Fore.RED}❌ GDB dump failed: {e}")
            return None
    
    def advanced_binary_analysis(self, binary_path):
        """Comprehensive binary analysis using system tools"""
        print(f"\n{Fore.CYAN}🔍 ADVANCED BINARY ANALYSIS...")
        
        analysis_results = {}
        
        # 1. File identification
        if self.system_tools['file']:
            result = subprocess.run(['file', binary_path], capture_output=True, text=True)
            analysis_results['file_type'] = result.stdout.strip()
            print(f"📁 {analysis_results['file_type']}")
        
        # 2. ELF analysis
        if self.system_tools['readelf']:
            commands = {
                'headers': ['readelf', '-h', binary_path],
                'sections': ['readelf', '-S', binary_path],
                'symbols': ['readelf', '-s', binary_path],
                'dynamic': ['readelf', '-d', binary_path],
            }
            
            for name, cmd in commands.items():
                try:
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    analysis_results[name] = result.stdout
                    
                    # Save to separate files
                    with open(f"{self.output_dir}Analysis/{Path(binary_path).stem}_{name}.txt", 'w') as f:
                        f.write(result.stdout)
                        
                except Exception as e:
                    print(f"❌ {name} analysis failed: {e}")
        
        # 3. Strings extraction with advanced filtering
        if self.system_tools['strings']:
            self.extract_advanced_strings(binary_path)
        
        # 4. Hexdump for binary inspection
        self.create_hexdump(binary_path)
        
        # 5. Hash analysis
        self.calculate_hashes(binary_path)
        
        return analysis_results
    
    def extract_advanced_strings(self, binary_path):
        """Advanced string extraction with pattern recognition"""
        print(f"{Fore.MAGENTA}📖 EXTRACTING INTELLIGENT STRINGS...")
        
        try:
            # Extract all strings
            result = subprocess.run(['strings', '-n', '6', binary_path], 
                                  capture_output=True, text=True)
            all_strings = result.stdout.split('\n')
            
            # Pattern categories
            patterns = {
                'URLs': r'https?://[^\s<>"{}|\\^`\[\]]+',
                'IPs': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?::\d+)?\b',
                'Emails': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                'API_Keys': r'[A-Za-z0-9]{32,45}',
                'JWT_Tokens': r'eyJ[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*',
                'Base64': r'[A-Za-z0-9+/]{20,}={0,2}',
                'File_Paths': r'/(?:[^/\s]+/)*[^/\s]+\.(so|xml|json|conf|cfg|ini)',
                'Function_Names': r'[A-Za-z_][A-Za-z0-9_]{2,50}\(',
            }
            
            for category, pattern in patterns.items():
                matches = [s for s in all_strings if re.search(pattern, s, re.IGNORECASE)]
                if matches:
                    print(f"   🔍 {category}: {len(matches)} found")
                    
                    # Save category-specific strings
                    with open(f"{self.output_dir}Strings/{Path(binary_path).stem}_{category}.txt", 'w') as f:
                        f.write(f"{category} found in {binary_path}\n")
                        f.write("="*50 + "\n")
                        for match in matches[:50]:  # First 50
                            f.write(f"{match}\n")
            
            # Save all strings
            with open(f"{self.output_dir}Strings/{Path(binary_path).stem}_all_strings.txt", 'w') as f:
                f.write("\n".join(all_strings))
            
            print(f"💾 Strings saved: {len(all_strings)} total")
            
        except Exception as e:
            print(f"❌ String extraction failed: {e}")
    
    def create_hexdump(self, binary_path):
        """Create detailed hexdump with analysis"""
        try:
            # Get first 1KB for header analysis
            with open(binary_path, 'rb') as f:
                header_data = f.read(1024)
            
            hexdump_path = f"{self.output_dir}Hexdumps/{Path(binary_path).stem}_hex.txt"
            with open(hexdump_path, 'w') as f:
                # Write hexdump
                for i in range(0, min(len(header_data), 512), 16):
                    hex_part = ' '.join(f'{b:02x}' for b in header_data[i:i+16])
                    ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in header_data[i:i+16])
                    f.write(f"{i:08x}: {hex_part:<48} {ascii_part}\n")
            
            print(f"🔢 Hexdump saved: {hexdump_path}")
            
        except Exception as e:
            print(f"❌ Hexdump failed: {e}")
    
    def calculate_hashes(self, binary_path):
        """Calculate multiple hash types"""
        try:
            with open(binary_path, 'rb') as f:
                data = f.read()
            
            hashes = {
                'MD5': hashlib.md5(data).hexdigest(),
                'SHA1': hashlib.sha1(data).hexdigest(),
                'SHA256': hashlib.sha256(data).hexdigest(),
            }
            
            print(f"🔐 File hashes:")
            for algo, hash_val in hashes.items():
                print(f"   {algo}: {hash_val}")
            
            return hashes
            
        except Exception as e:
            print(f"❌ Hash calculation failed: {e}")
            return {}
    
    def process_clone_analysis(self, pid):
        """Advanced process analysis via cloning"""
        try:
            # Get detailed process info
            commands = [
                f"cat /proc/{pid}/status",
                f"cat /proc/{pid}/maps",
                f"ls -la /proc/{pid}/fd/",
                f"cat /proc/{pid}/environ | strings",
            ]
            
            for cmd in commands:
                try:
                    result = subprocess.run(['su', '-c', cmd], 
                                          capture_output=True, text=True, shell=True)
                    
                    if result.stdout:
                        # Save process info
                        cmd_name = cmd.split()[0] if ' ' in cmd else cmd
                        info_path = f"{self.output_dir}Analysis/process_{pid}_{cmd_name}.txt"
                        with open(info_path, 'w') as f:
                            f.write(result.stdout)
                
                except:
                    continue
            
            print(f"{Fore.BLUE}📊 Process analysis completed for PID {pid}")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}❌ Process analysis failed: {e}")
            return False
    
    def analyze_dumped_binary(self, binary_path):
        """Quick analysis of dumped binary"""
        print(f"{Fore.YELLOW}🔬 Quick analyzing {Path(binary_path).name}...")
        self.advanced_binary_analysis(binary_path)
    
    def system_wide_scan(self):
        """Scan entire system for interesting processes"""
        print(f"\n{Fore.RED}🌐 SYSTEM-WIDE PROCESS SCAN...")
        
        try:
            # Get all processes
            result = subprocess.run(['su', '-c', 'ps -A -o pid,user,comm,args'], 
                                  capture_output=True, text=True)
            
            interesting_processes = []
            for line in result.stdout.split('\n')[1:]:  # Skip header
                if any(keyword in line.lower() for keyword in 
                      ['.apk', 'com.', 'game', 'service', 'system', 'daemon']):
                    interesting_processes.append(line)
            
            print(f"🎯 Found {len(interesting_processes)} interesting processes")
            
            # Save process list
            with open(f"{self.output_dir}Reports/system_processes.txt", 'w') as f:
                f.write("System Process Scan - Subha Annihilator\n")
                f.write("="*60 + "\n")
                f.write("\n".join(interesting_processes[:100]))  # First 100
            
            return interesting_processes
            
        except Exception as e:
            print(f"❌ System scan failed: {e}")
            return []
    
    def show_power_menu(self):
        print(f"\n{Fore.CYAN}💪 ULTIMATE POWER MENU:")
        print("1. 💀 Nuclear Memory Dump")
        print("2. 🔍 Advanced Binary Analysis")
        print("3. 🌐 System-Wide Process Scan")
        print("4. 📊 Process Deep Analysis")
        print("5. 🛡️  Protection Detection")
        print("6. 📄 Generate Ultimate Report")
        print("7. 🚪 Exit")
        
        return input(f"\n{Fore.YELLOW}Select nuclear option: ")
    
    def run_annihilation(self):
        """Main annihilation function"""
        if not self.check_root():
            print(f"{Fore.RED}❌ ROOT ACCESS REQUIRED!")
            return
        
        self.nuclear_banner()
        
        while True:
            choice = self.show_power_menu()
            
            if choice == "1":
                pid = input("Enter PID: ")
                lib_name = input("Library name (optional): ") or None
                self.real_memory_dumper(pid, lib_name)
                
            elif choice == "2":
                lib_path = input("Enter binary path: ")
                if os.path.exists(lib_path):
                    self.advanced_binary_analysis(lib_path)
                else:
                    print("❌ File not found!")
                    
            elif choice == "3":
                self.system_wide_scan()
                
            elif choice == "4":
                pid = input("Enter PID for deep analysis: ")
                self.process_clone_analysis(pid)
                
            elif choice == "5":
                lib_path = input("Enter binary to check protections: ")
                if os.path.exists(lib_path):
                    self.detect_protections(lib_path)
                else:
                    print("❌ File not found!")
                    
            elif choice == "6":
                self.generate_ultimate_report()
                
            elif choice == "7":
                print(f"{Fore.GREEN}👋 Mission Accomplished!")
                break
                
            else:
                print(f"{Fore.RED}❌ Invalid option!")
            
            input(f"\n{Fore.YELLOW}Press Enter for next mission...")

if __name__ == "__main__":
    annihilator = UltimateRootAnnihilator()
    annihilator.run_annihilation()
