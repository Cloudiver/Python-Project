稿件状态:
https://api.bilibili.com/x/web-interface/archive/stat?aid=98690417

稿件详细信息: 包括稿件cid,aid,稿件观看次数等(上面的稿件状态), 作者UID
https://api.bilibili.com/x/web-interface/view?bvid=BV1k7411m7nh
https://api.bilibili.com/x/web-interface/view?aid=98464354
https://api.bilibili.com/x/web-interface/view/detail?bvid=BV1k7411m7nh  (稿件页所有信息)

只通过bvid获取cid:
https://api.bilibili.com/x/player/pagelist?bvid=BV1c7411U7bh
或者通过aid获取cid:
https://api.bilibili.com/x/player/pagelist?aid=81909793

获取视频下载链接:
https://api.bilibili.com/x/player/playurl?cid=168087953&bvid=BV1FE411c7co&qn=80
另一个真实链接:
https://api.bilibili.com/pgc/player/web/playurl?avid=81909793&cid=140491572&qn=80

(登录才能获取720p以上)


获取用户的基本数据(uid,关注的人数,关注数)
https://api.bilibili.com/x/relation/stat?vmid=6887741

用户关注up(只有uid信息):
https://api.vc.bilibili.com/feed/v1/feed/get_attention_list?uid=6887741

用户个人信息:
https://api.bilibili.com/x/space/acc/info?mid=284393777
https://api.bilibili.com/x/web-interface/card?mid=6887741

动画区三日榜单:
https://www.bilibili.com/index/catalogy/1-3day.json

视频推荐:
http://comment.bilibili.com/recommendnew,97970673

当前是否登录:
https://api.bilibili.com/x/web-interface/nav

追番列表:
https://api.bilibili.com/x/space/bangumi/follow/list?type=1&vmid=6887741

直播间信息:
https://api.live.bilibili.com/room/v1/Room/getRoomInfoOld?mid=120586

在线人数:
https://api.bilibili.com/x/web-interface/online

视频评论:
https://api.bilibili.com/x/v2/reply?type=1&oid=98751705&sort=2&pn=2
页码: pn = 1, 2...
按热度排序: 2
按时间排序: 0

番剧播放数据:
https://api.bilibili.com/pgc/web/season/stat?season_id=29350

番剧缩略图:
https://api.bilibili.com/x/player/videoshot?aid=81909793&cid=140491572

番剧详细信息:
https://www.biliplus.com/api/bangumi?season=29350
https://api.bilibili.com/pgc/view/web/season?ep_id=84341
https://api.bilibili.com/pgc/view/web/season?season_id=29350

番剧基本信息:
https://api.bilibili.com/pgc/review/user?media_id=28224128

番剧所有剧集aid:
https://api.bilibili.com/pgc/web/season/section?season_id=29350

番剧承包排行榜:
http://bangumi.bilibili.com/sponsor/web_api/v2/rank/total?season_id=6339&season_type=1&page=1&pagesize=50


