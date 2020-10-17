# -*- coding: utf-8 -*-

class UIFacade:

    facades = {}

    def Register(_uuid, _facade):
        if _uuid in UIFacade.facades:
            raise KeyError('facade is exists')
        UIFacade.facades[_uuid] = _facade

    def Cancel(_uuid):
        if not _uuid in UIFacade.facades:
            raise KeyError('facade not found')
        del UIFacade.facades[_uuid] 

    def Find(_uuid):
        return UIFacade.facades[_uuid]
