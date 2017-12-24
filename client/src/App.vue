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
     conversion_unit: '',
     epubs: {}
    }
  },

  mounted: function(){
    BUS.$on('set_conversion_unit', unit =>{
      this.conversion_unit = unit
      WS.send(JSON.stringify({'do': 'set_conversion_unit', 'with': unit}))
    })

    BUS.$on('add_epub_file', epub =>{
      /*console.log('adding new epub file:', epub)*/

      // add epub to epubs object
      let epub_to_add = {}
      epub_to_add[epub.name] = {
        ready: 0
      }
      this.epubs = Object.assign({}, this.epubs, epub_to_add)

      // send epub to backend
      WS.send(JSON.stringify({"do": 'convert_epub', "with": epub}))
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
