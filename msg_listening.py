import asyncio
import websockets
import json

# 指定你想捕获的消息类型
# 1[普通弹幕]，2[点赞消息]，3[进入直播间]，4[关注消息]，5[礼物消息]，6[统计消息]，7[粉丝团消息]，8[直播间分享]，9[下播]
message_types_to_capture = {1, 4, 5}
message_type_descriptions = {
    1: "普通弹幕",
    2: "点赞消息",
    3: "进入直播间",
    4: "关注消息",
    5: "礼物消息",
    6: "统计消息",
    7: "粉丝团消息",
    8: "直播间分享",
    9: "下播"
}

async def receive_messages():
    uri = "ws://127.0.0.1:8888/"
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                while True:
                    message = await websocket.recv()
                    try:
                        # 解析消息中的JSON内容
                        msg_dict = json.loads(message)

                        # 获取Type字段，并检查它是否是我们感兴趣的类型
                        message_type = msg_dict.get("Type")
                        if message_type in message_types_to_capture:
                            # 获取Data字段，确保其为字符串
                            data_str = msg_dict.get("Data")
                            if isinstance(data_str, str):
                                # 替换转义的双引号以正确解析JSON
                                data_dict = json.loads(data_str.replace('\\"', '"'))
                                if isinstance(data_dict, dict):
                                    # 提取有用的部分
                                    content = data_dict.get("Content", "")
                                    user_info = data_dict.get("User", {})
                                    nickname = user_info.get("Nickname", "")
                                    # 获取消息类型的描述
                                    message_description = message_type_descriptions.get(message_type, "未知消息类型")
                                    # 打印有用的部分
                                    print(f"{message_description}, Nickname: {nickname}, Content: {content}")
                                else:
                                    print("Data is not a dictionary")
                            else:
                                print("Data is not a string")
                        # else:
                        #     print(f"Ignored message type: {message_type}")

                    except json.JSONDecodeError as e:
                        print(f"JSON decode error: {e}")
        except websockets.ConnectionClosedError as e:
            print(f"Connection closed with error: {e}")
            print("Attempting to reconnect...")
            await asyncio.sleep(5)  # 等待5秒钟再重新连接
        except Exception as e:
            print(f"An error occurred: {e}")
            break  # 如果出现ConnectionClosedError以外的错误，中断循环

asyncio.get_event_loop().run_until_complete(receive_messages())