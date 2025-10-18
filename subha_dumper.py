#!/data/data/com.termux/files/usr/bin/python3
import os
import re
import subprocess
import time
from colorama import Fore, Style, init

init(autoreset=True)

class UltimateRootAnnihilator:
    def __init__(self):
        self.output_dir = "/sdcard/SubhaUltimate/"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def banner(self):
        print(f"{Fore.RED}╔══════════════════════════════╗")
        print(f"║    SUBHA ULTIMATE DUMPER     ║")
        print(f"║      ROOT POWER EDITION      ║")
        print(f"╚══════════════════════════════╝")
    
    def check_root(self):
        try:
            result = subprocess.run(['su', '-c', 'id'], capture_output=True, text=True)
            if 'uid=0' in result.stdout:
                print(f"{Fore.GREEN}✅ ROOT ACCESS CONFIRMED!")
                return True
            else:
                print(f"{Fore.RED}❌ No root access")
                return False
        except:
            print(f"{Fore.RED}❌ Cannot check root")
            return False
    
    def memory_dump(self, pid):
        print(f"\n{Fore.RED}💀 Dumping PID: {pid}")
        try:
            result = subprocess.run(['su', '-c', f'cat /proc/{pid}/maps'], 
                                  capture_output=True, text=True, shell=True)
            
            if result.stdout:
                so_files = re.findall(r'.*\.so.*', result.stdout)
                print(f"{Fore.GREEN}📚 Found {len(so_files)} .so files")
                
                # Save to file
                with open(f"{self.output_dir}dump_{pid}.txt", 'w') as f:
                    f.write(f"Subha Ultimate Dumper\n")
                    f.write(f"PID: {pid}\n")
                    f.write(f"Time: {time.ctime()}\n")
                    f.write(f"Found {len(so_files)} libraries\n\n")
                    
                    for i, so in enumerate(so_files[:15]):
                        f.write(f"{i+1}. {so}\n")
                
                print(f"{Fore.GREEN}💾 Saved: {self.output_dir}dump_{pid}.txt")
                
                # Show some examples
                print(f"{Fore.YELLOW}📖 First 5 libraries:")
                for so in so_files[:5]:
                    lib_name = so.split('/')[-1] if '/' in so else so
                    print(f"   📍 {lib_name}")
            else:
                print(f"{Fore.RED}❌ Cannot access process {pid}")
                
        except Exception as e:
            print(f"{Fore.RED}❌ Error: {e}")
    
    def system_scan(self):
        print(f"\n{Fore.BLUE}🔍 System Process Scan...")
        os.system('ps -A | head -20')
    
    def show_menu(self):
        print(f"\n{Fore.CYAN}💪 ULTIMATE POWER MENU:")
        print("1. 💀 Memory Dump from PID")
        print("2. 🔍 System Process Scan")
        print("3. 📊 System Info")
        print("4. 🚪 Exit")
        return input(f"\n{Fore.YELLOW}Select option: ")
    
    def run_annihilation(self):
        if not self.check_root():
            print(f"{Fore.RED}❌ ROOT ACCESS REQUIRED!")
            return
        
        self.banner()
        
        while True:
            choice = self.show_menu()
            
            if choice == "1":
                pid = input("Enter PID: ")
                self.memory_dump(pid)
                
            elif choice == "2":
                self.system_scan()
                
            elif choice == "3":
                print(f"\n{Fore.GREEN}💻 System Info:")
                os.system('uname -a')
                print(f"📁 Dump folder: {self.output_dir}")
                
            elif choice == "4":
                print(f"{Fore.GREEN}👋 Mission Accomplished!")
                break
                
            else:
                print(f"{Fore.RED}❌ Invalid option!")
            
            input(f"\n{Fore.YELLOW}Press Enter to continue...")

if __name__ == "__main__":
    annihilator = UltimateRootAnnihilator()
    annihilator.run_annihilation()
