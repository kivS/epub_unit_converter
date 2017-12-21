// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'

Vue.config.productionTip = false

/* eslint-disable */

/* eslint-disable no-new */
new Vue({
  el: '#app',
  components: { App },
  template: '<App/>'
})

// 
window.BUS = new Vue()
window.WS = new WebSocket('ws://localhost:7000/wakey_wakey')

const ws = window.WS

ws.onmessage = e =>{
    console.log(e)
}

ws.onopen = function (event) {
   // set covertion type
   ws.send(JSON.stringify({"do": 'set_conversion_unit', "with": "imperial"}))
}

