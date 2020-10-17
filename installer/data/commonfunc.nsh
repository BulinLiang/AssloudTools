Function AdjustInstallPath
	#�˴��ж����һ�Σ�����Ѿ�������Ҫ׷�ӵ�Ŀ¼��һ�����Ͳ���׷���ˣ������һ��������Ҫ׷�� ͬʱ��¼��д��ע����·��  	
	nsNiuniuSkin::StringHelper "$0" "\" "" "trimright"
	pop $0
	nsNiuniuSkin::StringHelper "$0" "\" "" "getrightbychar"
	pop $1	
		
	${If} "$1" == "${INSTALL_APPEND_PATH}"
		StrCpy $INSTDIR "$0"
	${Else}
		StrCpy $INSTDIR "$0\${INSTALL_APPEND_PATH}"
	${EndIf}

FunctionEnd


#�ж�ѡ���İ�װ·���Ƿ�Ϸ�����Ҫ���Ӳ���Ƿ����[ֻ����HDD]��·���Ƿ�����Ƿ��ַ� ���������$R5�� 
Function IsSetupPathIlleagal

${GetRoot} "$INSTDIR" $R3   ;��ȡ��װ��Ŀ¼  

StrCpy $R0 "$R3\"  
StrCpy $R1 "invalid"  
${GetDrives} "HDD" "HDDDetection"            ;��ȡ��Ҫ��װ�ĸ�Ŀ¼��������

${If} $R1 == "HDD"              ;��Ӳ��       
	 StrCpy $R5 "1"	 
	 ${DriveSpace} "$R3\" "/D=F /S=M" $R0           #��ȡָ���̷���ʣ����ÿռ䣬/D=Fʣ��ռ䣬 /S=M��λ���ֽ�  
	 ${If} $R0 < 100                                #400������װ����Ҫռ�õ�ʵ�ʿռ䣬��λ��MB  
	    StrCpy $R5 "-1"		#��ʾ�ռ䲻�� 
     ${endif}
${Else}  
     #0��ʾ���Ϸ� 
	 StrCpy $R5 "0"
${endif}

FunctionEnd


Function HDDDetection
${If} "$R0" == "$9"
StrCpy $R1 "HDD"
goto funend
${Endif}
Push $0
funend:
FunctionEnd



#��ȡĬ�ϵİ�װ·�� 
Function GenerateSetupAddress
    StrCpy $INSTDIR "$APPDATA"		
FunctionEnd


#====================��ȡĬ�ϰ�װ��Ҫ��Ŀ¼ ����浽$R5�� 
Function GetDefaultSetupRootPath
#��Ĭ�ϵ�D�� 
${GetRoot} "D:\" $R3   ;��ȡ��װ��Ŀ¼  
StrCpy $R0 "$R3\"  
StrCpy $R1 "invalid"  
${GetDrives} "HDD" "HDDDetection"            ;��ȡ��Ҫ��װ�ĸ�Ŀ¼��������
${If} $R1 == "HDD"              ;��Ӳ��  
     #���ռ��Ƿ���
	 StrCpy $R5 "D:\" 2 0
	 ${DriveSpace} "$R3\" "/D=F /S=M" $R0           #��ȡָ���̷���ʣ����ÿռ䣬/D=Fʣ��ռ䣬 /S=M��λ���ֽ�  
	 ${If} $R0 < 300                                #400������װ����Ҫռ�õ�ʵ�ʿռ䣬��λ��MB  
	    StrCpy $R5 "C:"
     ${endif}
${Else}  
     #�˴���Ҫ����C��ΪĬ��·���� 
	 StrCpy $R5 "C:"
${endif}
FunctionEnd


# ����ж����� 
Function CreateUninstall
	#д��ע����Ϣ 
	SetRegView 32
	WriteRegStr HKLM "Software\${PRODUCT_PATHNAME}" "InstPath" "$INSTDIR"
	
	WriteUninstaller "$INSTDIR\uninst.exe"
	
	# ���ж����Ϣ���������
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_PATHNAME}" "DisplayName" "${PRODUCT_NAME}"
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_PATHNAME}" "UninstallString" "$INSTDIR\uninst.exe"
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_PATHNAME}" "DisplayIcon" "$INSTDIR\${EXE_NAME}"
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_PATHNAME}" "Publisher" "${PRODUCT_PUBLISHER}"
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_PATHNAME}" "DisplayVersion" "${PRODUCT_VERSION}"
FunctionEnd


# ========================= ��װ���� ===============================
Function CreateShortcut
  SetShellVarContext current
  # Ӧ����ʼĿ¼
  SetOutPath $INSTDIR
  CreateDirectory "$SMPROGRAMS\${PRODUCT_NAME}"
  CreateShortCut "$SMPROGRAMS\${PRODUCT_NAME}\${PRODUCT_NAME}.lnk" "$INSTDIR\${EXE_NAME}" "" "$INSTDIR\logo.ico"
  CreateShortCut "$SMPROGRAMS\${PRODUCT_NAME}\ж��${PRODUCT_NAME}.lnk" "$INSTDIR\uninst.exe"
  CreateShortCut "$DESKTOP\${PRODUCT_NAME}.lnk" "$INSTDIR\${EXE_NAME}"	
  SetShellVarContext current
FunctionEnd


Function ExtractFunc
	#��װ�ļ���7Zѹ����
	SetOutPath $INSTDIR
	File /oname=logo.ico "${INSTALL_ICO}" 	

	#������  
    File "${INSTALL_7Z_PATH}"
    GetFunctionAddress $R9 ExtractCallback
    nsis7z::ExtractWithCallback "$INSTDIR\${INSTALL_7Z_NAME}" $R9
	Delete "$INSTDIR\${INSTALL_7Z_NAME}"
	
	Sleep 500
FunctionEnd

Function un.DeleteShotcutAndInstallInfo
	SetRegView 32
	DeleteRegKey HKLM "Software\${PRODUCT_PATHNAME}"	
	DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_PATHNAME}"
	
	; ɾ����ݷ�ʽ
	SetShellVarContext current
	Delete "$SMPROGRAMS\${PRODUCT_NAME}\${PRODUCT_NAME}.lnk"
	Delete "$SMPROGRAMS\${PRODUCT_NAME}\ж��${PRODUCT_NAME}.lnk"
	RMDir "$SMPROGRAMS\${PRODUCT_NAME}\"
	Delete "$DESKTOP\${PRODUCT_NAME}.lnk"
	
	#ɾ����������  
    Delete "$SMSTARTUP\${PRODUCT_NAME}.lnk"
	SetShellVarContext current
FunctionEnd
