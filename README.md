# CYBER-SECURITY-INTRUSION-DETECTION-ML-PROJRCT-
This project builds and deploys a machine learning–based intrusion detection system using a synthetic cybersecurity session dataset .

This Cybersecurity Intrusion Detection Dataset is designed for detecting cyber intrusions based on network traffic and user
behavior. 

Dataset description: 

A. Network-Based Features These features describe network-level information such as packet size,protocol type, and encryption methods. 
     
     1.network_packet_size (Packet Size in Bytes) ---Represents the size of network packets,ranging between 64 to 1500 bytes. 
                                                  ---Packets on the lower end (~64 bytes) may indicate control messages, while larger packet (~1500 bytes) often carry bulk data. 
                                                  ---Attackers may use abnormally small or large packets for reconnaissance or exploitation attempts. 
     
     2.protocol_type (Communication Protocol)     ---The protocol used in the session: TCP, UDP, or ICMP. 
                                                  ---TCP(Transmission Control Protocol): Reliable, connection-oriented (common for HTTP, HTTPS, SSH). 
                                                  ---UDP (User Datagram Protocol): Faster but less reliable (used for VoIP, streaming). 
                                                  ---ICMP (Internet Control Message Protocol): Used for networkdiagnostics (ping); often abused in Denial-of-Service (DoS) attacks. 
   
    3. encryption_used (Encryption Protocol)      ---Values: AES, DES, None. ---AES (Advanced Encryption Standard): Strong encryption, commonly used. 
                                                  ---DES (Data Encryption Standard): Older encryption, weaker security. 
                                                  ---None: Indicates unencrypted communication, which can be risky. 
                                                  ---Attackers might use no encryption to avoid detection or weak encryption to exploit vulnerabilities. 

# B. User Behavior-Based Features These features track user activities, such as login attempts and session duration. 
    4.login_attempts (Number of Logins)            ---High values might indicate brute-force attacks (repeated login attempts). 
                                                  ---Typical users have 1–3 login attempts, while an attack may have hundreds or thousands. 
    5.session_duration (Session Length in Seconds) ---A very long session might indicate unauthorized access or persistence by an attacker. 
                                                  ---Attackers may try to stay connected to maintain access
    6.failed_logins (Failed Login Attempts) 
                                                  ---High failed login counts indicate credential stuffing or dictionary attacks. 
                                                  ---Many failed attempts followed by a successful login could suggest an account was compromised. 
    7.unusual_time_access (Login Time Anomaly)     ---A binary flag (0 or 1) indicating whether access happened at an unusual time. 
                                                  ---Attackers often operate outside normal business hours to evade detection.
    8.ip_reputation_score (Trustworthiness of IP Address) 
                                                  ---A score from 0 to 1, where higher values indicate suspicious activity. 
                                                  ---IP addresses associated with botnets, spam, or previous attacks tend to have higher scores. 
    9.browser_type (User’s Browser)                ---Common browsers: Chrome, Firefox, Edge, Safari. 
                                                  ---Unknown: Could be an indicator of automated scripts or bots. 

# C. Target
    Variable (attack_detected)                     ---Binary classification: 1 means an attack was detected, 0 means normal activity. 
                                                  ---The dataset isuseful for supervised machine learning, where a model learns from labeled attack patterns
