# wechat-egonet

Reference codes to collect wechat ego network data ( group--people bipartite graph )

Dependencies:

- `Python3`
- `itchat`

## Introduction

Ego network (egonet) is a common object in the social network analysis context. It centers at one chosen user and expands to her friend of friend (2 hops). In that way, one can not only see what contacts (direct friends) this user has, but also be able to see the connections between those contacts. That makes a minimum meaningful social graph to start analysis.

Collecting traditional egonet in wechat is impossible because you can not know another user's contact book. However, wechat is famous for its spontaneous grouping support. There were many groups created by wechat users in the past years. One group is in essence a super edge (the edge that can connect more than 2 vertices) among its members. This "group sharing same member", or "contact sharing the same groups" phenomenon gives us enough network structure to anaylse and to visualise the prosimity of graph objects.

Another way to look at the data is to treat Group Node and Contact Node separately. One edge represents a "group belongingship". We get a bipartite graph.

## Code status

Last updated: 20180927

The code is not actively maintained. It worked on the last udpate date. Check and test before you use. The purpose is to provide reference code for people who want to analyse wechat egonet. Use it in larger projects at your own risk. When you run into problems, feel free to discuss with other users on the issue tracker.

## Yet Another ...

There are already many wechat API libraries out there. This repo is not intended to use as a library. It gives a reference, especially addressing issue [#480](https://github.com/littlecodersh/ItChat/issues/480). By default, itchat only gets the member list of 3 of the recently updated chatrooms. One solution is to call `itchat.originInstance.update_chatroom(roomId, detailedMember=True) for each chatroom id (UserName)`

## What can we do with egonet?

Here are some sample articles produced with this dataset:

- **pwords**, 2018, _个人微信群组关系网络图 (ego-network)_ [Link](https://mp.weixin.qq.com/s/DgAXmcR2kn3q2xjsEiwpJg)

## License

GPL