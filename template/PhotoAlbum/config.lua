local description = {}
local count = {{__count__}}

for i=1,count
do
    description["img#" .. i .. ".jpg"] = {}
end

-- description["img#1.jpg"]["en_US"] = 'this is description.'

{{__description__}}

return {
    Desc = description,
}
