<script>
  export default{
    name: 'file-uploader',
    methods:{
        handle_on_drop: function(e){
            /*console.log(e)*/

            // datatranfer object
            const dt = e.dataTransfer

            let file = null

            // check which interface has file
            if(dt.items && dt.items.length > 0){
                for (var i = 0; i < dt.items.length; i++) {
                    file = dt.items[i].getAsFile()
                    this.processFile(file)
                }
            }else{
                for (var i = 0; i < dt.files.length; i++) {
                    file = dt.files[i]
                    this.processFile(file)
                }
            }

        },
        handle_on_drag_end: function(e){
            // clean files from dataTransfer object
            let dt = ev.dataTransfer

            if(dt.items && dt.items.length > 0){
                for (var i = 0; i < dt.items.length; i++) {
                    dt.items.remove(i)
                }
            }else{
                dt.clearData()
            }
        },
        handle_click: function(e){
            // emit click event on file input
            this.$refs.file_input.click()
        },
        handle_file_input_change: function(e){
            let files = e.target.files

            for (var i = 0; i < files.length; i++) {
                this.processFile(files[i])
            }
        },

        processFile: function(file){
            console.log('Processing file:', file)

            if(file.type != 'application/epub+zip'){
                console.error('File not supported!')
                return
            }
        }
    }
  }  
</script>

<template>
    <div class="dropzone" v-on:dragover.prevent @drop.prevent="handle_on_drop" @dragend="handle_on_drag_end" @click="handle_click">
        <input type="file" ref="file_input" multiple accept="application/epub+zip" style="display:none" @change="handle_file_input_change">
        <h1>I'm the file uploader</h1>
    </div>
</template>


<style>
    .dropzone{
        background: #b7b7ea;
        height: 199px;
    }
</style>