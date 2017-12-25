// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'

Vue.config.productionTip = false

window.BUS = new Vue()
window.WS = new WebSocket('ws://localhost:7000/wakey_wakey')

/* eslint-disable */

/* eslint-disable no-new */
new Vue({
  el: '#app',
  components: { App },
  template: '<App/>'
})

// handle messages from backend conversor
WS.onmessage = e =>{
    let data = null

    try{
        data = JSON.parse(e.data)
    }catch(err){
        console.log('Unstructered Message from server:', e.data)
    }
      
    if(data){
        switch(data.do){
            case 'notify_epub_conversion_completed':
                BUS.$emit('epub_conversion_completed', data.with)
            break
        }
    } 
}
