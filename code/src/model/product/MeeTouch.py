import PyMVCS
from PyQt5.QtCore import QProcess
import json
import os
import re
import copy


class MeeTouchProductStatus(PyMVCS.Status):
    def __init__(self):
        super(MeeTouchProductStatus, self).__init__()
        # self.preloads = [{"type": "AudioClip", "name": "audio", "count": 2, "suffix": ".ogg"}]
        self.xhub_path = ''  # xhub.cfg配置文件路径
        self.assloud_path = ''  # assloud资源文件夹路径
        self.linker_path = ''  # linker.json路径
        self.assloud_list = []  # assloud资源列表

        self.alias_list = []  # 项目中文名
        self.app_list = []  # 项目程序路径
        self.data_list = []  # 项目数据文件夹路径
        self.catalog_list = []  # 项目bundle配置文件路径
        self.label_list = []  # 项目类型
        self.check_flag = [0, 0, 0]  # 核对项目路径[项目程序路径，项目数据文件夹路径，项目bundle配置文件路径]
        self.root_path = ''  # meetouch_data路径

        self.active_bundle = {}  # 选中的bundle{"item":"标识","fodler":"_sign"}

        self.bundle_binary = {}  # {'标识':{'bundle':'_sign','assets':['***','***']}}
        self.linker = {}  # 存放链接文件路径

        self.meessage = {}

        self.run_flag = 1


