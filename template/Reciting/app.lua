local config = require('config')
local unity = CS.UnityEngine
local io = CS.System.IO
local logger = CS.API.Assloud.XSA.Logger
local media = CS.API.Assloud.XSA.Media
local opend = false

local view = {}
local play = false
local subtitles = {}

-- 字符切割函数
local function split(str, split_char)      
    local sub_str_tab = {}
    while true do          
        local pos = string.find(str, split_char) 
        if not pos then              
            table.insert(sub_str_tab,str)
            break
        end  
        local sub_str = string.sub(str, 1, pos - 1)              
        table.insert(sub_str_tab,sub_str)
        str = string.sub(str, pos + 1, string.len(str))
    end      
    return sub_str_tab
end

-- 获取剩余时间的字符串
local function getLeftTime()
    local left = view.audioSource.clip.length - view.audioSource.time
    local m = string.format("%02.0f", left/60)
    local s = string.format("%02s", left%60)
    return string.format("%02.0f:%02.0f", left/60, left%60)
end

local function bindPlayEvents(_slider)
    local eventTrigger = _slider.gameObject:AddComponent(typeof(unity.EventSystems.EventTrigger));
    -- 创建开始拖拽事件
    local entryBeginDrag = unity.EventSystems.EventTrigger.Entry();
    entryBeginDrag.eventID = unity.EventSystems.EventTriggerType.BeginDrag;
    entryBeginDrag.callback:AddListener(function(_e)
        view.audioSource:Pause()
        play = false
    end);
    eventTrigger.triggers:Add(entryBeginDrag);

    -- 创建结束拖拽事件
    local entryEndDrag = unity.EventSystems.EventTrigger.Entry();
    entryEndDrag.eventID = unity.EventSystems.EventTriggerType.EndDrag;
    entryEndDrag.callback:AddListener(function(_e)
        view.audioSource:Play()
        play = true
    end);
    eventTrigger.triggers:Add(entryEndDrag);

    -- 创建拖拽时事件
    local entryDrag = unity.EventSystems.EventTrigger.Entry();
    entryDrag.eventID = unity.EventSystems.EventTriggerType.Drag;
    entryDrag.callback:AddListener(function(_e)
        view.audioSource.time = view.audioSource.clip.length * view.progress.value
        view.txtTime.text = getLeftTime()
    end);
    eventTrigger.triggers:Add(entryDrag);

      -- 创建点击事件
    local entryClick = unity.EventSystems.EventTrigger.Entry();
    entryClick.eventID = unity.EventSystems.EventTriggerType.PointerClick;
    entryClick.callback:AddListener(function(_e)
        view.audioSource.time = view.audioSource.clip.length * view.progress.value
        view.txtTime.text = getLeftTime()
    end);
    eventTrigger.triggers:Add(entryClick);
end


local function onPlayClick()
    view.btnPlay.gameObject:SetActive(false)
    view.btnPause.gameObject:SetActive(true)
    play = true
    view.audioSource:Play()
end

local function onPauseClick()
    view.btnPlay.gameObject:SetActive(true)
    view.btnPause.gameObject:SetActive(false)
    play = false
    view.audioSource:Pause()
end

local function onVolumeClick()
    view.barVolume.gameObject:SetActive(not view.barVolume.gameObject.activeSelf)
end

local function onVolumeChanged(_value)
    view.audioSource.volume = _value
end

local function update()
    if false == play or nil == view.audioSource.clip
    then
        return
    end

    view.progress.value = view.audioSource.time / view.audioSource.clip.length
    view.txtTime.text = getLeftTime()
    view.scrollView.verticalNormalizedPosition = 1.0 - view.progress.value
end

