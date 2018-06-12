# UX Tracking Backend
Ux Tracking Backend is Flask-Restful python API for tracking a users behaviour on an application. It's one component out of three needed for the Ux-tracker to work.
- Backend
- [Dashboard](https://github.com/inuits/ux-tracking-frontend)
- [Library](https://github.com/inuits/ux-tracking-library)

## Quickstart
You can clone the repo, install the requirements using `requirements.txt` 
```bash
git clone https://github.com/inuits/ux-tracking-backend.git
cd ux-tracking-backend
pip install -r requirements.txt
```

Copy the dist config from `config/config.yml.dist` to `config/config.yml` and edit according to your settings.
```yaml
elasticsearch:
  host: localhost
  port: 9200

keys:
  - name: applicationOne
    key: keyOne
  - name: applicationTwo
    key: keyTwo

jwt_secret_key: your_jwt_secret_key_here
```

finally run it with 
```bash
python run.py
```




### SSL
Ux-tracking-backend tries to run on SSL. In order to do so, it needs some keys.
To generate self-signed keys:
```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

Place them in the same directory as the executable under a folder named `keys`.
```
.
├── keys
│   ├── cert.pem
│   └── key.pem
└── ux-tracking-backend
```


For more info please checkout the [Wiki](https://github.com/inuits/ux-tracking-backend/wiki)
