import app as bbs

app = bbs.configured_app()

# 在服务器上运行以下命令，即可运行此程序

# nohup gunicorn -b '0.0.0.0:80' appcorn:app &