# Oracle Bone Research · 甲骨文考释助手

**[EN](README.en.md)** · [CH-ZH](README.md) · [MIT License](LICENSE)

Give the skill a rubbing, an inscription number, or a paper. It helps you locate a particular glyph, compare published readings, and identify an inscription that could distinguish between them. The resulting research note gives another reader enough detail to check the argument against the sources.

**“Decipher one oracle bone character, earn RMB 100,000.”** The project motto refers to a historical award from the National Museum of Chinese Writing for decipherments of previously unread characters accepted by an expert panel. Eligibility, deadlines, and payment depend on the organizer’s announcement for each round. [Historical award notice](https://www.nopss.gov.cn/n1/2019/0523/c219469-31100368.html)

## Supported tools and installation

Download the standard or WorkBuddy ZIP from the latest release, then follow the instructions for your tool below. [Download the latest release](https://github.com/runnerback/Oracle-Bone-Research/releases/latest)

For tools that load a skills directory, copy the entire `skills/oracle-bone-research/` folder so the scripts and data travel with the instructions. For tools that accept a ZIP, run the commands below from the repository root. The packager uses the Python 3.8+ standard library and writes both archives to `dist/`. [Skill instructions](skills/oracle-bone-research/SKILL.md)

```sh
python3 tools/package_skill.py standard
python3 tools/package_skill.py workbuddy --author "Your publisher name"
```

| Tool | How to use the skill |
| --- | --- |
| Claude Code | Copy the skill folder into the target project’s `.claude/skills/`. In a local session, enter `/oracle-bone-research` followed by your question. [Claude Code guide](https://code.claude.com/docs/en/skills) |
| Codex | Open this repository and enter `$oracle-bone-research` followed by your question. Its `.agents/skills/` directory already points to the skill. For another project, copy the skill folder into that project’s `.agents/skills/`. [Codex guide](https://developers.openai.com/codex/skills/) |
| ChatGPT | In a workspace with Skills and uploads enabled, open **Plugins → Skills → Create → Upload from your computer** and select `dist/oracle-bone-research-standard.zip`. Availability depends on your plan and workspace settings. [ChatGPT guide](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) |
| WorkBuddy | In the Skills panel, choose **Add skill → Upload skill** and select `dist/oracle-bone-research-workbuddy.zip`. If you submit it to the Open Platform, set the publisher name with `--author` when building the ZIP. [Installation guide](https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market) · [Package specification](https://open.workbuddy.cn/docs/skill) |
| ByteDance TRAE IDE | Copy the skill folder into the target project’s `.trae/skills/`, then type `/` in chat to select it. In this repository, you can also enable the existing `.agents/skills/` directory in the IDE’s skills settings. [TRAE guide](https://docs.trae.cn/ide_skills) |
| ByteDance Coze (扣子编程) | Open the skills panel in a project chat, choose **Create skill → Local upload**, and select `dist/oracle-bone-research-standard.zip`. Add the uploaded skill to the current task from **My skills**. [Coze guide](https://docs.coze.cn/guides_using_skill) · [Supported archive formats](https://docs.coze.cn/guides_skill_faq) |
| ByteDance Doubao (豆包) and other LLM chat tools | For manual use, paste the contents of `SKILL.md` into the chat along with your question. To compare glyphs, run the local example below and share only the plate number, position, and observations cleared for that chat. |

You can also start with your tool’s PDF reader or provide an image of the relevant page. In a Python environment, the included PDF helper can search a local document and export individual pages as PNGs. [Sources and commands](skills/oracle-bone-research/references/sources.md)

## Trace one glyph across two plates

> Use $oracle-bone-research to find the second glyph in group 1 on Heji 659. Crop it from the AlphaOracle facsimile, find another plate where OBIMD assigns the same label, and explain how to compare the two uses.

The source repository includes the full annotations. Both release ZIPs include the plates needed for this example. From the repository root, set up a virtual environment with Python 3.11 or later and the pinned dependencies. The crop runs offline after setup.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r skills/oracle-bone-research/requirements.txt
.venv/bin/python skills/oracle-bone-research/scripts/glyph_case.py \
  --plate h00659.jpg --group 1 --position 2 \
  --crop research-data/h00659-g1-p2.png
```

The command saves an 85 × 132 pixel crop and prints a JSON record with the plate, position, bounding box, and labels of the surrounding glyphs. OBIMD assigns the same main-character identifier to position 8 in group 1 on `h05377.jpg`. Compare the strokes and the two inscription contexts before proposing a reading. This example runs offline. With an AlphaOracle API endpoint configured, you can also submit the crop for classification or retrieve visually similar glyphs. [Glyph lookup guide](skills/oracle-bone-research/references/glyph-case.md)

## Research materials in the repository

| Directory | Contents |
| --- | --- |
| [Skill assets](skills/oracle-bone-research/assets/) | Main-character annotations from OBIMD’s sentence-grouping task, five AlphaOracle example images, and their license and citation files. |
| [Training and evaluation tasks](tasks/) | OBIMD character detection, sentence grouping, and reading-order code, with the data, configurations, and weights supplied upstream. |
| [Research models](models/) | AlphaOracle implementations for rubbing analysis, glyph morphology, and literature retrieval, together with their third-party components. |
| [API and notebook examples](example/) | AlphaOracle’s command-line demo and Jupyter notebook. They use the same images as the skill. |
| [OBIMD documentation](docs/upstream/obimd/README.md) · [AlphaOracle documentation](docs/upstream/alphaoracle/README.md) | The upstream project descriptions, paper figures, and licenses. |

## Check a published reading

Attach the chapter PDF from Adam C. Schwartz’s translation of the Huayuanzhuang East inscriptions and try this question. [Translation and commentary](https://doi.org/10.1515/9781501505294-003)

> Revisit Huayuanzhuang East inscription 28.7. Look for the graph with three strokes next to 酉. Give the printed page and note number, compare two published readings, and identify a plate that could help test them.

You can check the answer on page 33 of the chapter PDF, printed page 107, note 100. The answer should identify whether its evidence comes from a transcription, a rubbing, or a secondary citation, and attribute the earlier reading 酒 (“wine”). [Worked example in Chinese](skills/oracle-bone-research/references/worked-example.md)

For your own material, try asking which strokes support treating two graphs as variants, where damage obscures the comparison, or which inscription is hardest to explain under each proposed reading.

## Acknowledgments and upstream projects

- **OBIMD.** We thank Bang Li and colleagues for publishing multimodal annotations that let researchers trace a glyph from its coordinates on one plate to related occurrences elsewhere. Please cite the dataset paper when using its annotations. [Project](https://github.com/libang1991/OBIMD) · [Paper](https://doi.org/10.1038/s41597-026-06967-0)
- **AlphaOracle.** We thank Yuliang Liu and colleagues for sharing their facsimile examples, character classification interface, and visual retrieval tools. They give researchers candidates to check against the inscriptions. Please cite the original work when using these materials or results. [Project](https://github.com/Yuliang-Liu/AlphaOracle) · [Paper](https://doi.org/10.1016/j.xinn.2026.101462)

For historical question answering and source citation, see [HistoryAgentSkills](https://github.com/quzhi1/HistoryAgentSkills).

## License

The project’s original code and skill instructions are available under the **MIT License**. Retain the copyright and permission notices when using, modifying, or distributing them. [Full MIT License](LICENSE)

Bundled upstream materials retain their own terms. OBIMD code uses the MIT License. The OBIMD repository version that supplied these annotations specifies academic research use and requires permission from the authors for commercial use. AlphaOracle uses Apache-2.0. Its third-party components and images retain the terms of their respective sources. [Attribution and citation details](skills/oracle-bone-research/references/acknowledgments.md)

## Packages and research files

The target tag for this security update is `0.3.2`. Create an annotated `MAJOR.MINOR.PATCH` tag on the release commit already pushed to `main`, then push the tag. GitHub Actions builds both packages from the tag, generates release notes, and publishes the release once the assets are attached.

```sh
git tag -a 0.3.2 -m "Release 0.3.2"
git push origin refs/tags/0.3.2
```

Both release ZIPs include the pinned dependency list, scripts, annotations for Heji 52, 659 and 5377, two plate images, and upstream licenses. Their default occurrence counts cover those three plates. Use `--obimd` with a local source checkout to search the full annotations. The repository also includes the training tasks, model sources, and upstream documentation. Keep your own papers, rubbings, and crops in `research-data/`, which Git ignores. External material remains subject to its source terms. The Schwartz chapter carries a [CC BY-NC-ND 4.0 license](https://creativecommons.org/licenses/by-nc-nd/4.0/).

When preparing an award submission, credit the contributors, cite earlier readings, and identify the evidence your research adds.
