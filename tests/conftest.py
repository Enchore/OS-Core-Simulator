"""按文件路径加载被测模块。

本项目的模块以目录分类但没有 __init__.py，直接用 import xxx 会依赖
sys.path 上的目录顺序，这里统一用文件路径加载，避免歧义。
"""
import importlib.util
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(module_name, relative_path):
    spec = importlib.util.spec_from_file_location(
        module_name, os.path.join(ROOT, relative_path)
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
