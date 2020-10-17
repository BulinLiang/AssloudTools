local config = require('config')
local unity = CS.UnityEngine
local io = CS.System.IO
local logger = CS.API.Assloud.XSA.Logger
local cache = CS.API.Assloud.XSA.Cache
local timer = CS.API.Assloud.XSA.Timer
local easyTouch = CS.HedgehogTeam.EasyTouch
local opend = false
local ui = {}
local currentIndex = 0

local function onAssetLoadFinish(_assetBundle)
    logger.Info(_assetBundle)
end

local function onSwipe(_gesture)
    -- print(_gesture.swipeVector)
    ui.tip:SetActive(false)
    
    if _gesture.swipeVector.x < 0
    then
        currentIndex = currentIndex + 1
        if currentIndex > config.Count
        then 
            currentIndex = 0
        end
    elseif _gesture.swipeVector.x > 0
    then 
        currentIndex = currentIndex - 1
        if currentIndex < 0
        then 
            currentIndex = config.Count
        end
    end

    local nextSprite = 'img#'..currentIndex..'.jpg'
    local exists, sprite = G_SpriteCaches:TryGetValue(nextSprite)
    if nil == sprite
    then
        return
    end
    ui.imgFrame.sprite = sprite
end


local function onAnimFinish()
    -- 挂载触控脚本
    local swipe = ui.imgFrame.gameObject:AddComponent(typeof(easyTouch.QuickSwipe))
    swipe.swipeDirection = easyTouch.QuickSwipe.SwipeDirection.Horizontal
    swipe.onSwipeAction = easyTouch.QuickSwipe.OnSwipeAction()
    swipe.onSwipeAction:AddListener(onSwipe)
    -- 显示提示
    ui.tip:SetActive(true)
    -- 隐藏封面
    ui.cover:SetActive(false)
end

local function onEnterClick()
    local animator = G_Canvas2D:Find("[ui]"):GetComponent(typeof(unity.Animator))
    animator:SetTrigger('out')
    -- 延迟1秒等待动画
    timer.DelaySeconds(1, onAnimFinish)
end

local function onCacheFinish()
    -- 隐藏进度条
    ui.slider.gameObject:SetActive(false)
    -- 显示进入按钮
    ui.btnEnter.gameObject:SetActive(true)
end

local function onCacheStep(_finish)
    -- 更新进度条
    ui.slider.value = _finish / config.Count
end

local function cacheSprites()
    logger.Info("source is " .. G_SOURCE)
    if G_SOURCE == 'file'
    then
        local files = {}
        for i=1, config.Count 
        do
            files[i-1] = 'img#' .. i .. '.jpg'
        end
        cache.CacheSpritesFromArchive(G_SOURCE_FILE, files, G_SpriteCaches, onCacheFinish, onCacheStep)
    elseif G_SOURCE == 'directory'
    then
        local files = {}
        for i=1, config.Count 
        do
            files[i-1] = io.Path.Combine(G_SOURCE_DIR, 'img#' .. i .. '.jpg')
        end
        cache.CacheSpritesFromFile(files, G_SpriteCaches, onCacheFinish, onCacheStep)
    elseif G_SOURCE == 'bytes'
    then

    end

    for k,v in pairs(G_SpriteCaches)
        do
            print(k)
        end

end

local function update()
end

local function run()
    print(config.Desc)
    logger.Debug("run app ...")
    logger.Info("sprites cache " .. G_SpriteCaches.Count)

    if G_SpriteCaches.Count == 0
    then
        return
    end

    local exists, sprite = G_SpriteCaches:TryGetValue('img#1.jpg')
    if nil == sprite
    then
        return
    end

    ui.imgFrame = G_Canvas2D:Find("[ui]/imgFrame"):GetComponent(typeof(unity.UI.Image))
    ui.imgFrame.sprite = sprite

    ui.slider = G_Canvas2D:Find("[ui]/cover/sdProgress"):GetComponent(typeof(unity.UI.Slider))
    ui.slider.value = 0

    ui.tip = G_Canvas2D:Find("[ui]/imgTip").gameObject
    ui.cover= G_Canvas2D:Find("[ui]/cover").gameObject

    ui.txtTitle = G_Canvas2D:Find("[ui]/cover/txtTitle"):GetComponent(typeof(unity.UI.Text))
    ui.txtTitle.text = config.Title
    ui.txtDesc = G_Canvas2D:Find("[ui]/cover/txtDescription"):GetComponent(typeof(unity.UI.Text))
    ui.txtDesc.text = config.Description

    ui.btnEnter = G_Canvas2D:Find("[ui]/cover/btnEnter"):GetComponent(typeof(unity.UI.Button))
    ui.btnEnter.onClick:AddListener(onEnterClick)
    
    -- 延迟1秒加载其他图片
    timer.DelaySeconds(1, cacheSprites)
end

local function stop()
    logger.Debug("stop app ...")
    ui.btnEnter.onClick:RemoveListener(onEnterClick)
end

local function handleEvent(_event, _data)
    logger.Debug("handle event  " .. _event)
end

app = {
    Run = run,
    Update = update,
    Stop = stop,
    HandleEvent = handleEvent,
}
