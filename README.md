# 重庆新闻联播文字稿

抓取重庆新闻联播官网 (cbg.cn) 的新闻内容，生成 Markdown 格式的本地存档。

## 使用方式

### 手动运行

```bash
# 抓取当天新闻
python cqnes.py

# 抓取指定日期新闻
python cqnes.py 20260425
```

日期格式：`YYYYMMDD`

### GitHub Action

推送到 GitHub 后，可通过 Actions 页面手动触发或设置定时自动运行：

- **手动触发**：Actions → 重庆新闻抓取 → Run workflow → 输入日期（留空抓当天）
- **定时任务**：每天北京时间 09:00 自动抓取当天新闻

抓取结果会提交到 `news` 分支。

## 项目结构

```
cqnews/
├── cqnes.py              # 抓取脚本
├── .github/
│   └── workflows/
│       └── news.yml      # GitHub Action 工作流
└── Chongqing_News_History/   # 抓取的新闻存档（生成后）
```

## 环境依赖

```
pip install requests beautifulsoup4
```
