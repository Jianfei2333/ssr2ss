# ssr2ss
Auto update SuanSuanRu subscription and change to ss-local configuration format.

## Usage

```bash
usage: main.py [-h] [--dist DIST] [--url URL]

Auto sync configurations from SSR subscription.

optional arguments:
  -h, --help   show this help message and exit
  --dist DIST  Dist path of configurations.
  --url URL    Subscription url.
```

For example:

```bash
python main.py --dist /home/huihui/Configs --url http://huihui.cn/subscription
```

You can also add this into cron to make it automated.
