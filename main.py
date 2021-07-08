import asyncio

from typing import List, Optional

from graia.application import GraiaMiraiApplication, Session
from graia.application.event.messages import GroupMessage, FriendMessage, TempMessage
from graia.application.event.mirai import NewFriendRequestEvent
from graia.application.friend import Friend
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Source, Plain, At, Image, Face
from graia.broadcast import Broadcast

from config import host, auth_key, account, database_path
from utils.decorator import command
from utils.database import Database


loop = asyncio.get_event_loop()
bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc, connect_info=Session(
        host=host, authKey=auth_key, account=account, websocket=True
    )
)

database = Database(database_path)


def process(message: MessageChain) -> Optional[MessageChain]:
    def handle_type(result: dict) -> List:
        if result['type'] == 'text':
            return [Plain(result['return'])]
        elif result['type'] == 'image':
            return [Image.fromLocalFile(result['return'])]
        elif result['type'] == 'error':
            return [Face(faceId=168), Plain(result['return'])]
        else:
            return []

    content = message.asDisplay().strip()
    # 命令运行
    if content.startswith('/'):
        return MessageChain.create(
            handle_type(command.from_str(content[1:]))
        )
    # 关键词回复
    returns = []
    for result in database.keyword_match(content):
        returns += handle_type(result) + [Plain('\n\n')]
    if returns:
        return MessageChain.create(returns[:-1])

@bcc.receiver(FriendMessage)  # 好友聊天
async def friend_message_listener(
    app: GraiaMiraiApplication, friend: Friend, message: MessageChain
):
    return_ = process(message)
    if return_:
        await app.sendFriendMessage(friend, return_)

@bcc.receiver(GroupMessage)  # 群组聊天
async def group_message_listener(
    app: GraiaMiraiApplication, group: Group, member: Member, message: MessageChain
):
    return_ = process(message)
    if return_:
        # await app.sendTempMessage(
        #     group, member, return_, quote=message.get(Source)[0]
        # )
        await app.sendGroupMessage(
            group, return_, quote=message.get(Source)[0]
        )

@bcc.receiver(TempMessage)  # 临时聊天
async def temp_message_listener(
    app: GraiaMiraiApplication, group: Group, member: Member, message: MessageChain
):
    return_ = process(message)
    if return_:
        await app.sendTempMessage(group, member, return_)

# @bcc.receiver(NewFriendRequestEvent)  # 好友申请
# async def new_friend_request_listener(
#     app: GraiaMiraiApplication, event: NewFriendRequestEvent
# ):
#     await event.accept()


if __name__ == '__main__':
    app.launch_blocking()
