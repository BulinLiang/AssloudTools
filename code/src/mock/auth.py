def Process(_url, _method, _params, _onReply, _onError, _options):
    if _options['code'] == 0:
        reply = str(_options)
        _onReply(reply)
    elif _options['code'] == 1:
        error = str(_options)
        _onError(error)
