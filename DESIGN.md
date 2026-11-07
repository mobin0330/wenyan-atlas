---
name: 文言星图
description: 清透白绿、以语境与原文证据为中心的学习工作台
colors:
  bg: "#f7faf8"
  paper: "#fff"
  rail: "#eaf2ed"
  ink: "#20382f"
  muted: "#52685e"
  line: "#d7e2da"
  accent: "#176a50"
  active: "#d3e9dc"
  violet: "#72529b"
  violet-soft: "#f0eaf7"
  blue: "#30668b"
  blue-soft: "#eaf2f9"
  warn: "#775514"
  warn-bg: "#fbf4df"
  error: "#aa3936"
  dark-bg: "#141e1a"
  dark-paper: "#1b2922"
  dark-rail: "#20362b"
  dark-ink: "#e3eee7"
  dark-muted: "#abbfb1"
  dark-line: "#3f5547"
  dark-accent: "#8bd8b4"
  dark-active: "#2c4d3d"
  dark-violet: "#c6afe7"
  dark-violet-soft: "#33283f"
  dark-blue: "#9dc6e4"
  dark-blue-soft: "#203544"
  dark-warn: "#e8cd8b"
  dark-warn-bg: "#3b3422"
  dark-error: "#f3a19c"
typography:
  headline:
    fontFamily: "-apple-system, BlinkMacSystemFont, \"PingFang SC\", \"Microsoft YaHei\", sans-serif"
    fontSize: "30px"
    fontWeight: 650
    lineHeight: 1.3
    letterSpacing: "-0.025em"
  title:
    fontFamily: "-apple-system, BlinkMacSystemFont, \"PingFang SC\", \"Microsoft YaHei\", sans-serif"
    fontSize: "20px"
    fontWeight: 700
    lineHeight: 1.5
  body:
    fontFamily: "-apple-system, BlinkMacSystemFont, \"PingFang SC\", \"Microsoft YaHei\", sans-serif"
    fontSize: "15px"
    lineHeight: 1.65
  quote:
    fontFamily: "\"Songti SC\", \"Noto Serif CJK SC\", serif"
    fontSize: "19px"
    lineHeight: 1.9
  original:
    fontFamily: "\"Songti SC\", \"Noto Serif CJK SC\", serif"
    fontSize: "25px"
    lineHeight: 2.1
    letterSpacing: "0.06em"
  label:
    fontFamily: "-apple-system, BlinkMacSystemFont, \"PingFang SC\", \"Microsoft YaHei\", sans-serif"
    fontSize: "12px"
    lineHeight: 1.65
  word:
    fontFamily: "\"Songti SC\", \"Noto Serif CJK SC\", serif"
    fontSize: "48px"
    lineHeight: 1.15
rounded:
  highlight: "3px"
  label: "5px"
  field: "8px"
  control: "9px"
  nav: "10px"
  surface: "14px"
spacing:
  step-8: "8px"
  step-12: "12px"
  step-14: "14px"
  step-16: "16px"
  step-18: "18px"
  step-20: "20px"
  step-24: "24px"
  step-28: "28px"
  step-32: "32px"
  step-36: "36px"
  step-44: "44px"
  step-48: "48px"
components:
  button-default:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    padding: "9px 15px"
  button-default-hover:
    backgroundColor: "{colors.rail}"
  button-primary:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.paper}"
    rounded: "{rounded.control}"
    padding: "9px 15px"
  button-primary-hover:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
  button-scope-selected:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.paper}"
    padding: "5px 9px"
  nav-active:
    backgroundColor: "{colors.active}"
    textColor: "{colors.accent}"
    rounded: "{rounded.nav}"
    padding: "12px 15px"
  sense-label:
    backgroundColor: "{colors.violet-soft}"
    textColor: "{colors.violet}"
    rounded: "{rounded.label}"
    padding: "3px 8px"
    typography: "{typography.label}"
  reading-chip:
    textColor: "{colors.accent}"
    rounded: "{rounded.field}"
    padding: "8px 16px"
  reading-sheet:
    backgroundColor: "{colors.paper}"
    rounded: "{rounded.surface}"
    padding: "32px"
  search-field:
    backgroundColor: "{colors.bg}"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    padding: "11px 14px"
  feedback:
    backgroundColor: "{colors.rail}"
    rounded: "{rounded.control}"
    padding: "18px"
  feedback-wrong:
    backgroundColor: "{colors.warn-bg}"
---
# Design System: 文言星图

## Overview

**Creative North Star: "白绿语境标本台"**

