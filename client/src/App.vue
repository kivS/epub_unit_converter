<script>
import fileUploader from './components/file-uploader'
import unitSelector from './components/unit-selector'
import toast from 'izitoast'
import 'izitoast/dist/css/iziToast.min.css'

// set izitoast as global
window.TOAST = toast

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

  methods:{
    download_epub: function(name){
      console.log('downloading:', name);
      location.replace(`http://localhost:7000/download_epub/${name}`)
    },

    remove_epub: function(name){
      this.$delete(this.epubs, name)
      WS.send(JSON.stringify({'do': 'remove_epub', 'with': name }))
    }
  },

  mounted: function(){
    BUS.$on('set_conversion_unit', unit =>{
      this.conversion_unit = unit
      WS.send(JSON.stringify({'do': 'set_conversion_unit', 'with': unit}))
      console.log('conversion unit set to:', unit);
    })

    BUS.$on('add_epub_file', epub =>{

      // if file is already converted or in process
      if(this.epubs[epub.name]){
        TOAST.warning({
          message: `File already added.`,
          timeout: 2000
        })
        return
      }

      console.log('adding new epub file:', epub)

      // add epub to epubs object
      let epub_to_add = {}
      epub_to_add[epub.name] = {
        ready: false
      }
      this.epubs = Object.assign({}, this.epubs, epub_to_add)

      // send epub to backend
      WS.send(JSON.stringify({"do": 'convert_epub', "with": epub}))
    })

    BUS.$on('epub_conversion_completed', epub =>{
      if(epub.num_of_changes == 0){
          TOAST.info({
              message:`No conversion needed for ${epub.name}..`
          })

      }else{
          TOAST.success({
              message: `${epub.name} conversion completed with ${epub.num_of_changes} change(s)`
          })
      }

      // set epub as ready
      this.epubs[epub.name].ready = true
    })

    BUS.$on('show_current_epubs', epubs =>{
       this.epubs = Object.assign({}, this.epubs, epubs)
    })
  }
}
</script>

<template>
  <div id="app">
    <unit-selector></unit-selector>
    <file-uploader></file-uploader>

    <div>
      <div class="epub" v-for="(epub,epub_name,index) in epubs" :key="index">
        <p>{{epub_name}}</p>

        <button @click="remove_epub(epub_name)">delete</button>
        <button v-if="epub.ready" @click="download_epub(epub_name)">Download</button>
        <span v-else>
          converting...
        </span>

      </div>
    </div>

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

.epub{
  border: 1px solid #000000;
  margin: 4px 0;
  padding: 4px 0;
}
</style>
