# GitHub 上传与提交规范

> 依据：《软件工程课程设计项目实践要求（版本 1）》第四节「工程实践要求——GitHub 全流程留痕」。
> 一句话结论：**在这个课程里，"上传文件"不等于"把文件拖进网页"，而等于"开 Issue → 拉分支 → 提交 → 发 PR → 他人评审 → 合并"**。

---

## 0. 先理解那条铁律

课程原文：**"不在仓库里发生的事，视为没有发生。"**

这句话决定了一切。教师会用 AI 审计工具读你仓库的 **commit 分布、PR 记录、Issue 状态、CI 运行历史、Milestone 进度**，然后生成证据档案。所以：

- 文件"传上去了"但**没走 PR** → 评审率不达标，丢分；
- 文件在 PR 评论里贴了图，但**没进仓库** → 不算交付物；
- 最后一次提交塞进 200 个文件 → 提交分布异常，直接判"最后一晚打包上传"。

---

## 1. 课程对"上传"的具体条款

| 环节 | 原文要求 | 对上传动作的含义 |
|---|---|---|
| 立项 | 建立仓库；README 载章程与选型论证 | 章程不是单独发群里，是**提交到 README 或 docs/** |
| 需求与变更 | 需求与变更一律建 Issue | 每份需求文档、每次改需求，**先有 Issue 再上传文件** |
| 建模与文档 | **模型文件入库，每张图一个 PR**；文档目录随仓库版本化 | 一张图 = 一个分支 = 一个 PR，不许一个 PR 塞十张图 |
| 编码 | **main 分支禁止直推，一律走 Pull Request** | 不能 `git push origin main` |
| 评审 | 每个 PR 至少 1 人评审后方可合并 | PR 必须有 approve 记录，自己 merge 自己不算 |
| 测试与迭代 | push 自动跑单测，**红灯禁止合并** | 合并前 CI 必须绿 |
| 部署 | 每个增量打 Release（v0.1/v0.2/v0.3） | 交付物打包挂 Release 附件 |
| 平时成绩 | **禁止"最后一晚打包上传"式的提交分布** | 小步、分散、按人、按天 |
| 附则 | 每周至少推送一次（镜像平台） | 即使没进展也要有提交，否则算停滞 |

---

## 2. 标准上传流程（命令级）

### 2.1 第一次准备（只做一次）

```bash
# 0) 登录 gh（当前机器尚未登录）
gh auth login

# 1) 确认身份（提交记录按人统计贡献度，邮箱必须是你自己的）
git config user.name  "你的真名或学号"
git config user.email "你的学校邮箱"

# 2) 拉最新
git switch main && git pull --ff-only
```

### 2.2 每次上传都走这七步

```bash
# 1) 先建 Issue（网页或命令行），拿到编号，例如 #12
gh issue create --title "UC-03 共享日程冲突检测 用例图" \
  --body "对应需求 UC-03；产出：docs/03-models/uc/uc03.puml + 导出 PNG" \
  --label "modeling" --milestone "v0.2"

# 2) 从最新 main 拉分支（命名见 §4）
git switch main && git pull --ff-only
git switch -c docs/uc03-usecase-diagram

# 3) 放文件（目录规范见 §3），检查将要提交什么
git status
git diff --stat

# 4) 提交：一个逻辑单元一次提交，信息里带 Issue 号
git add docs/03-models/uc/uc03.puml docs/03-models/uc/uc03.png
git commit -m "docs(model): add UC-03 use case diagram (#12)"

# 5) 推送分支（不是 main）
git push -u origin docs/uc03-usecase-diagram

# 6) 发 PR，关联 Issue
gh pr create --fill --base main \
  --body "Closes #12

## 变更
- 新增 UC-03 用例图（PlantUML 源 + PNG 导出）

## 自查
- [ ] 图与 SRS 2.3 节一致
- [ ] 已导出 PNG 并入库
- [ ] 无密钥/隐私数据"

# 7) 等 CI 绿 + 至少 1 人 approve，然后 squash 合并
gh pr merge --squash --delete-branch
```

> 用 `Closes #12` 的好处：合并瞬间 Issue 自动关闭，"Issue 闭环率"这项指标自动达标。

### 2.3 分支保护怎么开（现在你的仓库还没开）

网页路径：**Settings → Rules → Rulesets → New branch ruleset**（推荐，免费版私有仓库也可用）
或 **Settings → Branches → Add branch protection rule**（classic，私有仓库需 GitHub Pro）。

要勾的项：

- ✅ Require a pull request before merging（**至少 1 个 approving review**）
- ✅ Require status checks to pass（选上 CI 的 job 名，如 `test`）
- ✅ Require branches to be up to date before merging
- ✅ Block force pushes / 禁止删除
- ✅ Do not allow bypassing（连管理员也拦，否则评分工具会看到直推记录）

命令行等价（classic API，需已 `gh auth login`）：

```bash
gh api --method PUT repos/{owner}/{repo}/branches/main/protection --input - <<'JSON'
{
  "required_status_checks": { "strict": true, "contexts": ["test"] },
  "enforce_admins": true,
  "required_pull_request_reviews": { "required_approving_review_count": 1 },
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false
}
JSON
```

---

## 3. 目录规范（"文档目录随仓库版本化"）

```
workspace/
├── README.md                     # 章程 + 选型论证 + 快速开始
├── CONTRIBUTING.md               # 本规范（团队公约）
├── docs/
│   ├── 01-charter/               # 项目章程、过程模型选型论证
│   ├── 02-requirements/          # SRS、访谈纪要、变更记录
│   ├── 03-models/                # 用例图 / 类图 / 状态图（.puml + 导出图）
│   ├── 04-design/                # 概要设计、详细设计、评审单
│   ├── 05-test/                  # 测试计划、用例、报告
│   ├── 06-iteration/             # 迭代计划、回顾报告
│   ├── 07-ai/                    # AI 使用报告、关卡记录
│   └── 08-deploy/                # 部署说明、演示脚本
├── src/
├── tests/
└── .github/
    ├── workflows/ci.yml
    ├── PULL_REQUEST_TEMPLATE.md
    └── ISSUE_TEMPLATE/
```

**为什么按编号分目录**：10 项交付物与 8 个知识单元一一对应，教师和审计工具一眼能对上；Milestone 也能按目录归属统计。

### 图的特殊要求

课程原文是"**模型文件入库**，每张图一个 PR"。所以：

- ✅ 提交 **PlantUML / Mermaid 源码**（`.puml` / `.mmd`）+ 导出的 `.png`/`.svg`
- ❌ 只交 PNG（不可 diff、不可评审、改一次重画一次）
- ❌ 把图拖进 Issue/PR 评论（图存在 GitHub 的 CDN 上，**不在仓库里，不算入库**）
- ❌ 用 draw.io 的二进制 `.drawio` 单独入库（可入库，但必须同时给导出图，评审者不会点开看）

---

## 4. 命名与提交信息规范

**分支名**：`<类型>/<简短描述>`

| 类型 | 用途 | 例 |
|---|---|---|
| `feat/` | 新功能 | `feat/uc03-conflict-detect` |
| `docs/` | 文档、模型、图 | `docs/uc03-usecase-diagram` |
| `fix/` | 缺陷修复 | `fix/share-acl-403` |
| `chore/` | 配置、CI、脚手架 | `chore/ci-pytest` |
| `test/` | 测试补充 | `test/uc03-boundary` |

**提交信息**：`<类型>(<范围>): <做了什么> (#Issue)`

```
docs(model): add UC-03 use case diagram (#12)
feat(auth): add OAuth2 callback handler (#21)
fix(acl): deny cross-workspace read on shared files (#34)
test(schedule): add boundary cases for recurrence rule (#40)
```

禁止：`update`、`修改`、`111`、`最终版`、`最终版2`。

**PR 标题**：与提交信息同格式；**PR 描述**必须包含 `Closes #N` 与自查清单。

---

## 5. 大文件与敏感文件（最容易踩的两个坑）

### 5.1 大文件

| 文件 | 建议 |
|---|---|
| 文档 PDF、截图 | 直接入库（几 MB 没问题） |
| 原型 `.fig` / `.sketch` / 大图 | 超过 10 MB 用 **Git LFS** |
| 演示视频、录屏 | **不入库**。挂到 Release 附件，或网盘链接写进 `docs/08-deploy/` |
| 依赖、`node_modules`、虚拟环境 | `.gitignore` 排除 |

当前机器**未安装 git-lfs**，需要时：

```bash
brew install git-lfs && git lfs install
git lfs track "*.psd" "*.sketch" "docs/**/*.mp4"
git add .gitattributes
```

**为什么视频不能进 git**：一旦提交，它永久留在历史里，仓库体积暴涨，克隆变慢，审计工具也会标记"异常大文件提交"。

### 5.2 密钥与隐私（课程按**安全事故**处理）

必须建 `.gitignore`（你现在仓库还没有）：

```gitignore
.env
.env.*
*.pem
*.key
node_modules/
.venv/
__pycache__/
dist/
build/
.DS_Store
*.mp4
```

**已经误提交了怎么办**：`git rm` 只是删掉工作区文件，历史里还在，任何人都能 `git log -p` 翻出来。必须重写历史：

```bash
# 先轮换那把密钥（最重要，历史清了密钥也已泄露）
git filter-repo --path .env --invert-paths   # 需先 brew install git-filter-repo
git push --force-with-lease --all
```

**更稳的做法**：从第一天就用 `.env.example` 提交占位符，真实值只在本机。

---

## 6. 提交前自检清单

每个 PR 合并前过一遍：

- [ ] 分支不是 `main`，PR 已关联 Issue（`Closes #N`）
- [ ] CI 全绿（单元测试 + lint）
- [ ] 至少 1 名队友已 approve（**不是自己**）
- [ ] `git diff` 里没有 `.env`、密钥、真实用户手机号/身份证
- [ ] 图有源文件 + 导出图，且与 SRS 条目编号一致
- [ ] 提交信息带 Issue 号，无 `最终版` 之类
- [ ] 本次提交是**一个逻辑单元**（能一句话说清）
- [ ] 若关闭了需求变更，变更记录文档已同步更新

