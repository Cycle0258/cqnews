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

> 注意：新闻联播一般在当天晚上 6:30-7:00 播出，官网延迟到当晚 22:00 后甚至次日 9:00 才更新。因此定时任务默认抓取前一天的新闻。

### GitHub Action

- **手动触发**：Actions → 重庆新闻抓取 → Run workflow → 输入日期（留空抓前一天）
- **定时任务**：每天北京时间 09:00 自动抓取前一天晚上的新闻联播

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