以清透的白色阅读面、鼠尾草绿的导航区和墨绿的选择路径组织信息。植物标本分类的影响体现在分组、标签与选择反馈中：字词、具体用法、原文实例是不同类型，正文与操作始终使用标准网页控件。

这是由 HTML、CSS、原生 JavaScript 与 SVG 构成的工作界面。Operate 表达为选择用法、切换视图、搜索与练习；Read 表达为宋体原文、释义与可追溯出处。两者共用简洁边框、克制圆角与明确文字状态；没有装饰性栅格插画或出货栅格图片，品牌标志是手工几何 SVG。

**Key Characteristics:**

- 白绿中性面承担结构，语义色承担类型。
- 黑体操作与释义，宋体原文与中心字词。
- 桌面局部关系与证据并列，窄屏优先文字用法。
- 解释、原句、练习入口和审核链接保持相邻。

## Colors

配色采用清冷纸白、植物灰绿与墨绿，辅以承担明确类型的紫、蓝和提醒色。上方 frontmatter 的颜色值为规范来源；默认浅色，`data-theme=dark` 使用同名 `dark-` 映射。系统偏好用于首次默认值，用户切换结果保存在浏览器。

### Primary

- **墨绿 / 深色浅薄荷（accent）**：中心字词、主要行动、链接、选中路径、焦点环。
- **浅叶绿 / 深色叶影（active）**：当前导航、原文命中字词与正确答案底色。

### Secondary

- **义项紫（violet / violet-soft）**：具体用法的图节点、语法读音标签与展开的文字用法。
- **原文蓝（blue / blue-soft）**：原文实例图节点，与用法类型区分。

### Tertiary

- **核验赭黄（warn / warn-bg）**：样例、待核验提示和需重新判断的反馈。
- **错误红（error）**：错误选项边框；配合文字反馈使用。

### Neutral

- **薄雾底（bg）**：应用主背景和搜索底。
- **阅读纸面（paper）**：表单、关系面板、阅读与练习主面，也作为实心主按钮上的反色文字。
- **鼠尾草导航面（rail）**：侧栏、轻提示、悬停和次级选择面。
- **深墨 / 浅墨（ink）**：正文、标题与 toast 底色。
- **叶灰文字（muted）**：辅助说明、出处与次级导航。
- **浅绿分隔线（line）**：边框、列表分隔、未选择关系路径和滚动条。

**The 语义与选择分离 Rule.** 紫色表示具体用法，蓝色表示原文实例；绿色表示中心字词、当前选择与操作。类别必须同时有文字，颜色不能代替标签。

## Typography

**Display / Body Font:** 系统黑体栈；没有额外下载字体。大标题仍沿用正文家族，不引入装饰性展示字体。

**Original / Quote Font:** Songti SC，Noto Serif CJK SC，serif。

- **Headline**：主标题使用 frontmatter 的 headline；手机降至（26px）。
- **Title**：区块标题使用 title；较小标题为（16px）。
- **Body**：默认 body；手机根字号降至（14px）。页面标题的说明最长（65ch）。释义与注释按语境使用（14–15px）和（1.85–1.9）行高。
- **Quote**：证据引用使用 quote；手机及内联文字证据为（20px）。
- **Original**：全文使用 original；手机为（23px），保持宽松行距与字距。
- **Label**：语法、出处与提示以 label 为主；手机的辅助说明局部降至（10–11px），不将这种密度扩展为正文默认值。
- **Word**：中心字词使用 word；手机为（42px）。

**The 原文有独立声音 Rule.** 原文、引用与中心字词使用宋体栈；操作、释义、来源说明使用系统黑体栈。

## Layout

桌面应用壳为（224px）粘性侧栏加弹性工作区。顶栏、通知、正文保持共同左边线；正文最大宽度（1600px），默认横向内边距（36px），顶部（34px），底部（48px）。主关系视图是弹性图面加（300px）证据栏，间距（24px）。阅读页是正文加（270px）来源与关联词栏，间距（36px）。练习单列最大宽度（760px）；来源页最大宽度（900px）。

- **宽屏（min-width:1500px）**：正文横向留白扩大至（48px），关系证据栏（330px），关系图高（450px）。
- **中屏（max-width:1190px）**：侧栏收至（195px），正文横向留白（26px）；关系与证据改为一列，证据中的两处例句可并排。首次进入默认文字视图；仍可显式切换关系图。图面保留（790px）最小宽度，在最高（480px）的局部容器内滚动，不压缩节点文字。阅读侧栏缩至（220px）。
- **手机（max-width:760px）**：应用壳改为纵向；品牌、横向主导航、默认折叠的学习范围位于顶部。范围摘要显示当前选择，展开后提供多选。搜索旁提供“外观”。正文横向留白（18px）；阅读、比较、证据均改为单列。文字视图的展开项顺序为类型标签、释义、原句及回到原文、更多例句、练习、说明与来源，不另设遥远的证据面板。练习操作在手机使用两列。

