local config = require('config')
local util = require 'xlua.util'
local unity = CS.UnityEngine
local io = CS.System.IO
local logger = CS.API.Assloud.XSA.Logger
local opend = false

local function onAssetLoadFinish(_assetBundle)
    logger.Info(_assetBundle)
end

local function update()
end

local function run()
    print(config.Desc)
    logger.Debug("run app ...")
    logger.Info("sprites cache " .. G_SpriteCaches.Count)
    local animator = G_Canvas2D:Find("[ui]"):GetComponent(typeof(unity.Animator))
    local bigPicture = G_Canvas2D:Find("[ui]/frame/image"):GetComponent(typeof(unity.UI.Image))
    local txtDescription = G_Canvas2D:Find("[ui]/frame/mask/txtDescription"):GetComponent(typeof(unity.UI.Text))
    local btnClose = G_Canvas2D:Find("[ui]/frame/btnClose"):GetComponent(typeof(unity.UI.Button))
    btnClose.onClick:AddListener(function()
        opend = false
        animator:SetTrigger("close")
    end)

    local template = G_Canvas2D:Find("[ui]/Scroll View/Viewport/Content/template")
    template.gameObject:SetActive(false)
    for k, v in pairs(G_SpriteCaches)
    do
        local clone = unity.GameObject.Instantiate(template.gameObject)
        clone.name = k
        clone.transform:SetParent(template.parent)
        clone.transform.localPosition = unity.Vector3.zero;
        clone.transform.localRotation = unity.Quaternion.identity;
        clone.transform.localScale = unity.Vector3.one;
        clone:SetActive(true)
        local image = clone:GetComponent(typeof(unity.UI.Image))
        image.sprite = v

        local btn = clone:GetComponent(typeof(unity.UI.Button))
        btn.onClick:AddListener(function()
            bigPicture.sprite = image.sprite
            txtDescription.text = config.Desc[k]["en_US"]
            if false == opend
            then
                animator:SetTrigger("open")
            end
            opend = true
        end)
    end

end

local function stop()
    logger.Debug("stop app ...")
    util.print_func_ref_by_csharp()
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
