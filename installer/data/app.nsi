# ====================== �Զ���� ��Ʒ��Ϣ==============================
!define PRODUCT_NAME           		"Assloud"
!define PRODUCT_PATHNAME 			"assloud"  #��װж�����õ���KEY
!define INSTALL_APPEND_PATH         "Assloud"	  #��װ·��׷�ӵ����� 
!define INSTALL_DEFALT_SETUPPATH    ""       #Ĭ�����ɵİ�װ·��  
!define EXE_NAME               		"application\Assloud.exe"
!define PRODUCT_VERSION        		"1.0.0.0"
!define PRODUCT_PUBLISHER      		"meex.tech"
!define PRODUCT_LEGAL          		"Copyright��c��2018 MeeX"
!define INSTALL_OUTPUT_NAME    		"assloud_setup.exe"

# ====================== �Զ���� ��װ��Ϣ==============================
!define INSTALL_7Z_PATH 	   		"..\_output\app.7z"
!define INSTALL_7Z_NAME 	   		"app.7z"
!define INSTALL_RES_PATH       		"..\_output\skin.zip"
!define INSTALL_LICENCE_FILENAME    "license.txt"
!define INSTALL_ICO 				"logo.ico"
!define INSTALL_OUTPUT_PATH    		"..\_output"


!include "ui_app.nsh"

# ==================== NSIS���� ================================

# ���Vista��win7 ��UAC����Ȩ������.
# RequestExecutionLevel none|user|highest|admin
RequestExecutionLevel highest

#SetCompressor zlib

; ��װ������.
Name "${PRODUCT_NAME}"

# ��װ�����ļ���.

OutFile "${INSTALL_OUTPUT_PATH}\${INSTALL_OUTPUT_NAME}"

# ��װ��ж�س���ͼ��
Icon              "${INSTALL_ICO}"
UninstallIcon     "uninst.ico"