间距以 frontmatter 中已使用的步骤为准；不要把所有尺寸强行规整成新网格。按钮、范围选项、链接、选择框保持至少（44px）可操作高度；导航默认（48px）。小标签用于呈现状态，不充当紧密小触控目标。

## Elevation & Depth

界面不使用阴影。层次来自中性底、纸白面、导航绿面与细分隔线；证据栏以（3px）绿色顶边强调当前上下文。toast 使用反色平面，固定在视窗底部居中，层级（50）。跳到内容链接仅在获得焦点时进入视野，层级（20）。

**The 平面层级 Rule.** 使用纸面、导航面、细边框与语义底色区分层级，保持零阴影。

## Shapes

大阅读面与关系面使用 surface 圆角；标准按钮与搜索使用 control 圆角；导航使用 nav，字词小入口与选择框使用 field，语法标签使用 label，命中字词使用 highlight。边框以（1px）细线为主。SVG 中心字词是圆，义项与原文实例是不同大小的圆角矩形；图例以圆、圆角方、直角方配合文字区分类别。书目首字图标使用有书脊感的不对称圆角（4px 10px 10px 4px）。

## Components

### Buttons

标准按钮是细边框纸面控件，默认样式与主要按钮的颜色、内边距在 frontmatter。悬停转导航面并突出绿色边框；主按钮悬停用 ink 底、paper 字。禁用状态不响应点击并降至（0.55）不透明度。主要行动链接保持同一实心色体系，内边距（11px 16px）。分段切换默认透明，按下时 rail 底、accent 字。

状态变化使用（0.14s）的背景、边框或图节点描边过渡，不引入装饰移动。`prefers-reduced-motion: reduce` 关闭过渡和滚动动画。

### Inputs / Fields

搜索为带圆角和边框的单一容器，输入背景透明；原生选择框保持纸面和细线。插入光标为 accent。按钮、链接、输入框、选择框、范围摘要与可聚焦 SVG 目标有可见焦点反馈；普通控件为（3px）accent 外轮廓与（3px）偏移。

### Navigation and Scope

侧栏导航的当前页使用 active 底、accent 字和加重字重。手机导航横排，圆角只留顶部（8px 8px 0 0）。学习范围为原生 details，文字明确“展开 / 收起”，多选状态通过实心按钮与 `aria-pressed` 同步表达，至少保留一项。手机默认收起，桌面默认展开；这是入口初始化行为。

### Chips and Labels

原文侧栏的关联字词入口是细线圆角链接（21px）文字、（8px 16px）内边距。语法与读音使用紫色标签。审核状态使用文字，待审以 warn 呈现；标签不能替代“原典样例”“待人工审核”等内容真实性说明。

### Cards / Containers

关系面、原文纸面、练习纸面使用 paper、line 与 surface 圆角，不用卡片阴影。阅读与练习桌面内边距为（32px），手机分别为（20px 18px）与（22px 18px）。目录按整行链接排列，靠细线分隔；空状态为虚线边框、居中文案和具体下一步。

### Study Entry and Guide

任务入口沿用页面标题、正文与行动链接的现有层级；步骤提示用 rail 平面和 surface 圆角，桌面内边距（26px）、手机（20px）。五条故事线与手册采用来源页的窄阅读栏、区段分隔线和有序步骤，不引入独立视觉主题。产品说明、学生手册、教材溯源规范以清楚命名的下载链接并列呈现；窄屏自然换行。课文与背诵页保留回到原文及查看步骤的就近链接。

### Textbook Trail and Candidate Filters

课内目录与待核试读使用带下划线的文字链接切换，当前入口用加重字重与 `aria-current` 同步表达；待核说明保留独立提示面。教材入口是纸白、细线、无阴影的整块链接，局部圆角（12px）；桌面按至少（240px）的列宽自适应排列，间距（18px），手机单列。目录行继续使用书脊首字图标、课名与可换行的出处说明。

