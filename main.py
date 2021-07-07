import asyncio

from graia.application import GraiaMiraiApplication, Session
from graia.application.event.messages import GroupMessage, FriendMessage, TempMessage
from graia.application.event.mirai import NewFriendRequestEvent
from graia.application.friend import Friend
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Source, Plain, At, Image, Face
from graia.broadcast import Broadcast

from config import host, auth_key, account
from utils.decorator import command


loop = asyncio.get_event_loop()
bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc, connect_info=Session(
        host=host, authKey=auth_key, account=account, websocket=True
    )
)


def process(message: MessageChain) -> MessageChain:
    content = message.asDisplay().strip()
    if content.startswith('/'):
        result = command.from_str(content[1:])
        if result['type'] == 'text':
            return MessageChain.create([Plain(result['return'])])
        elif result['type'] == 'error':
            return MessageChain.create(
                [Face(faceId=168), Plain(result['return'])]
            )
    return message.asSendable()

@bcc.receiver(FriendMessage)  # 好友聊天
async def friend_message_listener(
    app: GraiaMiraiApplication, friend: Friend, message: MessageChain
):
    await app.sendFriendMessage(friend, process(message))

@bcc.receiver(GroupMessage)  # 群组聊天
async def group_message_listener(
    app: GraiaMiraiApplication, group: Group, member: Member, message: MessageChain
):
    await app.sendTempMessage(
        group, member, process(message), quote=message.get(Source)[0]
    )

@bcc.receiver(TempMessage)  # 临时聊天
async def temp_message_listener(
    app: GraiaMiraiApplication, group: Group, member: Member, message: MessageChain
):
    await app.sendTempMessage(group, member, process(message))

# @bcc.receiver(NewFriendRequestEvent)  # 好友申请
# async def new_friend_request_listener(
#     app: GraiaMiraiApplication, event: NewFriendRequestEvent
# ):
#     await event.accept()


app.launch_blocking()
