# NJU-admission-report
或许用于简化走读生每日入校申请
## 说明
此项目纯属娱乐，仅供api学习，**请不要使用本项目自动提交申请！！！！**
因为表格要求提交**当日**苏康码和行程码截图，如因提交**过期截图**造成损失，本项目概不负责。
请务必确保图片为 `base64` 格式，否则会造成图片无法正常查看。
## 更新

##  使用方法
1. 将本项目 Fork 到自己的仓库。
2. 打开自己 Fork 之后的仓库，进入`Settings`选项，点击`Secret`，并选择`New Repository Secret`。依次添加以下变量：

    - `username`: 学号
    - `password`: 南京大学统一认证的密码
    - `name`: 姓名+学号，对应表单的“人员”,姓名学号之间加空格（例如：张三 MG12345678）
    - `skm_pic`: 苏康码截图，必须为base64格式（转换可以使用utils.py文件）
    - `xcm_pic`: 行程码截图，必须为base64格式
3. 回到 Action 选项卡，重新运行 Action，或者静待自动打卡。
4. 项目默认是在 5:00（北京时间13:00）自动打卡，可以根据需要修改 .github/workflows/report.yml 中 cron 项。`schedule:- cron: '0 5 * * *`字段使用UTC时间，北京时间快8小时。5个参数分别对应`minute、hour、day(month)、month、day(week)`，一般修改第二个参数（5对应北京时间13点）。具体参考https://crontab.guru/examples.html。
5. 建议设置 GitHub Actions 通知为 Send notifications for failed workflows only 以接收构建失败的通知。这通常是默认设置项。
6. 如构建失败请根据日志文件查看原因
