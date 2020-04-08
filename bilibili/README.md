- Anime 为爬取b站所有番剧列表
- bilidownload 为下载b站视频, 包括番剧
- bili_live 开播通知
- wx 微信通知

bilidownload下载：

![bilidown.png](http://ww1.sinaimg.cn/large/9dc802a0gy1gdmmkmu6vsj20it0gamyv.jpg)

逻辑很明确，通过输入的id，先通过接口找到每个视频的bvid，再通过bvid找到cid，最后用bvid和cid找到下载地址。下载地址有效时间为2个小时。

功能：

1. 下载单个视频
2. 下载视频合集（也就是多p的视频）
3. 下载单集、整部番剧
4. 下载up所有投稿视频

目前存在的问题：

1. 下载过程中出现问题时，任务将会中断。
2. 没有采用多线程，下载效率较低。（考虑到使用IDM下载比较方便，没弄。）