---

## 7. 五个高频扣分点（按严重度排序）

1. **直推 main**。分支保护没开或开了但允许 admin bypass，审计工具一眼看到 → "PR 评审率"直接不合格。
2. **最后一天集中提交**。哪怕代码是你写的，提交分布异常就判"打包上传"，贡献度互评也救不回来。
3. **图只贴在 PR 评论里**。看着很完整，仓库里 `docs/03-models/` 是空的 → 建模质量项无证据。
4. **`.env` 进了历史**。按安全事故处理，可能影响整组成绩。
5. **一个 PR 塞进全部交付物**。评审无法进行，`每张图一个 PR` 的要求直接违反。

---

## 8. 关于平台预案

附则第 1 条：GitHub 访问不稳定时可用校内 GitLab / Gitee 镜像，但**每周至少推送一次**。

```bash
git remote add gitee git@gitee.com:<你的账号>/workspace.git
git push gitee main --tags          # 每周一次
```

镜像只做备份，**主仓库仍在 GitHub**，因为评分工具优先读 GitHub 的 PR/Issue/CI 数据。

---

## 附：如果你问的是"产品里的文件上传功能怎么做"

那是另一个问题（v0.1 的核心功能 + 外部集成点候选）。要点先给结论：

- **内容存对象存储，元数据存数据库**（S3 / 阿里云 OSS / MinIO），不要把文件塞进 MySQL BLOB；
- **预签名 URL 直传**，浏览器直连对象存储，后端只签发凭证——避免大文件压垮应用服务器；
- **权限校验放在签发 URL 的那一刻**（结合 v0.2 的资源级 ACL），而不是下载时再查；
- **分片上传 + 断点续传**处理大文件，**类型白名单 + 大小上限**做第一道防线；
- 元数据表存：`file_id / owner_id / workspace_id / folder_id / size / mime / sha256 / storage_key / created_at`；
- 回收站与配额、上传审计日志（谁在何时上传了什么到哪个工作区）。

这部分我可以按详细设计规约的格式展开（含接口契约、时序图、异常分支），需要的话说一声。
