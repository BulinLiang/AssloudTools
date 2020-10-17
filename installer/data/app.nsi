# ====================== 自定义宏 产品信息==============================
!define PRODUCT_NAME           		"Assloud"
!define PRODUCT_PATHNAME 			"assloud"  #安装卸载项用到的KEY
!define INSTALL_APPEND_PATH         "Assloud"	  #安装路径追加的名称 
!define INSTALL_DEFALT_SETUPPATH    ""       #默认生成的安装路径  
!define EXE_NAME               		"application\Assloud.exe"
!define PRODUCT_VERSION        		"1.0.0.0"
!define PRODUCT_PUBLISHER      		"meex.tech"
!define PRODUCT_LEGAL          		"Copyright（c）2018 MeeX"
!define INSTALL_OUTPUT_NAME    		"assloud_setup.exe"

# ====================== 自定义宏 安装信息==============================
!define INSTALL_7Z_PATH 	   		"..\_output\app.7z"
!define INSTALL_7Z_NAME 	   		"app.7z"
!define INSTALL_RES_PATH       		"..\_output\skin.zip"
!define INSTALL_LICENCE_FILENAME    "license.txt"
!define INSTALL_ICO 				"logo.ico"
!define INSTALL_OUTPUT_PATH    		"..\_output"


!include "ui_app.nsh"

# ==================== NSIS属性 ================================

# 针对Vista和win7 的UAC进行权限请求.
# RequestExecutionLevel none|user|highest|admin
RequestExecutionLevel highest

#SetCompressor zlib

; 安装包名字.
Name "${PRODUCT_NAME}"

# 安装程序文件名.

OutFile "${INSTALL_OUTPUT_PATH}\${INSTALL_OUTPUT_NAME}"

# 安装和卸载程序图标
Icon              "${INSTALL_ICO}"
UninstallIcon     "uninst.ico"
