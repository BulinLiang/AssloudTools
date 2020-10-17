local config = require('config')
local util = require 'xlua.util'
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

-- 解析歌词
local function parseLRC(_lrc)
    local lines = {}
    -- 按行分割
    lines = split(_lrc, '\n')

    -- 遍历每行，将时间转换为毫秒单位的时间戳
    for k, v in pairs(lines)
    do
        if "" ~= v
        then
            local min = tonumber(string.sub(v, 2, 3))
            local sec = tonumber(string.sub(v, 5, 6))
            local ms = tonumber(string.sub(v, 8, 9))
            local txt = string.sub(v, 11)
            local subtitle = {}
            subtitle["timestamp"] = min * 60 * 1000 + sec * 1000 + ms * 10
            subtitle["txt"] = txt
            table.insert(subtitles,subtitle)
        end
    end
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

local function unbindPlayEvents(_slider)
    local eventTrigger = _slider.gameObject:GetComponent(typeof(unity.EventSystems.EventTrigger))
    eventTrigger.triggers:RemoveAll()
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

local function onAccompanimentClick()
    view.btnAccompaniment.gameObject:SetActive(false)
    view.btnMusic.gameObject:SetActive(true)
    view.audioSourceMusic.gameObject:SetActive(true)
    view.audioSourceMusic.time = view.audioSourceAccompaniment.time
    view.audioSourceAccompaniment.gameObject:SetActive(false)
    view.audioSource = view.audioSourceMusic
    if play
    then
        view.audioSource:Play()
    end
end

local function onMusicClick()
    view.btnAccompaniment.gameObject:SetActive(true)
    view.btnMusic.gameObject:SetActive(false)
    view.audioSourceAccompaniment.gameObject:SetActive(true)
    view.audioSourceAccompaniment.time = view.audioSourceMusic.time
    view.audioSourceMusic.gameObject:SetActive(false)
    view.audioSource = view.audioSourceAccompaniment
    if play
    then
        view.audioSource:Play()
    end
end

local function onVolumeChanged(_value)
    view.audioSourceMusic.volume = _value
    view.audioSourceAccompaniment.volume = _value
end

local function update()
    if nil == view.coverTransform or false == play
    then
        return
    end

    view.coverTransform:Rotate(unity.Vector3.forward, unity.Time.deltaTime * -15)
    view.progress.value = view.audioSource.time / view.audioSource.clip.length
    view.txtTime.text = getLeftTime()

    local subtitle = ""
    for k, v in pairs(subtitles)
    do
        if v["timestamp"] < view.audioSource.time* 1000
        then
            subtitle = v["txt"]
        end
    end
    view.txtSubtitle.text = subtitle
end

local function run()
    logger.Debug("run app ...")
    parseLRC(config.LRC)
    view.bgImage = G_Canvas2D:Find("[ui]"):GetComponent(typeof(unity.UI.Image))
    view.audioSourceAccompaniment = G_Root.transform:Find("accompaniment"):GetComponent(typeof(unity.AudioSource))
    view.audioSourceMusic = G_Root.transform:Find("music"):GetComponent(typeof(unity.AudioSource))
    view.audioSource = view.audioSourceMusic

    view.btnPlay = G_Canvas2D:Find("[ui]/btnPlay"):GetComponent(typeof(unity.UI.Button))
    view.btnPause = G_Canvas2D:Find("[ui]/btnPause"):GetComponent(typeof(unity.UI.Button))
    view.btnPlay.gameObject:SetActive(false)
    view.progress = G_Canvas2D:Find("[ui]/sdProgress"):GetComponent(typeof(unity.UI.Slider))
    view.coverTransform = G_Canvas2D:Find("[ui]/cover")
    view.coverImage = G_Canvas2D:Find("[ui]/cover/img"):GetComponent(typeof(unity.UI.Image))
    view.btnAccompaniment = G_Canvas2D:Find("[ui]/btnAccompaniment"):GetComponent(typeof(unity.UI.Button))
    view.btnMusic = G_Canvas2D:Find("[ui]/btnMusic"):GetComponent(typeof(unity.UI.Button))
    view.btnVolume = G_Canvas2D:Find("[ui]/btnVolume"):GetComponent(typeof(unity.UI.Button))
    view.barVolume = G_Canvas2D:Find("[ui]/bar")
    view.sliderVolume = G_Canvas2D:Find("[ui]/bar/Slider"):GetComponent(typeof(unity.UI.Slider))
    view.txtTime = G_Canvas2D:Find("[ui]/txtTime"):GetComponent(typeof(unity.UI.Text))
    view.txtSubtitle = G_Canvas2D:Find("[ui]/txtSubtitle"):GetComponent(typeof(unity.UI.Text))

    local exists, music = G_AudioClipCaches:TryGetValue('audio#1.ogg')
    if nil ~= music 
    then
        view.audioSourceMusic.clip = music
    else
        logger.Warn("audio#1.ogg is nil")
    end

    local exists, accompaniment = G_AudioClipCaches:TryGetValue('audio#2.ogg')
    if nil ~= accompaniment
    then
        view.audioSourceAccompaniment.clip = accompaniment
    else
        view.audioSourceAccompaniment.clip = music
        logger.Warn("audio#2.ogg is nil")
    end

    local exists, bg = G_SpriteCaches:TryGetValue('bg#1.jpg')
    if nil ~= bg
    then
        view.bgImage.sprite = bg
    else
        logger.Warn("bg#1.jpg is nil")
    end

    local exists, cover = G_SpriteCaches:TryGetValue('cover#1.jpg')
    if nil ~= cover
    then
        view.coverImage.sprite = cover
    else
        logger.Warn("cover#1.jpg is nil")
    end

    view.progress.value = 0
    view.sliderVolume.value = 1
    view.barVolume.gameObject:SetActive(false)
    view.txtSubtitle.text = ""

    view.btnPlay.onClick:AddListener(onPlayClick)
    view.btnPause.onClick:AddListener(onPauseClick)
    view.btnVolume.onClick:AddListener(onVolumeClick)
    view.btnAccompaniment.onClick:AddListener(onAccompanimentClick)
    view.btnMusic.onClick:AddListener(onMusicClick)
    view.sliderVolume.onValueChanged:AddListener(onVolumeChanged)
    
    bindPlayEvents(view.progress)

    play = true
    view.audioSource:Play()
end

local function stop()
    logger.Debug("stop app ...")
    play = false
    unbindPlayEvents(view.progress)
    view.btnPlay.onClick:RemoveAllListeners()
    view.btnPause.onClick:RemoveAllListeners()
    view.btnVolume.onClick:RemoveAllListeners()
    view.sliderVolume.onValueChanged:RemoveAllListeners()
    util.print_func_ref_by_csharp()
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
