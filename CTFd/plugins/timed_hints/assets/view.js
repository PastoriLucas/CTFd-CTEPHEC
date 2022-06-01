CTFd._internal.hintsTimer.data = undefined

CTFd._internal.hintsTimer.renderer = CTFd.lib.markdown();


CTFd._internal.hintsTimer.preRender = function () { }

CTFd._internal.hintsTimer.render = function (markdown) {
    return CTFd._internal.hintsTimer.renderer.render(markdown)
}


CTFd._internal.hintsTimer.postRender = function () { }


CTFd._internal.hintsTimer.submit = function (preview) {
    var hintsTimer_id = parseInt(CTFd.lib.$('#hintsTimer-id').val())
    var submission = CTFd.lib.$('#hintsTimer-input').val()

    var body = {
        'hintsTimer_id': hintsTimer_id,
        'submission': submission,
    }
    var params = {}
    if (preview) {
        params['preview'] = true
    }

    return CTFd.api.post_hints_timer(params, body).then(function (response) {
        if (response.status === 429) {
            // User was ratelimited but process response
            return response
        }
        if (response.status === 403) {
            // User is not logged in or CTF is paused.
            return response
        }
        return response
    })
};