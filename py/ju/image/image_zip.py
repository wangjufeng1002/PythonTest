from PIL import Image, ImageSequence
import numpy as np
import io


def compress_animated_gif(input_bytes, max_size=600, quality=80, loop=0):
    """
    动态图压缩函数（支持多帧处理）
    :param input_bytes: 输入图片字节流
    :param max_size: 最大边长限制
    :param quality: 压缩质量（0-100）
    :param loop: 循环次数（0表示无限循环）
    :return: 压缩后的字节流
    """
    try:
        # 使用Pillow处理动态图
        with Image.open(io.BytesIO(input_bytes)) as img:
            # 检测是否为动态图
            if not getattr(img, "is_animated", False):
                return compress_static_image(img, max_size, quality)

            # 提取所有帧
            frames = []
            durations = []
            for frame in ImageSequence.Iterator(img):
                # 转换为RGBA模式避免透明度问题
                frame = frame.convert("RGBA")
                # 缩放处理
                if max(frame.size) > max_size:
                    ratio = max_size / max(frame.size)
                    frame = frame.resize((int(frame.width * ratio), int(frame.height * ratio)),
                                         Image.Resampling.LANCZOS)
                frames.append(frame)
                durations.append(img.info.get('duration', 100))

            # 合并帧并保存
            output = io.BytesIO()
            frames[0].save(
                output,
                format="GIF",
                save_all=True,
                append_images=frames[1:],
                duration=durations,
                loop=loop,
                optimize=True,
                disposal=2,  # 帧间优化
                quality=quality
            )
            return output.getvalue()
    except Exception as e:
        print(f"压缩失败: {str(e)}")
        return None


def compress_static_image(img, max_size=600, quality=80):
    """静态图压缩辅助函数"""
    if max(img.size) > max_size:
        ratio = max_size / max(img.size)
        img = img.resize((int(img.width * ratio), int(img.height * ratio)), Image.Resampling.LANCZOS)
    buffer = io.BytesIO()
    img.save(buffer, format="WEBP", quality=quality)
    return buffer.getvalue()


# 示例使用
if __name__ == "__main__":
    # 从文件读取
    with open("C:\\Users\\pc\\Documents\\2.gif", "rb") as f:
        gif_bytes = f.read()

    # 压缩处理
    compressed = compress_animated_gif(gif_bytes, max_size=800, quality=90, loop=0)

    # 保存结果
    if compressed:
        with open("2.gif", "wb") as f:
            f.write(compressed)