class MeeTouchProductModel(PyMVCS.Model):
    NAME = "MeeTouchProductModel"

    def _setup(self):
        self.logger.Trace("MeeTouchProductModel.setup")
        self.status = MeeTouchProductStatus()

    def _dismantle(self):
        self.logger.Trace("MeeTouchProductModel.dismantle")

    def getProjectsList(self):
        # 读取xhub.cfg文件
        home_path = os.path.expanduser('~')
        self.status.xhub_path = os.path.join(home_path, r'Documents\MeeX\xhub.cfg')
        if not os.path.exists(self.status.xhub_path):
            return
        else:
            try:
                with open(self.status.xhub_path, 'r', encoding='utf8') as f:
                    xhub_dict = json.loads(f.read())
                # assloud路径
                self.status.assloud_path = xhub_dict['assloud']['path']
                assloud_path = self.status.assloud_path + '\\bundle'
                for project_dict in xhub_dict['projects']:
                    self.status.alias_list.append(project_dict['alias'])
                    self.status.app_list.append(project_dict['app'])
                    self.status.data_list.append(project_dict['data'])
                    self.status.catalog_list.append(project_dict['catalog'])
                    self.status.label_list.append(project_dict['label'])

                # 提取assloud列表到内存
                if not os.path.exists(assloud_path):
                    return
                else:
                    bundle_list = os.listdir(assloud_path)
                    for bundle in bundle_list:
                        asset_list = os.listdir(os.path.join(assloud_path, bundle))
                        for asset in asset_list:
                            asset_path = os.path.join(assloud_path, bundle, asset)
                            if re.search("^_[a-z]+", asset) == None and os.path.isdir(asset_path):
                                self.status.assloud_list.append(os.path.join(bundle, asset))
                self.Broadcast("/product/meetouch/projects/update", None)
            except ValueError as ve:
                title = 'getProjectsList Information'
                info = 'xhub.cfg文件格式有错：' + str(ve)
                self.status.message = {"title": title, "info": info}
                self.Broadcast("/product/meetouch/message", None)

    # 获取bundle前，判断路径是否正确
    def getBundleList(self, _index):
        app_path = self.status.app_list[_index]
        data_path = self.status.data_list[_index]
        catalog_path = os.path.join(data_path, self.status.catalog_list[_index])
        # MeeTouch运行程序路径
        if os.path.exists(app_path):
            self.status.check_flag[0] = 1
        else:
            self.status.check_flag[0] = 0
        # 数据路径
        if os.path.exists(data_path):
            self.status.root_path = data_path
            self.status.check_flag[1] = 1
        else:
            self.status.check_flag[1] = 0
        # 从catalog.json目录配置文件提取目录名和目录下的资源
        if os.path.exists(catalog_path):
            self.status.check_flag[2] = 1
            try:
                with open(catalog_path, 'r', encoding='utf8') as f:
                    catalog_list = json.loads(f.read())
                for catalog in catalog_list:
                    if (catalog["groups"] == ["catalog"] or catalog["groups"] == []) and catalog["bundle"] != '':
                        # {'标识':'_sign'} 使用实时读取
                        bundle_key = catalog["alias"]["zh_CN"].split('/')[0]
                        bundle = catalog["bundle"]
                        bundle_path = os.path.join(data_path, 'bundle', bundle)
                        asset_link = []
                        asset_dir = []
                        if os.path.exists(bundle_path) == None:
                            break
                        else:
                            asset_list = os.listdir(bundle_path)
                            # 获取资源文件列表
                            for asset in asset_list:
                                if re.search("_[a-z]+", asset) == None:
                                    # 判断是否为链接文件夹
                                    asset_path = os.path.join(bundle_path, asset)
                                    if os.path.islink(asset_path):
                                        bundle_asset = os.path.realpath(asset_path).rsplit('\\', 2)
                                        asset_link.append(bundle_asset[1] + '\\' + bundle_asset[2])
                                        asset_link.sort(reverse=False)
                                    else:
                                        asset_dir.append(asset)
                                        asset_dir.sort(reverse=False)
                            # 将bundle对应的文件夹名和asset_list存入内存
                            self.status.bundle_binary[bundle_key] = {"bundle": bundle,
                                                                     "asset_dir": asset_dir,
                                                                     "assets": asset_link}
            except ValueError as ve:
                title = 'getBundleList Information'
                info = 'catalog.json文件格式有错：' + str(ve)
                self.status.message = {"title": title, "info": info}
                self.Broadcast("/product/meetouch/message", None)
            # 读取linker.json文件
            # 使用深拷贝，不然要改变bundle_binary的值
            self.status.linker = copy.deepcopy(self.status.bundle_binary)
            try:
                self.status.linker_path = os.path.join(data_path, 'linker.json')
                # 有链接文件时，以链接文件中的链接为基础更新assloud列表复选框
                if os.path.exists(self.status.linker_path):
                    with open(self.status.linker_path, 'r', encoding='GB2312') as f:
                        self.status.linker = json.loads(f.read())

                # 没有链接文件时，以读取出来的资源列表且删除了非链接文件为基础
                else:
                    for k in self.status.linker.keys():
                        self.status.linker[k].pop('asset_dir')
            except ValueError as ve:
                # 当文件为空，或者文件格式有错误时
                for k in self.status.linker.keys():
                    self.status.linker[k].pop('asset_dir')
                    self.status.linker[k]['assets'] = []
                title = 'getBundleList Information'
                info = "linker.json链接文件格式问题，可以删除该json文件再重启程序。\n" + str(ve)
                self.status.message = {"title": title, "info": info}
                self.Broadcast("/product/meetouch/message", None)
        else:
            self.status.bundle_binary = {}
            self.status.check_flag[2] = 0
        # print(self.status.linker)
        # print(self.status.bundle_binary)
        self.Broadcast("/product/meetouch/check_path", None)
        self.Broadcast("/product/meetouch/bundle/update", None)

    def getAssetList(self, _item, _uuid):
        item = _item.data(_uuid)
        fodler = self.status.bundle_binary[_item.data(_uuid)]['bundle']
        self.status.active_bundle = {"item": item, "fodler": fodler}
        self.Broadcast("/product/meetouch/asset/update", None)

    def getAssloudList(self, _item, _uuid):
        item = _item.data(_uuid)
        # 取self.status.linker[item] 和 self.status.bundle_binary[item]["assets"]并集
        try:
            link1 = self.status.linker[item]["assets"]
            link2 = self.status.bundle_binary[item]["assets"]
            self.status.chose = list(set(link1).union(set(link2)))
        except Exception as e:
            title = 'getAssloudList Information'
            info = "linker.json链接文件格式问题，可以删除该json文件再重启程序。\n" + str(e)
            self.status.message = {"title": title, "info": info}
            self.Broadcast("/product/meetouch/message", None)
        self.Broadcast("/product/meetouch/assloud_link/update", None)

    def editCatalog(self):
        if os.path.exists(self.status.xhub_path):
            os.system(self.status.xhub_path)
        else:
            return

    def createLink(self, _links, _uuid):
        # 1、取出选择的资源链接
        choose_links = []  # 存放选择了的链接列表
        count = _links.count()
        # assloud列表
        assloud_list = [_links.itemWidget(_links.item(i)) for i in range(count)]
        for assloud in assloud_list:
            if assloud.isChecked():
                choose_links.append(assloud.text())

        # 2、写入linker.json文件
        item = self.status.active_bundle["item"]
        self.status.linker[item]["assets"] = choose_links
        # 同时更新asset列表
        self.status.bundle_binary[item]["assets"] = choose_links
        with open(self.status.linker_path, 'w') as f:
            f.write(json.dumps(self.status.linker, ensure_ascii=False, indent=3))

        # 3、重新完成本地链接（包括先删除，然后重新创建链接）
        asset_path = os.path.join(self.status.root_path, "bundle", self.status.active_bundle["fodler"])
        asset_list = os.listdir(asset_path)
        for asset in asset_list:
            try:
                os.remove(os.path.join(asset_path, asset))
            except Exception as e:
                pass
        zip_src = []
        zip_dst = []
        for choose in choose_links:
            # 资源路径
            src_path = os.path.join(self.status.assloud_path, 'bundle', choose)
            # 目标路径
            dst_path = os.path.join(self.status.root_path, "bundle", self.status.active_bundle["fodler"],
                                    choose.split('\\')[1])
            zip_src.append(src_path)
            zip_dst.append(dst_path)
            try:
                os.symlink(src_path, dst_path)
            except Exception as e:
                print(e)
                pass
        # self.getAdmin(zip(zip_dst, zip_src))
        self.Broadcast("/product/meetouch/asset/update", None)

    def clearLink(self, _link):
        # 1、删除选择了的列表
        item = self.status.active_bundle["item"]
        self.status.linker[item]["assets"] = []
        # 同时更新asset列表
        self.status.bundle_binary[item]["assets"] = []
        # 2、删除本地链接文件的列表
        asset_path = os.path.join(self.status.root_path, "bundle", self.status.active_bundle["fodler"])
        asset_list = os.listdir(asset_path)
        for asset in asset_list:
            try:
                os.remove(os.path.join(asset_path, asset))
            except Exception as e:
                pass
        # 3、更新linker.json
        with open(self.status.linker_path, 'w') as f:
            f.write(json.dumps(self.status.linker, ensure_ascii=False, indent=3))

        self.Broadcast("/product/meetouch/asset/update", None)

    def exportToFolder(self, _index, _path):
        # 1、获取exe程序路径
        # 读取exe文件的上一级
        program_list = []
        program_path = os.path.dirname(self.status.app_list[_index])
        program_list.append(re.sub('/', '\\\\', program_path))

        # 2、获取data数据路径，本地资源会同时复制，所以不用管
        data_list = []
        data_path = self.status.data_list[_index]
        if os.path.islink(data_path):
            data_path = os.path.realpath(data_path)
            data_list.append(re.sub('/', '\\\\', data_path))
        else:
            data_list.append(re.sub('/', '\\\\', data_path))

        # 3、获取assloud选择了的资源路径
        assloud_path = os.path.join(self.status.assloud_path, 'bundle')
        src_list = self.status.bundle_binary
        asset_list = []
        for item in src_list:
            assets = src_list[item]['assets']
            for asset in assets:
                asset_path = os.path.join(assloud_path, asset)
                asset_list.append(re.sub('/', '\\\\', asset_path))

        # print(program_list, data_list, asset_list, sep='\n')
        # 4、写入copy_source.bat文件
        self.copySource(program_list, data_list, asset_list, _path)
        # 使用QProcess().start()阻塞函数
        copy_source = QProcess()
        copy_source.start('./copySource.bat')
        if copy_source.waitForFinished():
            try:
                os.remove('./copySource.bat')
            except Exception as e:
                print(str(e))

    def RUN(self, _index):
        try:
            app_path = self.status.app_list[_index]
            run_touch = QProcess()
            # startDetached 非阻塞函数，start阻塞函数
            run_touch.startDetached(app_path)
        except Exception as e:
            title = 'RUN-Process Information'
            info = str(e)
            self.status.message = {"title": title, "info": info}
            self.Broadcast("/product/meetouch/message", None)

        # 创建符号链接到C:\Users\Administrator\AppData\LocalLow\MeeX\MeeTouch
        # dir.json存放需要链接到上面路径的文件夹名，list型
        dir_config_path = os.path.join(self.status.root_path, 'dir.json')
        try:
            with open(dir_config_path, 'r', encoding='utf-8') as f:
                dir_list = json.loads(f.read())
            for dir_name in dir_list:
                if dir_name == '_native':
                    dir_path = os.path.join(self.status.assloud_path, dir_name)
                else:
                    dir_path = os.path.join(self.status.root_path, dir_name)
                home_path = os.path.expanduser('~')
                touch_path = os.path.join(home_path, r"AppData\LocalLow\MeeX\MeeTouch", dir_name)
                try:
                    os.remove(touch_path)
                except:
                    pass
                try:
                    os.symlink(dir_path, touch_path)
                except Exception as e:
                    title = 'RUN-Createlink Information'
                    info = str(e)
                    self.status.message = {"title": title, "info": info}
                    self.Broadcast("/product/meetouch/message", None)
                    return
        except Exception as e:
            title = 'RUN-Nodir.json Information'
            info = str(e)
            self.status.message = {"title": title, "info": info}
            self.Broadcast("/product/meetouch/message", None)

    def copySource(self, program_list, data_list, asset_list, dst_path):
        dst_path = re.sub('/', '\\\\', dst_path.rstrip('/'))
        del_meex = fr'if not exist {dst_path}\MeeX mkdir {dst_path}\MeeX'
        copy_program = ''
        copy_data = ''
        copy_asset = ''
        for program in program_list:
            src = program
            dst = dst_path + program.split(":")[1]
            # 对路径加引号是为了处理遇到空格目录的问题
            copy_program += f'xcopy /E "{src}" "{dst}"\n'
        for data in data_list:
            src = data
            dst = dst_path + data.split(":")[1]
            copy_data += f'xcopy /E "{src}" "{dst}"\n'
        for asset in asset_list:
            src = asset
            dst = dst_path + '\\Assloud\\MeeX\\' + asset.split("\\Assloud\\")[1]
            copy_asset += f'xcopy /E "{src}" "{dst}"\n'
        bat = fr'''@echo off  
  
:: BatchGotAdmin  获取管理员权限
:-------------------------------------  
REM  --> Check for permissions  
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"  
  
REM --> If error flag set, we do not have admin.  
if '%errorlevel%' NEQ '0' (  
:echo Requesting administrative privileges...  
    goto UACPrompt  
) else ( goto gotAdmin )  
  
:UACPrompt  
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"  
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"  
  
    "%temp%\getadmin.vbs"  
    exit /B  
  
:gotAdmin  
    if exist "%temp%\getadmin.vbs" ( del "%temp%\getadmin.vbs" )  
    pushd "%CD%"  
    CD /D "%~dp0"  
:--------------------------------------
{del_meex}
echo ---------------COPY PROGRAM---------------
{copy_program}
echo ---------------COPY DATA---------------
{copy_data}
echo ---------------COPY ASSET---------------
{copy_asset}

echo -------------------------------------
echo !                                   
echo !   安装完成，可以关闭此窗口          
echo !                                   
echo -------------------------------------
pause
'''
        with open('copySource.bat', 'w') as bat_f:
            bat_f.write(bat)