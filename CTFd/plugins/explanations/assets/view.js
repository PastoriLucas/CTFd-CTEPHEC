CTFd._internal.explanation.data = undefined

CTFd._internal.explanation.renderer = CTFd.lib.markdown();


CTFd._internal.explanation.preRender = function () { }

CTFd._internal.explanation.render = function (markdown) {
    return CTFd._internal.explanation.renderer.render(markdown)
}


CTFd._internal.explanation.postRender = function () { }


CTFd._internal.explanation.submit = function (preview) {
    var explanation_id = parseInt(CTFd.lib.$('#explanation-id').val())
    var submission = CTFd.lib.$('#explanation-textarea').val()

    var body = {
        'explanation_id': explanation_id,
        'submission': submission,
    }
    var params = {}
    if (preview) {
        params['preview'] = true
    }

    return CTFd.api.post_explanation(params, body).then(function (response) {
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
