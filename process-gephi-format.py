import os
from os import path
import pandas as pd

dir_output = 'data'
df_friends = pd.read_csv(path.join(dir_output, 'friend-list.csv'))
df_chatrooms = pd.read_csv(path.join(dir_output, 'chatrooms-meta.csv'))
df_connections = pd.read_csv(path.join(dir_output, 'chatroom-to-user-detail.csv'))

df_nodes_users = df_connections[['UserName', 'NickName']]
df_nodes_users['Type'] = 'User'
df_nodes_users = df_nodes_users.drop_duplicates()
print('# of user nodes:', len(df_nodes_users))

df_nodes_chatrooms = df_chatrooms[['UserName', 'NickName']]
df_nodes_chatrooms['Type'] = 'Chatroom'
print('# of chatroom nodes:', len(df_nodes_chatrooms))

df_nodes = pd.concat([df_nodes_chatrooms, df_nodes_users])
print('# of nodes (total):', len(df_nodes))

df_nodes.columns = ['Id', 'Label', 'Type']

print('formatting into gephi CSVs...')
df_nodes.to_csv(path.join(dir_output, 'gephi-nodes.csv'), index=None)
df_edges = df_connections[['ChatRoomId', 'UserName']].rename(columns={
  'ChatRoomId': 'Source',
    'UserName': 'Target',
})
df_edges['Type'] = 'undirected'
df_edges.to_csv(path.join(dir_output, 'gephi-edges.csv'), index=None)
