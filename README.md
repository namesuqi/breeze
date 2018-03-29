## Breeze 用户体验测试框架
* 构建在HoloWAN网络损伤仪的基础上
* 一个分布式测试框架
* 数据存储和分析
* 数据展示
* 自动部署和启动测试

#### 主要脚本
* leifeng.py: 启动雷锋，拉雷锋
* fe_play.py: start play by web
* custom_play.py: 单个运行某个网络条件的测试
* ue_loop.py: 循环运行制定网络条件的测试
* manage.py: 控制播放机和雷锋机上的进程，停止sdk，停止播放，收集p2p数据
* lib/const.py: 主要的变量都定义在该文件，运行时可能需要更新后再运行
