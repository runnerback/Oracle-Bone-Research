# 用 OBIMD 和 AlphaOracle 复核一个字位

脚本从技能内的 `assets/obimd/all_dataset.json` 读取 OBIMD 主字标注，每个字位由样本文件名、组序、组内位序定位。后两项从 1 起算，组序是数据集内的分组编号。报告引用正式著录辞号时需另外核对。

## 合 659 离线示例

以下命令从含有 `SKILL.md` 的技能目录运行。在源码仓库中先进入 `skills/oracle-bone-research/`，安装包解压后进入 `oracle-bone-research/`。脚本按自身位置定位资源，也可以从其他工作目录调用。

裁图使用 Pillow。已有 Pillow 的环境可直接执行第二段命令。新建本地环境可用：

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install Pillow
```

```sh
python3 scripts/glyph_case.py --plate h00659.jpg --group 1 --position 2 \
  --crop h00659-g1-p2.png
```

脚本输出 JSON，并将所选字位保存为 PNG。已有的输出文件会保留，复跑时可换文件名或省略 `--crop`。只查标注与异版用例时，省略 `--image` 和 `--crop`，仅需 Python 标准库。内置整图对应 `h00659.jpg`（摹本）和 `h00052.jpg`（拓片）。其他片号裁图时用 `--image` 指定对齐的整图。若要对照另一个版本的 OBIMD，可用 `--obimd` 指定该仓库根目录，并在裁图时显式提供相应版本的整图。

| 可复核的观察 | 如何使用 |
| --- | --- |
| 合 659 摹本为 448 × 1111 像素，第 1 组第 2 位的标注框为 `[246, 356, 85, 132]`。 | 以左上为原点，四个数依次是横坐标、纵坐标、宽、高。对照整版与裁图时，核实位置、方向、残损与描摹痕迹。更换图源时应先核对图版是否对齐，尺寸相同也可能有平移或翻转。 |
| 该位的主字 UID 为 `fmueu74w0p`。本地标注还在 `h05377.jpg` 第 1 组第 8 位收录了它。 | 调取第二片的原图，独立对照构件与所在辞例，再判断两处用法能否互证。UID 表示上游的归类；释义、读音与是否属于未释字需要各自的证据。 |

`group_uids` 保留目标所在组的完整 UID 序列及空值。`same_uid_on_other_plates` 统计其他样本文件内的同 UID 字位，默认列出前五处，可用 `--limit` 调整。一个样本可有多个字位，缀合、重印也需回著录核对。目标 UID 为空时，此项为 `null`，空标签不能用来归并字形。

## 加入 AlphaOracle 的模型候选

在上面的命令后追加以下参数即可调用研究者指定的服务。将环境变量设为实际 API 根地址；服务会收到按本次标注框截取的单字 PNG。

```sh
--alpha-task moben_danzi_classify --server-url "$ALPHAORACLE_SERVER_URL"
```

摹本单字选 `moben_danzi_classify`，拓片单字选 `tapian_danzi_classify`，找形近实例选 `dino_search`。保留返回的分类候选、排序、分值或检索标识，注明服务地址与任务。分类的 `Possibility` 和检索的 `score` 来自不同任务，不能据此换算考释成立的概率。检索命中若只有服务端文件标识，还需追查正式片号及图版。接口失败时，脚本仍输出 OBIMD 记录，并在 `alphaoracle.error` 记录原因，以非零状态退出。[上游接口示例](https://github.com/Yuliang-Liu/AlphaOracle/blob/main/example/demo.ipynb)
