# 用 OBIMD 和 AlphaOracle 复核一个字位

源码版从 `assets/obimd/all_dataset.json` 读取完整主字标注。两个发布 ZIP 中的 `assets/obimd/example_plates.json` 只收录合 52、659、5377。每个字位由样本文件名、组序、组内位序定位。后两项从 1 起算，组序是数据集内的分组编号。报告引用正式著录辞号时需另外核对。

## 合 659 离线示例

以下命令从含有 `SKILL.md` 的技能目录运行。在源码仓库中先进入 `skills/oracle-bone-research/`，安装包解压后进入 `oracle-bone-research/`。脚本按自身位置定位资源，也可以从其他工作目录调用。

裁图使用锁定版 Pillow。使用 Python 3.11 或更高版本在技能目录内建立虚拟环境。

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

```sh
.venv/bin/python scripts/glyph_case.py --plate h00659.jpg --group 1 --position 2 \
  --crop h00659-g1-p2.png
```

脚本输出 JSON，并将所选字位保存为 PNG。已有的输出文件会保留，复跑时可换文件名或省略 `--crop`。只查标注与异版用例时，省略 `--image` 和 `--crop`，仅需 Python 标准库。内置整图对应 `h00659.jpg`（摹本）和 `h00052.jpg`（拓片）。其他片号裁图时用 `--image` 指定对齐的整图。需要全库检索时，用 `--obimd` 指定本项目源码或 OBIMD 仓库的本地根目录，并在裁图时用 `--image` 提供对应整图。无需网络下载。输出的 `annotation_scope` 标记检索范围；`bundled_examples` 表示同 UID 计数仅覆盖三个示例样本，不能据其零命中作全库结论。

| 可复核的观察 | 如何使用 |
| --- | --- |
| 合 659 摹本为 448 × 1111 像素，第 1 组第 2 位的标注框为 `[246, 356, 85, 132]`。 | 以左上为原点，四个数依次是横坐标、纵坐标、宽、高。对照整版与裁图时，核实位置、方向、残损与描摹痕迹。更换图源时应先核对图版是否对齐，尺寸相同也可能有平移或翻转。 |
| 该位的主字 UID 为 `fmueu74w0p`。本地标注还在 `h05377.jpg` 第 1 组第 8 位收录了它。 | 调取第二片的原图，独立对照构件与所在辞例，再判断两处用法能否互证。UID 表示上游的归类；释义、读音与是否属于未释字需要各自的证据。 |

`group_uids` 保留目标所在组的完整 UID 序列及空值。`same_uid_on_other_plates` 统计其他样本文件内的同 UID 字位，默认列出前五处，可用 `--limit` 调整。一个样本可有多个字位，缀合、重印也需回著录核对。目标 UID 为空时，此项为 `null`，空标签不能用来归并字形。

## 加入 AlphaOracle 的模型候选

默认检索和裁图均在本地完成。用户明确要向指定服务查询时，先本地查看裁图，确认仅含可外发的目标字；优先使用自建或机构已批准的地址，远程服务优先使用 HTTPS。只设置 `ALPHAORACLE_SERVER_URL` 不会联网。显式选择 `--alpha-task` 后，脚本向 `--server-url`（优先）或该环境变量指定的服务 POST 仅含单字 PNG 的 JSON；图像元数据已移除。整片、PDF、路径和标注不会随请求发送。服务端是否保存裁图及保存期限由运营方决定，无法核实留存要求时使用本地流程。

给上述裁图命令增加以下参数即可查询；复跑时去掉已生成文件的 `--crop` 参数。

```sh
--alpha-task moben_danzi_classify --server-url "$ALPHAORACLE_SERVER_URL"
```

摹本单字选 `moben_danzi_classify`，拓片单字选 `tapian_danzi_classify`，找形近实例选 `dino_search`。脚本从返回值提取候选标识与数值分数，保留任务和服务来源。未识别字段、服务端文件路径及原始响应不写入结果。分类的 `Possibility` 和检索的 `score` 来自不同任务，不能据此换算考释成立的概率。检索命中若只有服务端文件标识，还需追查正式片号及图版。接口失败时，脚本仍输出 OBIMD 记录，并在 `alphaoracle.error` 记录原因，以非零状态退出。[上游接口示例](https://github.com/Yuliang-Liu/AlphaOracle/blob/main/example/demo.ipynb)
