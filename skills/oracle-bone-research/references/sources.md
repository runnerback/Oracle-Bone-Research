# 来源与定位

| 想解决的问题 | 从哪里查 | 带回什么 |
| --- | --- | --- |
| 字的哪几笔确实可见？ | [中央研究院甲骨文拓片资料库介绍](https://ascdc.digitalarchives.tw/site_3749.html)，或有图版号的发掘报告 | 馆藏号、著录号、面、目标所在行与前后字，注明图像类型 |
| 拓片、摹本和分句怎样对齐？ | [OBIMD 数据与代码](https://github.com/libang1991/OBIMD)及[数据论文](https://www.nature.com/articles/s41597-026-06967-0) | 记录样本编号、图像位置及标注来源。另核对目标是否在其收录范围 |
| 花园庄东地某辞有哪些解释？ | Adam C. Schwartz, *The Oracle Bone Inscriptions from Huayuanzhuang East*, [译注章节](https://doi.org/10.1515/9781501505294-003) | HYZ 片号、辞号、印刷页、注号。追查注中所引的原作者与文献 |
| 图形相似的候选从哪里找？ | [AlphaOracle 研究项目](https://github.com/Yuliang-Liu/AlphaOracle) | 把模型命中作为寻找原例的线索；回到著录核对时代、字形和用法 |
| 历史奖励依据是什么？ | [2019 年第二批征集公告](https://www.nopss.gov.cn/n1/2019/0523/c219469-31100368.html) | 该批截止于 2019 年 10 月 31 日。当前资格和期限须另查主办方的新公告 |

## 查本地 PDF

使用当前宿主的 PDF 阅读器即可。若能运行 Python，可用随附脚本检索有文本层的 PDF 和导出页图。以下命令从技能目录运行；将文件名换成用户提供的路径。PDF 应保存在研究者自己的资料目录。

```sh
python3 -m pip install pypdfium2 Pillow
python3 scripts/source_pages.py find "/path/to/chapter.pdf" --clause 28.7 --first-printed 75
python3 scripts/source_pages.py find "/path/to/chapter.pdf" --term "Zhu Fenghan"
python3 scripts/source_pages.py render "/path/to/chapter.pdf" 33 --output "page-33.png"
```

`--clause` 按本章「片号.辞号」的行首编号定位；跨行、带字母的编号或正文转引可改用 `--term`。结果列出命中页和首个命中的短文本，页序从 1 起算。`--first-printed` 只在已知首页页码且全文连续编页时使用。没有文字层时改看页图；页面提取的空格、替代字符和没有命中都可能源于字体编码。

只具备对话能力时，可请用户附相应页图或拓片。把能从所给材料确认的内容先交付，再列需要补查的资料。
