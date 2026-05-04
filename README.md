# Guipu（归普）

本仓库为 **Guipu** 工作区：产品文档、About 站点，以及通过 Git submodule 引入的 **Grepu iOS 工程**。

## 仓库结构

| 路径 | 说明 |
|------|------|
| `Doc/` | 需求、架构与原型等文档 |
| `about/` | About 页面静态资源 |
| `com.app.guipu/Grepu/` | **子模块** → [kinwah0706-crypto/Grepu](https://github.com/kinwah0706-crypto/Grepu)（Xcode 工程根目录） |

远程约定：

- **本父仓**：推送到 `Grepu-About`（远程名常为 `grepu-about`）
- **子模块**：独立仓库 [Grepu](https://github.com/kinwah0706-crypto/Grepu)，在本地的路径为 `com.app.guipu/Grepu`

## 克隆（含子模块）

首次克隆请带上子模块，否则 `com.app.guipu/Grepu` 会是空目录：

```bash
git clone --recurse-submodules <本仓库 URL>
```

若已克隆但未拉取子模块：

```bash
git submodule update --init --recursive
```

## 日常开发

- 在子模块目录内开发与提交，与**普通 Git 仓库**相同：

  ```bash
  cd com.app.guipu/Grepu
  git status
  git pull origin main
  # … 修改后 …
  git commit -am "your message"
  git push origin main
  ```

- 父仓会记录子模块的 **提交 SHA**。更新 Grepu 远程后，回到父仓根目录将指针提交上去：

  ```bash
  cd /path/to/Guipu
  cd com.app.guipu/Grepu && git pull origin main && cd ../..
  git add com.app.guipu/Grepu
  git commit -m "chore: bump Grepu submodule"
  git push grepu-about main
  ```

- 可选：把子模块远程 URL 从 HTTPS 换成 SSH（本机已配 GitHub SSH 时）：

  ```bash
  git config submodule.Grepu.url git@github.com:kinwah0706-crypto/Grepu.git
  ```

  该配置默认写在本地 `.git/config`，不会提交；团队仍以 `.gitmodules` 中的 URL 为准。

## CI（GitHub Actions）

本仓库 workflow 使用 `actions/checkout` 的 **`submodules: recursive`**，以便在 CI 中能访问 `com.app.guipu/Grepu` 下的文件。

若子模块仓库为**私有**，需在 checkout 步骤为子模块提供凭据，例如使用 Personal Access Token（PAT）或 `REPO_ACCESS_TOKEN` 等组织级 secret，并参阅 [checkout 文档](https://github.com/actions/checkout) 中的 `token` / ssh 配置。
