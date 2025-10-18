# B站歌曲自动收藏工具

这是一个基于Selenium的自动化脚本，用于批量搜索并收藏B站歌曲到指定收藏夹。脚本通过读取歌曲列表JSON文件，自动在B站搜索歌曲视频并添加到收藏夹(已完成)，支持验证码自动识别和登录功能(待完善)。

## 环境要求

- Python 3.x
- Chrome浏览器
- ChromeDriver（需与Chrome版本匹配）

### 依赖库

pip install selenium
pip install requests
pip install pyautogui
pip install keyboard



### 必须配置

CDriverPath = r"D:\system\driver\..."  # ChromeDriver可执行文件路径
sspath = r"D:\learn\python..."  # 验证码截图保存目录
tlusername = ""  # 图灵验证码API用户名
tlpassword = ""  # 图灵验证码API密码
tlId = "08272733"  # 图灵验证码API的ID，使用类型12
username = ""  # B站登录账号（手机号）
password = ""  # B站登录密码
userpath = r"user-data-dir=C:\Users\rubbish\AppData\Local\Google\Chrome\User Data"  # Chrome用户数据目录（保持登录状态）
favoritesName="听"  # 目标收藏夹名称


## 歌曲数据格式

在 `songData.json` 文件中准备歌曲列表，格式如下：

```json
[
  {
    "name": "歌曲名",
    "artist": "艺术家"
  },
  {
    "name": "起风了",
    "artist": "买辣椒也用券"
  }
]
```

## 使用方法

1. **配置环境**：按照上述配置说明修改脚本参数
2. **准备歌曲列表**：创建 `songData.json` 文件
3. **运行脚本**：
   ```bash
   python autoBilibili.py
   ```

### 登录模式

如需使用登录功能，取消主程序中的注释：

```python
bi = boot()
login(bi)  # 取消注释
input("请在浏览器中完成登录后按 Enter 继续...")
searchSong(bi)
```

### 免登录模式（推荐）

找一找方法使得Chrome用户数据目录，使每次登录都保持登录状态，无需每次登录：

```python
bi = boot()
searchSong(bi)  # 直接开始搜索
```

## 工作流程

脚本执行流程如下：启动Chrome浏览器并加载用户配置，从songData.json读取歌曲列表，对每首歌曲在B站搜索"歌名+艺术家"，打开搜索结果中的第一个视频，点击收藏按钮选择指定收藏夹，确认收藏后关闭视频页面返回搜索页，继续处理下一首歌曲，若出错则将当前歌曲信息保存到now search song.json用于排查问题。

## 注意事项

- **ChromeDriver版本**：确保ChromeDriver版本与Chrome浏览器版本匹配
- **网络稳定性**：脚本依赖网络请求，建议在稳定网络环境下运行
- **等待时间**：脚本使用WebDriverWait智能等待，但部分操作仍有固定sleep时间，可根据网速调整
- **验证码API**：图灵验证码识别API需要付费，仅在需要登录时使用
- **反爬虫**：频繁操作可能触发B站反爬虫机制，建议适当增加间隔时间
- **收藏夹名称**：确保 `favoritesName` 变量值与实际收藏夹名称完全一致（区分大小写）


## 文件说明

- `autoBilibili.py` - 主程序脚本
- `songData.json` - 歌曲列表数据（需自行创建）
- `screenshot/` - 验证码截图保存目录（需创建）

## 免责声明

本工具仅供学习和个人使用，请勿用于商业目的或大规模批量操作。使用本工具时请遵守B站用户协议和相关法律法规。
