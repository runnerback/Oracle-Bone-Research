"""Locate an OBIMD glyph, collect comparable occurrences, and optionally query AlphaOracle."""

import argparse
import base64
from http.client import HTTPException
from io import BytesIO
from ipaddress import ip_address
import json
import os
from pathlib import Path
import sys
from urllib.parse import urlsplit
from urllib.request import ProxyHandler, Request, build_opener


ASSETS = Path(__file__).resolve().parents[1] / "assets"
UPSTREAM_ANNOTATIONS = Path("tasks/cluster_sentence/datasets/all_dataset.json")
PLATE_IMAGES = {"h00659.jpg": "h00659.jpg", "h00052.jpg": "合52拓片.png"}
TASKS = ("moben_danzi_classify", "tapian_danzi_classify", "dino_search")


def occurrence(row, group, position):
    labels = row["line"][group - 1]
    boxes = row["box"][group - 1]
    if len(labels) != len(boxes):
        raise ValueError(f"{row['name']} 第 {group} 组的标签数与坐标框数不一致")
    box = [int(value) for value in boxes[position - 1].split(",")]
    if len(box) != 4 or min(box[2:]) <= 0:
        raise ValueError(f"{row['name']} 的字框无效：{box}")
    return {
        "plate": row["name"], "group": group, "position": position,
        "uid": labels[position - 1], "bbox_xywh": box, "group_uids": labels,
    }


def find_case(rows, plate, group, position, limit):
    row = next((r for r in rows if r["name"] == plate), None)
    if row is None:
        raise ValueError(f"找不到片号文件 {plate}，请核对 OBIMD 中的完整文件名")
    if not 1 <= group <= len(row["line"]):
        raise ValueError(f"{plate} 有 {len(row['line'])} 个标注组，组序从 1 起算")
    if not 1 <= position <= len(row["line"][group - 1]):
        raise ValueError(f"第 {group} 组有 {len(row['line'][group - 1])} 个字位，位序从 1 起算")
    target = occurrence(row, group, position)
    parallels = None
    if target["uid"] is not None:
        examples = []
        count = 0
        for other in rows:
            if other["name"] == plate:
                continue
            for g, labels in enumerate(other["line"], start=1):
                for p, label in enumerate(labels, start=1):
                    if label == target["uid"]:
                        count += 1
                        if len(examples) < limit:
                            examples.append(occurrence(other, g, p))
        parallels = {"total_occurrences": count, "examples": examples}
    return {
        "target": target, "plate_size_wh": [row["width"], row["height"]],
        "same_uid_on_other_plates": parallels,
    }


def crop_glyph(image_path, size, box):
    try:
        from PIL import Image
    except ImportError as exc:
        raise ValueError("裁图需要 Pillow，请先运行 python3 -m pip install Pillow") from exc
    x, y, width, height = box
    # A few upstream annotations extend a few pixels beyond the plate.
    bounds = (max(0, x), max(0, y), min(size[0], x + width), min(size[1], y + height))
    if bounds[2] <= bounds[0] or bounds[3] <= bounds[1]:
        raise ValueError("该标注框落在图版之外")
    with Image.open(image_path) as image:
        if list(image.size) != size:
            raise ValueError(f"图像尺寸 {image.size} 与标注 {size} 不符，请使用同版同坐标的整图")
        with image.crop(bounds) as glyph, BytesIO() as buf:
            glyph.info.clear()
            glyph.save(buf, format="PNG")
            return buf.getvalue(), bounds


def query_alpha(server, task, png):
    endpoint = server.rstrip("/") + "/" + task + "/"
    payload = {"image": base64.b64encode(png).decode("ascii")}
    request = Request(endpoint, json.dumps(payload).encode(), {"Content-Type": "application/json"})
    # A system-wide HTTP proxy must not route requests away from a local model server.
    host = urlsplit(server).hostname
    try:
        local = ip_address(host).is_loopback
    except ValueError:
        local = host.rstrip(".") == "localhost"
    opener = build_opener(ProxyHandler({})) if local else build_opener()
    with opener.open(request, timeout=60) as response:
        result = json.load(response)
    if task == "dino_search":
        valid = isinstance(result, dict) and isinstance(result.get("items"), list)
    else:
        valid = isinstance(result, list) and all(isinstance(r, dict) and "Category" in r for r in result)
    if not valid:
        raise ValueError(f"{task} 返回的数据与上游示例格式不符")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--obimd", type=Path, help="改用指定 OBIMD 仓库的主字标注，默认使用技能自带标注")
    parser.add_argument("--plate", required=True, help="OBIMD 样本文件名，如 h00659.jpg")
    parser.add_argument("--group", type=int, required=True, help="标注组序，从 1 起算")
    parser.add_argument("--position", type=int, required=True, help="组内字位，从 1 起算")
    parser.add_argument("--limit", type=int, default=5, help="最多列出的异版同 UID 字例数")
    parser.add_argument("--image", type=Path, help="与标注坐标对齐的整图；合 52 和合 659 有内置示例图")
    parser.add_argument("--crop", type=Path, help="把所选字保存到新的 PNG 文件")
    parser.add_argument("--alpha-task", choices=TASKS, help="将所选字图提交给 AlphaOracle")
    parser.add_argument("--server-url", help="AlphaOracle API 地址（也可用 ALPHAORACLE_SERVER_URL）")
    args = parser.parse_args()
    if args.limit < 0:
        parser.error("--limit 须为非负整数")
    image_path = args.image
    if (args.crop or args.alpha_task) and image_path is None:
        if args.obimd is not None or args.plate not in PLATE_IMAGES:
            parser.error("请通过 --image 提供与所选标注对齐的整版拓片或摹本")
        image_path = ASSETS / "alphaoracle/images" / PLATE_IMAGES[args.plate]
    if args.server_url and not args.alpha_task:
        parser.error("请用 --alpha-task 选择服务任务")
    server = args.server_url or os.environ.get("ALPHAORACLE_SERVER_URL", "")
    if args.alpha_task:
        address = urlsplit(server)
        if address.scheme not in ("http", "https") or not address.hostname:
            parser.error("请为 AlphaOracle 指定 HTTP(S) API 地址")

    data_path = args.obimd / UPSTREAM_ANNOTATIONS if args.obimd else ASSETS / "obimd/all_dataset.json"
    with data_path.open(encoding="utf-8") as src:
        case = find_case(json.load(src), args.plate, args.group, args.position, args.limit)
    case["annotations"] = str(data_path)
    if image_path is not None:
        png, bounds = crop_glyph(image_path, case["plate_size_wh"], case["target"]["bbox_xywh"])
        case["image"] = {"source": str(image_path), "crop_xyxy": bounds}
        if args.crop:
            args.crop.parent.mkdir(parents=True, exist_ok=True)
            with args.crop.open("xb") as dest:
                dest.write(png)
            case["image"]["crop_png"] = str(args.crop)
    status = 0
    if args.alpha_task:
        alpha = {"task": args.alpha_task, "server": server}
        case["alphaoracle"] = alpha
        try:
            alpha["result"] = query_alpha(server, args.alpha_task, png)
        except (OSError, ValueError, HTTPException) as exc:
            alpha["error"] = str(exc)
            status = 1
    print(json.dumps(case, ensure_ascii=False, indent=2))
    return status


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, IndexError, TypeError) as exc:
        sys.exit(f"glyph_case: {exc}")
