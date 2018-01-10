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
     conversion_unit: 'metric',
     epubs: {},
     show_conversions_for_epub: []
    }
  },

  methods:{
    handle_before_open_conversions: function(e){
      // set list of conversions for selected epub so modal can acess it
      if(this.epubs[e.params]){
        console.log('loading conversions...');
        this.show_conversions_for_epub = this.epubs[e.params]['conversions']
      }
      
    }
  
  },

  mounted: function(){

    // send default conversion unit
    WS.onopen = e => {
      WS.send(JSON.stringify({'do': 'set_conversion_unit', 'with': this.conversion_unit}))
    };

    BUS.$on('set_conversion_unit', unit =>{
      this.conversion_unit = unit
      WS.send(JSON.stringify({'do': 'set_conversion_unit', 'with': unit}))
      console.log('conversion unit set to:', unit)
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
        ready: false,
        conversions: []
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
          BUS.$emit('remove_epub', epub.name)
      }else{
          TOAST.success({
              message: `${epub.name} conversion completed with ${epub.num_of_changes} change(s)`
          })

          // set epub as ready
          this.epubs[epub.name].ready = true
      }
    })

    BUS.$on('show_current_epubs', epubs =>{
       this.epubs = Object.assign({}, this.epubs, epubs)
    })

    BUS.$on('conversion_update', data =>{
      this.epubs[data.file]['conversions'].push(data.conversion)
    })

    BUS.$on('notify_current_conversion_unit', unit =>{
      this.conversion_unit = unit
    })

    BUS.$on('remove_epub', name =>{
      this.$delete(this.epubs, name)
      WS.send(JSON.stringify({'do': 'remove_epub', 'with': name }))
    })
  }
}
</script>

<template>
  <div id="app">
    <div class="header">
       <div class="project_name">
            <span>Epub Unit Converter</span>
       </div>
       <unit-selector :conversion-unit="conversion_unit"></unit-selector>
    </div>

    <file-uploader :epubs="epubs"></file-uploader>

    <!-- List of conversions for selected epub file -->
    <modal 
      name="conversions" 
      :draggable="true" 
      :scrollable="true" 
      :height="'auto'" 
      @before-open="handle_before_open_conversions" 
      @closed="show_conversions_for_epub = []"
      >
      <div class="list_of_conversions">
        <p class="title">List of conversions:</p>
        <span class="list_items" v-for="(val, i) in show_conversions_for_epub" :key="i">
          {{val}}
        </span>
      </div>
    </modal>

  </div>
</template>

<style>
/* CONTAINER */
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  width: 80vw;
  margin: auto;
  display: grid;
  grid-template-columns: 1fr;
  grid-template-rows: 100px auto;
  grid-row-gap: 20px;
}


/* HEADER */
.header{
    display: grid;
    width: 34%;
    justify-self: center;
    grid-row-gap: 13px;
}
.project_name{
    align-self: center;
    justify-self: center;

    font-weight: 600;
    font-size: xx-large;
}
.menu{
    display: grid;
}
.menu .menu_items{
    align-self: center;
    justify-self: center;
}
.menu button{
    border: none;
    border-radius: 25px;
    width: 100px;
    padding: 7px;
    font-size: larger;
    cursor: pointer;
}
.menu button.active{
    color: #ffffff;
    background: #00bcd4;
    box-shadow: 1px 1px 8px 0px #1f1e1e;
}
.menu button:focus{
    outline: none;
}
.menu button:not(.active):hover{
    box-shadow: 1px 1px 1px 1px #adaaaa;
}


/* Conversion list modal */
.list_of_conversions{
  display: grid;
}
.list_of_conversions .title{
  justify-self:center;
  font-size: x-large;
}
.list_items{
  padding: 8px;
  text-align: center;
}
.list_items:nth-child(even){
  background: #bdbcbc;
}
</style>
