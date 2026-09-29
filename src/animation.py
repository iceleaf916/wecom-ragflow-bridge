"""动画效果模块"""

import asyncio
import logging
from collections.abc import Awaitable, Callable

from protocol import MessageBuilder

logger = logging.getLogger("wecom-RAGFLOW-bridge")


async def animate_waiting(
    send_message: Callable[[dict], Awaitable[None]],
    req_id: str,
    stream_id: str,
    timeout: int = 300,
):
    """发送企微原生思考动画，并等待最终回复关闭同一条流。

    OpenClaw 使用 ``<think></think>`` 作为首帧、``finish=false``，企微客户端
    会将其渲染为原生思考动画。这里不再发送可见的“正在思考”文本，也不发送
    普通文本消息；最终回复必须复用同一个 stream_id 并设置 finish=true。
    """
    try:
        await send_message(MessageBuilder.build_thinking(req_id, stream_id))
        await asyncio.sleep(timeout)
    except asyncio.CancelledError:
        raise
    except Exception as exc:
        logger.warning(
            "发送企微原生思考动画失败: req_id=%s, stream_id=%s, error=%s",
            req_id,
            stream_id,
            exc,
        )
