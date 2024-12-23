echo "========================开始更新文档========================"

# 1、注释@HTTPClient\.check_param装饰器
echo "================注释@HTTPClient.check_param装饰器==============="
echo "当前路径:"
pwd
cd ../../..
find . -name "*.py" -exec sed -i '' 's/@HTTPClient\.check_param/# @HTTPClient.check_param/g' {} \;
cd docs/Tools/SphinxSh
echo "===============注释@HTTPClient.check_param装饰器完成=============="

# 2、安装依赖
echo "=========================安装依赖========================="
echo "当前路径:"
pwd
python3 -m pip install -r requirements.txt

echo "安装当前目录的Appbuilder-SDK:"
cd ../../..
python3 -m pip uninstall appbuilder-sdk -y
rm -rf dist
python3 -u setup.py bdist_wheel
python3 -m pip install dist/*.whl
# 更新builde目录
rm -rf build

# 检查appbuilder目录是否已存在
if [ -d "appbuilder" ]; then
    echo "Error: Directory 'appbuilder' already exists."
    exit 1
fi

# 检查python目录是否存在，如果存在则重命名为appbuilder
if [ -d "python" ]; then
    mv python appbuilder
    echo "Directory 'python' has been renamed to 'appbuilder'."
else
    echo "Directory 'python' does not exist."
    find . -name "*.py" -exec sed -i '' 's/# @HTTPClient\.check_param/@HTTPClient.check_param/g' {} \; || { echo "恢复装饰器失败"; exit 1; }
    exit 1
fi
cd docs/Tools/SphinxSh
echo "=========================安装依赖========================="


# 3、删除 build 下的所有文件夹
echo "================删除 doc/build 下的所有文件夹================"
echo "当前路径:"
pwd
echo "删除  build 下的所有文件夹及文件:"
rm -r build/*
echo "删除  build 下的所有文件夹及文件完成"
echo "==============删除 doc/build  下的所有文件夹完成=============="


# 4、删除  doc/source 下除index.rst的所有.rst文件
echo "==========删除doc/source下除index.rst的所有.rst文件=========="
echo "当前路径:"
pwd
echo "删除  source 下除index.rst的所有.rst文件:"
cd source
find . -maxdepth 1 -type f -name '*.rst' ! -name 'index.rst' -exec rm {} \;|| { echo "删除  doc/source 下除index.rst的所有.rst文件失败"; exit 1; }
cd ..
echo "删除  source 下除index.rst的所有.rst文件完成"
echo "=========删除doc/source下除index.rst的所有.rst文件完成========="


# 5、删除原有的 docs/sphinx_md 文件夹及其文件
echo "============删除原有的 docs/sphinx_md 文件夹及其文件============"
echo "当前路径:"
pwd
rm -rf ../../API-Reference/Python/*
echo "===========删除原有的 docs/sphinx_md 文件夹及其文件完成==========="


# 6、在doc目录下下执行命令   sphinx-apidoc -o source ../appbuilder/
echo "=======执行命令 sphinx-apidoc -o source ../appbuilder/======="
echo "当前路径:"
pwd
sphinx-apidoc -o source ../../../appbuilder/
# 删除多余文档目录
rm ./source/appbuilder.tests.*
rm ./source/appbuilder.utils.*
rm ./source/appbuilder.core.assistant.type.rst
cp ./appbuilder.core.rst ./source/appbuilder.core.rst

cp update_rst.py source/
cd source
python3 update_rst.py
rm -rf update_rst.py
cd ..
echo "======执行命令 sphinx-apidoc -o source ../appbuilder/完成======"


# 7、在doc目录下执行命令 make markdown && make html
echo "==============在doc目录下执行命令 make markdown================"
echo "当前路径:"
pwd

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

DOC_DIR="$SCRIPT_DIR"
cd "$DOC_DIR" || { echo "无法切换到 $DOC_DIR 目录"; exit 1; }

echo "当前路径: $(pwd)"

export PATH=/path/to/your/python:$PATH
# 执行 make markdown
make markdown || { echo "make markdown 命令失败"; exit 1; }
# 迁移目录文档
cp PythonAPI.md build/markdown/
cp -r build/markdown/ ../../API-Reference/Python
echo "=============在doc目录下执行命令 make markdown 完成=============="


# 8、恢复装饰器
echo "========================恢复装饰器========================"
cd ../../..
echo "当前路径:"
pwd
find . -name "*.py" -exec sed -i '' 's/# @HTTPClient\.check_param/@HTTPClient.check_param/g' {} \; || { echo "恢复装饰器失败"; exit 1; }
cd docs/Tools/SphinxSh
echo "========================恢复装饰器完成========================"


# 9、清理多余文件
echo "========================清理多余文件========================"
echo "当前路径:"
pwd
cd source
find . -maxdepth 1 -type f -name '*.rst' ! -name 'index.rst' -exec rm {} \;|| { echo "删除  doc/source 下除index.rst的所有.rst文件失败"; exit 1; }
cd ..
echo "删除  doc/source 下除index.rst的所有.rst文件完成"
rm -rf /build/doctrees/*
cd ../../..
if [ -d "appbuilder" ]; then
    mv appbuilder python
    echo "Directory 'appbuilder' has been renamed to 'python'."
else
    echo "Directory 'appbuilder' does not exist."
    exit 1
fi
cd docs/Tools/SphinxSh
echo "======================清理多余文件完成======================"

# 10、拷贝组件README.md文件到docs/BasisModule/Components目录
echo "====拷贝组件README.md文件到docs/BasisModule/Components目录===="
echo "当前路径:"
pwd
cd ../../..
cp -r python/core/components/* docs/BasisModule/Components
cd docs/BasisModule/Components
find . -type f -name "*.py" -exec rm {} +
cd ../../Tools/SphinxSh
# 运行mkdocs更改文件
python3 get_components_md.py

# 更改API目录文件结构
python3 update_lib.py

echo "====拷贝组件README.md文件到docs/BasisModule/Components目录完成===="


echo "========================更新文档完成========================"
