(()=>{"use strict";var e="Ids",t="NotificationReceived",n="NotificationConverted",r="configs",i="permission",o="shouldResubscribe",a="flarelane_db",s="flarelane_db_window",c="flarelane_get",u="flarelane_getAll",l="flarelane_put",f="flarelane_delete",d="flarelane_clearTable";let h,p;const v=new WeakMap,b=new WeakMap,g=new WeakMap,y=new WeakMap,w=new WeakMap;let m={get(e,t,n){if(e instanceof IDBTransaction){if("done"===t)return b.get(e);if("objectStoreNames"===t)return e.objectStoreNames||g.get(e);if("store"===t)return n.objectStoreNames[1]?void 0:n.objectStore(n.objectStoreNames[0])}return E(e[t])},set:(e,t,n)=>(e[t]=n,!0),has:(e,t)=>e instanceof IDBTransaction&&("done"===t||"store"===t)||t in e};function D(e){return"function"==typeof e?(t=e)!==IDBDatabase.prototype.transaction||"objectStoreNames"in IDBTransaction.prototype?(p||(p=[IDBCursor.prototype.advance,IDBCursor.prototype.continue,IDBCursor.prototype.continuePrimaryKey])).includes(t)?function(...e){return t.apply(S(this),e),E(v.get(this))}:function(...e){return E(t.apply(S(this),e))}:function(e,...n){const r=t.call(S(this),e,...n);return g.set(r,e.sort?e.sort():[e]),E(r)}:(e instanceof IDBTransaction&&function(e){if(b.has(e))return;const t=new Promise(((t,n)=>{const r=()=>{e.removeEventListener("complete",i),e.removeEventListener("error",o),e.removeEventListener("abort",o)},i=()=>{t(),r()},o=()=>{n(e.error||new DOMException("AbortError","AbortError")),r()};e.addEventListener("complete",i),e.addEventListener("error",o),e.addEventListener("abort",o)}));b.set(e,t)}(e),n=e,(h||(h=[IDBDatabase,IDBObjectStore,IDBIndex,IDBCursor,IDBTransaction])).some((e=>n instanceof e))?new Proxy(e,m):e);var t,n}function E(e){if(e instanceof IDBRequest)return function(e){const t=new Promise(((t,n)=>{const r=()=>{e.removeEventListener("success",i),e.removeEventListener("error",o)},i=()=>{t(E(e.result)),r()},o=()=>{n(e.error),r()};e.addEventListener("success",i),e.addEventListener("error",o)}));return t.then((t=>{t instanceof IDBCursor&&v.set(t,e)})).catch((()=>{})),w.set(t,e),t}(e);if(y.has(e))return y.get(e);const t=D(e);return t!==e&&(y.set(e,t),w.set(t,e)),t}const S=e=>w.get(e);function B(e,t,{blocked:n,upgrade:r,blocking:i,terminated:o}={}){const a=indexedDB.open(e,t),s=E(a);return r&&a.addEventListener("upgradeneeded",(e=>{r(E(a.result),e.oldVersion,e.newVersion,E(a.transaction),e)})),n&&a.addEventListener("blocked",(e=>n(e.oldVersion,e.newVersion,e))),s.then((e=>{o&&e.addEventListener("close",(()=>o())),i&&e.addEventListener("versionchange",(e=>i(e.oldVersion,e.newVersion,e)))})).catch((()=>{})),s}function I(e,{blocked:t}={}){const n=indexedDB.deleteDatabase(e);return t&&n.addEventListener("blocked",(e=>t(e.oldVersion,e))),E(n).then((()=>{}))}const k=["get","getKey","getAll","getAllKeys","count"],L=["put","add","delete","clear"],x=new Map;function T(e,t){if(!(e instanceof IDBDatabase)||t in e||"string"!=typeof t)return;if(x.get(t))return x.get(t);const n=t.replace(/FromIndex$/,""),r=t!==n,i=L.includes(n);if(!(n in(r?IDBIndex:IDBObjectStore).prototype)||!i&&!k.includes(n))return;const o=async function(e,...t){const o=this.transaction(e,i?"readwrite":"readonly");let a=o.store;return r&&(a=a.index(t.shift())),(await Promise.all([a[n](...t),i&&o.done]))[0]};return x.set(t,o),o}var P;P=m,m={...P,get:(e,t,n)=>T(e,t)||P.get(e,t,n),has:(e,t)=>!!T(e,t)||P.has(e,t)};var R={none:0,error:1,verbose:5};const U=function(){function e(){}return e.setisTracerActivate=function(){this.isTracerActivate="true"===window.localStorage.getItem("flarelane_isTracerActivate")},e.setLogLevel=function(e){var t=R[e];void 0!==t?this.logLevel=t:this.error("Cannot set ".concat(e," in setLogLevel. Please set one of none, error, verbose."))},e.log=function(e){this.logLevel<R.verbose||console.log("[FLARELANE] - ".concat(e))},e.error=function(e){this.logLevel<R.error||console.error("[FLARELANE] - ".concat(e))},e.trace=function(e){for(var t=[],n=1;n<arguments.length;n++)t[n-1]=arguments[n];this.isTracerActivate&&console.log("%c[FLARELANE] - Call: ".concat(e,", Args: ").concat(JSON.stringify(t,null,2)),"color:gray")},e.logLevel=R.verbose,e.isTracerActivate=!1,e}();var O,C=new Uint8Array(16);function A(){if(!O&&!(O="undefined"!=typeof crypto&&crypto.getRandomValues&&crypto.getRandomValues.bind(crypto)||"undefined"!=typeof msCrypto&&"function"==typeof msCrypto.getRandomValues&&msCrypto.getRandomValues.bind(msCrypto)))throw new Error("crypto.getRandomValues() not supported. See https://github.com/uuidjs/uuid#getrandomvalues-not-supported");return O(C)}const W=/^(?:[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}|00000000-0000-0000-0000-000000000000)$/i,N=function(e){return"string"==typeof e&&W.test(e)};for(var F=[],j=0;j<256;++j)F.push((j+256).toString(16).substr(1));const V=function(e,t,n){var r=(e=e||{}).random||(e.rng||A)();if(r[6]=15&r[6]|64,r[8]=63&r[8]|128,t){n=n||0;for(var i=0;i<16;++i)t[n+i]=r[i];return t}return function(e){var t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:0,n=(F[e[t+0]]+F[e[t+1]]+F[e[t+2]]+F[e[t+3]]+"-"+F[e[t+4]]+F[e[t+5]]+"-"+F[e[t+6]]+F[e[t+7]]+"-"+F[e[t+8]]+F[e[t+9]]+"-"+F[e[t+10]]+F[e[t+11]]+F[e[t+12]]+F[e[t+13]]+F[e[t+14]]+F[e[t+15]]).toLowerCase();if(!N(n))throw TypeError("Stringified UUID is invalid");return n}(r)};var M=function(e,t,n,r){return new(n||(n=Promise))((function(i,o){function a(e){try{c(r.next(e))}catch(e){o(e)}}function s(e){try{c(r.throw(e))}catch(e){o(e)}}function c(e){var t;e.done?i(e.value):(t=e.value,t instanceof n?t:new n((function(e){e(t)}))).then(a,s)}c((r=r.apply(e,t||[])).next())}))},_=function(e,t){var n,r,i,o,a={label:0,sent:function(){if(1&i[0])throw i[1];return i[1]},trys:[],ops:[]};return o={next:s(0),throw:s(1),return:s(2)},"function"==typeof Symbol&&(o[Symbol.iterator]=function(){return this}),o;function s(o){return function(s){return function(o){if(n)throw new TypeError("Generator is already executing.");for(;a;)try{if(n=1,r&&(i=2&o[0]?r.return:o[0]?r.throw||((i=r.return)&&i.call(r),0):r.next)&&!(i=i.call(r,o[1])).done)return i;switch(r=0,i&&(o=[2&o[0],i.value]),o[0]){case 0:case 1:i=o;break;case 4:return a.label++,{value:o[1],done:!1};case 5:a.label++,r=o[1],o=[0];continue;case 7:o=a.ops.pop(),a.trys.pop();continue;default:if(!((i=(i=a.trys).length>0&&i[i.length-1])||6!==o[0]&&2!==o[0])){a=0;continue}if(3===o[0]&&(!i||o[1]>i[0]&&o[1]<i[3])){a.label=o[1];break}if(6===o[0]&&a.label<i[1]){a.label=i[1],i=o;break}if(i&&a.label<i[2]){a.label=i[2],a.ops.push(o);break}i[2]&&a.ops.pop(),a.trys.pop();continue}o=t.call(e,a)}catch(e){o=[6,e],r=0}finally{n=i=0}if(5&o[0])throw o[1];return{value:o[0]?o[1]:void 0,done:!0}}([o,s])}}},H=function(){function t(){}return t.get=function(e,t){return M(this,void 0,void 0,(function(){var n;return _(this,(function(r){switch(r.label){case 0:return U.trace("Fecth:get",e,t),[4,this.getBaseUrl(t)];case 1:return n=r.sent(),[4,fetch("".concat(n).concat(e),{method:"GET",headers:this.getHeaders()})];case 2:return[2,r.sent().json()]}}))}))},t.post=function(e,t,n){return M(this,void 0,void 0,(function(){var r;return _(this,(function(i){switch(i.label){case 0:return U.trace("Fecth:post",e,t),[4,this.getBaseUrl(n)];case 1:return r=i.sent(),[4,fetch("".concat(r).concat(e),{method:"POST",headers:this.getHeaders(),body:JSON.stringify(t)})];case 2:return[2,i.sent().json()]}}))}))},t.patch=function(e,t){return M(this,void 0,void 0,(function(){var n;return _(this,(function(r){switch(r.label){case 0:return U.trace("Fecth:patch",e,t),[4,this.getBaseUrl()];case 1:return n=r.sent(),[4,fetch("".concat(n).concat(e),{method:"PATCH",headers:this.getHeaders(),body:JSON.stringify(t)})];case 2:return[2,r.sent().json()]}}))}))},t.delete=function(e,t){return M(this,void 0,void 0,(function(){var n;return _(this,(function(r){switch(r.label){case 0:return U.trace("Fecth:delete",e,t),[4,this.getBaseUrl()];case 1:return n=r.sent(),[4,fetch("".concat(n).concat(e),{method:"DELETE",headers:this.getHeaders(),body:JSON.stringify(t)})];case 2:return[2,r.sent().json()]}}))}))},t.getHeaders=function(){return{"Content-Type":"application/json","x-flarelane-sdk-info":this.getSdkInfo()}},t.getSdkInfo=function(){return"".concat("native","-").concat("0.2.2")},t.getBaseUrl=function(t){return M(this,void 0,void 0,(function(){var n,r;return _(this,(function(i){switch(i.label){case 0:return t?(r=t,[3,3]):[3,1];case 1:return[4,oe.get(e,"projectId")];case 2:r=i.sent(),i.label=3;case 3:return n=r,[2,"".concat("https://service-api.flarelane.com/internal/v1/projects","/").concat(n)]}}))}))},t}(),G=function(){return!!window.postMessage||(U.error("This browser doesn't support window.postMessage()"),!1)},J=function(e,t,n){try{if(new URL(e).origin!==new URL(t).origin){if(n)throw new Error("Please check site url or subdomain in flarelane console");return!1}return!0}catch(e){if(n)throw e;return!1}},K=function(e){return JSON.parse(JSON.stringify(e))},q=function(e,t,n,r){return new(n||(n=Promise))((function(i,o){function a(e){try{c(r.next(e))}catch(e){o(e)}}function s(e){try{c(r.throw(e))}catch(e){o(e)}}function c(e){var t;e.done?i(e.value):(t=e.value,t instanceof n?t:new n((function(e){e(t)}))).then(a,s)}c((r=r.apply(e,t||[])).next())}))},$=function(e,t){var n,r,i,o,a={label:0,sent:function(){if(1&i[0])throw i[1];return i[1]},trys:[],ops:[]};return o={next:s(0),throw:s(1),return:s(2)},"function"==typeof Symbol&&(o[Symbol.iterator]=function(){return this}),o;function s(o){return function(s){return function(o){if(n)throw new TypeError("Generator is already executing.");for(;a;)try{if(n=1,r&&(i=2&o[0]?r.return:o[0]?r.throw||((i=r.return)&&i.call(r),0):r.next)&&!(i=i.call(r,o[1])).done)return i;switch(r=0,i&&(o=[2&o[0],i.value]),o[0]){case 0:case 1:i=o;break;case 4:return a.label++,{value:o[1],done:!1};case 5:a.label++,r=o[1],o=[0];continue;case 7:o=a.ops.pop(),a.trys.pop();continue;default:if(!((i=(i=a.trys).length>0&&i[i.length-1])||6!==o[0]&&2!==o[0])){a=0;continue}if(3===o[0]&&(!i||o[1]>i[0]&&o[1]<i[3])){a.label=o[1];break}if(6===o[0]&&a.label<i[1]){a.label=i[1],i=o;break}if(i&&a.label<i[2]){a.label=i[2],a.ops.push(o);break}i[2]&&a.ops.pop(),a.trys.pop();continue}o=t.call(e,a)}catch(e){o=[6,e],r=0}finally{n=i=0}if(5&o[0])throw o[1];return{value:o[0]?o[1]:void 0,done:!0}}([o,s])}}},z=function(){function t(){}return t.saveConfigs=function(t){return oe.put(e,r,t)},t.getConfigs=function(){return q(this,void 0,void 0,(function(){var t;return $(this,(function(n){switch(n.label){case 0:return[4,oe.get(e,r)];case 1:return t=n.sent(),this.additionalOrigin&&(t.originSiteUrl=this.additionalOrigin),[2,t]}}))}))},t.getRemoteConfigs=function(e){return q(this,void 0,void 0,(function(){var t;return $(this,(function(n){switch(n.label){case 0:return[4,H.get(this.url,e)];case 1:return t=n.sent(),this.additionalOrigin&&(t.data.originSiteUrl=this.additionalOrigin),[2,t.data]}}))}))},t.setAdditionalOrigin=function(e,n){if(e.originSiteUrl&&!J(e.originSiteUrl,n)){var r=function(e,t){try{return(null==e?void 0:e.filter((function(e){return new URL(e).origin===new URL(t).origin}))[0])||null}catch(e){return null}}(function(e,t,n){if(n||2===arguments.length)for(var r,i=0,o=t.length;i<o;i++)!r&&i in t||(r||(r=Array.prototype.slice.call(t,0,i)),r[i]=t[i]);return e.concat(r||Array.prototype.slice.call(t))}([],e.additionalOrigins,!0),n);if(null===r)throw new Error("Please check site url or subdomain in flarelane console");return t.additionalOrigin=r,r}},t.additionalOrigin=null,t.url="/remote-params-web",t}(),Q=function(){function e(){}return e.create=function(e){return document.createElement(e)},e.remove=function(e){var t=this.get(e);t&&t.remove()},e.get=function(e){return document.getElementById(e)},e.getBody=function(e){return e.document.body||e.document.getElementsByTagName("body")[0]},e.getHead=function(e){return e.document.head||e.document.getElementsByTagName("head")[0]},e.getParentWindow=function(){return window.opener||window.parent||null},e.setCss=function(e,t){if(!this.get(e)){var n=this.getHead(window),r=this.create("style");r.id=e,r.textContent=t,n.append(r)}},e.setMobileCss=function(e,t){var n="\n      @media screen and (max-width: 768px) {\n        ".concat(t,"\n      }\n    ");this.setCss(e,n)},e}(),X=function(e,t,n,r){return new(n||(n=Promise))((function(i,o){function a(e){try{c(r.next(e))}catch(e){o(e)}}function s(e){try{c(r.throw(e))}catch(e){o(e)}}function c(e){var t;e.done?i(e.value):(t=e.value,t instanceof n?t:new n((function(e){e(t)}))).then(a,s)}c((r=r.apply(e,t||[])).next())}))},Y=function(e,t){var n,r,i,o,a={label:0,sent:function(){if(1&i[0])throw i[1];return i[1]},trys:[],ops:[]};return o={next:s(0),throw:s(1),return:s(2)},"function"==typeof Symbol&&(o[Symbol.iterator]=function(){return this}),o;function s(o){return function(s){return function(o){if(n)throw new TypeError("Generator is already executing.");for(;a;)try{if(n=1,r&&(i=2&o[0]?r.return:o[0]?r.throw||((i=r.return)&&i.call(r),0):r.next)&&!(i=i.call(r,o[1])).done)return i;switch(r=0,i&&(o=[2&o[0],i.value]),o[0]){case 0:case 1:i=o;break;case 4:return a.label++,{value:o[1],done:!1};case 5:a.label++,r=o[1],o=[0];continue;case 7:o=a.ops.pop(),a.trys.pop();continue;default:if(!((i=(i=a.trys).length>0&&i[i.length-1])||6!==o[0]&&2!==o[0])){a=0;continue}if(3===o[0]&&(!i||o[1]>i[0]&&o[1]<i[3])){a.label=o[1];break}if(6===o[0]&&a.label<i[1]){a.label=i[1],i=o;break}if(i&&a.label<i[2]){a.label=i[2],a.ops.push(o);break}i[2]&&a.ops.pop(),a.trys.pop();continue}o=t.call(e,a)}catch(e){o=[6,e],r=0}finally{n=i=0}if(5&o[0])throw o[1];return{value:o[0]?o[1]:void 0,done:!0}}([o,s])}}},Z=function(){function e(){}return e.inject=function(e){return X(this,void 0,void 0,(function(){var t=this;return Y(this,(function(n){return U.trace("Iframe:inject",e),[2,new Promise((function(n,r){return X(t,void 0,void 0,(function(){var t,i,o;return Y(this,(function(a){try{if(Q.get(this.iframeId))return[2];t=Q.getBody(window),i=Q.create("iframe"),(o=new URL(e)).pathname="iframe.html",i.id=this.iframeId,i.src=o.href,i.style.display="none",i.setAttribute("sandbox","allow-popups allow-popups-to-escape-sandbox allow-same-origin allow-scripts allow-top-navigation"),i.addEventListener("load",(function(){n(!0)})),t.append(i)}catch(e){r(e)}return[2]}))}))}))]}))}))},e.get=function(){return Q.get(this.iframeId)||null},e.remove=function(){var e=Q.get(this.iframeId);e&&e.remove()},e.iframeId="flarelane-iframe",e}(),ee=function(e,t,n,r){return new(n||(n=Promise))((function(i,o){function a(e){try{c(r.next(e))}catch(e){o(e)}}function s(e){try{c(r.throw(e))}catch(e){o(e)}}function c(e){var t;e.done?i(e.value):(t=e.value,t instanceof n?t:new n((function(e){e(t)}))).then(a,s)}c((r=r.apply(e,t||[])).next())}))},te=function(e,t){var n,r,i,o,a={label:0,sent:function(){if(1&i[0])throw i[1];return i[1]},trys:[],ops:[]};return o={next:s(0),throw:s(1),return:s(2)},"function"==typeof Symbol&&(o[Symbol.iterator]=function(){return this}),o;function s(o){return function(s){return function(o){if(n)throw new TypeError("Generator is already executing.");for(;a;)try{if(n=1,r&&(i=2&o[0]?r.return:o[0]?r.throw||((i=r.return)&&i.call(r),0):r.next)&&!(i=i.call(r,o[1])).done)return i;switch(r=0,i&&(o=[2&o[0],i.value]),o[0]){case 0:case 1:i=o;break;case 4:return a.label++,{value:o[1],done:!1};case 5:a.label++,r=o[1],o=[0];continue;case 7:o=a.ops.pop(),a.trys.pop();continue;default:if(!((i=(i=a.trys).length>0&&i[i.length-1])||6!==o[0]&&2!==o[0])){a=0;continue}if(3===o[0]&&(!i||o[1]>i[0]&&o[1]<i[3])){a.label=o[1];break}if(6===o[0]&&a.label<i[1]){a.label=i[1],i=o;break}if(i&&a.label<i[2]){a.label=i[2],a.ops.push(o);break}i[2]&&a.ops.pop(),a.trys.pop();continue}o=t.call(e,a)}catch(e){o=[6,e],r=0}finally{n=i=0}if(5&o[0])throw o[1];return{value:o[0]?o[1]:void 0,done:!0}}([o,s])}}},ne=function(){function e(){}return e.sendToOrigin=function(e,t,n,r){return ee(this,void 0,void 0,(function(){var i,o,a,s,c;return te(this,(function(u){switch(u.label){case 0:return G()?(U.trace("sendToOrigin",e,t,n,r),(i=Q.getParentWindow())?[4,this.getSendToConfigs(r)]:[2]):[2];case 1:return o=u.sent(),a=o.id,s=o.originSiteUrl,c={type:e,data:t,id:a},n&&this.addEventListenerOnce(s,a,n,"*"===s),i.postMessage(c,s),[2]}}))}))},e.sendToIframe=function(e,t,n,r){return ee(this,void 0,void 0,(function(){var i,o,a,s,c;return te(this,(function(u){switch(u.label){case 0:return G()?(U.trace("sendToIframe",e,t,n,r),(i=Z.get())?[4,this.getSendToConfigs(r)]:[2]):[2];case 1:return o=u.sent(),a=o.id,s=o.proxySiteUrl,c={type:e,data:t,id:a},n&&this.addEventListenerOnce(s,a,n),i.contentWindow.postMessage(c,s),[2]}}))}))},e.sendToWindow=function(t,n,r,i){return ee(this,void 0,void 0,(function(){var o,a,s,c,u;return te(this,(function(l){switch(l.label){case 0:return G()?(U.trace("sendToWindow",t,n,r,i),(o=e.windowSubscribePopup)?[4,this.getSendToConfigs(i)]:[2]):[2];case 1:return a=l.sent(),s=a.id,c=a.proxySiteUrl,u={type:t,data:n,id:s},r&&this.addEventListenerOnce(c,s,r),o.postMessage(u,c),[2]}}))}))},e.addEventListenerOnce=function(e,t,n,r){U.trace("addEventListenerOnce",e,t,n,r);var i=function(o){try{if(!r&&!J(e,o.origin))return;if(o.data.id!==t)return;window.removeEventListener("message",i),n(o.data,(function(){window.removeEventListener("message",i)}))}catch(e){}};window.addEventListener("message",i)},e.addEventListener=function(e,t,n){U.trace("addEventListener",e,t,n);var r=function(i){try{if(e&&!n&&!J(i.origin,e))return;t(i.data,(function(){window.removeEventListener("message",r)}))}catch(e){}};window.addEventListener("message",r)},e.getSendToConfigs=function(e){return ee(this,void 0,void 0,(function(){var t,n,r;return te(this,(function(i){switch(i.label){case 0:return t=(null==e?void 0:e.replyId)||V(),(n=null==e?void 0:e.origin)?[2,{id:t,proxySiteUrl:n,originSiteUrl:n}]:[3,1];case 1:return[4,z.getConfigs()];case 2:return r=i.sent(),[2,{id:t,proxySiteUrl:r.proxySiteUrl,originSiteUrl:r.originSiteUrl}]}}))}))},e.windowSubscribePopup=null,e}(),re=function(e,t,n,r){return new(n||(n=Promise))((function(i,o){function a(e){try{c(r.next(e))}catch(e){o(e)}}function s(e){try{c(r.throw(e))}catch(e){o(e)}}function c(e){var t;e.done?i(e.value):(t=e.value,t instanceof n?t:new n((function(e){e(t)}))).then(a,s)}c((r=r.apply(e,t||[])).next())}))},ie=function(e,t){var n,r,i,o,a={label:0,sent:function(){if(1&i[0])throw i[1];return i[1]},trys:[],ops:[]};return o={next:s(0),throw:s(1),return:s(2)},"function"==typeof Symbol&&(o[Symbol.iterator]=function(){return this}),o;function s(o){return function(s){return function(o){if(n)throw new TypeError("Generator is already executing.");for(;a;)try{if(n=1,r&&(i=2&o[0]?r.return:o[0]?r.throw||((i=r.return)&&i.call(r),0):r.next)&&!(i=i.call(r,o[1])).done)return i;switch(r=0,i&&(o=[2&o[0],i.value]),o[0]){case 0:case 1:i=o;break;case 4:return a.label++,{value:o[1],done:!1};case 5:a.label++,r=o[1],o=[0];continue;case 7:o=a.ops.pop(),a.trys.pop();continue;default:if(!((i=(i=a.trys).length>0&&i[i.length-1])||6!==o[0]&&2!==o[0])){a=0;continue}if(3===o[0]&&(!i||o[1]>i[0]&&o[1]<i[3])){a.label=o[1];break}if(6===o[0]&&a.label<i[1]){a.label=i[1],i=o;break}if(i&&a.label<i[2]){a.label=i[2],a.ops.push(o);break}i[2]&&a.ops.pop(),a.trys.pop();continue}o=t.call(e,a)}catch(e){o=[6,e],r=0}finally{n=i=0}if(5&o[0])throw o[1];return{value:o[0]?o[1]:void 0,done:!0}}([o,s])}}},oe=function(){function r(){}return r.get=function(e,t){return re(this,void 0,void 0,(function(){return ie(this,(function(n){switch(n.label){case 0:return this.isIndirect?[4,this.getRemoteDBDataFromDispatchEvent(c,e,t)]:[3,2];case 1:case 3:case 6:return[2,n.sent()];case 2:return this.isWindowPopupIndirect?[4,this.getRemoteDBDataFromWindowPopupDispatchEvent(c,e,t)]:[3,4];case 4:return U.trace("DB:get",e,t),[4,this.getDatabase()];case 5:return[4,n.sent().get(e,t)]}}))}))},r.getAll=function(e){return re(this,void 0,void 0,(function(){return ie(this,(function(t){switch(t.label){case 0:return this.isIndirect?[4,this.getRemoteDBDataFromDispatchEvent(u,e)]:[3,2];case 1:case 3:case 6:return[2,t.sent()];case 2:return this.isWindowPopupIndirect?[4,this.getRemoteDBDataFromWindowPopupDispatchEvent(u,e)]:[3,4];case 4:return U.trace("DB:getAll",e),[4,this.getDatabase()];case 5:return[4,t.sent().getAll(e)]}}))}))},r.put=function(e,t,n){return re(this,void 0,void 0,(function(){return ie(this,(function(r){switch(r.label){case 0:return this.isIndirect?[4,this.getRemoteDBDataFromDispatchEvent(l,e,t,n)]:[3,2];case 1:case 3:case 6:return[2,r.sent()];case 2:return this.isWindowPopupIndirect?[4,this.getRemoteDBDataFromWindowPopupDispatchEvent(l,e,t,n)]:[3,4];case 4:return U.trace("DB:put",e,t,n),[4,this.getDatabase()];case 5:return[4,r.sent().put(e,n,t)]}}))}))},r.delete=function(e,t){return re(this,void 0,void 0,(function(){return ie(this,(function(n){switch(n.label){case 0:return this.isIndirect?[4,this.getRemoteDBDataFromDispatchEvent(f,e,t)]:[3,2];case 1:case 3:case 6:return[2,n.sent()];case 2:return this.isWindowPopupIndirect?[4,this.getRemoteDBDataFromWindowPopupDispatchEvent(f,e,t)]:[3,4];case 4:return U.trace("DB:delete",e,t),[4,this.getDatabase()];case 5:return[4,n.sent().delete(e,t)]}}))}))},r.clearTable=function(e){return re(this,void 0,void 0,(function(){return ie(this,(function(t){switch(t.label){case 0:return this.isIndirect?[4,this.getRemoteDBDataFromDispatchEvent(d,e)]:[3,2];case 1:case 3:case 6:return[2,t.sent()];case 2:return this.isWindowPopupIndirect?[4,this.getRemoteDBDataFromWindowPopupDispatchEvent(d,e)]:[3,4];case 4:return U.trace("DB:clearTable",e),[4,this.getDatabase()];case 5:return[4,t.sent().clear(e)]}}))}))},r.deleteDatabase=function(){return re(this,void 0,void 0,(function(){return ie(this,(function(e){switch(e.label){case 0:return U.trace("DB:deleteDatabase"),[4,I(this.databaseName)];case 1:return e.sent(),[2]}}))}))},r.getDatabase=function(){return re(this,void 0,void 0,(function(){var e;return ie(this,(function(t){switch(t.label){case 0:return this.shouldDbRestart&&this.idb&&(this.idb.close(),this.idb=null),this.idb?[3,2]:(this.shouldDbRestart=!1,e=this,[4,this.open()]);case 1:e.idb=t.sent(),this.idb.onerror=function(){r.shouldDbRestart=!0},t.label=2;case 2:return[2,this.idb]}}))}))},r.open=function(){return re(this,void 0,void 0,(function(){return ie(this,(function(e){switch(e.label){case 0:return[4,B(this.databaseName,this.databaseVersion,{upgrade:r.upgrade,terminated:r.terminated})];case 1:return[2,e.sent()]}}))}))},r.upgrade=function(r){return re(this,void 0,void 0,(function(){return ie(this,(function(i){return U.trace("DB:upgrade"),r.createObjectStore(e),r.createObjectStore(t),r.createObjectStore(n),[2]}))}))},r.dataToOriginDBEventHandler=function(e){return re(this,void 0,void 0,(function(){var t,n;return ie(this,(function(i){switch(i.label){case 0:return i.trys.push([0,11,,12]),e.type!==a?[2]:(U.trace("DB:Event:".concat(a),e),t=e.data,n=null,t.method===c&&t.key?[4,r.get(t.table,t.key)]:[3,2]);case 1:return n=i.sent(),[3,10];case 2:return t.method!==u?[3,4]:[4,r.getAll(t.table)];case 3:return n=i.sent(),[3,10];case 4:return t.method===l&&t.key?[4,r.put(t.table,t.key,t.value)]:[3,6];case 5:return n=i.sent(),[3,10];case 6:return t.method===f&&t.key?[4,r.delete(t.table,t.key)]:[3,8];case 7:return n=i.sent(),[3,10];case 8:return t.method!==d?[3,10]:[4,r.clearTable(t.table)];case 9:n=i.sent(),i.label=10;case 10:return ne.sendToOrigin(a,n,null,{replyId:e.id}),[3,12];case 11:return i.sent(),[3,12];case 12:return[2]}}))}))},r.dataToWindowPopupDBEventHandler=function(e){return re(this,void 0,void 0,(function(){var t,n;return ie(this,(function(i){switch(i.label){case 0:return i.trys.push([0,11,,12]),e.type!==s?[2]:(U.trace("DB:Event:".concat(s),e),t=e.data,n=null,t.method===c&&t.key?[4,r.get(t.table,t.key)]:[3,2]);case 1:return n=i.sent(),[3,10];case 2:return t.method!==u?[3,4]:[4,r.getAll(t.table)];case 3:return n=i.sent(),[3,10];case 4:return t.method===l&&t.key?[4,r.put(t.table,t.key,t.value)]:[3,6];case 5:return n=i.sent(),[3,10];case 6:return t.method===f&&t.key?[4,r.delete(t.table,t.key)]:[3,8];case 7:return n=i.sent(),[3,10];case 8:return t.method!==d?[3,10]:[4,r.clearTable(t.table)];case 9:n=i.sent(),i.label=10;case 10:return ne.sendToWindow(s,n,null,{replyId:e.id}),[3,12];case 11:return i.sent(),[3,12];case 12:return[2]}}))}))},r.getRemoteDBDataFromDispatchEvent=function(e,t,n,r){var i=this;return new Promise((function(o,s){U.trace("DB:getRemoteDBDataFromDispatchEvent",e,t,n,r);try{var c={method:e,table:t,key:n,value:r};ne.sendToIframe(a,c,(function(e){U.trace("DB:Event:".concat(a),e),o(e.data)}),{origin:i.indirectSubdomain})}catch(e){s(e)}}))},r.getRemoteDBDataFromWindowPopupDispatchEvent=function(e,t,n,r){return new Promise((function(i,o){U.trace("DB:getRemoteDBDataFromWindowPopupDispatchEvent",e,t,n,r);try{var a={method:e,table:t,key:n,value:r};ne.sendToOrigin(s,a,(function(e){U.trace("DB:Event:".concat(s),e),i(e.data)}),{origin:"*"})}catch(e){o(e)}}))},r.terminated=function(){U.trace("DB:terminated"),r.shouldDbRestart=!0},r.isIndirect=!1,r.isWindowPopupIndirect=!1,r.databaseName="FlareLane_SDK_DB",r.databaseVersion=1,r.idb=null,r.shouldDbRestart=!1,r}();const ae=function(){function t(){}return t.sendEvent=function(t,n,r,i,o){return a=this,s=void 0,u=function(){var a,s;return function(e,t){var n,r,i,o,a={label:0,sent:function(){if(1&i[0])throw i[1];return i[1]},trys:[],ops:[]};return o={next:s(0),throw:s(1),return:s(2)},"function"==typeof Symbol&&(o[Symbol.iterator]=function(){return this}),o;function s(o){return function(s){return function(o){if(n)throw new TypeError("Generator is already executing.");for(;a;)try{if(n=1,r&&(i=2&o[0]?r.return:o[0]?r.throw||((i=r.return)&&i.call(r),0):r.next)&&!(i=i.call(r,o[1])).done)return i;switch(r=0,i&&(o=[2&o[0],i.value]),o[0]){case 0:case 1:i=o;break;case 4:return a.label++,{value:o[1],done:!1};case 5:a.label++,r=o[1],o=[0];continue;case 7:o=a.ops.pop(),a.trys.pop();continue;default:if(!((i=(i=a.trys).length>0&&i[i.length-1])||6!==o[0]&&2!==o[0])){a=0;continue}if(3===o[0]&&(!i||o[1]>i[0]&&o[1]<i[3])){a.label=o[1];break}if(6===o[0]&&a.label<i[1]){a.label=i[1],i=o;break}if(i&&a.label<i[2]){a.label=i[2],a.ops.push(o);break}i[2]&&a.ops.pop(),a.trys.pop();continue}o=t.call(e,a)}catch(e){o=[6,e],r=0}finally{n=i=0}if(5&o[0])throw o[1];return{value:o[0]?o[1]:void 0,done:!0}}([o,s])}}}(this,(function(c){switch(c.label){case 0:return[4,oe.get(e,"platform")];case 1:return a=c.sent(),s={notificationId:n,deviceId:t,type:r,createdAt:(new Date).toISOString(),platform:o||a||"UNKNOWN"},[4,H.post(this.url,s,i)];case 2:return c.sent(),[2]}}))},new((c=void 0)||(c=Promise))((function(e,t){function n(e){try{i(u.next(e))}catch(e){t(e)}}function r(e){try{i(u.throw(e))}catch(e){t(e)}}function i(t){var i;t.done?e(t.value):(i=t.value,i instanceof c?i:new c((function(e){e(i)}))).then(n,r)}i((u=u.apply(a,s||[])).next())}));var a,s,c,u},t.url="/events",t}();var se=function(e,t,n,r){return new(n||(n=Promise))((function(i,o){function a(e){try{c(r.next(e))}catch(e){o(e)}}function s(e){try{c(r.throw(e))}catch(e){o(e)}}function c(e){var t;e.done?i(e.value):(t=e.value,t instanceof n?t:new n((function(e){e(t)}))).then(a,s)}c((r=r.apply(e,t||[])).next())}))},ce=function(e,t){var n,r,i,o,a={label:0,sent:function(){if(1&i[0])throw i[1];return i[1]},trys:[],ops:[]};return o={next:s(0),throw:s(1),return:s(2)},"function"==typeof Symbol&&(o[Symbol.iterator]=function(){return this}),o;function s(o){return function(s){return function(o){if(n)throw new TypeError("Generator is already executing.");for(;a;)try{if(n=1,r&&(i=2&o[0]?r.return:o[0]?r.throw||((i=r.return)&&i.call(r),0):r.next)&&!(i=i.call(r,o[1])).done)return i;switch(r=0,i&&(o=[2&o[0],i.value]),o[0]){case 0:case 1:i=o;break;case 4:return a.label++,{value:o[1],done:!1};case 5:a.label++,r=o[1],o=[0];continue;case 7:o=a.ops.pop(),a.trys.pop();continue;default:if(!((i=(i=a.trys).length>0&&i[i.length-1])||6!==o[0]&&2!==o[0])){a=0;continue}if(3===o[0]&&(!i||o[1]>i[0]&&o[1]<i[3])){a.label=o[1];break}if(6===o[0]&&a.label<i[1]){a.label=i[1],i=o;break}if(i&&a.label<i[2]){a.label=i[2],a.ops.push(o);break}i[2]&&a.ops.pop(),a.trys.pop();continue}o=t.call(e,a)}catch(e){o=[6,e],r=0}finally{n=i=0}if(5&o[0])throw o[1];return{value:o[0]?o[1]:void 0,done:!0}}([o,s])}}};self.addEventListener("push",(function(e){return e.waitUntil(function(e){var n,r,i,o;return se(this,void 0,void 0,(function(){var a,s;return ce(this,(function(c){switch(c.label){case 0:if(c.trys.push([0,6,,7]),!(a=null===(n=e.data)||void 0===n?void 0:n.json())||!a.isFlareLane)return[2];c.label=1;case 1:return c.trys.push([1,3,,4]),[4,oe.put(t,a.notificationId,K(a))];case 2:case 3:return c.sent(),[3,4];case 4:return[4,self.registration.showNotification(a.title||(null===(r=a.webPushConfig)||void 0===r?void 0:r.siteName)||"",{body:a.body,data:K(a),icon:(null===(i=a.webPushConfig)||void 0===i?void 0:i.siteIcon)||void 0,badge:(null===(o=a.webPushConfig)||void 0===o?void 0:o.siteBadge)||void 0,image:a.imageUrl||void 0,vibrate:[200,100,200]})];case 5:return c.sent(),[3,7];case 6:return s=c.sent(),console.error(s),[3,7];case 7:return[2]}}))}))}(e))})),self.addEventListener("notificationclick",(function(e){return e.waitUntil(function(e){var t;return se(this,void 0,void 0,(function(){var r,i,o,a,s,c;return ce(this,(function(u){switch(u.label){case 0:if(u.trys.push([0,9,,10]),e.notification.close(),r=e.notification,i=r.data.projectId,o=r.data.deviceId,!i||!o)return[3,4];u.label=1;case 1:return u.trys.push([1,3,,4]),[4,ae.sendEvent(o,r.data.notificationId,"CONVERTED",i,r.data.platform)];case 2:case 3:return u.sent(),[3,4];case 4:a=null;try{r.data.url&&(a=new URL(r.data.url).href)}catch(e){}return(s=null===(t=r.data.webPushConfig)||void 0===t?void 0:t.originSiteUrl)?(a||(a=s),[4,oe.clearTable(n)]):[2];case 5:return u.sent(),J(a,s)?[4,oe.put(n,r.data.notificationId,r.data)]:[3,7];case 6:u.sent(),u.label=7;case 7:return[4,self.clients.openWindow(a)];case 8:return u.sent(),[3,10];case 9:return c=u.sent(),console.error(c),[3,10];case 10:return[2]}}))}))}(e))})),self.addEventListener("pushsubscriptionchange",(function(t){return t.waitUntil(function(){return se(this,void 0,void 0,(function(){return ce(this,(function(t){switch(t.label){case 0:return t.trys.push([0,2,,3]),[4,oe.put(e,o,!0)];case 1:case 2:return t.sent(),[3,3];case 3:return[2]}}))}))}())})),self.addEventListener("activate",(function(t){return t.waitUntil(function(){return se(this,void 0,void 0,(function(){var t;return ce(this,(function(n){switch(n.label){case 0:return n.trys.push([0,3,,4]),[4,self.registration.pushManager.permissionState()];case 1:return t=n.sent(),[4,oe.put(e,i,t)];case 2:case 3:return n.sent(),[3,4];case 4:return[2]}}))}))}())})),function(){se(this,void 0,void 0,(function(){var t,n=this;return ce(this,(function(r){switch(r.label){case 0:return r.trys.push([0,3,,4]),"permissions"in navigator?[4,navigator.permissions.query({name:"notifications"})]:[3,2];case 1:(t=r.sent()).onchange=function(){return se(n,void 0,void 0,(function(){return ce(this,(function(n){switch(n.label){case 0:return n.trys.push([0,4,,5]),"granted"===t.state?[3,3]:[4,oe.put(e,o,!0)];case 1:return n.sent(),[4,oe.put(e,i,t.state)];case 2:n.sent(),n.label=3;case 3:return[3,5];case 4:return n.sent(),[3,5];case 5:return[2]}}))}))},r.label=2;case 2:return[3,4];case 3:return r.sent(),[3,4];case 4:return[2]}}))}))}(),self.addEventListener("install",(function(e){e.waitUntil(self.skipWaiting())}))})();