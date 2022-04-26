# NJU-admission-report
或许用于简化走读生每日入校申请
## 说明
此项目纯属娱乐，仅供api学习，**请不要使用本项目自动提交申请！！！！**
因为表格要求提交**当日**苏康码和行程码截图，如因提交**过期截图**造成损失，本项目概不负责。
## 更新
- 2022.4.27 图片太大无法保存为 SECRET，改为读取加密图片文件
##  使用方法
1. 将本项目 Fork 到自己的仓库。
2. 打开自己 Fork 之后的仓库，进入`Settings`选项，点击`Secret`，并选择`New Repository Secret`。依次添加以下变量：

    - `username`: 学号
    - `password`: 南京大学统一认证的密码
    - `name`: 姓名+学号，对应表单的“人员”,姓名学号之间加空格（例如：张三 MG12345678）
    - `aes_key`: 截图的加密密钥，用于读取苏康码和行程码文件
3. 用 utils.py 文件内的`encrypt_img`方法，设置密钥`key`为`aes_key`，将苏康码和行程码截图保存为 skm_pic.txt 和 xcm_pic.txt 文件（建议先压缩图片），放在`/assets`文件夹中。windows使用`pip install pycryptodome`安装Crypto，linux使用`pip install pycrypto`
4. 回到 Action 选项卡，重新运行 Action，或者静待自动打卡。
5. 项目默认是在 5:00（北京时间13:00）自动打卡，可以根据需要修改 .github/workflows/report.yml 中 cron 项。`schedule:- cron: '0 5 * * *`字段使用UTC时间，北京时间快8小时。5个参数分别对应`minute、hour、day(month)、month、day(week)`，一般修改第二个参数（5对应北京时间13点）。具体参考https://crontab.guru/examples.html。
6. 建议设置 GitHub Actions 通知为 Send notifications for failed workflows only 以接收构建失败的通知。这通常是默认设置项。
7. 如构建失败请根据日志文件查看原因
## TODO
- [ ] 自动更新苏康码和行程码截图