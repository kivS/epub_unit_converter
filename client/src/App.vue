<script>
import fileUploader from './components/file-uploader'
import unitSelector from './components/unit-selector'

export default {
  name: 'app',
  components: {
    fileUploader,
    unitSelector
  },
  data: function(){
    return {
     conversion_unit: ''
    }
  },

  mounted: function(){
    BUS.$on('set_conversion_unit', unit =>{
      this.conversion_unit = unit
      WS.send(JSON.stringify({'do': 'set_conversion_unit', 'with': unit}))
    })
  }
}
</script>

<template>
  <div id="app">
    <unit-selector></unit-selector>
    <file-uploader></file-uploader>
  </div>
</template>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
