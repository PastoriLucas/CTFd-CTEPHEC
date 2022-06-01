/******/ (function(modules) { // webpackBootstrap
/******/ 	// install a JSONP callback for chunk loading
/******/ 	function webpackJsonpCallback(data) {
/******/ 		var chunkIds = data[0];
/******/ 		var moreModules = data[1];
/******/ 		var executeModules = data[2];
/******/
/******/ 		// add "moreModules" to the modules object,
/******/ 		// then flag all "chunkIds" as loaded and fire callback
/******/ 		var moduleId, chunkId, i = 0, resolves = [];
/******/ 		for(;i < chunkIds.length; i++) {
/******/ 			chunkId = chunkIds[i];
/******/ 			if(installedChunks[chunkId]) {
/******/ 				resolves.push(installedChunks[chunkId][0]);
/******/ 			}
/******/ 			installedChunks[chunkId] = 0;
/******/ 		}
/******/ 		for(moduleId in moreModules) {
/******/ 			if(Object.prototype.hasOwnProperty.call(moreModules, moduleId)) {
/******/ 				modules[moduleId] = moreModules[moduleId];
/******/ 			}
/******/ 		}
/******/ 		if(parentJsonpFunction) parentJsonpFunction(data);
/******/
/******/ 		while(resolves.length) {
/******/ 			resolves.shift()();
/******/ 		}
/******/
/******/ 		// add entry modules from loaded chunk to deferred list
/******/ 		deferredModules.push.apply(deferredModules, executeModules || []);
/******/
/******/ 		// run deferred modules when all chunks ready
/******/ 		return checkDeferredModules();
/******/ 	};
/******/ 	function checkDeferredModules() {
/******/ 		var result;
/******/ 		for(var i = 0; i < deferredModules.length; i++) {
/******/ 			var deferredModule = deferredModules[i];
/******/ 			var fulfilled = true;
/******/ 			for(var j = 1; j < deferredModule.length; j++) {
/******/ 				var depId = deferredModule[j];
/******/ 				if(installedChunks[depId] !== 0) fulfilled = false;
/******/ 			}
/******/ 			if(fulfilled) {
/******/ 				deferredModules.splice(i--, 1);
/******/ 				result = __webpack_require__(__webpack_require__.s = deferredModule[0]);
/******/ 			}
/******/ 		}
/******/ 		return result;
/******/ 	}
/******/
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// object to store loaded and loading chunks
/******/ 	// undefined = chunk not loaded, null = chunk preloaded/prefetched
/******/ 	// Promise = chunk loading, 0 = chunk loaded
/******/ 	var installedChunks = {
/******/ 		"pages/explanations": 0
/******/ 	};
/******/
/******/ 	var deferredModules = [];
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "/themes/admin/static/js";
/******/
/******/ 	var jsonpArray = window["webpackJsonp"] = window["webpackJsonp"] || [];
/******/ 	var oldJsonpFunction = jsonpArray.push.bind(jsonpArray);
/******/ 	jsonpArray.push = webpackJsonpCallback;
/******/ 	jsonpArray = jsonpArray.slice();
/******/ 	for(var i = 0; i < jsonpArray.length; i++) webpackJsonpCallback(jsonpArray[i]);
/******/ 	var parentJsonpFunction = oldJsonpFunction;
/******/
/******/
/******/ 	// add entry module to deferred list
/******/ 	deferredModules.push(["./CTFd/themes/admin/assets/js/pages/explanation.js","components","helpers","vendor","default~pages/explanation~pages/explanations~pages/configs~pages/editor~pages/main~pages/notifications~p~95e76be0"]);
/******/ 	// run deferred modules when ready
/******/ 	return checkDeferredModules();
/******/ })
/************************************************************************/
/******/ ({

/***/ "./CTFd/themes/admin/assets/js/pages/explanation.js":
/*!********************************************************!*\
  !*** ./CTFd/themes/admin/assets/js/pages/explanation.js ***!
  \********************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

;
eval("\n\n__webpack_require__(/*! ./main */ \"./CTFd/themes/admin/assets/js/pages/main.js\");\n\nvar _utils = __webpack_require__(/*! core/utils */ \"./CTFd/themes/core/assets/js/utils.js\");\n\nvar _jquery = _interopRequireDefault(__webpack_require__(/*! jquery */ \"./node_modules/jquery/dist/jquery.js\"));\n\n__webpack_require__(/*! bootstrap/js/dist/tab */ \"./node_modules/bootstrap/js/dist/tab.js\");\n\nvar _CTFd = _interopRequireDefault(__webpack_require__(/*! core/CTFd */ \"./CTFd/themes/core/assets/js/CTFd.js\"));\n\nvar _ezq = __webpack_require__(/*! core/ezq */ \"./CTFd/themes/core/assets/js/ezq.js\");\n\nvar _helpers = _interopRequireDefault(__webpack_require__(/*! core/helpers */ \"./CTFd/themes/core/assets/js/helpers.js\"));\n\nvar _styles = __webpack_require__(/*! ../styles */ \"./CTFd/themes/admin/assets/js/styles.js\");\n\nvar _vueEsm = _interopRequireDefault(__webpack_require__(/*! vue/dist/vue.esm.browser */ \"./node_modules/vue/dist/vue.esm.browser.js\"));\n\nvar _CommentBox = _interopRequireDefault(__webpack_require__(/*! ../components/comments/CommentBox.vue */ \"./CTFd/themes/admin/assets/js/components/comments/CommentBox.vue\"));\n\nvar _FlagList = _interopRequireDefault(__webpack_require__(/*! ../components/flags/FlagList.vue */ \"./CTFd/themes/admin/assets/js/components/flags/FlagList.vue\"));\n\nvar _Requirements = _interopRequireDefault(__webpack_require__(/*! ../components/requirements/Requirements.vue */ \"./CTFd/themes/admin/assets/js/components/requirements/Requirements.vue\"));\n\nvar _TopicsList = _interopRequireDefault(__webpack_require__(/*! ../components/topics/TopicsList.vue */ \"./CTFd/themes/admin/assets/js/components/topics/TopicsList.vue\"));\n\nvar _TagsList = _interopRequireDefault(__webpack_require__(/*! ../components/tags/TagsList.vue */ \"./CTFd/themes/admin/assets/js/components/tags/TagsList.vue\"));\n\nvar _ChallengeFilesList = _interopRequireDefault(__webpack_require__(/*! ../components/files/ChallengeFilesList.vue */ \"./CTFd/themes/admin/assets/js/components/files/ChallengeFilesList.vue\"));\n\nvar _HintsList = _interopRequireDefault(__webpack_require__(/*! ../components/hints/HintsList.vue */ \"./CTFd/themes/admin/assets/js/components/hints/HintsList.vue\"));\n\nvar _highlight = _interopRequireDefault(__webpack_require__(/*! highlight.js */ \"./node_modules/highlight.js/lib/index.js\"));\n\nfunction _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { \"default\": obj }; }\n\nvar displayHint = function displayHint(data) {\n  (0, _ezq.ezAlert)({\n    title: \"Hint\",\n    body: data.html,\n    button: \"Got it!\"\n  });\n};\n\nvar loadHint = function loadHint(id) {\n  _CTFd[\"default\"].api.get_hint({\n    hintId: id,\n    preview: true\n  }).then(function (response) {\n    if (response.data.content) {\n      displayHint(response.data);\n      return;\n    } // displayUnlock(id);\n\n  });\n};\n\nvar storeTimeHint = function storeTimeHint(id, exp, team) {\n  _CTFd[\"default\"].api.post_hints_timer({\n    hintId: id,\n    expId: exp,\n    teamId: team,\n    preview: true\n  }).then(function (response) {\n    if (response.data.content) {\n      displayHint(response.data);\n      return;\n    }\n  });\n};\n\nfunction renderExplanation(response) {\n  var result = response.data;\n  var explanation_input = (0, _jquery[\"default\"])(\"#feedback-textarea\");\n}\n\nfunction renderSubmissionResponse(response, cb) {\n  var result = response.data;\n  var result_message = (0, _jquery[\"default\"])(\"#result-message\");\n  var result_notification = (0, _jquery[\"default\"])(\"#result-notification\");\n  var answer_input = (0, _jquery[\"default\"])(\"#submission-input\");\n  result_notification.removeClass();\n  result_message.text(result.message);\n\n  if (result.status === \"authentication_required\") {\n    window.location = _CTFd[\"default\"].config.urlRoot + \"/login?next=\" + _CTFd[\"default\"].config.urlRoot + window.location.pathname + window.location.hash;\n    return;\n  } else if (result.status === \"incorrect\") {\n    // Incorrect key\n    result_notification.addClass(\"alert alert-danger alert-dismissable text-center\");\n    result_notification.slideDown();\n    answer_input.removeClass(\"correct\");\n    answer_input.addClass(\"wrong\");\n    setTimeout(function () {\n      answer_input.removeClass(\"wrong\");\n    }, 3000);\n  } else if (result.status === \"correct\") {\n    // Challenge Solved\n    result_notification.addClass(\"alert alert-success alert-dismissable text-center\");\n    result_notification.slideDown();\n    (0, _jquery[\"default\"])(\".explanation-solves\").text(parseInt((0, _jquery[\"default\"])(\".explanation-solves\").text().split(\" \")[0]) + 1 + \" Solves\");\n    answer_input.val(\"\");\n    answer_input.removeClass(\"wrong\");\n    answer_input.addClass(\"correct\");\n  } else if (result.status === \"already_solved\") {\n    // Challenge already solved\n    result_notification.addClass(\"alert alert-info alert-dismissable text-center\");\n    result_notification.slideDown();\n    answer_input.addClass(\"correct\");\n  } else if (result.status === \"paused\") {\n    // CTF is paused\n    result_notification.addClass(\"alert alert-warning alert-dismissable text-center\");\n    result_notification.slideDown();\n  } else if (result.status === \"ratelimited\") {\n    // Keys per minute too high\n    result_notification.addClass(\"alert alert-warning alert-dismissable text-center\");\n    result_notification.slideDown();\n    answer_input.addClass(\"too-fast\");\n    setTimeout(function () {\n      answer_input.removeClass(\"too-fast\");\n    }, 3000);\n  }\n\n  setTimeout(function () {\n    (0, _jquery[\"default\"])(\".alert\").slideUp();\n    (0, _jquery[\"default\"])(\"#explanation-submit\").removeClass(\"disabled-button\");\n    (0, _jquery[\"default\"])(\"#explanation-submit\").prop(\"disabled\", false);\n  }, 3000);\n\n  if (cb) {\n    cb(result);\n  }\n}\n\nfunction loadChalTemplate(explanation) {\n  _CTFd[\"default\"]._internal.explanation = {};\n\n  _jquery[\"default\"].getScript(_CTFd[\"default\"].config.urlRoot + explanation.scripts.view, function () {\n    var template_data = explanation.create;\n    (0, _jquery[\"default\"])(\"#create-exp-entry-div\").html(template_data);\n    (0, _styles.bindMarkdownEditors)();\n\n    _jquery[\"default\"].getScript(_CTFd[\"default\"].config.urlRoot + explanation.scripts.create, function () {\n      (0, _jquery[\"default\"])(\"#create-exp-entry-div form\").submit(function (event) {\n        event.preventDefault();\n        var params = (0, _jquery[\"default\"])(\"#create-exp-entry-div form\").serializeJSON();\n\n        _CTFd[\"default\"].fetch(\"/api/v1/explanations\", {\n          method: \"POST\",\n          credentials: \"same-origin\",\n          headers: {\n            Accept: \"application/json\",\n            \"Content-Type\": \"application/json\"\n          },\n          body: JSON.stringify(params)\n        }).then(function (response) {\n          return response.json();\n        }).then(function (response) {\n          if (response.success) {\n            (0, _jquery[\"default\"])(\"#explanation-create-options #explanation_id\").val(response.data.id);\n            (0, _jquery[\"default\"])(\"#explanation-create-options\").modal();\n          } else {\n            var body = \"\";\n\n            for (var k in response.errors) {\n              body += response.errors[k].join(\"\\n\");\n              body += \"\\n\";\n            }\n\n            (0, _ezq.ezAlert)({\n              title: \"Error\",\n              body: body,\n              button: \"OK\"\n            });\n          }\n        });\n      });\n    });\n  });\n}\n\nfunction handleChallengeOptions(event) {\n  event.preventDefault();\n  var params = (0, _jquery[\"default\"])(event.target).serializeJSON(true);\n  var flag_params = {\n    explanation_id: params.explanation_id,\n    content: params.flag || \"\",\n    type: params.flag_type,\n    data: params.flag_data ? params.flag_data : \"\"\n  }; // Define a save_explanation function\n\n  var save_explanation = function save_explanation() {\n    _CTFd[\"default\"].fetch(\"/api/v1/explanations/\" + params.explanation_id, {\n      method: \"PATCH\",\n      credentials: \"same-origin\",\n      headers: {\n        Accept: \"application/json\",\n        \"Content-Type\": \"application/json\"\n      },\n      body: JSON.stringify({\n        state: params.state\n      })\n    }).then(function (response) {\n      return response.json();\n    }).then(function (data) {\n      if (data.success) {\n        setTimeout(function () {\n          window.location = _CTFd[\"default\"].config.urlRoot + \"/admin/explanations/\" + params.explanation_id;\n        }, 700);\n      }\n    });\n  };\n\n  Promise.all([// Save flag\n  new Promise(function (resolve, _reject) {\n    if (flag_params.content.length == 0) {\n      resolve();\n      return;\n    }\n\n    _CTFd[\"default\"].fetch(\"/api/v1/flags\", {\n      method: \"POST\",\n      credentials: \"same-origin\",\n      headers: {\n        Accept: \"application/json\",\n        \"Content-Type\": \"application/json\"\n      },\n      body: JSON.stringify(flag_params)\n    }).then(function (response) {\n      resolve(response.json());\n    });\n  }), // Upload files\n  new Promise(function (resolve, _reject) {\n    var form = event.target;\n    var data = {\n      explanation: params.explanation_id,\n      type: \"explanation\"\n    };\n    var filepath = (0, _jquery[\"default\"])(form.elements[\"file\"]).val();\n\n    if (filepath) {\n      _helpers[\"default\"].files.upload(form, data);\n    }\n\n    resolve();\n  })]).then(function (_responses) {\n    save_explanation();\n  });\n}\n\n(0, _jquery[\"default\"])(function () {\n  (0, _jquery[\"default\"])(\".preview-explanation\").click(function (_e) {\n    _CTFd[\"default\"]._internal.explanation = {};\n\n    _jquery[\"default\"].get(_CTFd[\"default\"].config.urlRoot + \"/api/v1/explanations/\" + window.EXPLANATION_ID, function (response) {\n      // Preview should not show any solves\n      var explanation_data = response.data;\n      explanation_data[\"solves\"] = null;\n\n      _jquery[\"default\"].getScript(_CTFd[\"default\"].config.urlRoot + explanation_data.type_data.scripts.view, function () {\n        var explanation = _CTFd[\"default\"]._internal.explanation; // Inject explanation data into the plugin\n\n        explanation.data = response.data;\n        (0, _jquery[\"default\"])(\"#explanation-window\").empty(); // Call preRender function in plugin\n\n        explanation.preRender();\n        (0, _jquery[\"default\"])(\"#explanation-window\").append(explanation_data.view);\n        (0, _jquery[\"default\"])(\"#explanation-window #explanation-input\").addClass(\"form-control\");\n        (0, _jquery[\"default\"])(\"#explanation-window #explanation-submit\").addClass(\"btn btn-md btn-outline-secondary float-right\");\n        (0, _jquery[\"default\"])(\".explanation-solves\").hide();\n        (0, _jquery[\"default\"])(\".nav-tabs a\").click(function (e) {\n          e.preventDefault();\n          (0, _jquery[\"default\"])(this).tab(\"show\");\n        }); // Handle modal toggling\n\n        (0, _jquery[\"default\"])(\"#explanation-window\").on(\"hide.bs.modal\", function (_event) {\n          (0, _jquery[\"default\"])(\"#explanation-input\").removeClass(\"wrong\");\n          (0, _jquery[\"default\"])(\"#explanation-input\").removeClass(\"correct\");\n          (0, _jquery[\"default\"])(\"#incorrect-key\").slideUp();\n          (0, _jquery[\"default\"])(\"#correct-key\").slideUp();\n          (0, _jquery[\"default\"])(\"#already-solved\").slideUp();\n          (0, _jquery[\"default\"])(\"#too-fast\").slideUp();\n        });\n        (0, _jquery[\"default\"])(\".load-hint\").on(\"click\", function (_event) {\n          loadHint((0, _jquery[\"default\"])(this).data(\"hint-id\"));\n          storeTimeHint((0, _jquery[\"default\"])(this).data(\"hint-id\"), (0, _jquery[\"default\"])(this).data(\"exp-id\"), (0, _jquery[\"default\"])(this).data(\"team-id\"));\n        });\n        (0, _jquery[\"default\"])(\"#explanation-submit\").click(function (e) {\n          e.preventDefault();\n          (0, _jquery[\"default\"])(\"#explanation-submit\").addClass(\"disabled-button\");\n          (0, _jquery[\"default\"])(\"#explanation-submit\").prop(\"disabled\", true);\n\n          _CTFd[\"default\"]._internal.explanation.submit(true).then(renderSubmissionResponse); // Preview passed as true\n\n        });\n        (0, _jquery[\"default\"])(\"#explanation-input\").keyup(function (event) {\n          if (event.keyCode == 13) {\n            (0, _jquery[\"default\"])(\"#explanation-submit\").click();\n          }\n        });\n        explanation.postRender();\n        (0, _jquery[\"default\"])(\"#explanation-window\").find(\"pre code\").each(function (_idx) {\n          _highlight[\"default\"].highlightBlock(this);\n        });\n        window.location.replace(window.location.href.split(\"#\")[0] + \"#preview\");\n        (0, _jquery[\"default\"])(\"#explanation-window\").modal();\n      });\n    });\n  });\n  (0, _jquery[\"default\"])(\".comments-explanation\").click(function (_event) {\n    (0, _jquery[\"default\"])(\"#explanation-comments-window\").modal();\n  });\n  (0, _jquery[\"default\"])(\".delete-explanation\").click(function (_e) {\n    (0, _ezq.ezQuery)({\n      title: \"Delete Challenge\",\n      body: \"Are you sure you want to delete {0}\".format(\"<strong>\" + (0, _utils.htmlEntities)(window.EXPLANATION_ID) + \"</strong>\"),\n      success: function success() {\n        _CTFd[\"default\"].fetch(\"/api/v1/explanations/\" + window.EXPLANATION_ID, {\n          method: \"DELETE\"\n        }).then(function (response) {\n          return response.json();\n        }).then(function (response) {\n          if (response.success) {\n            window.location = _CTFd[\"default\"].config.urlRoot + \"/admin/explanations\";\n          }\n        });\n      }\n    });\n  });\n  (0, _jquery[\"default\"])(\"#explanation-update-container > form\").submit(function (e) {\n    e.preventDefault();\n    var params = (0, _jquery[\"default\"])(e.target).serializeJSON(true);\n\n    _CTFd[\"default\"].fetch(\"/api/v1/explanations/\" + window.EXPLANATION_ID + \"/flags\", {\n      method: \"GET\",\n      credentials: \"same-origin\",\n      headers: {\n        Accept: \"application/json\",\n        \"Content-Type\": \"application/json\"\n      }\n    }).then(function (response) {\n      return response.json();\n    }).then(function (response) {\n      var update_explanation = function update_explanation() {\n        _CTFd[\"default\"].fetch(\"/api/v1/explanations/\" + window.EXPLANATION_ID, {\n          method: \"PATCH\",\n          credentials: \"same-origin\",\n          headers: {\n            Accept: \"application/json\",\n            \"Content-Type\": \"application/json\"\n          },\n          body: JSON.stringify(params)\n        }).then(function (response) {\n          return response.json();\n        }).then(function (response) {\n          if (response.success) {\n            (0, _jquery[\"default\"])(\".explanation-state\").text(response.data.state);\n\n            switch (response.data.state) {\n              case \"visible\":\n                (0, _jquery[\"default\"])(\".explanation-state\").removeClass(\"badge-danger\").addClass(\"badge-success\");\n                break;\n\n              case \"hidden\":\n                (0, _jquery[\"default\"])(\".explanation-state\").removeClass(\"badge-success\").addClass(\"badge-danger\");\n                break;\n\n              default:\n                break;\n            }\n\n            (0, _ezq.ezToast)({\n              title: \"Success\",\n              body: \"Your explanation has been updated!\"\n            });\n          } else {\n            var body = \"\";\n\n            for (var k in response.errors) {\n              body += response.errors[k].join(\"\\n\");\n              body += \"\\n\";\n            }\n\n            (0, _ezq.ezAlert)({\n              title: \"Error\",\n              body: body,\n              button: \"OK\"\n            });\n          }\n        });\n      }; // Check if the explanation doesn't have any flags before marking visible\n\n\n      if (response.data.length === 0 && params.state === \"visible\") {\n        (0, _ezq.ezQuery)({\n          title: \"Missing Flags\",\n          body: \"This explanation does not have any flags meaning it may be unsolveable. Are you sure you'd like to update this explanation?\",\n          success: update_explanation\n        });\n      } else {\n        update_explanation();\n      }\n    });\n  });\n  (0, _jquery[\"default\"])(\"#explanation-create-options form\").submit(handleChallengeOptions); // Load FlagList component\n\n  if (document.querySelector(\"#explanation-flags\")) {\n    var flagList = _vueEsm[\"default\"].extend(_FlagList[\"default\"]);\n\n    var vueContainer = document.createElement(\"div\");\n    document.querySelector(\"#explanation-flags\").appendChild(vueContainer);\n    new flagList({\n      propsData: {\n        explanation_id: window.EXPLANATION_ID\n      }\n    }).$mount(vueContainer);\n  } // Load TopicsList component\n\n\n  if (document.querySelector(\"#explanation-topics\")) {\n    var topicsList = _vueEsm[\"default\"].extend(_TopicsList[\"default\"]);\n\n    var _vueContainer = document.createElement(\"div\");\n\n    document.querySelector(\"#explanation-topics\").appendChild(_vueContainer);\n    new topicsList({\n      propsData: {\n        explanation_id: window.EXPLANATION_ID\n      }\n    }).$mount(_vueContainer);\n  } // Load TagsList component\n\n\n  if (document.querySelector(\"#explanation-tags\")) {\n    var tagList = _vueEsm[\"default\"].extend(_TagsList[\"default\"]);\n\n    var _vueContainer2 = document.createElement(\"div\");\n\n    document.querySelector(\"#explanation-tags\").appendChild(_vueContainer2);\n    new tagList({\n      propsData: {\n        explanation_id: window.EXPLANATION_ID\n      }\n    }).$mount(_vueContainer2);\n  } // Load Requirements component\n\n\n  if (document.querySelector(\"#prerequisite-add-form\")) {\n    var reqsComponent = _vueEsm[\"default\"].extend(_Requirements[\"default\"]);\n\n    var _vueContainer3 = document.createElement(\"div\");\n\n    document.querySelector(\"#prerequisite-add-form\").appendChild(_vueContainer3);\n    new reqsComponent({\n      propsData: {\n        explanation_id: window.EXPLANATION_ID\n      }\n    }).$mount(_vueContainer3);\n  } // Load ChallengeFilesList component\n\n\n  if (document.querySelector(\"#explanation-files\")) {\n    var explanationFilesList = _vueEsm[\"default\"].extend(_ChallengeFilesList[\"default\"]);\n\n    var _vueContainer4 = document.createElement(\"div\");\n\n    document.querySelector(\"#explanation-files\").appendChild(_vueContainer4);\n    new explanationFilesList({\n      propsData: {\n        explanation_id: window.EXPLANATION_ID\n      }\n    }).$mount(_vueContainer4);\n  } // Load HintsList component\n\n\n  if (document.querySelector(\"#explanation-hints\")) {\n    var hintsList = _vueEsm[\"default\"].extend(_HintsList[\"default\"]);\n\n    console.log(hintsList);\n\n    var _vueContainer5 = document.createElement(\"div\");\n\n    document.querySelector(\"#explanation-hints\").appendChild(_vueContainer5);\n    new hintsList({\n      propsData: {\n        explanation_id: window.EXPLANATION_ID\n      }\n    }).$mount(_vueContainer5);\n  } // Because this JS is shared by a few pages,\n  // we should only insert the CommentBox if it's actually in use\n\n\n  if (document.querySelector(\"#comment-box\")) {\n    // Insert CommentBox element\n    var commentBox = _vueEsm[\"default\"].extend(_CommentBox[\"default\"]);\n\n    var _vueContainer6 = document.createElement(\"div\");\n\n    document.querySelector(\"#comment-box\").appendChild(_vueContainer6);\n    new commentBox({\n      propsData: {\n        type: \"explanation\",\n        id: window.EXPLANATION_ID\n      }\n    }).$mount(_vueContainer6);\n  }\n\n  _jquery[\"default\"].get(_CTFd[\"default\"].config.urlRoot + \"/api/v1/explanations/types\", function (response) {\n    var data = response.data;\n    loadChalTemplate(data[\"standard\"]);\n    (0, _jquery[\"default\"])(\"#create-exps-select input[name=type]\").change(function () {\n      var explanation = data[this.value];\n      loadChalTemplate(explanation);\n    });\n  });\n\n  (0, _jquery[\"default\"])(\".load-timedhint\").click(function (_event) {\n    storeTimedHint(this.value);\n  });\n});\n\nvar storeTimedHint = function storeTimedHint(id) {\n  var exp = id;\n  var today = new Date();\n  var date = today.getFullYear() + '-' + (today.getMonth() + 1) + '-' + today.getDate();\n  var time = today.getHours() + \":\" + today.getMinutes() + \":\" + today.getSeconds();\n  var dateTime = date + ' ' + time;\n  console.log(dateTime);\n  console.log(exp);\n  console.log(teamId);\n\n  _CTFd[\"default\"].api.post_hints_timer({\n    team_id: teamId,\n    explanation_id: exp,\n    end_time: dateTime\n  }).then(function (response) {\n    if (response.data.content) {\n      displayHint(response.data);\n      return;\n    }\n  });\n};\n\n//# sourceURL=webpack:///./CTFd/themes/admin/assets/js/pages/explanation.js?");

/***/ })

/******/ });