# 甲骨文考释助手 · Oracle Bone Research

[EN](README.en.md) · **[CH-ZH](README.md)** · [MIT 许可证](LICENSE)

给 AI 一张拓片、一条辞号或一篇论文，让它找出目标字在材料中的位置，比较前人的释读，并说明哪条辞例最能区分两种解释。这个 skill 适合整理可以交给其他研究者复核的考释草稿。

**项目口号：「破解一个甲骨文，奖励十万元。」** 十万元出自中国文字博物馆的历史征集公告，面向经专家鉴定通过的未释字破译成果。申报资格、期限与奖金以主办方当期公告为准。[历史公告](https://www.nopss.gov.cn/n1/2019/0523/c219469-31100368.html)

## 支持的工具与安装方式

最新发布页提供标准版和 WorkBuddy 版 ZIP，可直接下载后按下表安装。[下载最新版本](https://github.com/runnerback/Oracle-Bone-Research/releases/latest)

项目技能目录为 `skills/oracle-bone-research/`。按目录安装时，请复制整个文件夹，保留其中的脚本和数据。需要 ZIP 的平台可在仓库根目录运行以下命令生成安装包，产物位于 `dist/`。打包只需 Python 3.8 或更高版本的标准库。[技能正文](skills/oracle-bone-research/SKILL.md)

```sh
python3 tools/package_skill.py standard
python3 tools/package_skill.py workbuddy --author "你的发布者名称"
```

| 工具 | 使用方法 |
| --- | --- |
| Claude Code | 将技能文件夹复制到目标项目的 `.claude/skills/` 下，在本地会话输入 `/oracle-bone-research` 和研究问题。[官方说明](https://code.claude.com/docs/en/skills) |
| Codex | 本仓库已配置 `.agents/skills/`，打开本项目后输入 `$oracle-bone-research` 和研究问题即可。用于其他项目时，将技能文件夹复制到该项目的 `.agents/skills/` 下。[官方说明](https://developers.openai.com/codex/skills/) |
| ChatGPT | 在已开放 Skills 和上传权限的工作区，从 Plugins → Skills → Create → Upload from your computer 导入标准包 `dist/oracle-bone-research-standard.zip`。功能开放情况取决于套餐和管理员设置。[官方说明](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) |
| WorkBuddy | 在技能面板选择「添加技能 → 上传技能」，导入 `dist/oracle-bone-research-workbuddy.zip`。若提交到开放平台，打包时请用 `--author` 指定发布署名。[安装说明](https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market) · [开放平台规范](https://open.workbuddy.cn/docs/skill) |
| 字节跳动 TRAE IDE | 将技能文件夹复制到目标项目的 `.trae/skills/` 下，在对话中输入 `/` 选择该技能。使用本仓库时，也可在「设置 → 技能与命令」中启用已有的 `.agents/skills/` 目录。[官方说明](https://docs.trae.cn/ide_skills) |
| 字节跳动扣子编程（Coze） | 在项目对话框打开「技能 → 创建技能 → 本地上传」，选择 `dist/oracle-bone-research-standard.zip`，再从「我的技能」添加到当前任务。[使用说明](https://docs.coze.cn/guides_using_skill) · [技能包格式](https://docs.coze.cn/guides_skill_faq) |
| 字节跳动豆包及其他通用 LLM 对话工具 | 手动使用时，把 `SKILL.md` 正文和研究问题一起贴入对话。需要核对字形时，先用下文的本地命令生成裁图和 JSON，再把材料交给模型比较。 |

使用宿主自带的 PDF 阅读器或直接上传页图即可开始。可运行 Python 的环境还可启用离线页码检索和 PNG 导出，详见[资料与命令](skills/oracle-bone-research/references/sources.md)。

## 用两个项目复核同一个字

在本项目中可以直接尝试以下请求。

> 用 $oracle-bone-research 找出合 659 第 1 组第 2 个字。从 AlphaOracle 摹本裁出字形，查 OBIMD 里还有哪一片标了同一个字，并告诉我应当怎样核对这两处用法。

仓库和技能安装包都自带主字标注及示例图。在装有 Pillow 的 Python 环境中，从项目根目录运行以下命令即可离线裁图。

```sh
python3 skills/oracle-bone-research/scripts/glyph_case.py \
  --plate h00659.jpg --group 1 --position 2 \
  --crop research-data/h00659-g1-p2.png
```

输出是一张 85 × 132 像素的局部摹本，以及一份含片号、字位、坐标和同组标签的 JSON。这个字在 OBIMD 中还见于 `h05377.jpg` 第 1 组第 8 位。两处被标为同一主字，下一步可以比较两处的刻画与它们在辞中的用法。整个示例可离线运行。配置 AlphaOracle API 后，同一张裁图也能用于单字分类或相似字形检索。[操作说明](skills/oracle-bone-research/references/glyph-case.md)

## 在仓库中找到研究材料

| 目录 | 内容与来源 |
| --- | --- |
| [技能资源](skills/oracle-bone-research/assets/) | OBIMD 分句任务的主字标注，AlphaOracle 的五张示例图片，以及它们的许可与引用信息。 |
| [训练与评测任务](tasks/) | OBIMD 的字检测、分句、组内排序代码，以及原仓库随附的数据、配置和权重。 |
| [研究模型](models/) | AlphaOracle 的拓片解析、字形分析、文献检索实现及其第三方组件。 |
| [接口与笔记本示例](example/) | AlphaOracle 的命令行演示和 Jupyter Notebook。示例与技能共用图像。 |
| [OBIMD 上游说明](docs/upstream/obimd/README.md) · [AlphaOracle 上游说明](docs/upstream/alphaoracle/README_zh-CN.md) | 随原仓库提供的说明、论文插图和许可证。 |

## 试一个有出处的例子

从 [Schwartz 的花园庄东地译注章](https://doi.org/10.1515/9781501505294-003)取得章节 PDF，将它附在对话里，输入下面这句话。

> 请用甲骨文考释助手复核花东 28.7。目标是酉旁有三笔的字。请定位印刷页和注号，比较两种已有释读，并指出需要查哪一片才能检验两说。

核对输出时，应能翻到该章 PDF 第 33 页、印刷第 107 页、注 100。答复应交代所用的是释文、原拓还是转引，并指出「读作酒」已有学者提出。[查看复核示例](skills/oracle-bone-research/references/worked-example.md)

换成自己的材料时，可以问「这张拓片第三行里两个字是否为异体？请标出共同笔画、残损处和仍需核对的地方」，也可以问「选一个有争议的字，为两种旧说各找最难解释的一条辞例」。

## 项目声明、致谢与支持

- **OBIMD**　感谢并支持李邦及合作者开放甲骨文多模态标注，使研究者能从一个字的坐标追查整版和异版辞例。使用标注时请引用数据论文。[项目](https://github.com/libang1991/OBIMD) · [论文](https://doi.org/10.1038/s41597-026-06967-0)
- **AlphaOracle**　感谢并支持刘禹良等作者公开摹本示例、单字识别与形近检索接口，使同一字位可交给模型提出候选，再回到材料检验。使用相关结果时请引用原作。[项目](https://github.com/Yuliang-Liu/AlphaOracle) · [论文](https://doi.org/10.1016/j.xinn.2026.101462)

历史问答与史料引证还可参考 [HistoryAgentSkills](https://github.com/quzhi1/HistoryAgentSkills)。

## 开源协议

本项目原创代码和技能说明采用 **MIT License**。使用、修改或分发这些内容时，请保留版权声明和许可文本。[MIT 许可证全文](LICENSE)

随包上游材料保留各自的许可。OBIMD 代码采用 MIT，其 GitHub 仓库随附标注按该版本的说明供学术研究使用，商用需取得作者许可。AlphaOracle 仓库采用 Apache-2.0，其中的第三方组件和图像依各自来源条款使用。[完整声明与引用](skills/oracle-bone-research/references/acknowledgments.md)

## 发布与资料

维护者在已推送到 `main` 的发布提交上创建并推送新标签。标签格式为 `v主版本.次版本.修订号`。例如，下列命令发布 `v0.3.1`。GitHub Actions 会按该标签构建两个安装包，生成发布说明，并在附件上传完成后公开 Release。

```sh
git tag -a v0.3.1 -m "Release v0.3.1"
git push origin refs/tags/v0.3.1
```

两个安装包均包含本地研究脚本、主字标注、五张示例图与上游许可。训练任务、模型源码和完整的上游说明随项目源码提供。研究者可将自己的论文、拓片和裁图放在 `research-data/`，该目录已从 Git 默认跟踪范围中排除。外部资料的使用依各来源的许可。Schwartz 章节标注为 [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/)。

整理申奖材料时，保留贡献者署名、文献依据和新增证据，明确指出哪些解释已由前人提出。
