# **Flask + HAProxy + Nginx Architecture** 🌐🛠️

```mermaid
graph LR
    U[🌍 User] --> N[🛡️ Nginx:80]
    N --> |📁 Static Files| S[/var/www/static]
    N --> |🔄 Dynamic| H[⚖️ HAProxy:8080]
    H --> F1[🐍 Flask App:5000]
    H --> F2[🐍 Flask App:5001]
    
    style U fill:#f9f,stroke:#333
    style N fill:#39f,stroke:#333
    style H fill:#f80,stroke:#333
    style F1,F2 fill:#6f6,stroke:#333
```

## **Core Components** 🧩
1. **🌍 User Requests**  
   - Hits your domain (e.g., `example.com`)

2. **🛡️ Nginx (Port 80)**  
   - 📁 **Serves static files** directly (`/var/www/static`)  
   - 🔄 **Proxies dynamic requests** to HAProxy  

3. **⚖️ HAProxy (Port 8080)**  
   - Load balances between Flask instances  
   - Health checks (`/health` endpoint)  
   - 🔍 **Stats Dashboard** at `:8404/stats`  

4. **🐍 Flask Apps (Ports 5000 & 5001)**  
   - Identical instances for redundancy  
   - 🏗️ Business logic and API routes  

---

## **Key Configs** ⚙️

### **Nginx (`/etc/nginx/sites-available/myapp`)**
```nginx
location / {
    try_files $uri @proxy;  # Try static first → else proxy
}

location @proxy {
    proxy_pass http://127.0.0.1:8080;  # Send to HAProxy
}
```

### **HAProxy (`/etc/haproxy/haproxy.cfg`)**
```cfg
backend flask_apps
    balance roundrobin
    server flask1 127.0.0.1:5000 check inter 2s
    server flask2 127.0.0.1:5001 check inter 2s
```

---

## **Deployment Steps** 🚀

1. **Start Flask Apps**  
   ```bash
   # Terminal 1
   gunicorn -b 127.0.0.1:5000 app:app
   
   # Terminal 2
   gunicorn -b 127.0.0.1:5001 app:app
   ```

2. **Launch HAProxy & Nginx**  
   ```bash
   sudo systemctl restart haproxy nginx
   ```

3. **Verify**  
   ```bash
   curl -I http://localhost  # Should return 200
   ```

---

## **Monitoring** 📊  
Access HAProxy stats:  
🔗 `http://your-server:8404/stats`  
🔐 Auth: `admin:yourpassword`  

---

### **Troubleshooting** 🔧  
- **502 Bad Gateway?**  
  ```bash
  sudo tail -f /var/log/nginx/error.log  # Check Nginx errors
  sudo journalctl -u haproxy -f         # HAProxy logs
  ```