local function run()
    logger.Debug("run app ...")
    view.bgImage = G_Canvas2D:Find("[ui]"):GetComponent(typeof(unity.UI.Image))
    view.audioSource = G_Root.transform:Find("music"):GetComponent(typeof(unity.AudioSource))

    view.btnPlay = G_Canvas2D:Find("[ui]/bar/btnPlay"):GetComponent(typeof(unity.UI.Button))
    view.btnPause = G_Canvas2D:Find("[ui]/bar/btnPause"):GetComponent(typeof(unity.UI.Button))
    view.btnPlay.gameObject:SetActive(false)
    view.progress = G_Canvas2D:Find("[ui]/bar/sdProgress"):GetComponent(typeof(unity.UI.Slider))
    view.btnVolume = G_Canvas2D:Find("[ui]/bar/btnVolume"):GetComponent(typeof(unity.UI.Button))
    view.barVolume = G_Canvas2D:Find("[ui]/bar/barVolume")
    view.sliderVolume = G_Canvas2D:Find("[ui]/bar/barVolume/Slider"):GetComponent(typeof(unity.UI.Slider))
    view.txtTime = G_Canvas2D:Find("[ui]/bar/txtTime"):GetComponent(typeof(unity.UI.Text))
    view.txtTitle = G_Canvas2D:Find("[ui]/txtTitle"):GetComponent(typeof(unity.UI.Text))
    view.txtAuthor = G_Canvas2D:Find("[ui]/txtAuthor"):GetComponent(typeof(unity.UI.Text))
    view.txtReciter = G_Canvas2D:Find("[ui]/txtReciter"):GetComponent(typeof(unity.UI.Text))
    view.scrollView = G_Canvas2D:Find("[ui]/Scroll View"):GetComponent(typeof(unity.UI.ScrollRect))
    view.txtContent = G_Canvas2D:Find("[ui]/Scroll View/Viewport/Content/txtContent"):GetComponent(typeof(unity.UI.Text))
    view.blockArea = G_Canvas2D:Find("[ui]/bar/blockArea")

    local exists, music = G_AudioClipCaches:TryGetValue('audio#1.ogg')
    if nil ~= music 
    then
        view.audioSource.clip = music
        view.scrollView.vertical = false
        view.blockArea.gameObject:SetActive(false)
    else
        logger.Warn("audio#1.ogg is nil")
        view.scrollView.vertical = true
        view.blockArea.gameObject:SetActive(true)
    end

    local exists, bg = G_SpriteCaches:TryGetValue('bg#1.jpg')
    if nil ~= bg
    then
        view.bgImage.sprite = bg
    else
        logger.Warn("bg#1.jpg is nil")
    end

    view.progress.value = 0
    view.sliderVolume.value = 1
    view.barVolume.gameObject:SetActive(false)
    view.txtTitle.text = config.Title
    view.txtAuthor.text = config.Author
    view.txtReciter.text = config.Reciter
    view.txtContent.text = config.Content
    
    -- 延迟一帧开启ContentSizeFitter才能改变大小
    local delayFrame = function()
        G_Canvas2D:Find("[ui]/Scroll View/Viewport/Content"):GetComponent(typeof(unity.UI.ContentSizeFitter)).enabled = true
    end
    CS.API.Assloud.XSA.Timer.DelayFrame( delayFrame )

    view.btnPlay.onClick:AddListener(onPlayClick)
    view.btnPause.onClick:AddListener(onPauseClick)
    view.btnVolume.onClick:AddListener(onVolumeClick)
    view.sliderVolume.onValueChanged:AddListener(onVolumeChanged)
    
    bindPlayEvents(view.progress)

    play = true
    view.audioSource:Play()
end

local function stop()
    logger.Debug("stop app ...")
    play = false
    view.audioSource:Stop()
    view.btnPlay.onClick:RemoveAllListeners()
    view.btnPause.onClick:RemoveAllListeners()
    view.btnVolume.onClick:RemoveAllListeners()
    view.sliderVolume.onValueChanged:RemoveAllListeners()
end

local function handleEvent(_event, _data)
	logger.Debug("handle event " .. _event)
end

app = {
    Run = run,
    Update = update,
    Stop = stop,
    HandleEvent = handleEvent,
}
