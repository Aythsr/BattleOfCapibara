import os

class GlobalConfig (object):
    """The config of the game"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GlobalConfig, cls).__new__(cls)
        return cls._instance

    def __str__(self) -> str:
        res = f" ==== Game Global Config ==== \n"
        res += f"game_name:     {self.game_name}\n"
        res += f"game_version:  {self.game_version}\n"
        res += f"font_dir:      {self.font_dir}\n"
        res += f"img_dir:       {self.img_dir}\n"
        res += f"db_dir:        {self.db_dir}\n"
        res += f"data_dir:      {self.data_dir}\n"
        res += f"music_dir:     {self.music_dir}\n"
        res += f" === (Game Global Config) === \n"
        return res

    def __init__(self):
        project_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(project_dir)
        self.DEBUG = True
        self.font_dir = os.path.join(project_dir, 'font')
        self.img_dir = os.path.join(project_dir, 'img')
        self.db_dir = os.path.join(project_dir, 'database')
        self.data_dir = os.path.join(project_dir, 'datas')
        self.music_dir = os.path.join(project_dir, 'music')
        self.game_name = 'nome'
        self.game_version = '1.0'
        self.author = 'Wang Haiyang'
        self.site = 'blog.wanghaiyang.site'