import os
from os import path
import time

import itchat
import pandas as pd

# The data dir for all wechat ego-network
dir_output = 'data'
if not path.exists(dir_output):
    os.makedirs(dir_output)
# Raw chatroom data in with the name {id} in CSV format. 
# One chatroom one file.
# One chatroom can be a single contact dialogue window, or a wechat group
dir_raw_chatrooms = path.join(dir_output, 'raw_chatrooms')
if not path.exists(dir_raw_chatrooms):
    os.makedirs(dir_raw_chatrooms)

def itchat_login():
    itchat.auto_login(hotReload=True)
    # itchat.login()

def scrape_friend_list():
    print('--- scrape contacts ---')
    friends = itchat.get_friends(update=True)
    df = pd.DataFrame(friends)
    df.to_csv(path.join(dir_output, 'friend-list.csv'))
    print('scraped {0} contacts'.format(len(df)))


def scrape_group():
    # Note:
    #     By default, itchat only gets the member list of 3 of the 
    #     recently updated chatrooms.
    #
    #     Ref issue: https://github.com/littlecodersh/ItChat/issues/480
    #
    #     The trick is to call 
    #     itchat.originInstance.update_chatroom(detailedMember=True)
    #     for each chatroom id (UserName)
    #
    print('--- scrape groups ---')
    chatrooms = itchat.get_chatrooms(update=True)
    pd.DataFrame(chatrooms).to_csv(path.join(dir_output, 'chatrooms-meta.csv'))

    print('scraped {0} groups'.format(len(chatrooms)))
    i = 0
    for c in chatrooms:
        i += 1
        print('#', i, c['UserName'])
        csv_path = path.join(dir_raw_chatrooms, c['UserName'])
        try:
            if not os.path.exists(csv_path):
                print('crawling')
                cc = itchat.originInstance.update_chatroom(c['UserName'], detailedMember=True)
                if 'MemberList' in cc:
                    pd.DataFrame(cc['MemberList']).to_csv(csv_path)
                    print('scraped {0} memberes from group {1} ({2})'.format(
                        len(cc['MemberList']), cc['NickName'], cc['UserName']
                    ))
                else:
                    print('failed to scrape members of group {0} ({1})'.format(
                        cc['NickName'], cc['UserName']
                    ))
                print('sleep for 2 seconds...')
                time.sleep(2)
            else:
                # Note:
                #     The chatroom ID is execution locally consistent
                #     Every time you login the itchat again, those IDs will change.
                print('group {0} ({1}) exists. skip.'.format(
                     c['NickName'], c['UserName']
                ))
        except Exception as e:
            print(e)
    print('scrape group member list done')

def merge_group_info():
    print('--- merge groups into one CSV ---')
    chatroom_to_user = []
    fn_chatrooms = os.listdir(dir_raw_chatrooms)

    for fn in fn_chatrooms:
        df = pd.read_csv(path.join(dir_raw_chatrooms, fn))
        for (i, m) in df.iterrows():
            tmp = {
                'ChatroomID': fn,
                'UserName': m['UserName'],
                'NickName': m['NickName']
            }
            tmp.update(m.to_dict())
            chatroom_to_user.append(tmp)
    df_details = pd.DataFrame(chatroom_to_user)
    df_details.to_csv(path.join(dir_output, 'chatroom-to-user-detail.csv'))
    #pd.DataFrame(chatroom_to_user)

itchat_login()
scrape_friend_list()
scrape_group()
merge_group_info()
