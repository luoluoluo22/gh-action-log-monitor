# GitHub Actions 自动化日志看板

这是一个基于 GitHub Actions 和 GitHub Pages 的简单自动化任务模板。
它会在后台定时运行你的 Python 脚本，并将运行日志自动更新到一个静态网页上，方便随时查看。

## 目录结构

*   `.github/workflows/main.yml`: GitHub Actions 配置文件，定义了定时任务和自动提交逻辑。
*   `frontend/index.html`: 前端日志展示页面。
*   `frontend/data.json`: 存储历史日志的 JSON 数据库（由脚本自动更新，初始含有一条演示数据）。
*   `task_script.py`: **你的业务逻辑脚本**（在这个文件里写爬虫、数据处理等代码）。
*   `update_history.py`: 助手脚本，用于将运行日志追加到 JSON 文件中。

## 如何使用

1.  **创建仓库**：在 GitHub 上创建一个新的公开仓库（Public）。
2.  **推送代码**：将本文件夹内的所有文件上传/推送到该仓库。
3.  **启用 GitHub Pages**：
    *   进入仓库的 **Settings** (设置) -> **Pages** (页面)。
    *   在 **Build and deployment** (构建与部署) 下：
        *   **Source**: 选择 `Deploy from a branch`。
        *   **Branch**: 选择 `main` (或 master) 分支，并选择 `/frontend` 文件夹 (注意不是 /(root))。
        *   点击 **Save**。
4.  **启用写权限**：
    *   进入仓库的 **Settings** -> **Actions** -> **General**。
    *   滚动到底部的 **Workflow permissions**。
    *   勾选 **Read and write permissions** (这一步很重要，否则 Actions 无法更新 `data.json`)。
    *   点击 **Save**。

## 查看结果

*   **手动触发**：你可以去仓库的 **Actions** 标签页，点击左侧的 "Daily Task & Log Update"，然后点击右侧的 **Run workflow** 按钮来立即测试一次。
*   **查看看板**：等待 Action 运行完成后（通常几十秒），访问你的 GitHub Pages 链接（在 Settings -> Pages 里可以看到，通常是 `https://你的用户名.github.io/仓库名/`）。