教材名、学制、册次、所据版本说明、篇目与页码和“查看所据教材文档”形成就近证据链；本句教材注释比对单列在 rail 底的说明块中，其定位与候选释义分别呈现。“目录已比对”“本句注释已比对”“学校当前印次已确认”是不同状态，不合并为单一完成徽章。当前仅有部分六上/七上所查电子本的目录及注释比对，不能据此建立全量覆盖的视觉承诺。

字词页使用有可见标签的原生选择框筛选“全部／实词候选／虚词候选／指代用法（待教材定类）／待分类”。选择框使用 paper、ink、line 和 field 圆角，至少（44px）高、最大宽度不超出容器。分类落到具体用法；列表同时显示本库用法数量和具有本句注释比对的数量，候选标签不呈现为教材定论。

### Self-directed Recitation

背诵沿用分段按钮切换“看全文朗读／关键词提示／遮住原文回忆”，按下状态使用 rail 底和 accent 字。句段范围使用原生 fieldset、legend 和 checkbox；每行是完整可点击的文字标签，用细线分隔，复选框为（22px）且使用 accent，整行保留舒适触控范围。桌面范围容器内边距（18px），手机（14px），局部圆角（12px）。至少保留一个句段；自动分句以明确文字说明，不能冒充教材自然段。

原文纸面与宋体字级保持不变，背诵纸面最大宽度（900px）。关键词模式保留少量字符、标点并以“□”遮挡其余内容；完全遮住时显示可读的回忆提示，每句旁提供“看这一句”。遮挡内容不以模糊滤镜或浅色原文泄露，揭示后聚焦当前句段。关键词模式也计入提示，切换到遮住模式保留计数；提示次数配合明确文字展示。

保存自评使用带标签的原生选择框与既有主要按钮。“自评独立完成（未检测）”仅在遮住模式且未使用提示时可选；关键词或单句揭示后禁用该选项，并保留文字说明。空范围或已保存时禁用保存按钮，保存结果以可聚焦状态文字和 toast 明确反馈。历史记录用普通列表列出自评、句段数、提示数和时间，并提供“恢复这次范围”；恢复只还原范围并开始新一轮，历史结果保留。开始新一轮清零提示；原文版本变化时显示核对入口，拒绝自动套用旧范围。所有状态均称自主练习，不呈现录音、自动评分或背诵认证通过的视觉承诺。

### Context Map and Inline Evidence

关系图只表现当前字词的局部关系；选择用法以绿色路径和较粗描边反馈。类型颜色与文字保持一致，图有放大、缩小、复位和文字视图入口。文字视图不是缩略备选：展开用法后就地给出释义、两处优先来自不同作品的证据、返回原文、练习及来源。图模式的右侧证据栏承载相同类型的信息。

### Reading and Focus

原文中的重点词保持原文排版，用 active 底、accent 字及下划线表示可操作；点击回到对应具体用法。纯原文、重点字词、原文与解释、重点词读音四种显示层使用分段按钮。进入引用的原文时，高亮句子获得程序焦点并滚动到上下文；句子焦点有（2px）accent 轮廓和（6px）偏移。切换同一地图用法恢复到相应文字按钮或图节点；局部重绘保留仍可用的操作焦点，答题反馈与提示可承接焦点。

### Practice and Evidence States

选项为全宽、左对齐按钮，带圆形字母标记。选择使用 rail 底与 accent 边；正确使用 active 底；错误选项用 error 边，反馈区用 warn-bg 并给出文字解释。提示和反馈是圆角平面块。练习状态说明是否使用提示；阅读记录、辨析、背诵、默写分别呈现，界面不把浏览升级成学习效果结论。

## Do's and Don'ts

### Do:

- **Do** 延续现有主题变量及其完整深色映射；主题状态不改变颜色的语义。
- **Do** 在文字视图的同一展开项内保留释义、例句、回到原文、练习与来源入口。
- **Do** 保留可见键盘焦点、触控高度和 reduced-motion 支持。
- **Do** 对待审释义、教材归属缺口与尚未评估状态使用明确文字。
- **Do** 在教材目录、候选分类和自主背诵中继续使用原生链接、选择框与复选框，并把来源定位和提示使用状态写在相关操作附近。

### Don't:

- **Don't** 把义项紫色或实例蓝色当作任意装饰色。
- **Don't** 用拖动或缩放关系图作为获得释义与证据的唯一途径。
- **Don't** 将待审样例包装成已审核教材，或把浏览记录呈现为掌握结论。
- **Don't** 为学习内容添加无关位图装饰或复杂星空动效。
- **Don't** 把目录比对呈现为全文或全部释义审核，也不把自主背诵自评呈现为自动检测通过。
